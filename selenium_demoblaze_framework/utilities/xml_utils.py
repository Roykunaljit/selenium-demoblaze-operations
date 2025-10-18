# utilities/xml_utils.py

import xml.etree.ElementTree as ET
from lxml import etree
import os


class XMLUtils:
    @staticmethod
    def read_xml_data(file_path):
        """
        Read data from an XML file.
        Assumes each <testcase> element contains child elements representing key-value pairs.
        Returns a list of dictionaries.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"XML file not found: {file_path}")

        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        for item in root.findall('.//testcase'):
            test_data = {}
            for child in item:
                test_data[child.tag] = child.text
            data.append(test_data)

        return data

    @staticmethod
    def write_xml_data(file_path, data, root_name='testdata'):
        """
        Write a list of dictionaries to an XML file.
        Each dictionary becomes a <testcase> element with child tags for each key.
        """
        if not data:
            raise ValueError("No data provided to write to XML.")

        root = ET.Element(root_name)

        for item in data:
            testcase = ET.SubElement(root, 'testcase')
            for key, value in item.items():
                child = ET.SubElement(testcase, key)
                child.text = str(value)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

    @staticmethod
    def validate_xml(xml_file, xsd_file):
        """
        Validate an XML file against an XSD schema using lxml.
        Returns True if valid, False otherwise.
        Raises FileNotFoundError if either file is missing.
        """
        if not os.path.exists(xml_file):
            raise FileNotFoundError(f"XML file not found: {xml_file}")
        if not os.path.exists(xsd_file):
            raise FileNotFoundError(f"XSD schema file not found: {xsd_file}")

        xml_doc = etree.parse(xml_file)
        xsd_doc = etree.parse(xsd_file)
        schema = etree.XMLSchema(xsd_doc)

        return schema.validate(xml_doc)

    @staticmethod
    def xpath_query(file_path, xpath_expression):
        """
        Execute an XPath query on an XML file using xml.etree.ElementTree.
        Returns a list of text content from matching elements.
        Note: ElementTree supports only a subset of XPath (e.g., no full XPath 1.0).
        For advanced XPath, consider using lxml.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"XML file not found: {file_path}")

        tree = ET.parse(file_path)
        root = tree.getroot()

        results = []
        # ElementTree's findall supports limited XPath
        for elem in root.findall(xpath_expression):
            results.append(elem.text if elem.text is not None else '')

        return results