import xml.etree.ElementTree as ET
import xml.dom.minidom as dom
import httplib

ns = {'sld': "http://www.opengis.net/sld", 'ogc': "http://www.opengis.net/ogc",
      'xlink':'http://www.w3.org/1999/xlink', 'xsi':"http://www.w3.org/2001/XMLSchema-instance"}

ET.register_namespace("", ns['sld'])
ET.register_namespace("ogc", ns['ogc'])
ET.register_namespace("xlink", ns['xlink'])


def checkLinkExists(link):
      c = httplib.HTTPConnection( link )
      c.request("HEAD", '')
      if c.getresponse().status == 200:
         return True
      else:
         return False

