from bootstrap import *


class ogcFilter:
    def __init__(self):
        """OGC-filter"""
        self.filter = ET.Element('{{{ogc}}}Filter'.format(**ns))

    @staticmethod
    def category(PropertyName, Value):
        """
        :param PropertyName: attribute containing the categories
        :param Value: value of the category
        """
        filterClass = ogcFilter()
        node = ET.Element('{{{ogc}}}PropertyIsEqualTo'.format(**ns))
        ET.SubElement(node ,'{{{ogc}}}PropertyName'.format(**ns)).text = PropertyName
        ET.SubElement(node, '{{{ogc}}}Literal'.format(**ns)).text = str(Value)
        filterClass.filter.append(node)
        return filterClass

    @staticmethod
    def between(PropertyName, lowerValue, upperValue):
        """
        :param PropertyName: attribute containing the categories
        :param lowerValue: min value of category
        :param upperValue: max value of category
        """
        filterClass = ogcFilter()
        node = ET.Element('{{{ogc}}}And'.format(**ns))

        lowerBound = ET.SubElement(node, '{{{ogc}}}PropertyIsGreaterThanOrEqualTo'.format(**ns))
        ET.SubElement(lowerBound ,'{{{ogc}}}PropertyName'.format(**ns)).text = PropertyName
        ET.SubElement(lowerBound, '{{{ogc}}}Literal'.format(**ns)).text = str(lowerValue)

        upperBound = ET.SubElement(node, '{{{ogc}}}PropertyIsLessThan'.format(**ns))
        ET.SubElement(upperBound, '{{{ogc}}}PropertyName'.format(**ns)).text = PropertyName
        ET.SubElement(upperBound, '{{{ogc}}}Literal'.format(**ns)).text = str(upperValue)

        filterClass.filter.append(node)
        return filterClass

    @staticmethod
    def notInCollection(PropertyName, collection=[]):
        """
        :param PropertyName: attribute containing value that can't be included
        :param collection: series of values
        """
        filterClass = ogcFilter()

        node = ET.Element('{{{ogc}}}And'.format(**ns))
        for value in collection:
            compare = ET.SubElement(node, '{{{ogc}}}PropertyIsNotEqualTo'.format(**ns))
            ET.SubElement(compare, '{{{ogc}}}PropertyName'.format(**ns)).text = PropertyName
            ET.SubElement(compare, '{{{ogc}}}Literal'.format(**ns)).text = str(value)

        filterClass.filter.append(node)
        return filterClass

    def node(self):
        """":return: a ElementTree xml-node"""
        return self.filter