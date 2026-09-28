import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Yield Rate at U.S. Colleges", layout="centered")

st.title("Yield Rate at U.S. Colleges, by Selectivity")
st.write("The yield rate is the percentage of admitted students choosing to enroll.")

# Interactive slider to progress the year timeline
selected_year = st.slider("Progress Year:", min_value=2001, max_value=2023, value=2023, step=1)

# Full dataset (2001 - 2023)
all_years = np.arange(2001, 2024)

# Data points based on original plot
elite_all = [38.0, 39.2, 39.2, 39.2, 38.0, 37.2, 37.8, 36.5, 35.5, 35.2, 35.5, 36.5, 37.0, 37.5, 37.5, 38.3, 39.8, 42.5, 44.0, 40.2, 47.0, 47.5, 49.0]
selective_all = [37.5, 37.8, 36.5, 36.5, 36.5, 36.0, 34.0, 33.0, 33.2, 33.0, 31.5, 31.2, 30.2, 29.5, 29.0, 28.0, 28.5, 28.3, 28.2, 25.5, 27.5, 27.0, 26.2]
somewhat_all = [39.8, 38.2, 38.5, 37.5, 36.0, 35.0, 34.0, 33.0, 31.5, 31.0, 30.5, 29.2, 29.2, 28.0, 27.5, 26.5, 26.0, 25.2, 24.2, 21.5, 21.7, 21.0, 19.8]
less_all = [41.0, 40, 38.5, 37.5, 36.2, 35.7, 34.5, 33.8, 32.0, 30.8, 30.0, 28.0, 27.5, 26.5, 26.2, 25.5, 24.8, 23.8, 22.5, 20.5, 20.0, 19.2, 18.2]
much_less_all = [42.0, 42.3, 40.8, 39.5, 38.5, 38.2, 37.0, 35.5, 34.0, 32.5, 31.8, 30.5, 29.8, 28.0, 27.5, 26.0, 25.2, 24.5, 23.2, 20.5, 20.0, 19.5, 18.8]

# Filter dataset up to the user-selected year
idx = selected_year - 2001 + 1
years = all_years[:idx]
elite = elite_all[:idx]
selective = selective_all[:idx]
somewhat = somewhat_all[:idx]
less = less_all[:idx]
much_less = much_less_all[:idx]

c_elite, c_selective, c_somewhat, c_less, c_much_less = '#00a8ff', '#10ac84', '#ff9f43', '#ff6b81', '#ff4757'

fig, ax = plt.subplots(figsize=(10, 6.5), facecolor='#ebebeb')
ax.set_facecolor('#ebebeb')

ax.plot(years, elite, color=c_elite, linewidth=2.5, label='Elite (<20%)')
ax.plot(years, selective, color=c_selective, linewidth=2.5, label='Selective (20%-40%)')
ax.plot(years, somewhat, color=c_somewhat, linewidth=2.5, label='Somewhat selective (40%-60%)')
ax.plot(years, less, color=c_less, linewidth=2.5, label='Less selective (60%-80%)')
ax.plot(years, much_less, color=c_much_less, linewidth=2.5, label='Much less selective (>80%)')

# Display COVID-19 indicator line if the slider reaches 2020
if selected_year >= 2020:
    ax.axvline(x=2020, color='#555555', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.text(2020, 51.5, 'COVID-19 (2020)', fontsize=9, color='#333333', fontweight='bold', ha='center', va='bottom',
            bbox=dict(boxstyle='square,pad=0.2', facecolor='#ebebeb', edgecolor='none'))

ax.set_ylim(8, 53)
ax.set_xlim(2000.5, 2023.5)
ax.set_yticks([10, 20, 30, 40, 50])
ax.set_yticklabels(['10%', '20%', '30%', '40%', '50% yield rate'], fontsize=10, color='#555555')
ax.set_xticks([2001, 2005, 2010, 2015, 2020])
ax.set_xticklabels(['2001', '2005', '2010', '2015', '2020'], fontsize=10, color='#555555')

for spine in ['top', 'left', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='y', linestyle=':', color='#cccccc', alpha=0.7)

# Calculate dynamic % changes based on current slider position
def chg_str(start, end):
    c = ((end - start) / start) * 100
    return f"{'+' if c >= 0 else ''}{c:.1f}%"

pct_change_text = (
    f"Change (2001–{selected_year})\n"
    f"------------------------\n"
    f"• Elite: {chg_str(elite[0], elite[-1])}\n"
    f"• Selective: {chg_str(selective[0], selective[-1])}\n"
    f"• Somewhat: {chg_str(somewhat[0], somewhat[-1])}\n"
    f"• Less: {chg_str(less[0], less[-1])}\n"
    f"• Much less: {chg_str(much_less[0], much_less[-1])}"
)

ax.text(0.98, 0.5, pct_change_text, transform=ax.transAxes, fontsize=9, verticalalignment='center', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#cccccc', linewidth=1.0))

ax.legend(loc='lower left', frameon=True, facecolor='#ffffff', edgecolor='#cccccc', fontsize=8.5)

st.pyplot(fig)
st.caption("Source: U.S. Department of Education, National Center for Education Statistics • Note: Based on 2021 admission rates.")
