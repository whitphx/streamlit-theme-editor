import re


def parse_hex(rgb_hex_str: str) -> tuple[float, float, float]:
    if not re.match(r"^#[0-9a-fA-F]{6}$", rgb_hex_str):
        raise ValueError("Invalid hex color")
    return tuple(int(rgb_hex_str[i:i+2], 16) / 255 for i in (1, 3, 5))
