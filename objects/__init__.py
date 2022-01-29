# Code to import each item in this Directory as a sub package.
# E.G. objects.Cube

import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)

for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
    __import__(modname)

del ispkg, pkgutil, modname, importer
