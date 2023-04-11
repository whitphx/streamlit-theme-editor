import colorsys

import streamlit as st
import wcag_contrast_ratio as contrast

import util


def color_picker(label: str, key: str, default_color: str, l_only: bool) -> None:
    def on_color_change():
        rgb = util.parse_hex(st.session_state[key])
        hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
        st.session_state[f"{key}H"] = round(hls[0] * 360)
        st.session_state[f"{key}L"] = round(hls[1] * 100)
        st.session_state[f"{key}S"] = round(hls[2] * 100)

    def on_hls_change():
        h = st.session_state[f"{key}H"]
        l = st.session_state[f"{key}L"]
        s = st.session_state[f"{key}S"]
        r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
        st.session_state[key] = f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"

    col1, col2 = st.columns([1, 3])
    with col1:
        color = st.color_picker(label, key=key, on_change=on_color_change)
    with col2:
        r,g,b = util.parse_hex(default_color)
        h,l,s = colorsys.rgb_to_hls(r,g,b)
        if l_only:
            if f"{key}H" not in st.session_state:
                st.session_state[f"{key}H"] = round(h * 360)
        else:
            st.slider(f"H for {label}", key=f"{key}H", min_value=0, max_value=360, value=round(h * 360), format="%d°", label_visibility="collapsed", on_change=on_hls_change)

        st.slider(f"L for {label}", key=f"{key}L", min_value=0, max_value=100, value=round(l * 100), format="%d%%", label_visibility="collapsed", on_change=on_hls_change)

        if l_only:
            if f"{key}S" not in st.session_state:
                st.session_state[f"{key}S"] = round(s * 100)
        else:
            st.slider(f"S for {label}", key=f"{key}S", min_value=0, max_value=100, value=round(s * 100), format="%d%%", label_visibility="collapsed", on_change=on_hls_change)

    return color


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
    st.header("Sample components")
    st.slider("Slider", min_value=0, max_value=100, key=f"{key}:slider")
