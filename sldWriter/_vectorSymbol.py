from bootstrap import *

class vectorSymbol:
    #static properties
    pointTypeNames = ["circle", "square", "cross", "star", "x", ""]
    dtypes = ["PointSymbolizer","LineSymbolizer","PolygonSymbolizer"]

    def __init__(self, dtype="PointSymbolizer", pointType="circle", size=7,
                strokeColor="#000000", strokeWidth=1, fillColor="#FFFFFF", opacity=1, rotation=0, externalGraphic=None):
        """
        A symbol object can be used for rendering
        :param dtype: "PointSymbolizer","LineSymbolizer","PolygonSymbolizer","TextSymbolizer" or "RasterSymbolizer"
        :param strokeColor: color as hex
        :param strokeWidth: in pixel
        :param fillColor: color as hex
        """
        # validation
        if not ( 1 >= opacity >= 0):
            raise Exception("opacity needs to be in between 1 and 0")
        if dtype not in self.dtypes:
            raise Exception(
            '{0} is not a supported symboly type, only {1} are supporded'.format(dtype, ", ".join(self.dtypes) ))

        self.symbol = ET.Element( "{{{sld}}}".format(**ns)+ dtype )

        if dtype == "PointSymbolizer":
            if externalGraphic:
                Graphic= self._getExternalGraphic( externalGraphic, size, rotation, opacity )
                self.symbol.append(Graphic)
            elif pointType in self.pointTypeNames:
                Graphic= self._getSimpleGrapic(size, fillColor, strokeColor, strokeWidth, rotation, opacity, pointType)
                self.symbol.append(Graphic)
            else:
                raise Exception("Parameter of grapic are not correct")

        elif dtype == "LineSymbolizer":
            stroke = ET.SubElement( self.symbol, "{{{sld}}}Stroke".format(**ns) )
            ET.SubElement(stroke, "{{{sld}}}CssParameter".format(**ns), name="stroke" ).text = strokeColor
            ET.SubElement(stroke, "{{{sld}}}CssParameter".format(**ns), name="stroke-width").text = strokeWidth
            ET.SubElement(stroke, "{{{sld}}}CssParameter".format(**ns), name="stroke-opacity").text = opacity

        elif dtype ==  "PolygonSymbolizer":
            stroke = ET.SubElement( self.symbol, "{{{sld}}}Stroke".format(**ns) )
            ET.SubElement(stroke, "{{{sld}}}CssParameter".format(**ns), name="stroke" ).text = strokeColor
            ET.SubElement(stroke, "{{{sld}}}CssParameter".format(**ns), name="stroke-width").text = str(strokeWidth)
            ET.SubElement(stroke, "{{{sld}}}CssParameter".format(**ns), name="stroke-opacity").text = str(opacity)

            fill = ET.SubElement( self.symbol, "{{{sld}}}Fill".format(**ns) )
            ET.SubElement(fill, "{{{sld}}}CssParameter".format(**ns), name="fill" ).text = fillColor
            ET.SubElement(fill, "{{{sld}}}CssParameter".format(**ns), name="fill-opacity").text = str(opacity)

    @staticmethod
    def _getSimpleGrapic(size, color, color_border, border_width, angle, opacity, typeName):
        grapicTXT = """
        <Graphic xmlns="http://www.opengis.net/sld" >
            <Mark>
                <WellKnownName>{{typeName}}</WellKnownName>
                <Fill>
                    <CssParameter name="fill">{{color}}</CssParameter>
                </Fill>
                <Stroke>
                    <CssParameter name="stroke">{{color_border}}</CssParameter>
                    <CssParameter name="stroke-width">{{border_width}}</CssParameter>
                </Stroke>
            </Mark>
            <Size>{{size}}</Size>
            <Rotation>{{angle}}</Rotation>
            <Opacity>{{opacity}}</Opacity>
        </Graphic>""".format(size=size, color=color, color_border=color_border, opacity=opacity,
                             border_width=border_width, angle=angle, typeName=typeName )
        return ET.fromstring(grapicTXT)

    @staticmethod
    def _getExternalGraphic(link, size, angle , opacity):
        if link.upper().endswith("JPG") or  link.upper().endswith("JPEG"):
            mime = "image/jpeg"
        elif  link.upper().endswith("GIF"):
            mime = "image/gif"
        elif link.upper().endswith("SVG"):
            mime = "image/svg+xml"
        else:
            mime = "image/png"

        grapicTXT = """
        <Graphic xmlns="http://www.opengis.net/sld" >
           <ExternalGraphic>
               <OnlineResource xlink:type="simple"
                               xlink:href="{{link}}" />
               <Format>{{mime}}</Format>
           </ExternalGraphic>
           <Size>{{size}}/Size>
           <Rotation>{{angle}}</Rotation>
           <Opacity>{{opacity}}</Opacity>
        </Graphic>""".format(size=size, opacity=opacity, angle=angle, link=link, mime=mime )

        return ET.fromstring(grapicTXT)

    def node(self):
        """:return: a ElementTree xml-node of the symbol in the QGIS format"""
        return self.symbol



