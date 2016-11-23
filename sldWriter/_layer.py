from bootstrap import *

class layer:
    def __init__(self, layerName, layerDescription="", styleName="", initStyles=[]):
        """
        :param layerName: the name of the layer to apply the style to, required
        :param layerDescription: a free text description
        :param styleName: the name of the Style
        :param initStyles: the intital styles
        """
        self.styles = []
        self.namedLayer = ET.Element( '{{{sld}}}NamedLayer'.format( **ns ) )
        ET.SubElement(self.namedLayer ,'{{{sld}}}Name'.format( **ns )).text = layerName
        if len(layerDescription) > 0:
            ET.SubElement(self.namedLayer, '{{{sld}}}Description'.format(**ns)).text = layerDescription
        #add the default layer
        self._addUserStyle( name=styleName, title=styleName, isDefault=False, styles=initStyles )

    def _addUserStyle(self, name="", title="", isDefault=False, styles=[] ):
        """
        :param name: the name of the style
        :param title: the title to display in the legend
        :param isDefault: boolean
        :param styles: a list ofstyles to add to the layer
        """
        self.userStyle = ET.SubElement(self.namedLayer, '{{{sld}}}UserStyle'.format(**ns))
        if len(name) > 0:
            ET.SubElement(self.userStyle, '{{{sld}}}Name'.format(**ns)).text = name
        if len(title) > 0:
            ET.SubElement(self.userStyle, '{{{sld}}}Title'.format(**ns)).text = title
        if isDefault:
            ET.SubElement(self.userStyle, '{{{sld}}}IsDefault'.format(**ns)).text = '1'

        for style in styles:
            self.userStyle.append(style.node())

    def addStyle(self, style):
        """
        :param style: add a new style
        """
        self.userStyle.append(style.node())

    def node(self):
        """":return: a ElementTree xml-node"""
        return self.namedLayer

