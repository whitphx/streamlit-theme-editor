import streamlit as st
import wcag_contrast_ratio as contrast


def contrast_summary(rgb1: tuple[float, float, float], rgb2: tuple[float, float, float]) -> None:
    contrast_ratio = contrast.rgb(rgb1, rgb2)
    contrast_ratio_str = f"{contrast_ratio:.2f}"
    st.metric("", value=f"{contrast_ratio_str} : 1")


def sample_components(key: str):
    st.slider("Slider", min_value=0, max_value=100, key=f"{key}:slider")
