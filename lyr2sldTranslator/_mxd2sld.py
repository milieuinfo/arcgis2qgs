from mxdParser import *
import sldWriter as sld
from _polygonTranslator import polygonTranslator
from _polylineTranslator import polylineTranslator
from _pointTranslator import pointTranslator

class mxd2sld:
    def __init__(self):
        self.mxdOrLyr = None
        self.supportedTypes = ["vector", "raster"]
        self.sld = sld.sldWriter()

    def convertLyr(self, lyrPath, sldPath):
        """
        :param lyrPath: path to the input
        :param sldPath: path to the output sld-file
        """
        self._convert(lyrPath, sldPath, 0)

    def convertMxd(self, mxdPath, sldPath, lyrID=0 ):
        """
        :param mxdPath: path to the input
        :param sldPath: path to the output sld-file
        :param lyrID: the id (position) of the layer in the mxd
        """
        self._convert(mxdPath, sldPath, lyrID)

    def _convert(self, mxdOrLyrPath, sldPath, lyrID):
        self.mxdOrLyr = mxdReader(mxdOrLyrPath, getRemoteProj4=False)
        arclyr = self.mxdOrLyr.layers[lyrID]

        if arclyr["type"] not in self.supportedTypes:
            raise Exception(
                "layer of type {0} is not supported, only layers of type '{1}' are supported".format(
                    arclyr["type"], ", ".join(self.supportedTypes)))
        datageomType = arclyr["geomType"] if arclyr["type"] == "vector" else None
        sldLayer = sld.layer(arclyr["name"], arclyr['description'])

        if arclyr['minScale'] >= 0 and arclyr['maxScale'] > 0:
            minScale, maxScale = (arclyr['minScale'], arclyr['maxScale'])
        else:
            minScale, maxScale = (-1, -1)

        if arclyr["type"] == "vector":
            layout = arclyr['layout']['renderer']
            sldStyle = None
            lblExpr = None

            if 'labelExpression' in arclyr.keys():
                lblExpr = arclyr['labelExpression'].strip("[]\"")

            if datageomType == 'Point':
                sldStyle = pointTranslator.getPointRender(layout, minScale, maxScale, arclyr["name"], labelField=lblExpr)
            elif datageomType == 'Polygon':
                sldStyle = polygonTranslator.getPolygonRender(layout, minScale, maxScale, arclyr["name"], labelField=lblExpr)
            elif datageomType == 'Line':
                sldStyle = polylineTranslator.getLineRender(layout, minScale, maxScale, arclyr["name"], labelField=lblExpr)

            if sldStyle:
                sldLayer.addStyle(sldStyle)
                self.sld.addlayer(sldLayer)

        elif arclyr["type"] == "raster":
            if 'symbology' in arclyr and arclyr['symbology']['type'] == "classBreaks" and len(arclyr['symbology']['classBreakInfos']) >= 1:
                rasterStyle = sld.rasterSymbol(colormapType="intervals")
                initVal = arclyr['symbology']['minValue']
                colorHex = "#000000"
                opacity = 0

                if 'defaultSymbol' in  arclyr['symbology']:
                    initRGB =  arclyr['symbology']['defaultSymbol']['color']
                    colorHex = '#%02x%02x%02x' % (initRGB[0], initRGB[1], initRGB[2])
                    opacity = initRGB[3] / 255
                    rasterStyle.addColorMapEntry(color="#000000", label=">"+ str(initVal), quantity=initVal, opacity=0)

                for classBreak in arclyr['symbology']['classBreakInfos']:
                    maxVal = classBreak["classMaxValue"]
                    minVal = classBreak["classMinValue"]
                    lbl = "{0} - {1}".format(minVal, maxVal)
                    rasterStyle.addColorMapEntry(color=colorHex, label=lbl, quantity=maxVal, opacity=opacity)
                    if 'symbol' in classBreak:
                        rgba = classBreak['symbol']['color']
                        colorHex = '#%02x%02x%02x' % (rgba[0], rgba[1], rgba[2])
                        opacity = rgba[3] / 255

                sldLayer.addStyle(rasterStyle)
                self.sld.addlayer(sldLayer)

        self.sld.save(sldPath, True)




