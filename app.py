import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(page_title="Yield Rate at U.S. Colleges", layout="centered")

st.title("Yield Rate at U.S. Colleges, by Selectivity")
st.write("The yield rate is the percentage of admitted students choosing to enroll.")

# --- Sidebar Category Toggles ---
st.sidebar.header("Select Categories")

categories_data = {
    'Elite (<20%)': ([38.0, 39.2, 39.2, 39.2, 38.0, 37.2, 37.8, 36.5, 35.5, 35.2, 35.5, 36.5, 37.0, 37.5, 37.5, 38.3, 39.8, 42.5, 44.0, 40.2, 47.0, 47.5, 49.0], '#00a8ff'),
    'Selective (20%-40%)': ([37.5, 37.8, 36.5, 36.5, 36.5, 36.0, 34.0, 33.0, 33.2, 33.0, 31.5, 31.2, 30.2, 29.5, 29.0, 28.0, 28.5, 28.3, 28.2, 25.5, 27.5, 27.0, 26.2], '#10ac84'),
    'Somewhat selective (40%-60%)': ([39.8, 38.2, 38.5, 37.5, 36.0, 35.0, 34.0, 33.0, 31.5, 31.0, 30.5, 29.2, 29.2, 28.0, 27.5, 26.5, 26.0, 25.2, 24.2, 21.5, 21.7, 21.0, 19.8], '#ff9f43'),
    'Less selective (60%-80%)': ([41.0, 40.0, 38.5, 37.5, 36.2, 35.7, 34.5, 33.8, 32.0, 30.8, 30.0, 28.0, 27.5, 26.5, 26.2, 25.5, 24.8, 23.8, 22.5, 20.5, 20.0, 19.2, 18.2], '#ff6b81'),
    'Much less selective (>80%)': ([42.0, 42.3, 40.8, 39.5, 38.5, 38.2, 37.0, 35.5, 34.0, 32.5, 31.8, 30.5, 29.8, 28.0, 27.5, 26.0, 25.2, 24.5, 23.2, 20.5, 20.0, 19.5, 18.8], '#ff4757')
}

selected_categories = []
for label in categories_data.keys():
    if st.sidebar.toggle(label, value=True):
        selected_categories.append(label)

# --- Interactive Slider & Play Button Layout ---
col_slider, col_btn = st.columns([4, 1])

with col_btn:
    st.write("")  # Spacing alignment with slider
    st.write("")
    play_button = st.button("▶ Play", use_container_width=True)

with col_slider:
    selected_year = st.slider("Progress Year:", min_value=2001, max_value=2023, value=2023, step=1)

# Placeholder container for updating graph during animation
plot_container = st.empty()

def create_plot(year):
    all_years = np.arange(2001, 2024)
    idx = year - 2001 + 1
    years = all_years[:idx]

    fig, ax = plt.subplots(figsize=(10, 6.5), facecolor='#ebebeb')
    ax.set_facecolor('#ebebeb')

    def chg_str(start, end):
        c = ((end - start) / start) * 100
        return f"{'+' if c >= 0 else ''}{c:.1f}%"

    pct_change_lines = [f"Change (2001–{year})", "------------------------"]

    for label in selected_categories:
        data, color = categories_data[label]
        series = data[:idx]
        ax.plot(years, series, color=color, linewidth=2.5, label=label)
        short_label = label.split(' ')[0]
        pct_change_lines.append(f"• {short_label}: {chg_str(series[0], series[-1])}")

    # COVID-19 Indicator Line
    if year >= 2020:
        ax.axvline(x=2020, color='#555555', linestyle='--', linewidth=1.5, alpha=0.8)
        ax.text(2020, 51.5, 'COVID-19 (2020)', fontsize=9, color='#333333', fontweight='bold', ha='center', va='bottom',
                bbox=dict(boxstyle='square,pad=0.2', facecolor='#ebebeb', edgecolor='none'))

    # Axes styling and bounds
    ax.set_ylim(8, 55)
    ax.set_xlim(2000.5, 2023.5)
    ax.set_yticks([10, 20, 30, 40, 50])
    ax.set_yticklabels(['10%', '20%', '30%', '40%', '50% yield rate'], fontsize=10, color='#555555')
    ax.set_xticks([2001, 2005, 2010, 2015, 2020])
    ax.set_xticklabels(['2001', '2005', '2010', '2015', '2020'], fontsize=10, color='#555555')

    for spine in ['top', 'left', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#cccccc')
    ax.grid(axis='y', linestyle=':', color='#cccccc', alpha=0.7)

    # Change box positioned upper-left above legend
    if selected_categories:
        pct_change_text = "\n".join(pct_change_lines)
        ax.text(0.03, 0.95, pct_change_text, transform=ax.transAxes, fontsize=9, 
                verticalalignment='top', horizontalalignment='left',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#cccccc', linewidth=1.0))

    ax.legend(loc='lower left', frameon=True, facecolor='#ffffff', edgecolor='#cccccc', fontsize=8.5)
    return fig

# Execute automated loop when Play is pressed, otherwise display selected slider year
if play_button:
    for yr in range(2001, 2024):
        fig = create_plot(yr)
        plot_container.pyplot(fig)
        plt.close(fig)
        time.sleep(0.2)
else:
    fig = create_plot(selected_year)
    plot_container.pyplot(fig)
    plt.close(fig)

st.caption("Source: U.S. Department of Education, National Center for Education Statistics • Note: Based on 2021 admission rates.")
