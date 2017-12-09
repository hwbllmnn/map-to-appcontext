from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
from qgis.core import QgsMapLayerRegistry, QgsRasterLayer
import os.path
from .create_appcontext_dialog import CreateAppcontextDialog
from cgi import parse_qs
import json

class MapToAppcontext:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = u'&terrestris'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MapToAppcontext')
        self.toolbar.setObjectName(u'MapToAppcontext')

    def initGui(self):
        action = QAction('Create appcontext', self.iface.mainWindow())
        action.triggered.connect(self.showAppcontextDialog)
        action.setEnabled(True)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                u'&terrestris',
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def showAppcontextDialog(self):
        crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        self.contextDialog = CreateAppcontextDialog()
        self.contextDialog.accepted.connect(self.createAppcontext)
        self.contextDialog.exec_()

    def createMapconfig(self, mapconfig):
        canvas = self.iface.mapCanvas()
        extent = canvas.extent()
        center = extent.center()
        mapconfig['center'] = {'x': center.x(), 'y': center.y()}
        mapconfig['extent'] = {
            'lowerLeft': {
                'x': extent.xMinimum(),
                'y': extent.yMinimum()
            },
            'upperRight': {
                'x': extent.xMaximum(),
                'y': extent.yMaximum()
            }
        }
        crs = canvas.mapSettings().destinationCrs()
        mapconfig['projection'] = crs.postgisSrid()
        return mapconfig

    def createMaplayers(self):
        result = []
        registry = QgsMapLayerRegistry.instance()
        layers = registry.mapLayers()
        for id in layers:
            layer = layers[id]
            if layer.type() == 1:
                obj = {}
                obj['name'] = layer.name()
                parsed = parse_qs(layer.source())
                obj['source'] = {
                    'layerNames': parsed['layers'][0],
                    'layerStyles': '',
                    'url': parsed['url'][0],
                    'type': 'TileWMS',
                    'version': '1.1.1'
                }
                if 'style' in parsed:
                    obj['source']['layerStyles'] = parsed['style'][0]
                result.append(obj)
        return result

    def createAppcontext(self):
        file = self.contextDialog.fileField.text()
        result = {
            'viewport': {
                'subModules': [{
                    'mapConfig': {},
                    'mapLayers': []
                }]
            }
        }
        if file != '':
            with open(file) as jsonData:
                result = json.load(jsonData)

        context = result['viewport']['subModules'][0]['subModules'][0]
        self.createMapconfig(context['mapConfig'])
        context['mapLayers'] = self.createMaplayers()
        with open(file, 'w') as outfile:
            json.dump(result, outfile)
