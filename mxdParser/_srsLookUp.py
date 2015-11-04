import os, sys, urllib2


class srsLookUp:
    def __init__(self, timeout=15, proxyHost="", port="", proxyUser=None, proxyPass=None):
        "find SRS params using http://epsg.io/"
        self.timeout = timeout
        self.Url = "http://epsg.io/"
        self.proxyUrl = ""

        if (isinstance(proxyHost, unicode) or isinstance(proxyHost, str)) & proxyHost.startswith("http://"):
            self.proxyUrl = "http://"
            if proxyUser and proxyPass:
                self.proxyUrl += proxyUser + ':' + proxyPass + '@'
            self.proxyUrl += proxyHost + ':' + port
            self.opener = urllib2.build_opener(self.proxyUrl)
        else:
            self.opener = None

    def wkid2proj4(self, wkid, format="proj4"):
        """
        :param wkid: the espg or other well known id, like 4326 for wgs84
        :param format: *format*: The crs format of the returned string. One of "ogcwkt", "esriwkt", or "proj4"
        :return: a string in the requested format if one was found otherwese None
        """
        link = self.Url + "{0}.{1}".format(wkid, format)
        try:
            if self.opener:
                result = self.opener.open(link, timeout=self.timeout)
            else:
                result = urllib2.urlopen(link, timeout=self.timeout)
        except urllib2.URLError as er:
            print( "Could not find proj4 because: " + er.reason )
            return None

        if 'text/html' in result.info().getheader("Content-Type"):
           print( "Could not find proj4 because: {} is not a valid code".format(wkid) )
           return None
        else:
           return result.read()
