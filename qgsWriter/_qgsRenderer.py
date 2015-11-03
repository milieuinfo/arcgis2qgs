import os, sys
import xml.etree.ElementTree as ET

class qgsRenderer:
    def __init__(self, symbolType , symbollevels=0 ):
        """
        only simple renderer are supported now
        :param symbolType: singleSymbol, categorizedSymbol, ...
        :param symbollevels: int
        """
        self.renderer = ET.Element("renderer-v2", symbollevels=str(symbollevels), type=symbolType)
        self.symbols = ET.SubElement(self.renderer, "symbols")
        ET.SubElement( self.renderer, "rotation" )
        ET.SubElement( self.renderer, "sizescale", scalemethod="diameter" )

    def addSymbol(self, symbol):
        ":param symbol: add qgsSymbol to the render"
        self.symbols.append( symbol.node() )

    def node(self):
        ":return: a ElementTree xml-node of the renderer in the QGIS format"
        return self.renderer

    def clear(self):
        "clear all symbols"
        for child in self.symbols: self.symbols.remove( child )