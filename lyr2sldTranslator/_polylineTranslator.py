# -*- coding: utf-8 -*-
import sldWriter as sld

class polylineTranslator:
    def __init__(self):
        pass

    @staticmethod
    def getLineRender(layout, minScale=-1, maxScale=-1, name="", labelField=None):
        sldStyle = sld.style()

        if 'symbol' in layout.keys():
            color_rgba = layout['symbol']['color']
            colorHex = '#%02x%02x%02x' % (color_rgba[0], color_rgba[1], color_rgba[2])
            opacity = color_rgba[0] / 255
            outLine_width = layout['symbol']['width']

            symbol = sld.vectorSymbol(dtype="LineSymbolizer", strokeColor=colorHex, strokeWidth=outLine_width, opacity=opacity)
            sldStyle.addRule(name=name, Symbolizer=symbol, MinScale=minScale, MaxScale=maxScale, labelField=labelField)

        elif "uniqueValueInfos" in layout.keys():
            target_attr = layout['field1']
            uniqueValues = []

            for valueInfo in layout['uniqueValueInfos']:
                if 'symbol' in valueInfo.keys():
                    color_rgba = valueInfo['symbol']['color']
                    colorHex = '#%02x%02x%02x' % (color_rgba[0], color_rgba[1], color_rgba[2])
                    opacity = color_rgba[3] / 255
                    outLine_width = layout['symbol']['width']

                    symbol = sld.vectorSymbol(dtype="LineSymbolizer", strokeColor=colorHex,  strokeWidth=outLine_width,
                                              opacity=opacity)

                    uniqueValues.append(valueInfo['value'])
                    ogcFilter = sld.ogcFilter.category(target_attr, str(valueInfo['value']))
                    label = str(valueInfo['value']) if not "label" in valueInfo.keys() else valueInfo["label"]

                    sldStyle.addRule(name=label, Filter=ogcFilter, title=label, Symbolizer=symbol,
                                     MinScale=minScale, MaxScale=maxScale, labelField=labelField)

                if 'defaultSymbol' in layout.keys():
                    color_rgba =  layout['defaultSymbol']['color']
                    colorHex = '#%02x%02x%02x' % (color_rgba[0], color_rgba[1], color_rgba[2])
                    opacity = color_rgba[3] / 255
                    outLine_width = layout['defaultSymbol']['width']

                    label = "" if not "defaultLabel" in layout.keys() else layout["defaultLabel"]
                    symbol = sld.vectorSymbol(dtype="LineSymbolizer", fillColor=colorHex, strokeColor=colorHex,
                                              strokeWidth=outLine_width, opacity=opacity)

                    ogcFilter = sld.ogcFilter.notInCollection(target_attr, uniqueValues)

                    sldStyle.addRule(name=label, title=label, Filter=ogcFilter, Symbolizer=symbol,
                                     MinScale=minScale, MaxScale=maxScale, labelField=labelField)

        elif "classBreakInfos"  in layout.keys():
            target_attr = layout['field']

            for valueInfo in layout['classBreakInfos']:
                if 'symbol' in valueInfo.keys():
                    color_rgba = valueInfo['symbol']['color']
                    colorHex = '#%02x%02x%02x' % (color_rgba[0], color_rgba[1], color_rgba[2])
                    opacity = color_rgba[3] / 255
                    outLine_width = layout['symbol']['width']

                    ogcFilter = sld.ogcFilter.between(target_attr, str(valueInfo['classMinValue']), str(valueInfo['classMaxValue']))
                    symbol = sld.vectorSymbol(dtype="LineSymbolizer", fillColor=colorHex, strokeColor=colorHex,
                                              strokeWidth=outLine_width, opacity=opacity)

                    if 'label' in valueInfo.keys():
                        label = valueInfo['label']
                        sldStyle.addRule(name=label, title=label, Filter=ogcFilter, Symbolizer=symbol,
                                         MinScale=minScale, MaxScale=maxScale, labelField=labelField)
                    else:
                        label = "{0} - {1}".format(valueInfo['classMinValue'], valueInfo['classMaxValue'])
                        sldStyle.addRule(name=label, title=label, Filter=ogcFilter, Symbolizer=symbol,
                                         MinScale=minScale, MaxScale=maxScale, labelField=labelField)
        else:
            return None

        return sldStyle
