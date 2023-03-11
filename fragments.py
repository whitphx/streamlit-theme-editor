import streamlit as st
import wcag_contrast_ratio as contrast

import util


def contrast_summary(foreground_rgb_hex: str, background_rgb_hex: str) -> None:
    rgb_foreground = util.parse_hex(foreground_rgb_hex)
    rgb_background = util.parse_hex(background_rgb_hex)
    contrast_ratio = contrast.rgb(rgb_foreground, rgb_background)
    contrast_ratio_str = f"{contrast_ratio:.2f}"
    st.metric("", value=f"{contrast_ratio_str} : 1")

    st.markdown(f'<p style="color: {foreground_rgb_hex}; background-color: {background_rgb_hex}; padding: 12px">Lorem ipsum</p>', unsafe_allow_html=True)

def sample_components(key: str):
    st.slider("Slider", min_value=0, max_value=100, key=f"{key}:slider")
