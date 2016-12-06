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
        self.mxdOrLyr = mxdReader(mxdOrLyrPath)
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

            if datageomType == 'Point':
                sldStyle = pointTranslator.getPointRender(layout, minScale, maxScale, arclyr["name"])
            elif datageomType == 'Polygon':
                sldStyle = polygonTranslator.getPolygonRender(layout, minScale, maxScale, arclyr["name"])
            elif datageomType == 'Line':
                sldStyle = polylineTranslator.getLineRender(layout, minScale, maxScale, arclyr["name"])

            if sldStyle:
                sldLayer.addStyle(sldStyle)
                self.sld.addlayer(sldLayer)

        elif arclyr["type"] == "raster":
            pass
        self.sld.save(sldPath, True)




