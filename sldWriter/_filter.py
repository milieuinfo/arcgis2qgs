from bootstrap import *


class sldFilter:
    def __init__(self):
        """OGC-filter"""
        self.filter = ET.Element('{{{ogc}}}Filter'.format(**ns))

    def category(self, PropertyName, Value):
        """
        :param PropertyName: attribute containing the categories
        :param Value: value of the category
        """
        node = ET.Element('{{{ogc}}}PropertyIsEqualTo'.format(**ns))
        ET.SubElement(node ,'{{{ogc}}}PropertyName'.format(**ns)).text = PropertyName
        ET.SubElement(node, '{{{ogc}}}Literal'.format(**ns)).text = str(Value)
        self.filter.append(node)

    def between(self, PropertyName, lowerValue, upperValue):
        """
        :param PropertyName: attribute containing the categories
        :param lowerValue: min value of category
        :param upperValue: max value of category
        """
        node = ET.Element('{{{ogc}}}And'.format(**ns))
        lowerBound = ET.SubElement(node, '{{{ogc}}}PropertyIsGreaterThanOrEqualTo'.format(**ns))
        ET.SubElement(lowerBound ,'{{{ogc}}}PropertyName'.format(**ns)).text = PropertyName
        ET.SubElement(lowerBound, '{{{ogc}}}Literal'.format(**ns)).text = str(lowerValue)
        upperBound = ET.SubElement(node, '{{{ogc}}}PropertyIsLessThan'.format(**ns))
        ET.SubElement(upperBound, '{{{ogc}}}PropertyName'.format(**ns)).text = PropertyName
        ET.SubElement(upperBound, '{{{ogc}}}Literal'.format(**ns)).text = str(upperValue)
        self.filter.append(node)

    def node(self):
        """":return: a ElementTree xml-node"""
        return self.filter