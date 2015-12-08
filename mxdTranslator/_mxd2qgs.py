from mxdParser import *
from utils import run_in_other_thread
from qgsWriter import *
from _polygonTranslator import polygonTranslator
from _polylineTranslator import polylineTranslator
from _pointTranslator import pointTranslator
from xml.sax.saxutils import escape

class mxd2qgs:
    def __init__(self):
        self.mxd = None
        self.prjSrs = None
        self.prjQgs = None

    def convertMxd(self, mxdPath, qgsPath, startQgis=False ):
        """
        :param mxdPath: path to the input
        :param qgsPath: path to the output qgs-file
        :param startQgis: bool, laucht the qgs-file
        """
        self.mxd = mxdReader(mxdPath)

        self.prjSrs = qgsSrs(self.mxd.crsProj4, None, self.mxd.crsCode, self.mxd.crsName, self.mxd.crsProjectionacronym,
                             self.mxd.crsEllipsoidacronym, self.mxd.crsGeographic, self.mxd.crsAuth)

        self.prjQgs = qgsWriter(projectname= self.mxd.title, bbox= self.mxd.bbox, mapUnits= self.mxd.mapUnits,
                                srs= self.prjSrs)

        for arclyr in  self.mxd.layers:
            lyrSrs = self.prjSrs   #TODO -> find out lyr srs if not same as map crs
            dataType =  arclyr["type"]

            if dataType not in ["vector", "raster", "service"]: continue # other types are not supported yet

            dataName = arclyr["name"]

            datageomType = arclyr["geomType"] if dataType == "vector" else None

            qgsLyr = qgsMapLayer(dataName, dataType, datageomType, lyrSrs, visible= arclyr['visible'])
            qgsLyr.layerTitle = dataName

            if dataType == "vector":
               dataPath = arclyr["path"]
                #TODO def query
               if dataPath.endswith(".shp"):
                  qgsLyr.setDatasource(dataPath, None, provider="ogr" )
               else:
                  path, datalayer = os.path.split(dataPath)
                  qgsLyr.setDatasource(path, datalayer, provider="ogr" )

               layout = arclyr['layout']['renderer']
               render = None

               if datageomType == 'Line':
                   render = polylineTranslator.getLineRender(layout)
               elif datageomType == 'Polygon':
                   render = polygonTranslator.getPolygonRender(layout)
               elif datageomType == 'Point':
                   render =  pointTranslator.getPointRender(layout)

               if render: qgsLyr.setRenderer( render )

               if 'labelExpression' in arclyr.keys():
                   expr = arclyr['labelExpression'].replace("[",'').replace("]",'')
                   qgsLyr.customproperties = {
                       "labeling": "pal",
                       "labeling/enabled":"true",
                       "labeling/fieldName": expr
                   }

            elif dataType == "raster":
                dataPath = arclyr["path"]
                qgsLyr.setDatasource(dataPath, None, provider="gdal" )

            elif dataType == "service":
                if not 'serviceProperties' in arclyr.keys(): continue
                if arclyr['serviceProperties']['ServiceType'].upper() != 'WMS' : continue

                url = arclyr['serviceProperties']['URL'].split("?")[0]
                layerName = arclyr['serviceProperties']['Name']
                style = ""
                crs = self.mxd.crsCode

                wmsUri = escape( "dpiMode=7&url=%s&layers=%s&format=image/png&styles=%s&crs=EPSG:%s" % (url, layerName, style, crs) )
                qgsLyr.setDatasource(wmsUri, None, provider="wms" )

            self.prjQgs.addLayer(qgsLyr, checked= arclyr['visible'])

        self.prjQgs.save(qgsPath)

        if startQgis:
           startfile = run_in_other_thread(os.startfile)
           startfile(qgsPath)















    #-----------private-------------
    # def _makeLayerTree(self):
    #     self.qgsTree = qgsLayerTree()
    #     layers = self.prjQgs.layers
    #
    #     tree = [{"id": k, 'path': v.layerName.split("\\"), "layer": v} for k,v in layers.items()]
    #     self._parseTree(tree, self.qgsTree.tree)
    #     return self.qgsTree

    # def _parseTree(self, pathTree, layerTree):
    #
    #     groupCount = 0
    #     groups = {}
    #     subGroups = []
    #
    #     for rec in pathTree:
    #         layerId = rec['id']
    #         path = rec['path']
    #         layer = rec['layer']
    #
    #         if len(pathTree) == 1:
    #             self.qgsTree.addLayer(layerId, layer.layerName, layerTree, layer.visible)
    #
    #         elif len(pathTree) > 1:
    #             groupName = path[0]
    #             subPath = "\\".join( path[1:] )
    #
    #             if not groupName in groups.values():
    #                subTree= layerTree['layers'][groupCount]
    #                groups[groupCount] = groupName
    #                self.qgsTree.addGroup( groupName, subTree )
    #
    #             subGroups.append({"id": layerId, 'path': subPath, "layer": layer, 'groupID': groupCount})
    #
    #         groupCount += 1
    #
    #     for groupID in groups.keys():
    #         subPathTree = [ n for n in subGroups if n['groupID'] == groupID ]
    #         subLayerTree = layerTree['layers'][groupID]
    #         self._parseTree(subPathTree, subLayerTree)