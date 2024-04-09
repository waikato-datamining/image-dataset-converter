from setuptools import setup, find_namespace_packages


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="image-dataset-converter",
    description="Python3 library for converting between various image annotation dataset formats.",
    long_description=(
            _read('DESCRIPTION.rst') + b'\n' +
            _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-datamining/image-dataset-converter",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    license='MIT License',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    install_requires=[
        "seppl>=0.1.3",
        "wai.logging",
        "wai.common>=0.0.44",
        "pillow",
        "matplotlib",
        "imagesize",
        "opex",
        "defusedxml",
        "numpy",
        "shapely",
    ],
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "idc-convert=idc.tool.convert:sys_main",
            "idc-find=idc.tool.find:sys_main",
            "idc-help=idc.tool.help:sys_main",
            "idc-registry=idc.registry:sys_main",
        ],
        "idc.readers": [
            "idc_readers1=idc.reader:seppl.io.Reader",
            "idc_readers_imgcls1=idc.reader.imgcls:seppl.io.Reader",
            "idc_readers_imgseg1=idc.reader.imgseg:seppl.io.Reader",
            "idc_readers_objdet1=idc.reader.objdet:seppl.io.Reader",
        ],
        "idc.filters": [
            "idc_filters1=idc.filter:seppl.io.Filter",
            "idc_filters_imgcls1=idc.filter.imgcls:seppl.io.Filter",
            "idc_filters_imgseg1=idc.filter.imgseg:seppl.io.Filter",
            "idc_filters_objdet1=idc.filter.objdet:seppl.io.Filter",
        ],
        "idc.writers": [
            "idc_writers1=idc.writer:seppl.io.Writer",
            "idc_writers_imgcls1=idc.writer.imgcls:seppl.io.Writer",
            "idc_writers_imgseg1=idc.writer.imgseg:seppl.io.Writer",
            "idc_writers_objdet1=idc.writer.objdet:seppl.io.Writer",
        ]
    },
)
