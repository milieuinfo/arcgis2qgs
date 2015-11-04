import mxdParser as mp
import qgsWriter as qw
import sys, os

import xml.dom.minidom as xml

mxdPath = r'C:\Users\k.warrie\Projects\arcgis2qgs\examples\test2.mxd'
qgsPath = r'C:\Users\k.warrie\Projects\tests\test2.qgs'
mxd = mp.mxdReader(mxdPath)

prjSrs = qw.qgsSrs(mxd.crsProj4, None, mxd.crsCode, mxd.crsName,
                   mxd.crsProjectionacronym, mxd.crsEllipsoidacronym, mxd.crsGeographic, mxd.crsAuth)

prjQgs = qw.qgsWriter( projectname=mxd.title, bbox=mxd.bbox, mapUnits=mxd.mapUnits, srs=prjSrs)

for arclyr in mxd.layers:
    print arclyr

    dataType =  arclyr["type"]

    if dataType not in [ "vector", "raster" ]: continue #other types are not supported yet

    dataPath = arclyr["path"]
    dataName = arclyr["name"]
    datageomType = None

    if dataType == "vector":
        datageomType = arclyr["geomType"]

    qgsLyr = qw.qgsMapLayer(dataName, dataType, datageomType, prjSrs )
    qgsLyr.layerTitle = dataName

    if dataType == "vector":
       if dataPath.endswith(".shp"):
          qgsLyr.setDatasource(dataPath, None, provider="ogr" )
       else:
          path, datalayer = os.path.split(dataPath)
          qgsLyr.setDatasource(path, datalayer, provider="ogr" )
    elif dataType == "raster":
        qgsLyr.setDatasource(dataPath, None, provider="gdal" )

    prjQgs.addLayer(qgsLyr)

x= xml.parseString(prjQgs.toSring())
print( x.toprettyxml() )

# fl= open(qgsPath, 'w')
# fl.write( x.toprettyxml())
# fl.close()
