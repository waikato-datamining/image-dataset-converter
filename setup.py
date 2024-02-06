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
        "seppl>=0.1.0",
        "wai.logging",
    ],
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "img-convert=idc.tool.convert:sys_main",
            "img-find=idc.tool.find:sys_main",
            "img-help=idc.tool.help:sys_main",
            "img-registry=idc.registry:sys_main",
        ],
        "idc.readers": [
            "idc_readers1=idc.reader:seppl.io.Reader",
        ],
        "idc.filters": [
            "idc_filters1=idc.filter:seppl.io.Filter",
        ],
        "idc.writers": [
            "idc_writers1=idc.pretrain:seppl.io.Writer",
        ]
    },
)