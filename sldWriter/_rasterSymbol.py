from bootstrap import *

class rasterSymbol:
    colorMapTypss = ["ramp", "intervals", "values"]


    def __init__(self, opacity=1, colormapType="ramp", enhancement=None, gamma=2):
        if not ( 1 >= opacity >= 0):
            raise Exception("opacity needs to be in between 1 and 0")
        if colormapType not in self.colorMapTypss:
            raise Exception(
               "{0} is not a supported symboly type, only {1} are supporded".format(colormapType, ", ".join(self.colorMapTypss)) )

        self.symbol = ET.Element("{{{sld}}}RasterSymbolizer".format(**ns))
        ET.SubElement(self.symbol, "{{{sld}}}Opacity".format(**ns)).text = str(opacity)

        self.colorMap = ET.SubElement( self.symbol, "{{{sld}}}ColorMap".format(**ns), type=colormapType)

        if enhancement == "Normalize":
            contrast =  ET.SubElement(self.symbol, "{{{sld}}}ContrastEnhancement".format(**ns))
            ET.SubElement(contrast, "{{{sld}}}Normalize".format(**ns))
        elif enhancement== "Histogram":
            contrast = ET.SubElement(self.symbol, "{{{sld}}}ContrastEnhancement".format(**ns))
            ET.SubElement(contrast, "{{{sld}}}Histogram".format(**ns))
        elif enhancement == "GammaValue":
            contrast = ET.SubElement(self.symbol, "{{{sld}}}ContrastEnhancement".format(**ns))
            ET.SubElement(contrast, "{{{sld}}}GammaValue".format(**ns)).text = str(gamma)

    def addColorMapEntry(self, entry):
        return ET.SubElement(self.colorMap, "{{{sld}}}ColorMapEntry".format(**ns),
                    color=entry.color , quantity=str(entry.quantity), label=entry.labe1, opacity=str(entry.opacity) )

    def node(self):
        """:return: a ElementTree xml-node of the symbol in the QGIS format"""
        return self.symbol


class colorMapEntry:
    def __init__(self, color="#FFFFFF", quantity=0, label="", opacity=1):
        self.color = color
        self.quantity = quantity
        self.label = label
        self.opacity = opacity

