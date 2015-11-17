from distutils.core import setup
setup(name='mxdTranslator',
    description='Translate ESRI Arcgis .mxd files to QGIS .qgs files.',
    author='Kay Warrie',
    author_email='kaywarrie@gmail.com',
    version='1.0',
    packages=['mxdParser','mxdTranslator','qgsWriter' ],
    package_dir={'qgsWriter': 'qgsWriter',
                 'mxdTranslator':'mxdTranslator',
                 'mxdParser':'mxdParser'},
    data_files=[('Lib/site-packages/mxdTranslator/esri/toolboxes', ['QGIStool.pyt'])]  ,
    # package_data={'mxdTranslator': ['esri/toolboxes/*.*']},
    scripts=[]
    )