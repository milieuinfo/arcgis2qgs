import os, sys, datetime
import xml.etree.ElementTree as ET
from _qgsSrs import qgsSrs
from _qgsRenderer import qgsRenderer
from _qgsSymbol import qgsSymbol

class qgsMapLayer:
    def __init__(self, name, dataType="vector", geometryType=None, srs=None, renderer=None, visible=True):
        """
        Create a maplayer object, only gdal/ogr sources are supported
        :param name: a name for the layer
        :param dataType: "vector" or "raster"
        :param geometryType: "Polygon","Point" or "Line"
        :param srs: a qgsWriter.qgsSrs object of the map crs, if Not set it will default to WGS84
        """
        geomTypes = ["Polygon","Point","Line"]
        dataTypes = ["vector", "raster"]
        #valdiation
        if  dataType not in dataTypes:
            raise Exception(
                "{0} is not a supported datatype, only {1} are supporded".format(dataType, ", ".join(dataTypes)))
        if dataType == "vector" and geometryType not in geomTypes:
            raise Exception(
                "{0} is not a supported geometry type, only {1} are supporded".format(geometryType, ", ".join(geomTypes)))

        #public properties
        self.layerName  = name
        self.visible = visible
        self.layerTitle  = ""
        self.abstract = ""
        self.keywords = []
        self.layerID = name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.minimumScale = 0
        self.maximumScale = 10**8
        self.minLabelScale = 0
        self.maxLabelScale = 10**8
        self.hasScaleBasedVisibilityFlag = False
        self.scaleBasedLabelVisibilityFlag = False
        if srs: self.srs = srs
        else: self.setSrs()

        #private properties
        self._geom = geometryType
        self._type = dataType
        self._datasource = None
        self._provider = "ogr"
        self._encoding = ""

        self.customproperties = {}

        if renderer:
            self.renderer = renderer
        elif dataType == "vector" :
            self.setRenderer()
        else:
            self.renderer = None

    def setDatasource(self, path, layer=None, encoding="UTF-8", provider="ogr"):
        self._datasource = path
        self._encoding = encoding
        self._provider = provider
        if layer:
            self._datasource += "|layername=" + layer

    def setSrs(self, proj4="+proj=longlat +datum=WGS84 +no_defs", srsid=None,
               crs=4326, description="WGS 84", ellipsoidacronym="WGS 84", geographic=True):
        self.srs = qgsSrs(proj4, srsid, crs, description, "", ellipsoidacronym, geographic)

    def setRenderer(self, renderer=None):
        """
        Set the vector renderer
        :param renderer: qgsRenderer object, if None a defualt style will be used
        """
        if self._type != "vector":
           return False #only for vectors
        if renderer != None:
           self.renderer = renderer
           return True

        #set default if no randerer provided
        self.renderer = qgsRenderer("singleSymbol")

        if self._geom == "Polygon":
            symbol = qgsSymbol(1,"fill")
            symbol.setSimpleFill()
            self.renderer.addSymbol(symbol)
        elif self._geom == "Line":
            symbol = qgsSymbol(1,"line")
            symbol.setSimpleLine()
            self.renderer.addSymbol(symbol)
        elif self._geom == "Point":
            symbol = qgsSymbol(1,"marker")
            symbol.setSimpleMarker()
            self.renderer.addSymbol(symbol)
        return True

    def node(self):
        """Convert to a XML node object"""
        #base setting
        mapLayer = ET.Element("maplayer")
        ET.SubElement(mapLayer, 'id').text = self.layerID
        ET.SubElement(mapLayer, 'title').text = self.layerTitle
        ET.SubElement(mapLayer, 'layername' ).text = self.layerName
        ET.SubElement(mapLayer, 'abstract').text = self.abstract
        keywordList = ET.SubElement(mapLayer, 'keywordList')
        for keyword in self.keywords:
            ET.SubElement(keywordList, 'value').text= keyword
        #attributes
        mapLayer.attrib['minimumScale'] = str( self.minimumScale )
        mapLayer.attrib['maximumScale'] = str( self.maximumScale )
        mapLayer.attrib['type'] = self._type
        if self._type == 'vector' :
            mapLayer.attrib['minLabelScale'] = str( self.minLabelScale )
            mapLayer.attrib['maxLabelScale'] = str( self.maxLabelScale )
            mapLayer.attrib['geometry'] = self._geom
            mapLayer.attrib['hasScaleBasedVisibilityFlag'] = "1" if self.hasScaleBasedVisibilityFlag else "0"
        mapLayer.attrib['scaleBasedLabelVisibilityFlag'] = "1" if self.scaleBasedLabelVisibilityFlag else "0"

        #datasource Settings
        ET.SubElement(mapLayer, 'datasource').text = self._datasource
        ET.SubElement(mapLayer, 'provider', encoding=self._encoding).text = self._provider

        #srs
        ET.SubElement(mapLayer, 'srs').append(self.srs.node())

        #renderer
        if self.renderer: mapLayer.append( self.renderer.node() )

        if self.customproperties:
            customproperties = ET.SubElement(mapLayer, 'customproperties')
            for key, val in self.customproperties.items():
                ET.SubElement(customproperties, 'property', {"key":key, "value": val} )

        return mapLayer