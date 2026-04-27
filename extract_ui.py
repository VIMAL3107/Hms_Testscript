import xml.etree.ElementTree as ET
import re

def get_clickable_bounds(xml_file):
    try:
        # Read the file and handle encoding issues
        with open(xml_file, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore')
        
        # Remove the XML declaration if it's causing issues
        content = re.sub(r'<\?xml.*?\?>', '', content)
        
        root = ET.fromstring(content)
        for elem in root.iter():
            if elem.attrib.get('clickable') == 'true':
                print(f"Text: '{elem.attrib.get('text')}' | Desc: '{elem.attrib.get('content-desc')}' | Bounds: {elem.attrib.get('bounds')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    get_clickable_bounds('exact_view.xml')
