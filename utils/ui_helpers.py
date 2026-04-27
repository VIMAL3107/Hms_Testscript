"""
UI Helper Utilities — for parsing XML dumps and extracting element info.
"""

import xml.etree.ElementTree as ET
import re


def get_clickable_bounds(xml_file):
    """
    Parse an Android UI XML dump and print all clickable elements
    with their text, content-desc, and bounds.
    """
    try:
        with open(xml_file, "rb") as f:
            content = f.read().decode("utf-8", errors="ignore")

        # Remove XML declaration if it causes issues
        content = re.sub(r"<\?xml.*?\?>", "", content)

        root = ET.fromstring(content)
        clickable_elements = []

        for elem in root.iter():
            if elem.attrib.get("clickable") == "true":
                info = {
                    "text": elem.attrib.get("text", ""),
                    "content_desc": elem.attrib.get("content-desc", ""),
                    "bounds": elem.attrib.get("bounds", ""),
                    "class": elem.attrib.get("class", ""),
                }
                clickable_elements.append(info)
                print(
                    f"Text: '{info['text']}' | "
                    f"Desc: '{info['content_desc']}' | "
                    f"Bounds: {info['bounds']}"
                )

        return clickable_elements

    except Exception as e:
        print(f"Error parsing XML: {e}")
        return []


def parse_bounds(bounds_str):
    """
    Parse bounds string like '[0,0][1080,1920]' into a dict
    with keys: left, top, right, bottom, center_x, center_y.
    """
    match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds_str)
    if not match:
        return None

    left, top, right, bottom = [int(g) for g in match.groups()]
    return {
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "center_x": (left + right) // 2,
        "center_y": (top + bottom) // 2,
        "width": right - left,
        "height": bottom - top,
    }


if __name__ == "__main__":
    get_clickable_bounds("exact_view.xml")
