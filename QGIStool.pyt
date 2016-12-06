import arcpy, os.path, tempfile
from mxd2qgsTranslator import mxd2qgs
from lyr2sldTranslator import mxd2sld

class Toolbox:
    def __init__(self):
        self.label =  "QGIS_Toolbox"
        self.alias  = "QGIS-Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [mxd2qgsTool, lyr2sldTool]

class mxd2qgsTool:
    def __init__(self):
        self.label       = "MXD to QGIS"
        self.description = "Translate a Arcgis .mxd projectfile to a QGIS .qgs project file, " \
                           "only shapefiles, FGDB-feature classes en File rasters (like .tif) will be available. " \
                           "Markers with icons connot be translated in QGS, only simple symbogy will be supported."

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_mxd = arcpy.Parameter(
            displayName="Input Mapdocument (.mxd)",
            name="in_mxd",
            datatype="DEMapDocument",
            parameterType="Required",
            direction="Input")

        out_qgs = arcpy.Parameter(
            displayName="Output QGIS file (.qgs)",
            name="out_qgs",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")

        out_qgs.filter.list = ['qgs']

        start_qgs = arcpy.Parameter(
            displayName="Launch QGIS when finished (QGIS needs to be installed)",
            name="launch",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Output")
        start_qgs.value = False

        parameters = [in_mxd, out_qgs, start_qgs]
        return parameters

    def execute(self, parameters, messages):
        mxdPath =  parameters[0].valueAsText
        qgsPath =  parameters[1].valueAsText
        startQgis = parameters[2].value
        mxd2qgs().convertMxd(mxdPath, qgsPath, startQgis)

class lyr2sldTool:
    def __init__(self):
        self.label       = "Layer to SLD"
        self.description = "Convert a layer to a 'Styled Layer Descriptor', a SLD-file. " \
                           "SLD is an OGC standard to store the layout of a GIS layer." \
                           "This type of file can be imported in QGIS and Geoserver." \
                           "Only vector-layout is support right now"

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_lyr = arcpy.Parameter(
            displayName="Input laag",
            name="in_lyr",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input")

        out_sld = arcpy.Parameter(
            displayName="Output SLD-file (.sld)",
            name="out_sld",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")
        out_sld.filter.list = ['sld']

        parameters = [in_lyr, out_sld]
        return parameters

    def execute(self, parameters, messages):
        lyr = parameters[0].valueAsText
        sldPath =  parameters[1].valueAsText

        if os.path.exists(lyr) and lyr.endswith(".lyr"):
            mxd2sld().convertLyr( lyr, sldPath )
        else:
            layer = parameters[0].value
            tmpDir = tempfile.gettempdir()
            tempLyr = arcpy.CreateUniqueName(lyr, tmpDir) + ".lyr"
            layer.save( tempLyr )
            mxd2sld().convertLyr(tempLyr, sldPath)
            os.remove(tempLyr)

