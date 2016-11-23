from bootstrap import *
from _layer import layer

class sldWriter:
    def __init__(self, version="1.0.0"):
        self.StyledLayerDescriptor = ET.Element("{{{sld}}}StyledLayerDescriptor".format(**ns),
             {'{{{xsi}}}schemaLocation'.format(**ns): "http://www.opengis.net/sld StyledLayerDescriptor.xsd", 'version': version})

    def addlayer(self, newlayer):
        """add a Layer
        :param newlayer: layer to add
        """
        if isinstance(newlayer,layer):
            self.StyledLayerDescriptor.append( newlayer.node() )
        else:
            raise Exception("instance is not a NamedLayer")

    def save(self, sldFilePath):
        """Save the sldqgsFilePath: the path to the output file."""
        tree = ET.ElementTree(self.StyledLayerDescriptor)
        tree.write(sldFilePath)

    def printString(self):
        """for debugging purposes"""
        sldTXT = ET.tostring(self.StyledLayerDescriptor)
        print dom.parseString(sldTXT).toprettyxml()