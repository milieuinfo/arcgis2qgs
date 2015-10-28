# -*- coding: utf-8 -*-
import sys, os
import xml.etree.ElementTree as ET
from _srs import srs

class qgsWriter:
    def __init__(self, projectname="", version="2.0.1-Dufour", bbox=[0,-180,360,-180], srs=None, mapUnits="unknown" ):
        """
        :param projectname: the name/title of your project
        :param version: the version of qgis
        :param bbox: the boundingbox of the map in the form [xmin,ymin,xmax,ymax]
        :param mapUnits: meters or degrees
        :param srs: a qgsWriter.srs object of the map crs
        """
        self.qgis = ET.Element("qgis", projectname=projectname, version=version)
        ET.SubElement(self.qgis, "title" ).text = projectname

        self._setMapCanvas(bbox, mapUnits, srs)

    def _setMapCanvas(self, bbox, mapUnits, crs):
        self.mapcanvas =  ET.Element("mapcanvas")
        ET.SubElement(self.mapcanvas, "units" ).text =  mapUnits

        extent = ET.SubElement(self.mapcanvas, "extent" )
        ET.SubElement(extent, "xmin" ).text = str( bbox[0] )
        ET.SubElement(extent, "ymin" ).text = str( bbox[1] )
        ET.SubElement(extent, "xmax" ).text = str( bbox[2] )
        ET.SubElement(extent, "ymax" ).text = str( bbox[3] )
        #TODO: handle data with projection diffrent hten mapprojection
        ET.SubElement(self.mapcanvas, "projections" ).text = "0"

        if crs:
            ET.SubElement(self.mapcanvas, "destinationsrs").append( crs.crsNode() )

        for child in self.qgis:
            if child.name == "mapcanvas":
                self.qgis.remove( child )
        self.qgis.append(self.mapcanvas)

    def addLegendItem(self):
        #TODO: implementation
        pass

    def addProjectLayerItem(self):
        #TODO: implementation
        pass

    #------------------------------------------#
    def save(self, qgsFilePath):
        tree= ET.ElementTree(self.qgis)
        tree.write(qgsFilePath)

    def log(self):
        print( ET.tostring( self.qgis ) )