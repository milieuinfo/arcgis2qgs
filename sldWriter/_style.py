from bootstrap import *
from _filter import sldFilter
from _vectorSymbol import vectorSymbol
from _rasterSymbol import rasterSymbol

class style:
    def __init__(self, name="", title="", description=""):
        """
        FeatureTypeStyle
        :param name: the name of the style
        :param title:
        :param description:
        """
        self.FeatureTypeStyle = ET.Element('{{{sld}}}FeatureTypeStyle'.format( **ns ))
        if len(name) > 0:
            ET.SubElement( self.FeatureTypeStyle, '{{{sld}}}Name'.format( **ns )).text = name
        if len(title) > 0:
            ET.SubElement( self.FeatureTypeStyle, '{{{sld}}}Title'.format(**ns)).text = title
        if len(description) > 0:
            ET.SubElement( self.FeatureTypeStyle, '{{{sld}}}Abstract'.format(**ns)).text = description

    def addRule(self, name="", title="", description="", Filter=None, MinScale=-1, MaxScale=-1, Symbolizer=None ):
        rule = ET.SubElement( self.FeatureTypeStyle, '{{{sld}}}Rule'.format( **ns ))
        if len(name) > 0:
            ET.SubElement( rule, '{{{sld}}}Name'.format( **ns )).text = name
        if len(title) > 0:
            ET.SubElement( rule, '{{{sld}}}Title'.format(**ns)).text = title
        if len(description) > 0:
            ET.SubElement( rule, '{{{sld}}}Abstract'.format(**ns)).text = description

        if isinstance(Filter, sldFilter):
            rule.append( Filter.node() )

        if MinScale >= 0:
            ET.SubElement(rule, '{{{sld}}}MinScaleDenominator'.format(**ns)).text = str(MinScale)
        if MaxScale > 0:
            ET.SubElement(rule, '{{{sld}}}MaxScaleDenominator'.format(**ns)).text = str(MaxScale)

        if isinstance(Symbolizer, vectorSymbol ):
            rule.append( Symbolizer.node() )
        elif isinstance(Symbolizer, rasterSymbol ):
            rule.append( Symbolizer.node() )

        return rule

    def node(self):
        """":return: a ElementTree xml-node"""
        return self.FeatureTypeStyle

