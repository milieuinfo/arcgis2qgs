# -*- coding: utf-8 -*-
import sys, os, arcpy, json

class mxdReader:
    def __init__(self, mxdPath):
        """
        :param mxdPath: path to the ESRI mapfile (.mxd)
        """
        self.mxd = arcpy.mapping.MapDocument(mxdPath)
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]

        self.title = self.mxd.title
        self.desciption = self.mxd.description
        self.author = self.mxd.author

        self.bbox = [ self.df.extent.lowerLeft.X, self.df.extent.lowerLeft.Y,
                      self.df.extent.upperRight.X, self.df.extent.upperRight.Y ]

        self.layers = []
        self._layersInfo()

    def _layersInfo(self):
        lyrs = arcpy.mapping.ListLayers(self.df)

        for lyr in lyrs:
            layer = {}
            layer["path"] = lyr.dataSource
            layer["name"] = lyr.name

            if lyr.isFeatureLayer:
                layer["type"] = "feature"
                symbols = json.loads( lyr._arc_object.getsymbology() )
                # example of the symbology json-like dict:
                # { u'renderer': {
                #     u'symbol': {u'color': [0, 166, 116, 255], u'style': u'esriSMSCircle', u'type': u'esriSMS',
                #     u'outline': {u'color': [0, 0, 0, 255], u'width': 1.0}, u'size': 4.0},
                #  u'type': u'simple'},
                #  u'transparency': 0}
                layer['layout'] = symbols

            #TODO: symbology for other types:
            elif lyr.isGroupLayer:
                layer["type"] = "group"
            elif lyr.isRasterLayer:
                layer["type"] = "raster"
            else:
                break

            self.layers.append(layer)

