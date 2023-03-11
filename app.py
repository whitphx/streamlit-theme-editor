import re

import streamlit as st

import fragments

if 'primaryColor' not in st.session_state:
    st.session_state['primaryColor'] = "#F63366"
if 'backgroundColor' not in st.session_state:
    st.session_state['backgroundColor'] = "#FFFFFF"
if 'secondaryBackgroundColor' not in st.session_state:
    st.session_state['secondaryBackgroundColor'] = "#F0F2F6"
if 'textColor' not in st.session_state:
    st.session_state['textColor'] = "#262730"


primary_color = st.color_picker('Primary color', key="primaryColor")
text_color = st.color_picker('Text color', key="textColor")
background_color = st.color_picker('Background color', key="backgroundColor")
secondary_background_color = st.color_picker('Secondary background color', key="secondaryBackgroundColor")


def parse_hex(rgb_hex_str: str) -> tuple[float, float, float]:
    if not re.match(r"^#[0-9a-fA-F]{6}$", rgb_hex_str):
        raise ValueError("Invalid hex color")
    return tuple(int(rgb_hex_str[i:i+2], 16) / 255 for i in (1, 3, 5))


st.header("WCAG contrast ratio")

def synced_color_picker(label: str, value: str, key: str):
    def on_change():
        st.session_state[key] = st.session_state[key + "2"]
    st.color_picker(label, value=value, key=key + "2", on_change=on_change)

col1, col2, col3 = st.columns(3)
with col2:
    synced_color_picker("Background color", value=background_color, key="backgroundColor")
with col3:
    synced_color_picker("Secondary background color", value=secondary_background_color, key="secondaryBackgroundColor")

col1, col2, col3 = st.columns(3)
with col1:
    synced_color_picker("Primary color", value=primary_color, key="primaryColor")
with col2:
    fragments.contrast_summary("Primary/Background", primary_color, background_color)
with col3:
    fragments.contrast_summary("Primary/Secondary background", primary_color, secondary_background_color)

col1, col2, col3 = st.columns(3)
with col1:
    synced_color_picker("Text color", value=text_color, key="textColor")
with col2:
    fragments.contrast_summary("Text/Background", text_color, background_color)
with col3:
    fragments.contrast_summary("Text/Secondary background", text_color, secondary_background_color)


st.header("Config")

st.code(f"""
primaryColor="{primary_color}"
backgroundColor="{background_color}"
secondaryBackgroundColor="{secondary_background_color}"
textColor="{text_color}"
""")


apply_theme = st.checkbox("Apply theme to this page")

if apply_theme:
    def reconcile_theme_config():
        keys = ['primaryColor', 'backgroundColor', 'secondaryBackgroundColor', 'textColor']
        has_changed = False
        for key in keys:
            if st._config.get_option(f'theme.{key}') != st.session_state[key]:
                st._config.set_option(f'theme.{key}', st.session_state[key])
                has_changed = True
        if has_changed:
            st.experimental_rerun()

    reconcile_theme_config()



fragments.sample_components("body")
with st.sidebar:
    fragments.sample_components("sidebar")
