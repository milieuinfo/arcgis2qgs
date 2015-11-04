from qgsWriter import *
from mxdParser.utils import run_in_other_thread
from mxdParser import *
import os, sys

def convertMxd(mxdPath, qgsPath, startQgis  ):
    """
    :param mxdPath: path to the input
    :param qgsPath: path to the output qgs-file
    :param startQgis: bool, laucht the qgs-file
    """
    mxd = mxdReader(mxdPath)

    prjSrs = qgsSrs(mxd.crsProj4, None, mxd.crsCode, mxd.crsName,
                       mxd.crsProjectionacronym, mxd.crsEllipsoidacronym, mxd.crsGeographic, mxd.crsAuth)

    prjQgs = qgsWriter( projectname=mxd.title, bbox=mxd.bbox, mapUnits=mxd.mapUnits, srs=prjSrs)

    for arclyr in mxd.layers:
        dataType =  arclyr["type"]

        if dataType not in [ "vector", "raster" ]: continue #other types are not supported yet

        dataPath = arclyr["path"]
        dataName = arclyr["name"]
        datageomType = None

        if dataType == "vector":
            datageomType = arclyr["geomType"]

        qgsLyr = qgsMapLayer(dataName, dataType, datageomType, prjSrs )
        qgsLyr.layerTitle = dataName

        if dataType == "vector":
           if dataPath.endswith(".shp"):
              qgsLyr.setDatasource(dataPath, None, provider="ogr" )
           else:
              path, datalayer = os.path.split(dataPath)
              qgsLyr.setDatasource(path, datalayer, provider="ogr" )

           #SET STYLE, TODO -> improve
           layout = arclyr['layout']['renderer']
           if 'symbol' in layout.keys():
             color =  layout['symbol']['color']
             render = qgsRenderer(symbolType="singleSymbol")

             if datageomType == 'Line':
                 symbol = qgsSymbol(dtype='line')
                 symbol.setSimpleLine(color=color)
                 render.addSymbol(symbol)
                 qgsLyr.setRenderer(render)
             elif datageomType == 'Polygon':
                 symbol = qgsSymbol(dtype='fill')
                 symbol.setSimpleFill(color=color)
                 render.addSymbol(symbol)
                 qgsLyr.setRenderer(render)
             elif datageomType == 'Point':
                 symbol = qgsSymbol(dtype='marker')
                 symbol.setSimpleMarker(color=color)
                 render.addSymbol(symbol)
                 qgsLyr.setRenderer(render)


        elif dataType == "raster":
            qgsLyr.setDatasource(dataPath, None, provider="gdal" )

        prjQgs.addLayer(qgsLyr, checked= arclyr['visible'])

    prjQgs.save(qgsPath)

    if startQgis:
       startfile = run_in_other_thread(os.startfile)
       startfile(qgsPath)

if __name__ == "__main__":
    mxd = sys.argv[1]
    qgs = sys.argv[2]
    convertMxd( mxd, qgs, False )