import loady
from . types import make
from . types.defaults import FIELD_TYPES
from distutils.version import LooseVersion


MINIMUM_VERSIONS = {'serial': '2.7'}

INSTALL_NAMES = {
    'BiblioPixelAnimations': 'BiblioPixelAnimations',
    'flask': 'flask',
    'noise': 'noise',
    'serial': 'pyserial',
}

VERSION_MESSAGE = """
You have version %s of module '%s' but you need version %s.

Please upgrade at the command line with:

    $ pip install %s --upgrade

"""

MISSING_MESSAGE = """
You are missing module '%s'.

Please install it at the command line with:

    $ pip install %s

"""


def _validate_typename(typename):
    root_module = typename.split('.')[0]
    min_version = MINIMUM_VERSIONS.get(root_module)
    if not min_version:
        return

    version = __import__(root_module).VERSION
    if LooseVersion(version) >= LooseVersion(min_version):
        return

    install_name = INSTALL_NAMES.get(root_module, root_module)
    raise ValueError(VERSION_MESSAGE % (
        root_module, version, min_version, install_name))


def _import(typename, base_path=None, module=False):
    try:
        loader = loady.code.load_module if module else loady.code.load_code
        result = loader(typename, base_path)
        _validate_typename(typename)
        return result

    except ImportError as e:
        root_module = typename.split('.')[0]
        install_name = INSTALL_NAMES.get(root_module)
        if install_name:
            try:
                __import__(root_module)
            except ImportError:
                msg = MISSING_MESSAGE % (root_module, install_name)
                e.msg = msg + e.msg
        raise


def import_symbol(typename, base_path=None):
    return _import(typename, base_path)


def import_module(typename, base_path=None):
    return _import(typename, base_path, True)


def make_object(*args, typename, base_path=None, **kwds):
    """Make an object from a symbol."""
    object_class = import_symbol(typename, base_path)
    field_types = getattr(object_class, 'FIELD_TYPES', FIELD_TYPES)
    return object_class(*args, **make.component(kwds, field_types))
