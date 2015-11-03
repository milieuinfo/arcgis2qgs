# -*- coding: utf-8 -*-
import sys, os, datetime
import xml.etree.ElementTree as ET
from _qgsMapLayer import qgsMapLayer
from _qgsSrs import qgsSrs

class qgsWriter:
    def __init__(self, projectname="", version="2.0.1-Dufour", bbox=[0,-180,360,-180], srs=None, mapUnits="unknown" ):
        """
        :param projectname: the name/title of your project
        :param version: the version of qgis
        :param bbox: the boundingbox of the map in the form [xmin,ymin,xmax,ymax]
        :param mapUnits: meters or degrees
        :param srs: a qgsWriter.qgsSrs object of the map crs, if none it will default to WGS84
        """
        self.qgis = ET.Element("qgis", projectname=projectname, version=version)
        ET.SubElement(self.qgis, "title" ).text = projectname

        if not srs: srs= self._setSrs()

        self.mapCanvas = self._setMapCanvas(bbox, mapUnits, srs)
        self.legend = ET.SubElement(self.qgis, "legend", updateDrawingOrder="true" )
        self.projectlayers = ET.SubElement(self.qgis, "projectlayers", layercount="0" )

        self.layers = {}

    def _setMapCanvas(self, bbox, mapUnits, srs):
        mapcanvas =  ET.Element("mapcanvas")
        ET.SubElement(mapcanvas, "units" ).text =  mapUnits

        extent = ET.SubElement(mapcanvas, "extent" )
        ET.SubElement(extent, "xmin" ).text = str( bbox[0] )
        ET.SubElement(extent, "ymin" ).text = str( bbox[1] )
        ET.SubElement(extent, "xmax" ).text = str( bbox[2] )
        ET.SubElement(extent, "ymax" ).text = str( bbox[3] )
        #TODO: handle data with projection different mapprojections
        ET.SubElement(mapcanvas, "projections" ).text = "0"

        if srs:
            ET.SubElement(mapcanvas, "destinationsrs").append(srs.node())

        for child in self.qgis:
            if child.tag == "mapcanvas":
                self.qgis.remove( child )
        self.qgis.append(mapcanvas)
        return mapcanvas

    def _addLegendItem(self, layerName, active=False, opened=True, checked=True, visible=True, drawingOrder=-1):
        layerID = layerName + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        if active:
            self.legend.attrib['activeLayer'] = layerID
        #create attribute values
        openAttr = "true" if opened else "false"
        checkedAttr = "Qt::Checked" if checked else "Qt::Unchecked"
        hiddenAttr= "false" if visible else 'true'
        visibleAttr= "1" if visible else '0'
        #create elements
        legendlayer = ET.SubElement(self.legend, 'legendlayer', drawingOrder=str(drawingOrder),
                 open=openAttr, checked=checkedAttr, name=layerName, showFeatureCount="0" )
        filegroup = ET.SubElement(legendlayer, 'filegroup', {"open":openAttr, "hidden":hiddenAttr} )
        ET.SubElement(filegroup, 'legendlayerfile', isInOverview="0", layerid=layerID, visible=visibleAttr )

        return layerID

    def _addProjectLayerItem(self, mapLayer ):
        self.projectlayers.append(mapLayer.node())
        self.projectlayers.attrib["layercount"] = str(int(self.projectlayers.attrib["layercount"]) + 1)

    def _setSrs(self, proj4="+proj=longlat +datum=WGS84 +no_defs",
               srsid=None, crs=4326, description="WGS 84", ellipsoidacronym="WGS 84", geographic=True):
        return qgsSrs(proj4, srsid, crs, description, "", ellipsoidacronym, geographic)

    #--------------Public-----------------#
    def addLayer(self, mapLayer, active=False, opened=True, checked=True, visible=True, drawingOrder=-1):
        layerID = self._addLegendItem( mapLayer.layerName, active, opened, checked, visible, drawingOrder)
        #set new laterID
        mapLayer.layerID = layerID
        self.layers[layerID] = mapLayer
        self._addProjectLayerItem(mapLayer)

    def save(self, qgsFilePath):
        tree= ET.ElementTree(self.qgis)
        tree.write(qgsFilePath)

    def log(self):
        "for debugging purposes"
        print( ET.tostring( self.qgis ) )