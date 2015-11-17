# -*- coding: utf-8 -*-
import sys, os, arcpy, json
from _srsLookUp import srsLookUp

class mxdReader:
    def __init__(self, mxdPath):
        """
        :param mxdPath: path to the ESRI mapfile (.mxd)
        """
        self.mxd = arcpy.mapping.MapDocument(mxdPath)
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]
        self.srs = self.df.spatialReference

        self.title = self.mxd.title
        self.desciption = self.mxd.description
        self.author = self.mxd.author

        self.mapUnits =  self.df.mapUnits
        self.rotation = self.df.rotation

        #CRS
        self.crsGeographic = not self.srs.PCSCode > 0
        self.crsCode = self.srs.factoryCode
        self.crsName = self.srs.name
        self.crsAuth = "EPSG" if self.crsCode < 32767 else "ESRI"

        if not self.crsGeographic:
            self.crsProjectionacronym = self.srs.PCSName
            self.crsEllipsoidacronym = self.srs.GCS.GCSName
        else:
            self.crsProjectionacronym = ''
            self.crsEllipsoidacronym = self.srs.GCSName

        self.crsProj4 = srsLookUp().wkid2proj4(self.crsCode, "proj4")

        self.bbox = [ self.df.extent.lowerLeft.X, self.df.extent.lowerLeft.Y,
                      self.df.extent.upperRight.X, self.df.extent.upperRight.Y ]

        self.layers = []
        self._layersInfo()

    def _layersInfo(self):
        lyrs = arcpy.mapping.ListLayers(self.df)

        for lyr in lyrs:
            layer = {}
            layer["name"] = lyr.longName
            layer["visible"] = lyr.visible

            if lyr.isFeatureLayer:
                layer["type"] = "vector"
                layer['definitionQuery'] = lyr.definitionQuery

                if lyr.dataSource.endswith(".shp"): layer["path"] = lyr.dataSource
                else: layer["path"] = os.path.join( lyr.workspacePath, lyr.datasetName)

                symbols = json.loads( lyr._arc_object.getsymbology() )
                # example of the symbology json-like dict:
                # { u'renderer': {
                #     u'symbol': {u'color': [0, 166, 116, 255], u'style': u'esriSMSCircle', u'type': u'esriSMS',
                #     u'outline': {u'color': [0, 0, 0, 255], u'width': 1.0}, u'size': 4.0},
                #  u'type': u'simple'},
                #  u'transparency': 0}
                layer['layout'] = symbols
                ds = arcpy.Describe( lyr.dataSource )

                if "point" in ds.ShapeType.lower(): layer['geomType'] = "Point"
                elif "line" in ds.ShapeType.lower(): layer['geomType'] = "Line"
                elif "polygon" in ds.ShapeType.lower(): layer['geomType'] = "Polygon"
                else: layer['geomType'] = "Other"

                if lyr.showLabels and len(lyr.labelClasses):
                    labelClass = lyr.labelClasses[0]
                    layer["labelExpression"] = labelClass.expression

            #TODO: symbology for rasters, put group layer in a group:
            elif lyr.isGroupLayer:
                layer["type"] = "group"
                layer["childeren"] = [n.longName for n in arcpy.mapping.ListLayers(lyr)][1:]

            elif lyr.isRasterLayer:
                layer["type"] = "raster"
                layer["path"] = lyr.dataSource
            else:
                break

            self.layers.append(layer)

    def _layers2json(self):
        pass