# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

class qgsLayerTree:
    def __init__(self, rootName=""):
        """
        :param rootName: the name of the rootlayer
        """
        self.tree = dict(name=rootName, layers=[], checked='Qt::Checked', expanded='1')

    def addLayer(self, layerId, name="", level=None, checked=True, expanded=True):
        """
        Add a regular layer
        :param layerId:
        :param name:
        :param level:
        :param checked:
        :param expanded:
        """
        if not level:
           level = self.tree

        checkedStr = "Qt::Checked" if checked else "Qt::Unchecked"
        expandedStr = "1" if expanded else "0"
        layer = dict(id=str(layerId), name=name, checked=checkedStr, expanded=expandedStr)
        level['layers'].append(layer)

    def addGroup(self, name='', level=None, checked=True, expanded=True):
        """
        Add a gropup layer
        :param name:
        :param level:
        :param checked:
        :param expanded:
        """
        if not level:
           level = self.tree
        else:
            if 'layers' in level.keys(): raise Exception("layer is not a group layer")

        checkedStr = "Qt::Checked" if checked else "Qt::Unchecked"
        expandedStr = "1" if expanded else "0"
        layer = dict(name=name, layers=[], checked=checkedStr, expanded=expandedStr)
        level['layers'].append( layer )
        return

    def _appendNodes(self, treeRecord, node):
        if 'layers' in treeRecord.keys():
            attribs = { k:n for k,n in treeRecord.items() if k <> 'layers' }

            group = ET.SubElement(node ,'layer-tree-group', attribs)
            for layer in treeRecord['layers']:
                self._appendNodes( layer, group )
            return group
        else:
            return ET.SubElement(node, 'layer-tree-layer', treeRecord)


    def node(self):
        rootName = self.tree['name']
        rootGroup = ET.Element('layer-tree-group',  expanded="1", checked="Qt::Checked", name=rootName)

        for layer in self.tree['layers']:
            self._appendNodes( layer, rootGroup )

        return rootGroup
