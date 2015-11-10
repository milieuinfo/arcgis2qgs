import os
from mxdParser import *
from utils import run_in_other_thread
from qgsWriter import *

class mxd2qgs:
    def __init__(self):
        self.mxd = None
        self.prjSrs = None
        self.prjQgs = None

    def convertMxd(self, mxdPath, qgsPath, startQgis=False  ):
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

            if dataType not in [ "vector", "raster" ]: continue #other types are not supported yet

            dataPath = arclyr["path"]
            dataName = arclyr["name"]

            datageomType = arclyr["geomType"] if dataType == "vector" else None

            qgsLyr = qgsMapLayer(dataName, dataType, datageomType, lyrSrs )
            qgsLyr.layerTitle = dataName

            if dataType == "vector":
               if dataPath.endswith(".shp"):
                  qgsLyr.setDatasource(dataPath, None, provider="ogr" )
               else:
                  path, datalayer = os.path.split(dataPath)
                  qgsLyr.setDatasource(path, datalayer, provider="ogr" )

               layout = arclyr['layout']['renderer']
               render = None

               if datageomType == 'Line':
                   render = self.getLineRender(layout)
               elif datageomType == 'Polygon':
                   render = self.getPolygonRender(layout)
               elif datageomType == 'Point':
                   render =  self.getPointRender(layout)

               if render: qgsLyr.setRenderer( render )

            elif dataType == "raster":
                qgsLyr.setDatasource(dataPath, None, provider="gdal" )

            self.prjQgs.addLayer(qgsLyr, checked= arclyr['visible'])

        self.prjQgs.save(qgsPath)

        if startQgis:
           startfile = run_in_other_thread(os.startfile)
           startfile(qgsPath)

    def getPointRender(self, layout):
        render = None

        if 'symbol' in layout.keys():
            color = layout['symbol']['color']
            size = layout['symbol']['size']

            outLine_color, outLine_width = ([0,0,0,255], 2)
            if 'outline' in  layout['symbol'].keys():
                outLine_color = layout['symbol']['outline']['color']
                outLine_width = layout['symbol']['outline']['width']

            pointStyle =  layout['symbol']['style'].lower().replace("esrisms","")
            if pointStyle not in qgsSymbol.pointTypeNames:
                pointStyle = "pentagon"

            render = qgsRenderer(symbolType="singleSymbol")

            symbol = qgsSymbol(dtype='marker')
            symbol.setSimpleMarker(color=color, color_border=outLine_color, typeName=pointStyle,
                                   outline_width=outLine_width, size=size, unit="Pixel")
            render.addSymbol(symbol)

        elif "uniqueValueInfos" in layout.keys():
            target_attr = layout['field1']
            render = qgsRenderer(symbolType="categorizedSymbol", target_attr=target_attr)
            categoryList = []
            default_symbol = None
            n = 0

            for uniqueValueInfo in layout['uniqueValueInfos']:
                color =  uniqueValueInfo['symbol']['color']
                size = uniqueValueInfo['symbol']['size']

                outLine_color, outLine_width = ([0,0,0,255], 2)
                if 'outline' in  uniqueValueInfo['symbol'].keys():
                    outLine_color = uniqueValueInfo['symbol']['outline']['color']
                    outLine_width = uniqueValueInfo['symbol']['outline']['width']

                pointStyle =  uniqueValueInfo['symbol']['style'].lower().replace("esrisms","")
                if pointStyle not in qgsSymbol.pointTypeNames:
                    pointStyle = "pentagon"

                symbol = qgsSymbol(dtype='marker')
                symbol.setSimpleMarker(color=color, color_border=outLine_color, typeName=pointStyle,
                                       outline_width=outLine_width, size=size, unit="Pixel")

                symCat = symbolCategory(uniqueValueInfo['value'], uniqueValueInfo['label'], str(n), symbol)
                categoryList.append(symCat)
                n += 1

            if 'defaultSymbol' in layout.keys():
                color = layout['defaultSymbol']['color']
                size = layout['defaultSymbol']['size']

                outLine_color, outLine_width = ([0,0,0,255], 2)
                if 'outline' in  layout['defaultSymbol'].keys():
                    outLine_color = layout['defaultSymbol']['outline']['color']
                    outLine_width = layout['defaultSymbol']['outline']['width']

                pointStyle =  layout['defaultSymbol']['style'].lower().replace("esrisms","")
                if pointStyle not in qgsSymbol.pointTypeNames:
                    pointStyle = "pentagon"

                default_symbol = qgsSymbol(dtype='marker')
                default_symbol.setSimpleMarker(color=color, color_border=outLine_color, typeName=pointStyle,
                                               outline_width=outLine_width, size=size, unit="Pixel")

            render.addCategorizedSymbols(categoryList, default_symbol)
        else:
            return None

        return render

    def getPolygonRender(self, layout):
        render = None

        if 'symbol' in layout.keys():
            color =  layout['symbol']['color']

            outLine_color = layout['symbol']['outline']['color']
            outLine_width = layout['symbol']['outline']['width']
            outLine_style = layout['symbol']['outline']['style'].lower().replace("esrisfs","")

            fillStyle = layout['symbol']['style'].lower().replace("esrisfs","")

            render = qgsRenderer(symbolType="singleSymbol")

            symbol = qgsSymbol(dtype='fill')
            symbol.setSimpleFill(color=color, color_border=outLine_color, outline_width=outLine_width,
                                 style_border=outLine_style, style=fillStyle, unit="Pixel")
            render.addSymbol(symbol)

        elif "uniqueValueInfos" in layout.keys():
            target_attr = layout['field1']
            render = qgsRenderer(symbolType="categorizedSymbol", target_attr=target_attr)
            categoryList = []
            default_symbol = None
            n = 0

            for uniqueValueInfo in layout['uniqueValueInfos']:
                color =         uniqueValueInfo['symbol']['color']
                outLine_color = uniqueValueInfo['symbol']['outline']['color']
                outLine_width = uniqueValueInfo['symbol']['outline']['width']
                outLine_style = uniqueValueInfo['symbol']['outline']['style'].lower().replace("esrisfs","")
                fillStyle =     uniqueValueInfo['symbol']['style'].lower().replace("esrisfs","")

                symbol = qgsSymbol(dtype='fill')
                symbol.setSimpleFill(color=color, color_border=outLine_color, outline_width=outLine_width,
                                     style_border=outLine_style, style=fillStyle, unit="Pixel")

                symCat = symbolCategory(uniqueValueInfo['value'], uniqueValueInfo['label'], str(n), symbol)
                categoryList.append(symCat)
                n += 1

            if 'defaultSymbol' in layout.keys():
                color =         layout['defaultSymbol']['color']
                outLine_color = layout['defaultSymbol']['outline']['color']
                outLine_width = layout['defaultSymbol']['outline']['width']
                outLine_style = layout['defaultSymbol']['outline']['style'].lower().replace("esrisfs","")
                fillStyle =     layout['defaultSymbol']['style'].lower().replace("esrisfs","")

                default_symbol = qgsSymbol(dtype='fill')
                default_symbol.setSimpleFill(color=color, color_border=outLine_color, outline_width=outLine_width,
                                             style_border=outLine_style, style=fillStyle, unit="Pixel")

            render.addCategorizedSymbols(categoryList, default_symbol)
        else:
            return None

        return render

    def getLineRender(self, layout):
        if 'symbol' in layout.keys():
            color =  layout['symbol']['color']
            width = layout['symbol']['width']
            style = "solid"

            render = qgsRenderer(symbolType="singleSymbol")

            symbol = qgsSymbol(dtype='line')
            symbol.setSimpleLine(color=color, line_width=width, line_style=style, unit="Pixel")
            render.addSymbol(symbol)

        elif "uniqueValueInfos" in layout.keys():
            target_attr = layout['field1']
            render = qgsRenderer(symbolType="categorizedSymbol", target_attr=target_attr)
            categoryList = []
            default_symbol = None
            n = 0

            for uniqueValueInfo in layout['uniqueValueInfos']:
                color =  uniqueValueInfo['symbol']['color']
                width = uniqueValueInfo['symbol']['width']
                style = "solid"

                symbol = qgsSymbol(dtype='line')
                symbol.setSimpleLine(color=color, line_width=width, line_style=style, unit="Pixel")

                symCat = symbolCategory(uniqueValueInfo['value'], uniqueValueInfo['label'], str(n), symbol)
                categoryList.append(symCat)
                n += 1

            if 'defaultSymbol' in layout.keys():
                color =  layout['defaultSymbol']['color']
                width = layout['defaultSymbol']['width']
                style = "solid"

                default_symbol = qgsSymbol(dtype='line')
                default_symbol.setSimpleLine(color=color, line_width=width, line_style=style, unit="Pixel")

            render.addCategorizedSymbols(categoryList, default_symbol)
        else:
            return None

        return render