# -*- coding: utf-8 -*-
import os, arcpy, json
from _srsLookUp import srsLookUp

class mxdReader:
    def __init__(self, mxdOrLyrPath="", getRemoteProj4=True):
        """
        :param mxdOrLyrPath: path to the ESRI mapfile (.mxd), ESROI layerfiles (.lyr) are also accecpted
        """
        if mxdOrLyrPath.endswith(".mxd"):
            self.isMxd = True
            self.layerCollection = arcpy.mapping.MapDocument(mxdOrLyrPath)
            self.df = arcpy.mapping.ListDataFrames(self.layerCollection)[0]
            self.srs = self.df.spatialReference
            self.bbox = [self.df.extent.lowerLeft.X, self.df.extent.lowerLeft.Y,
                         self.df.extent.upperRight.X, self.df.extent.upperRight.Y]

            self.title = self.layerCollection.title
            self.author = self.layerCollection.author
            self.desciption = self.layerCollection.description
            self.mapUnits = self.df.mapUnits
            self.rotation = self.df.rotation

        elif mxdOrLyrPath.endswith(".lyr"):
            self.isMxd = False
            self.layerCollection = arcpy.mapping.Layer(mxdOrLyrPath)
            self.df = None
            self.srs = arcpy.Describe( self.layerCollection.dataSource ).Spatialreference
            self.bbox = [self.layerCollection.getExtent().lowerLeft.X, self.layerCollection.getExtent().lowerLeft.Y,
                         self.layerCollection.getExtent().upperRight.X, self.layerCollection.getExtent().upperRight.Y]

            self.title = self.layerCollection.longName
            self.author = self.layerCollection.credits
            self.desciption = self.layerCollection.description
            self.mapUnits = 'Meters'
            self.rotation = 0

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

        if getRemoteProj4:
            self.crsProj4 = srsLookUp().wkid2proj4(self.crsCode, "proj4")
        else:
            self.crsProj4 = ""

        self.layers = []
        self._layersInfo()

    def _layersInfo(self):
        lyrs = arcpy.mapping.ListLayers(self.layerCollection)
        flatWMSProps = self.flattenWMS(lyrs)
        urls = []

        for lyr in lyrs:
            layer = {"name": lyr.longName, "visible": lyr.visible, "description": lyr.description,
                     "minScale": lyr.minScale, "maxScale": lyr.maxScale}

            if lyr.isFeatureLayer:
                if not arcpy.Exists( lyr.dataSource ): continue

                layer["type"] = "vector"
                layer['definitionQuery'] = lyr.definitionQuery
                if lyr.dataSource.endswith(".shp"): layer["path"] = lyr.dataSource
                else: layer["path"] = os.path.join( lyr.workspacePath, lyr.datasetName)

                symbols = json.loads( lyr._arc_object.getsymbology() )
                layer['layout'] = symbols

                descrip = arcpy.Describe( lyr.dataSource )
                layer['crsID'] = descrip.Spatialreference.factoryCode
                layer['crsName'] = descrip.Spatialreference.name
                layer['crsGeographic'] = not descrip.Spatialreference.PCSCode > 0
                layer['crsAuth'] =  "EPSG" if self.crsCode < 32767 else "ESRI"

                if "point" in descrip.ShapeType.lower(): layer['geomType'] = "Point"
                elif "line" in descrip.ShapeType.lower(): layer['geomType'] = "Line"
                elif "polygon" in descrip.ShapeType.lower(): layer['geomType'] = "Polygon"
                else: layer['geomType'] = "Other"

                if lyr.showLabels and len(lyr.labelClasses):
                    labelClass = lyr.labelClasses[0]
                    layer["labelExpression"] = labelClass.expression
                if lyr.definitionQuery:
                    layer["definitionQuery"] = lyr.definitionQuery

            elif lyr.isGroupLayer:
                layer["type"] = "group"
                layer["childeren"] = [n.longName for n in arcpy.mapping.ListLayers(lyr)
                                                                 if not n.isServiceLayer ][1:]
            elif lyr.isRasterLayer:
                layer["type"] = "raster"
                layer["path"] = lyr.dataSource

                if len(lyr._arc_object.getsymbology()):
                    symbols = json.loads( lyr._arc_object.getsymbology() )
                    if 'renderer' in symbols: layer['symbology'] = symbols['renderer']

                descrip = arcpy.Describe( lyr.dataSource )
                layer['crsID'] = descrip.Spatialreference.factoryCode
                layer['crsName'] = descrip.Spatialreference.name
                layer['crsGeographic'] = not descrip.Spatialreference.PCSCode > 0
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
        """
        :param lyrs: a iterator with layers, Like from arcpy.ListLayerd
        :return: a list with the sublayers in de ServiceLayer
        """
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
        del self.layerCollection
        del self.df