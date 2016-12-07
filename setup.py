from distutils.core import setup
setup(name='QGIS Tools for Arcgis',
    description='Translate ESRI Arcgis .mxd files to QGIS .qgs-files and layers to .sld-files',
    author='Kay Warrie',
    author_email='kaywarrie@gmail.com',
    version= '1.2.1',
    packages= ['mxdParser','mxd2qgsTranslator','qgsWriter','lyr2sldTranslator','sldWriter' ],
    package_dir= {'qgsWriter': 'qgsWriter', 'mxd2qgsTranslator':'mxd2qgsTranslator', 'mxdParser':'mxdParser',
                 'lyr2sldTranslator':'lyr2sldTranslator', 'sldWriter':'sldWriter' },
    data_files= [('Lib/site-packages/mxd2qgsTranslator/esri/toolboxes', ['QGIStool.pyt'])]
    )