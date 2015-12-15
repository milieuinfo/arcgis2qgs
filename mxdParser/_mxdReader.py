# -*- coding: utf-8 -*-
import os, arcpy, json
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

        self.bbox = [ self.df.extent.lowerLeft.X , self.df.extent.lowerLeft.Y ,
                      self.df.extent.upperRight.X, self.df.extent.upperRight.Y ]

        self.layers = []
        self._layersInfo()

    def _layersInfo(self):
        lyrs = arcpy.mapping.ListLayers(self.df)
        flatWMSProps = self.flattenWMS(lyrs)
        urls = []

        for lyr in lyrs:
            layer = {"name": lyr.longName, "visible": lyr.visible}

            if lyr.isFeatureLayer:
                if not arcpy.Exists( lyr.dataSource ): continue

                layer["type"] = "vector"
                layer['definitionQuery'] = lyr.definitionQuery
                if lyr.dataSource.endswith(".shp"): layer["path"] = lyr.dataSource
                else: layer["path"] = os.path.join( lyr.workspacePath, lyr.datasetName)

                symbols = json.loads( lyr._arc_object.getsymbology() )
                layer['layout'] = symbols

                ds = arcpy.Describe( lyr.dataSource )
                layer['crsID'] = ds.Spatialreference.factoryCode
                layer['crsName'] = ds.Spatialreference.name
                layer['crsGeographic'] = not ds.Spatialreference.PCSCode > 0
                layer['crsAuth'] =  "EPSG" if self.crsCode < 32767 else "ESRI"

                if "point" in ds.ShapeType.lower(): layer['geomType'] = "Point"
                elif "line" in ds.ShapeType.lower(): layer['geomType'] = "Line"
                elif "polygon" in ds.ShapeType.lower(): layer['geomType'] = "Polygon"
                else: layer['geomType'] = "Other"

                if lyr.showLabels and len(lyr.labelClasses):
                    labelClass = lyr.labelClasses[0]
                    layer["labelExpression"] = labelClass.expression
                if lyr.definitionQuery:
                    layer["definitionQuery"] = lyr.definitionQuery

            #TODO: symbology for rasters, put group layer in a group:
            elif lyr.isGroupLayer:
                layer["type"] = "group"
                layer["childeren"] = [n.longName for n in arcpy.mapping.ListLayers(lyr)
                                                                 if not n.isServiceLayer ][1:]
            elif lyr.isRasterLayer:
                layer["type"] = "raster"
                layer["path"] = lyr.dataSource

                ds = arcpy.Describe( lyr.dataSource )
                layer['crsID'] = ds.Spatialreference.factoryCode
                layer['crsName'] = ds.Spatialreference.name
                layer['crsGeographic'] = not ds.Spatialreference.PCSCode > 0
                layer['crsAuth'] =  "EPSG" if self.crsCode < 32767 else "ESRI"

            elif lyr.isServiceLayer and not lyr.isGroupLayer:
                URL =  lyr.serviceProperties['URL']
                if URL in urls: continue
                else: urls.append (URL)

                wmsProps = [wms for wms in flatWMSProps if URL == wms['URL'] ]
                if len(wmsProps):
                    layer['type'] = "service"
                    layer['visible'] = True
                    layer['serviceProperties'] = wmsProps[0]
            else:
                break

            self.layers.append(layer)

    @staticmethod
    def flattenWMS(lyrs):
        URLs = []
        mergeLyrsProps = []

        for wmsLyr in lyrs:
            if not wmsLyr.isServiceLayer: continue
            if wmsLyr.isGroupLayer : continue
            if not wmsLyr.visible : continue

            if wmsLyr.serviceProperties['URL'] in URLs and len(mergeLyrsProps):
                mergeLyrsProps[-1]['Names'].append( wmsLyr.serviceProperties['Name'] )
            else:
                URLs.append( wmsLyr.serviceProperties['URL'] )
                props = wmsLyr.serviceProperties
                props['Names'] = [wmsLyr.serviceProperties['Name']]
                mergeLyrsProps.append( props )
        return  mergeLyrsProps

    def __del__(self):
        del self.mxd
        del self.df