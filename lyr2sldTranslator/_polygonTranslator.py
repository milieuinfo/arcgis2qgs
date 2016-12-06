# -*- coding: utf-8 -*-
import sldWriter as sld

class polygonTranslator:
    def __init__(self):
        pass

    @staticmethod
    def getPolygonRender(layout, minScale=-1, maxScale=-1, name="", labelField=None):
        sldStyle = sld.style()

        if 'symbol' in layout.keys():
            color_rbga = layout['symbol']['color']
            colorHex = '#%02x%02x%02x' % ( color_rbga[0] , color_rbga[1], color_rbga[2])
            opacity = color_rbga[3] / 255

            outLine_colorHex, outLine_width = ("#000000", 1)
            if 'outline' in  layout['symbol'].keys():
                outLine_rgba = layout['symbol']['outline']['color']
                outLine_colorHex = '#%02x%02x%02x' % (outLine_rgba[0], outLine_rgba[1], outLine_rgba[2])
                outLine_width = layout['symbol']['outline']['width']

            #TODO: fillstyle
            #fillStyle = layout['symbol']['style'].lower().replace("esrisfs","")

            symbol = sld.vectorSymbol(dtype="PolygonSymbolizer", fillColor=colorHex, strokeColor=outLine_colorHex,
                                      strokeWidth=outLine_width,  opacity=opacity)
            sldStyle.addRule(name=name, Symbolizer=symbol, MinScale=minScale, MaxScale=maxScale, labelField=labelField)

        elif "uniqueValueInfos" in layout.keys():
            target_attr = layout['field1']
            uniqueValues = []

            for valueInfo in layout['uniqueValueInfos']:
                if 'symbol' in valueInfo.keys():
                    color_rbga = valueInfo['symbol']['color']
                    colorHex = '#%02x%02x%02x' % (color_rbga[0], color_rbga[1], color_rbga[2])
                    opacity = color_rbga[3] / 255
                    #outLine_style = valueInfo['symbol']['outline']['style'].lower().replace("esrisfs","")
                    #fillStyle =     valueInfo['symbol']['style'].lower().replace("esrisfs","")

                    outLine_colorHex, outLine_width = ("#000000", 1)
                    if 'outline' in  valueInfo['symbol'].keys():
                        outLine_rgba = valueInfo['symbol']['outline']['color']
                        outLine_colorHex = '#%02x%02x%02x' % (outLine_rgba[0], outLine_rgba[1], outLine_rgba[2])
                        outLine_width = valueInfo['symbol']['outline']['width']

                    symbol = sld.vectorSymbol(dtype="PolygonSymbolizer", fillColor=colorHex,
                                              strokeColor=outLine_colorHex, strokeWidth=outLine_width, opacity=opacity)
                    uniqueValues.append(valueInfo['value'])
                    ogcFilter = sld.ogcFilter.category(target_attr, str(valueInfo['value']))
                    label = str(valueInfo['value']) if not "label" in valueInfo.keys() else valueInfo["label"]

                    sldStyle.addRule(name=label, Filter=ogcFilter, title=label, Symbolizer=symbol,
                                     MinScale=minScale, MaxScale=maxScale, labelField=labelField)

            if 'defaultSymbol' in layout.keys():
                color_rbga = layout['defaultSymbol']['color']
                colorHex = '#%02x%02x%02x' % (color_rbga[0], color_rbga[1], color_rbga[2])
                opacity = color_rbga[3] / 255

                outLine_colorHex, outLine_width = ("#000000", 1)
                if 'outline' in layout['defaultSymbol'].keys():
                    outLine_rgba = layout['defaultSymbol']['outline']['color']
                    outLine_colorHex = '#%02x%02x%02x' % (outLine_rgba[0], outLine_rgba[1], outLine_rgba[2])
                    outLine_width = layout['defaultSymbol']['outline']['width']

                label = "" if not "defaultLabel" in layout.keys() else layout["defaultLabel"]
                ogcFilter = sld.ogcFilter.notInCollection(target_attr, uniqueValues)
                symbol = sld.vectorSymbol(dtype="PolygonSymbolizer", fillColor=colorHex,
                                          strokeColor=outLine_colorHex, strokeWidth=outLine_width, opacity=opacity)

                sldStyle.addRule(name=label, title=label, Filter=ogcFilter, Symbolizer=symbol,
                                 MinScale=minScale, MaxScale=maxScale, labelField=labelField)

        elif "classBreakInfos"  in layout.keys():
            target_attr = layout['field']

            for valueInfo in layout['classBreakInfos']:
                if 'symbol' in valueInfo.keys():
                    color_rbga =  valueInfo['symbol']['color']
                    colorHex = '#%02x%02x%02x' % (color_rbga[0], color_rbga[1], color_rbga[2])
                    opacity = color_rbga[3] / 255
                    #outLine_style = valueInfo['symbol']['outline']['style'].lower().replace("esrisfs","")
                    #fillStyle =     valueInfo['symbol']['style'].lower().replace("esrisfs","")

                    outLine_colorHex, outLine_width = ("#000000", 1)
                    if 'outline' in  valueInfo['symbol'].keys():
                        outLine_rgba = layout['defaultSymbol']['outline']['color']
                        outLine_colorHex = '#%02x%02x%02x' % (outLine_rgba[0], outLine_rgba[1], outLine_rgba[2])
                        outLine_width = layout['defaultSymbol']['outline']['width']

                    symbol = sld.vectorSymbol(dtype="PolygonSymbolizer", fillColor=colorHex,
                                              strokeColor=outLine_colorHex, strokeWidth=outLine_width, opacity=opacity)
                    ogcFilter = sld.ogcFilter.between(target_attr, str(valueInfo['classMinValue']), str(valueInfo['classMaxValue']))

                    if 'label' in valueInfo.keys(): #if label left blank, there will be no label key
                        sldStyle.addRule(name=valueInfo['label'], Filter=ogcFilter, title=valueInfo['label'],
                                         Symbolizer=symbol, MinScale=minScale, MaxScale=maxScale, labelField=labelField)
                    else:
                        label = "{0} - {1}".format(valueInfo['classMinValue'], valueInfo['classMaxValue'])
                        sldStyle.addRule(name=label, Filter=ogcFilter, title=label, Symbolizer=symbol, MinScale=minScale,
                                         MaxScale=maxScale, labelField=labelField)
        else:
            return None

        return sldStyle