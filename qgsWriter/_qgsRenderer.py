import xml.etree.ElementTree as ET

class qgsRenderer:
    def __init__(self, symbolType , symbollevels=0, target_attr=None, force_raster=False ):
        """
        only simple and categorized renderer are supported now
        :param symbolType: singleSymbol, categorizedSymbol, ...
        :param symbollevels: int
        """
        attr = {}
        attr["symbollevels"] = str(symbollevels)
        attr["type"] = symbolType
        attr["forceraster"] = "1" if force_raster else "0"
        if target_attr: attr["attr"] = target_attr

        self.renderer = ET.Element("renderer-v2", attr)
        self.symbols = ET.SubElement(self.renderer, "symbols")
        self.categories = None
        ET.SubElement( self.renderer, "rotation" )
        ET.SubElement( self.renderer, "sizescale", scalemethod="diameter" )

    def addSymbol(self, symbol):
        ":param symbol: add qgsSymbol to the render"
        self.symbols.append( symbol.node() )

    def addCategorizedSymbols(self, list_of_symbolCategory=[], default_symbol=None ):
        self.categories= ET.SubElement( self.renderer, "categories" )

        for symbolCat in list_of_symbolCategory:
            attrib = {}
            attrib["render"] = 'true'
            attrib["value"] = symbolCat.value
            attrib["label"] =  symbolCat.label
            attrib["symbol"] = str( symbolCat.ID )
            self.addSymbol( symbolCat.symbol )
            ET.SubElement(self.categories, "category", attrib )

        if symbolCategory:
           default = ET.SubElement( self.renderer, "source-symbol" )
           default.append(default_symbol.node())

    def node(self):
        ":return: a ElementTree xml-node of the renderer in the QGIS format"
        return self.renderer

    def clear(self):
        "clear all symbols"
        for child in self.symbols: self.symbols.remove( child )
        if self.categories: self.renderer.remove( self.categories )

class symbolCategory:
    def __init__(self, value, label, ID, symbol):
        self.value = value
        self.label = label
        self.ID = ID
        symbol.symbol.set("name",ID)
        self.symbol = symbol
