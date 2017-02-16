from distutils.core import setup
import py2exe

setup(
    console = [{
        "script": "OSRBoxDriver.py",
        "icon_resources": [(1, "OSRBox.ico")]
    }],
    data_files = [( "", [ "OSRBox.yml" ])]
)
