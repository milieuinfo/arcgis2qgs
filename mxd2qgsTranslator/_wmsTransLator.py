import os, sys


class wmsTransLator:
    def __init__(self):
        pass

    @staticmethod
    def makeWMSurl( url, layerNames, crs=31370 ):

        wmsUri =  "dpiMode=7&url={0}&format=image/png&crs=EPSG:{1}".format(url, crs)

        for lyrName in layerNames:
            wmsUri = wmsUri + "&styles=&layers=" + lyrName

        return wmsUri
