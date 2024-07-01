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
        "seppl>=0.2.6",
        "wai.logging",
        "wai.common>=0.0.44",
        "pillow",
        "matplotlib",
        "imagesize",
        "fast-opex>=0.0.2",
        "defusedxml",
        "numpy",
        "shapely",
        "python-image-complete",
    ],
    version="0.0.3",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "idc-convert=idc.tool.convert:sys_main",
            "idc-exec=idc.tool.exec:sys_main",
            "idc-find=idc.tool.find:sys_main",
            "idc-help=idc.tool.help:sys_main",
            "idc-registry=idc.registry:sys_main",
            "idc-test-generator=idc.tool.test_generator:sys_main",
        ],
        "class_lister": [
            "idc=idc.class_lister",
        ],
    },
)
