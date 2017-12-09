# -*- coding: utf-8 -*-

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    from .map_to_appcontext import MapToAppcontext
    return MapToAppcontext(iface)
