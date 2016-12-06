import xml.etree.cElementTree as ET

class qgsSymbol:
    #static properties
    pointTypeNames = ["circle", "square", "cross", "rectangle", "diamond","pentagon","triangle",
                      "equilateral_triangle","star","regular_star","arrow","filled_arrowhead","x"]
    measuretypes =  ["MM","Pixel","MapUnit"]
    dtypes = ["fill","marker","line"]
    def __init__(self, alpha=1, dtype=None, name="0" ):
        """
        A symbol object can be used for rendering
        :param alpha: alfa transparency needs to be in between 1 and 0
        :param dtype: fill, line or marker
        :param name: a name for the symbol, optional
        """
        if not ( 1 >= alpha >= 0):
            raise Exception("alfa needs to be in between 1 and 0")
        if dtype not in self.dtypes:
            raise Exception(
                "{0} is not a supported symboly type, only fill, line and marker are supporded".format(dtype))

        self.symbol = ET.Element("symbol", alpha=str(alpha), type=dtype, name=name)
        self.layers = []

    def setSimpleMarker(self, color=(255,255,255,255), color_border=(0,0,0,255), angle=0, typeName="circle",
                              offset=(0,0) , outline_width=0.2, size=2, unit="MM" ):
        """
        Set the symbol as a SimpleMarker
        :param color: the inside color: a tuple of (r,b,g,a)
        :param color_border: a tuple of (r,b,g,a)
        :param angle: the angel in degrees
        :param typeName: the type icon: "circle","square","cross","rectangle","diamond","x", ...
        :param offset: offset of the icon from te center in unit, a tuple with (x,y) -offset
        :param outline_width: the with of the outline in 'unit'
        :param size: size of the icon in 'unit'
        :param unit: MM, MapUnit or Pixel
        """
        layer = ET.SubElement(self.symbol, "layer", {"pass":"0", "class":"SimpleMarker", "locked":"0"})
        #validation
        if not typeName in self.pointTypeNames:
            raise Exception("{0} is not a support Typename".format(typeName))
        if not unit in self.measuretypes:
            raise Exception("{0} is not a support unit, only MM, MapUnit and Pixel are supported".format(unit))

        #set props
        ET.SubElement(layer, "prop", k="angle", v=str(angle) )
        ET.SubElement(layer, "prop", k="color", v=",".join([str(n) for n in color]) )
        ET.SubElement(layer, "prop", k="color_border", v=",".join([str(n) for n in color_border]) )
        ET.SubElement(layer, "prop", k="name", v=typeName )

        ET.SubElement(layer, "prop", k="offset", v="{0},{1}".format(offset[0],offset[1]) )
        ET.SubElement(layer, "prop", k="outline_width", v=str(outline_width) )
        ET.SubElement(layer, "prop", k="scale_method", v="area")
        ET.SubElement(layer, "prop", k="size", v=str(size) )

        #assume allways same type of measurement
        ET.SubElement(layer, "prop", k="size_unit", v=unit)
        ET.SubElement(layer, "prop", k="offset_unit", v=unit)
        ET.SubElement(layer, "prop", k="outline_width_unit", v=unit)

        self.layers.append(layer)
        return layer

    def setSimpleFill(self, color=(255,255,255,255), color_border=(0,0,0,255), style="solid", style_border="solid",
                            offset=(0,0) , outline_width=0.2, unit="MM" ):
        """
        Set the symbol as a SimpleFill
        :param color: the inside color: a tuple of (r,b,g,a)
        :param color_border: a tuple of (r,b,g,a)
        :param style:
        :param style_border
        :param offset: offset of the icon from te center in unit, a tuple with (x,y) -offset
        :param outline_width: the with of the outline in 'unit'
        :param unit: MM, MapUnit or Pixel
        """
        layer = ET.SubElement(self.symbol, "layer", {"pass":"0", "class":"SimpleFill", "locked":"0"})
        #validation
        if not unit in self.measuretypes:
            raise Exception("{0} is not a support unit, only MM, MapUnit and Pixel are supported".format(unit))

        #set props
        ET.SubElement(layer, "prop", k="color", v=",".join([str(n) for n in color]) )
        ET.SubElement(layer, "prop", k="color_border", v=",".join([str(n) for n in color_border]) )
        ET.SubElement(layer, "prop", k="style", v=style )
        ET.SubElement(layer, "prop", k="offset", v="{0},{1}".format(offset[0],offset[1]) )
        ET.SubElement(layer, "prop", k="outline_width", v=str(outline_width) )
        ET.SubElement(layer, "prop", k="outline_style", v=style_border )

        #assume allways same type of measurement
        ET.SubElement(layer, "prop", k="outline_width_unit", v=unit)
        ET.SubElement(layer, "prop", k="offset_unit", v=unit)

        self.layers.append(layer)
        return layer

    def setSimpleLine(self, color=(0,0,0,255), capstyle="square", joinstyle="bevel", line_style ="solid",
                     offset=0 , line_width=0.2, useCustomdash=False, customdash=(5,2), unit="MM"  ):
        """
        Set the symbol as a SimpleLine
        :param color:  a tuple of (r,b,g,a)
        :param capstyle: square, flat or round
        :param joinstyle: bevel, miter or round
        :param offset: offset in 'unit'
        :param line_width: line width in 'unit'
        :param useCustomdash: bool
        :param customdash: ( dashlength , whitespace ) in 'unit'
        :param unit:  MM, MapUnit or Pixel
        """
        layer = ET.SubElement(self.symbol, "layer", {"pass":"0", "class":"SimpleLine", "locked":"0"})
        #validation
        if not unit in self.measuretypes:
            raise Exception("{0} is not a support unit, only MM, MapUnit and Pixel are supported".format(unit))

        #set props
        ET.SubElement(layer, "prop", k="capstyle", v=capstyle )
        ET.SubElement(layer, "prop", k="joinstyle", v=joinstyle )
        ET.SubElement(layer, "prop", k="line_color", v=",".join([str(n) for n in color]) )
        ET.SubElement(layer, "prop", k="line_style", v=line_style )
        ET.SubElement(layer, "prop", k="offset", v=str(offset) )
        ET.SubElement(layer, "prop", k="line_width", v=str(line_width) )
        ET.SubElement(layer, "prop", k="width_map_unit_scale", v="0,0,0,0,0,0" )

        #dash
        use_custom_dash = "1" if useCustomdash else "0"
        ET.SubElement(layer, "prop", k="use_custom_dash", v=use_custom_dash )
        ET.SubElement(layer, "prop", k="customdash", v="{0};{1}".format(customdash[0],customdash[1]) )
        ET.SubElement(layer, "prop", k="customdash_map_unit_scale", v="0,0,0,0,0,0" )

        #assume allways same type of measurement
        ET.SubElement(layer, "prop", k="offset_unit", v=unit)
        ET.SubElement(layer, "prop", k="line_width_unit", v=unit)
        ET.SubElement(layer, "prop", k="customdash_unit", v=unit)

        self.layers.append(layer)
        return layer

    def layerFromDict(self , symbolClass , props={} ):
        """
        Add a layer to the symbol from a dict of properties
        :param symbolClass: the class of the layer like  SimpleLine or SimpleLine
        :param props: the dictionary of properties
        """
        layer = ET.SubElement(self.symbol, "layer", {"pass":"0", "class": symbolClass, "locked":"0"})
        for prop in props.items():
            ET.SubElement(layer, "prop", k=prop[0] , v=str( prop[1] ) )

        self.layers.append(layer)
        return layer

    def node(self):
        ":return: a ElementTree xml-node of the symbol in the QGIS format"
        return self.symbol

    def clear(self):
        "clear all layers"
        for child in self.symbol: self.symbol.remove( child )
        self.layers = []



