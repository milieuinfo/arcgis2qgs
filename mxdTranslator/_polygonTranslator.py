# -*- coding: utf-8 -*-
from qgsWriter import *

class polygonTranslator:
    def __init__(self):
        pass

    @staticmethod
    def getPolygonRender(layout):
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

            for valueInfo in layout['uniqueValueInfos']:
                symbol = qgsSymbol(dtype='fill')

                if 'symbol' in valueInfo:
                    color =         valueInfo['symbol']['color']
                    outLine_color = valueInfo['symbol']['outline']['color']
                    outLine_width = valueInfo['symbol']['outline']['width']
                    outLine_style = valueInfo['symbol']['outline']['style'].lower().replace("esrisfs","")
                    fillStyle =     valueInfo['symbol']['style'].lower().replace("esrisfs","")

                    symbol.setSimpleFill(color=color, color_border=outLine_color, outline_width=outLine_width,
                                     style_border=outLine_style, style=fillStyle, unit="Pixel")

                if 'label' in valueInfo.keys(): #if label left blank, there will be no label key
                    symCat = symbolCategory(valueInfo['value'], valueInfo['label'], str(n), symbol)
                else:
                    symCat = symbolCategory(valueInfo['value'], valueInfo['value'], str(n), symbol)

                categoryList.append(symCat)
                n += 1

            if 'defaultSymbol' in layout.keys():
                color =         layout['defaultSymbol']['color']
                outLine_color = layout['defaultSymbol']['outline']['color']
                outLine_width = layout['defaultSymbol']['outline']['width']
                outLine_style = layout['defaultSymbol']['outline']['style'].lower().replace("esrisfs","")
                fillStyle =     layout['defaultSymbol']['style'].lower().replace("esrisfs","")
                label = "" if not "defaultLabel" in layout.keys() else layout["defaultLabel"]

                default_symbol = qgsSymbol(dtype='fill')
                default_symbol.setSimpleFill(color=color, color_border=outLine_color, outline_width=outLine_width,
                                             style_border=outLine_style, style=fillStyle, unit="Pixel")
                symCat = symbolCategory("", label, str(n+1), default_symbol)
                categoryList.append(symCat)

            render.addCategorizedSymbols(categoryList, default_symbol)

        elif "classBreakInfos"  in layout.keys():
            target_attr = layout['field']
            render = qgsRenderer(symbolType="graduatedSymbol", target_attr=target_attr, graduatedMethod="GraduatedColor")
            classList = []
            n = 0

            for valueInfo in layout['classBreakInfos']:
                symbol = qgsSymbol(dtype='fill')
                if 'symbol' in valueInfo.keys():
                    color =         valueInfo['symbol']['color']
                    outLine_color = valueInfo['symbol']['outline']['color']
                    outLine_width = valueInfo['symbol']['outline']['width']
                    outLine_style = valueInfo['symbol']['outline']['style'].lower().replace("esrisfs","")
                    fillStyle =     valueInfo['symbol']['style'].lower().replace("esrisfs","")

                    symbol.setSimpleFill(color=color, color_border=outLine_color, outline_width=outLine_width,
                                     style_border=outLine_style, style=fillStyle, unit="Pixel")

                if 'label' in valueInfo.keys():
                    symCat = symbolRange(valueInfo['classMinValue'], valueInfo['classMaxValue'],
                                         valueInfo['label'], str(n), symbol)
                else:
                    label = "{0} - {1}".format(valueInfo['classMinValue'], valueInfo['classMaxValue'])
                    symCat = symbolRange(valueInfo['classMinValue'], valueInfo['classMaxValue'], label, str(n), symbol)

                classList.append(symCat)
                n += 1

            render.addRangedSymbols(classList)

        else:
            return None

        return render