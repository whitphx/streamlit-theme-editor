import streamlit as st

if 'primaryColor' not in st.session_state:
    st.session_state['primaryColor'] = "#F63366"
if 'backgroundColor' not in st.session_state:
    st.session_state['backgroundColor'] = "#FFFFFF"
if 'secondaryBackgroundColor' not in st.session_state:
    st.session_state['secondaryBackgroundColor'] = "#F0F2F6"
if 'textColor' not in st.session_state:
    st.session_state['textColor'] = "#262730"


def reconcile_theme_config():
    keys = ['primaryColor', 'backgroundColor', 'secondaryBackgroundColor', 'textColor']
    has_changed = False
    for key in keys:
        if st._config.get_option(f'theme.{key}') != st.session_state[key]:
            st._config.set_option(f'theme.{key}', st.session_state[key])
            has_changed = True
    if has_changed:
        st.experimental_rerun()


primary_color = st.color_picker('Primary color', key="primaryColor")

background_color = st.color_picker('Background color', key="backgroundColor")

secondary_background_color = st.color_picker('Secondary background color', key="secondaryBackgroundColor")

text_color = st.color_picker('Text color', key="textColor")

reconcile_theme_config()

st.code("""
primaryColor="{primaryColor}"
backgroundColor="{backgroundColor}"
secondaryBackgroundColor="{secondaryBackgroundColor}}"
textColor="{textColor}}"
""")


def sample_components(key: str):
    st.slider("Slider", min_value=0, max_value=100, key=f"{key}:slider")

sample_components("body")
with st.sidebar:
    sample_components("sidebar")
