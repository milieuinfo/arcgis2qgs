import xml.etree.cElementTree as ET

class qgsRenderer:
    def __init__(self, symbolType , symbollevels=0, target_attr=None, force_raster=False, graduatedMethod=None):
        """
        only simple and categorized renderer are supported now
        :param symbolType: singleSymbol, categorizedSymbol, graduatedSymbo
        :param symbollevels: int
        :param target_attr: target for the classified renderer
        :param force_raster: bool
        :param graduatedMethod: method for the Ranged randerer, like GraduatedColor
        """
        attr = {}
        attr["symbollevels"] = str(symbollevels)
        attr["type"] = symbolType
        if force_raster: attr["forceraster"] = "1"
        if target_attr: attr["attr"] = target_attr
        if graduatedMethod: attr["graduatedMethod"] = graduatedMethod

        self.renderer = ET.Element("renderer-v2", attr)
        self.symbols = ET.SubElement(self.renderer, "symbols")
        self.categories = None
        ET.SubElement( self.renderer, "rotation" )
        ET.SubElement( self.renderer, "sizescale", scalemethod="diameter" )

    def addSymbol(self, symbol):
        ":param symbol: add qgsSymbol to the render"
        self.symbols.append( symbol.node() )

    def addCategorizedSymbols(self, list_of_symbolCategory=[], default_symbol=None ):
        """
        Add the list with symbols for the categoried renderer
        :param list_of_symbolCategory: the list of values of type symbolCategory
        :param default_symbol: a qgssymbol for default walue
        """
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

    def addRangedSymbols(self, list_of_symbolRange=[] ):
        """
        Add the list with symbols for the Ranged randerer
        :param list_of_symbolRange: the list of values of type symbolRange
        """
        self.categories= ET.SubElement( self.renderer, "ranges" )

        for symbolRange in list_of_symbolRange:
            attrib = {}
            attrib["render"] = 'true'
            attrib["upper"] = str( symbolRange.upper )
            attrib["lower"] = str( symbolRange.lower )
            attrib["label"] =  symbolRange.label
            attrib["symbol"] = str( symbolRange.ID )
            self.addSymbol( symbolRange.symbol )
            ET.SubElement(self.categories, "range", attrib )

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

class symbolRange:
    def __init__(self, lower, upper, label, ID, symbol):
        self.lower = lower
        self.upper = upper
        self.label = label
        self.ID = ID
        symbol.symbol.set("name",ID)
        self.symbol = symbol
