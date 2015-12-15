import os, sys
import xml.etree.cElementTree as ET

class qgsSrs:
    def __init__(self, proj4="", srsid=None, crs=4326, description="", projectionacronym="",
                 ellipsoidacronym="", geographic=False, auth="EPSG" ):
        """
        :param proj4: the proj4 string
        :param srsid: internal srsid of qgis, leave empty if unknown
        :param crs: the Well Known ID of hte srs
        :param description: the name/description of the srs
        :param projectionacronym: the projection acronym
        :param ellipsoidacronym: the ellipsoid acronym
        :param geographic: bool, true if not projected
        :param auth: authority like EPSG or ESRI
        """
        self.proj4 = proj4
        self.srsid = srsid
        self.srid = str(crs)
        self.authid = "{1}:{0}".format(crs, auth)
        self.description =description
        self.projectionacronym = projectionacronym
        self.ellipsoidacronym = ellipsoidacronym
        self.geographic = geographic
        if geographic: self.geographicflag = "true"
        else: self.geographicflag = "false"

    def node(self):
        """
        :return: a ElementTree xml-node of the projection in the QGIS format
        """
        self.spatialrefsysNode = ET.Element("spatialrefsys")

        if self.proj4:
            ET.SubElement(self.spatialrefsysNode, "proj4").text = self.proj4
        else:
            ET.SubElement(self.spatialrefsysNode, "proj4")
        if self.srsid:
            ET.SubElement(self.spatialrefsysNode, "srsid" ).text = self.srsid
        else:
            ET.SubElement(self.spatialrefsysNode, "srsid" )

        ET.SubElement(self.spatialrefsysNode, "srid"    ).text = self.srid
        ET.SubElement(self.spatialrefsysNode, "authid"  ).text = self.authid
        ET.SubElement(self.spatialrefsysNode, "description").text = self.description

        ET.SubElement(self.spatialrefsysNode, "projectionacronym" ).text = self.projectionacronym
        ET.SubElement(self.spatialrefsysNode, "ellipsoidacronym"  ).text = self.ellipsoidacronym
        ET.SubElement(self.spatialrefsysNode, "geographicflag"  ).text = self.geographicflag

        return self.spatialrefsysNode