import arcpy, os
from mxdTranslator import mxd2qgs

class Toolbox:
    def __init__(self):
        self.label =  "QGIS_Toolbox"
        self.alias  = "QGIS-Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [mxd2qgsTool]

class mxd2qgsTool:
    def __init__(self):
        self.label       = "MXD to QGIS"
        self.description = "Translate a Arcgis .mxd projectfile to a QGIS .qgs project file, " \
                           "only shapefiles, FGDB-feature classes en File rasters (like .tif) will be available. " \
                           "Markers with icons connot be translated in QGS, only simple symbogy will be supported"

    def getParameterInfo(self):
        "Define parameter definitions"

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
