import colorsys
from typing import NamedTuple

import streamlit as st

import fragments

import util

class ThemeColor(NamedTuple):
    primaryColor: str
    backgroundColor: str
    secondaryBackgroundColor: str
    textColor: str


preset_colors: list[tuple[str, ThemeColor]] = [
    ("Default light", ThemeColor(
            primaryColor="#ff4b4b",
            backgroundColor="#ffffff",
            secondaryBackgroundColor="#f0f2f6",
            textColor="#31333F",
        )),
    ("Default dark", ThemeColor(
            primaryColor="#ff4b4b",
            backgroundColor="#0e1117",
            secondaryBackgroundColor="#262730",
            textColor="#fafafa",
    ))
]

if 'theme_from_initial_config' not in st.session_state:
    config_theme_primaryColor = st._config.get_option(f'theme.primaryColor')
    config_theme_backgroundColor = st._config.get_option(f'theme.backgroundColor')
    config_theme_secondaryBackgroundColor = st._config.get_option(f'theme.secondaryBackgroundColor')
    config_theme_textColor = st._config.get_option(f'theme.textColor')
    if config_theme_primaryColor and config_theme_backgroundColor and config_theme_secondaryBackgroundColor and config_theme_textColor:
        st.session_state['theme_from_initial_config'] = ThemeColor(
            primaryColor=config_theme_primaryColor,
            backgroundColor=config_theme_backgroundColor,
            secondaryBackgroundColor=config_theme_secondaryBackgroundColor,
            textColor=config_theme_textColor,
        )

if 'theme_from_initial_config' in st.session_state:
    preset_colors.append((
        "From the config",
        st.session_state['theme_from_initial_config'],
    ))

default_color = preset_colors[0][1]


if 'preset_color' not in st.session_state or 'backgroundColor' not in st.session_state or 'secondaryBackgroundColor' not in st.session_state or 'textColor' not in st.session_state:
    st.session_state['primaryColor'] = default_color.primaryColor
    st.session_state['backgroundColor'] = default_color.backgroundColor
    st.session_state['secondaryBackgroundColor'] = default_color.secondaryBackgroundColor
    st.session_state['textColor'] = default_color.textColor


st.title("Streamlit color theme editor")

def on_preset_color_selected():
    _, color = preset_colors[st.session_state.preset_color]
    st.session_state['primaryColor'] = color.primaryColor
    st.session_state['backgroundColor'] = color.backgroundColor
    st.session_state['secondaryBackgroundColor'] = color.secondaryBackgroundColor
    st.session_state['textColor'] = color.textColor


st.selectbox("Preset colors", key="preset_color", options=range(len(preset_colors)), format_func=lambda idx: preset_colors[idx][0], on_change=on_preset_color_selected)


def sync_rgb_to_hls(key: str):
    rgb = util.parse_hex(st.session_state[key])
    hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    st.session_state[f"{key}H"] = round(hls[0] * 360)
    st.session_state[f"{key}L"] = round(hls[1] * 100)
    st.session_state[f"{key}S"] = round(hls[2] * 100)


def sync_hls_to_rgb(key: str):
    h = st.session_state[f"{key}H"]
    l = st.session_state[f"{key}L"]
    s = st.session_state[f"{key}S"]
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    st.session_state[key] = f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"


def color_picker(label: str, key: str, default_color: str, l_only: bool) -> None:
    col1, col2 = st.columns([1, 3])
    with col1:
        color = st.color_picker(label, key=key, on_change=sync_rgb_to_hls, kwargs={"key": key})
    with col2:
        r,g,b = util.parse_hex(default_color)
        h,l,s = colorsys.rgb_to_hls(r,g,b)
        if l_only:
            if f"{key}H" not in st.session_state:
                st.session_state[f"{key}H"] = round(h * 360)
        else:
            st.slider(f"H for {label}", key=f"{key}H", min_value=0, max_value=360, value=round(h * 360), format="%d°", label_visibility="collapsed", on_change=sync_hls_to_rgb, kwargs={"key": key})

        st.slider(f"L for {label}", key=f"{key}L", min_value=0, max_value=100, value=round(l * 100), format="%d%%", label_visibility="collapsed", on_change=sync_hls_to_rgb, kwargs={"key": key})

        if l_only:
            if f"{key}S" not in st.session_state:
                st.session_state[f"{key}S"] = round(s * 100)
        else:
            st.slider(f"S for {label}", key=f"{key}S", min_value=0, max_value=100, value=round(s * 100), format="%d%%", label_visibility="collapsed", on_change=sync_hls_to_rgb, kwargs={"key": key})

    return color


primary_color = color_picker('Primary color', key="primaryColor", default_color=default_color.primaryColor, l_only=True)
text_color = color_picker('Text color', key="textColor", default_color=default_color.textColor, l_only=True)
background_color = color_picker('Background color', key="backgroundColor", default_color=default_color.backgroundColor, l_only=True)
secondary_background_color = color_picker('Secondary background color', key="secondaryBackgroundColor", default_color=default_color.secondaryBackgroundColor, l_only=True)


def parse_hex(rgb_hex_str: str) -> tuple[float, float, float]:
    if not re.match(r"^#[0-9a-fA-F]{6}$", rgb_hex_str):
        raise ValueError("Invalid hex color")
    return tuple(int(rgb_hex_str[i:i+2], 16) / 255 for i in (1, 3, 5))


st.header("WCAG contrast ratio")
st.markdown("""
Check if the color contrasts of the selected colors are enough to the WCAG guidelines recommendation.
For the details about it, see some resources such as the [WCAG document](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) or the [MDN page](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Understanding_WCAG/Perceivable/Color_contrast).""")

def synced_color_picker(label: str, value: str, key: str):
    def on_change():
        st.session_state[key] = st.session_state[key + "2"]
        sync_rgb_to_hls(key)
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

st.subheader("Config file (`.streamlit/config.toml`)")
st.code(f"""
[theme]
primaryColor="{primary_color}"
backgroundColor="{background_color}"
secondaryBackgroundColor="{secondary_background_color}"
textColor="{text_color}"
""", language="toml")

st.subheader("Command line argument")
st.code(f"""
streamlit run app.py \\
    --theme.primaryColor="{primary_color}" \\
    --theme.backgroundColor="{background_color}" \\
    --theme.secondaryBackgroundColor="{secondary_background_color}" \\
    --theme.textColor="{text_color}"
""")


if st.checkbox("Apply theme to this page"):
    st.info("Select 'Custom Theme' in the settings dialog to see the effect")

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
