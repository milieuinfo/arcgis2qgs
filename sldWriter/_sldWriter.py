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

    def save(self, sldFilePath, pretty=False):
        """Save the sldqgsFilePath: the path to the output file."""
        tree = ET.ElementTree(self.StyledLayerDescriptor)
        if pretty:
            sldTXT = ET.tostring(self.StyledLayerDescriptor)
            with open(sldFilePath, 'w') as fl:
                fl.write(dom.parseString(sldTXT).toprettyxml())
        else:
            tree.write(sldFilePath)
