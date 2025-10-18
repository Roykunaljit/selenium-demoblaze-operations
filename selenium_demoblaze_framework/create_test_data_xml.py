# create_test_data_xml.py

import os
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

os.makedirs("data", exist_ok=True)

# Root element
root = Element("testdata")

# Test case 1
tc1 = SubElement(root, "testcase")
SubElement(tc1, "username").text = "testuser1"
SubElement(tc1, "password").text = "Test@123"
SubElement(tc1, "product").text = "Samsung galaxy s6"
SubElement(tc1, "category").text = "Phones"

# Test case 2
tc2 = SubElement(root, "testcase")
SubElement(tc2, "username").text = "testuser2"
SubElement(tc2, "password").text = "Test@456"
SubElement(tc2, "product").text = "Sony vaio i5"
SubElement(tc2, "category").text = "Laptops"

# Pretty-print and write
rough_string = tostring(root, "utf-8")
reparsed = xml.dom.minidom.parseString(rough_string)
pretty_xml = reparsed.toprettyxml(indent="  ")

# Remove extra blank lines from toprettyxml
xml_lines = [line for line in pretty_xml.splitlines() if line.strip()]
final_xml = "\n".join(xml_lines)

with open("data/test_data.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)

print("✅ XML file 'data/test_data.xml' created successfully.")