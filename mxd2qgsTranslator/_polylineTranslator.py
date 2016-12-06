# -*- coding: utf-8 -*-
from qgsWriter import *

class polylineTranslator:
    def __init__(self):
        pass

    @staticmethod
    def getLineRender(layout):
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

            for valueInfo in layout['uniqueValueInfos']:
                symbol = qgsSymbol(dtype='line')
                if 'symbol' in valueInfo.keys():
                    color =  valueInfo['symbol']['color']
                    width = valueInfo['symbol']['width']
                    style = "solid"

                    symbol.setSimpleLine(color=color, line_width=width, line_style=style, unit="Pixel")

                if 'label' in valueInfo.keys():
                    symCat = symbolCategory(valueInfo['value'], valueInfo['label'], str(n), symbol)
                else:
                    symCat = symbolCategory(valueInfo['value'], valueInfo['value'], str(n), symbol)

                categoryList.append(symCat)
                n += 1

            if 'defaultSymbol' in layout.keys():
                color =  layout['defaultSymbol']['color']
                width = layout['defaultSymbol']['width']
                style = "solid"
                label = "" if not "defaultLabel" in layout.keys() else layout["defaultLabel"]

                default_symbol = qgsSymbol(dtype='line')
                default_symbol.setSimpleLine(color=color, line_width=width, line_style=style, unit="Pixel")
                symCat = symbolCategory("", label, str(n+1), default_symbol)
                categoryList.append(symCat)

            render.addCategorizedSymbols(categoryList, default_symbol)

        elif "classBreakInfos"  in layout.keys():
            target_attr = layout['field']
            render = qgsRenderer(symbolType="graduatedSymbol", target_attr=target_attr, graduatedMethod="GraduatedColor")
            classList = []
            n = 0

            for valueInfo in layout['classBreakInfos']:
                symbol = qgsSymbol(dtype='line')
                if 'symbol' in valueInfo.keys():
                    color =  valueInfo['symbol']['color']
                    width = valueInfo['symbol']['width']
                    style = "solid"

                    symbol.setSimpleLine(color=color, line_width=width, line_style=style, unit="Pixel")

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
