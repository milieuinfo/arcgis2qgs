# -*- coding: utf-8 -*-
from qgsWriter import *

class pointTranslator:
    def __init__(self):
        pass

    @staticmethod
    def getPointRender(layout):
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

            for valueInfo in layout['uniqueValueInfos']:
                symbol = qgsSymbol(dtype='marker')
                if 'symbol' in valueInfo.keys():
                    color =  valueInfo['symbol']['color']
                    size = valueInfo['symbol']['size']

                    outLine_color, outLine_width = ([0,0,0,255], 2)
                    if 'outline' in  valueInfo['symbol'].keys():
                        outLine_color = valueInfo['symbol']['outline']['color']
                        outLine_width = valueInfo['symbol']['outline']['width']

                    pointStyle =  valueInfo['symbol']['style'].lower().replace("esrisms","")
                    if pointStyle not in qgsSymbol.pointTypeNames:
                        pointStyle = "pentagon"

                    symbol.setSimpleMarker(color=color, color_border=outLine_color, typeName=pointStyle,
                                       outline_width=outLine_width, size=size, unit="Pixel")

                if 'label' in valueInfo.keys(): #if label left blank, there will be no label key
                    symCat = symbolCategory(valueInfo['value'], valueInfo['label'], str(n), symbol)
                else:
                    symCat = symbolCategory(valueInfo['value'], valueInfo['value'], str(n), symbol)

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
                label = "" if not "defaultLabel" in layout.keys() else layout["defaultLabel"]

                default_symbol = qgsSymbol(dtype='marker')
                default_symbol.setSimpleMarker(color=color, color_border=outLine_color, typeName=pointStyle,
                                               outline_width=outLine_width, size=size, unit="Pixel")
                symCat = symbolCategory("", label, str(n+1), default_symbol)
                categoryList.append(symCat)

            render.addCategorizedSymbols(categoryList, default_symbol)

        elif "classBreakInfos"  in layout.keys():
            target_attr = layout['field']
            render = qgsRenderer(symbolType="graduatedSymbol", target_attr=target_attr, graduatedMethod="GraduatedColor")
            classList = []
            n = 0

            for valueInfo in layout['classBreakInfos']:
                symbol = qgsSymbol(dtype='marker')

                if 'symbol' in valueInfo.keys():
                    color =  valueInfo['symbol']['color']
                    size = valueInfo['symbol']['size']

                    outLine_color, outLine_width = ([0,0,0,255], 2)
                    if 'outline' in  valueInfo['symbol'].keys():
                        outLine_color = valueInfo['symbol']['outline']['color']
                        outLine_width = valueInfo['symbol']['outline']['width']

                    pointStyle =  valueInfo['symbol']['style'].lower().replace("esrisms","")
                    if pointStyle not in qgsSymbol.pointTypeNames:
                        pointStyle = "pentagon"

                    symbol.setSimpleMarker(color=color, color_border=outLine_color, typeName=pointStyle,
                                       outline_width=outLine_width, size=size, unit="Pixel")

                if 'label' in valueInfo.keys(): #if label left blank, there will be no label key
                    symCat = symbolRange(valueInfo['classMinValue'], valueInfo['classMaxValue'], valueInfo['label'], str(n), symbol)
                else:
                    label = "{0} - {1}".format(valueInfo['classMinValue'], valueInfo['classMaxValue'])
                    symCat = symbolRange(valueInfo['classMinValue'], valueInfo['classMaxValue'], label, str(n), symbol)

                classList.append(symCat)
                n += 1

            render.addRangedSymbols(classList)
        else:
            return None

        return render