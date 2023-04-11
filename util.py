import re
import random
from colorsys import hls_to_rgb

import wcag_contrast_ratio as contrast


def parse_hex(rgb_hex_str: str) -> tuple[float, float, float]:
    if not re.match(r"^#[0-9a-fA-F]{6}$", rgb_hex_str):
        raise ValueError("Invalid hex color")
    return tuple(int(rgb_hex_str[i:i+2], 16) / 255 for i in (1, 3, 5))


def random_hls():
    h = random.random()
    l = random.random()
    s = random.random()

    # Make sure the color is light or dark enough.
    MAX_LIGHTNESS = 0.3
    if l < 0.5:
        # Make the color darker.
        l = l * (MAX_LIGHTNESS / 0.5)
    else:
        # Make the color lighter.
        l = 1 - l
        l = l * (MAX_LIGHTNESS / 0.5)
        l = 1 - l
    return (h, l, s)


def high_contrast_color(color):
    h, l, s = color
    l = 1 - l
    return (h, l, s)


def hls_to_hex(color):
    r, g, b = hls_to_rgb(*color)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


def find_color_with_contrast(base_color, min_contrast_ratio, max_attempts):
    for _ in range(max_attempts):
        candidate_color = random_hls()
        if contrast.rgb(hls_to_rgb(*candidate_color), hls_to_rgb(*base_color)) > min_contrast_ratio:
            return candidate_color
    return high_contrast_color(base_color)


def generate_color_scheme():
    primary_color = random_hls()
    basic_background = high_contrast_color(primary_color)

    text_color = find_color_with_contrast(basic_background, 7, 100)
    secondary_background = find_color_with_contrast(primary_color, 7, 100)

    return hls_to_hex(primary_color), hls_to_hex(text_color), hls_to_hex(basic_background), hls_to_hex(secondary_background)
