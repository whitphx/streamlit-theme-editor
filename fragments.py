import streamlit as st
import wcag_contrast_ratio as contrast

import util


def contrast_summary(label: str, foreground_rgb_hex: str, background_rgb_hex: str) -> None:
    rgb_foreground = util.parse_hex(foreground_rgb_hex)
    rgb_background = util.parse_hex(background_rgb_hex)
    contrast_ratio = contrast.rgb(rgb_foreground, rgb_background)
    contrast_ratio_str = f"{contrast_ratio:.2f}"

    st.metric(label, value=f"{contrast_ratio_str} : 1", label_visibility="collapsed")

    if contrast.passes_AAA(contrast_ratio):
        st.markdown(":white_check_mark: :white_check_mark: WCAG AAA")
    elif contrast.passes_AA(contrast_ratio):
        st.markdown(":white_check_mark: WCAG AA")
    else:
        st.markdown(":x: Fail WCAG")

    st.markdown(f'<p style="color: {foreground_rgb_hex}; background-color: {background_rgb_hex}; padding: 12px">Lorem ipsum</p>', unsafe_allow_html=True)


def sample_components(key: str):
    st.slider("Slider", min_value=0, max_value=100, key=f"{key}:slider")
