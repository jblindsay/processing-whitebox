# -*- coding: utf-8 -*-

"""
***************************************************************************
    whiteboxProvider.py
    ---------------------
    Date                 : December 2017
    Copyright            : (C) 2017 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'December 2017'
__copyright__ = '(C) 2017, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import QgsProcessingProvider, QgsMessageLog

from processing.core.ProcessingConfig import ProcessingConfig, Setting

from processing_whitebox import whiteboxUtils

pluginPath = os.path.dirname(__file__)


class WhiteboxProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()
        self.algs = []

    def id(self):
        return 'whitebox'

    def name(self):
        return 'WhiteBox Tools'

    def longName(self):
        version = whiteboxUtils.version()
        return 'WhiteBox Tools ({})'.format(version) if version is not None else 'WhiteBox Tools'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'whiteboxtools.png'))

    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(),
                                            whiteboxUtils.WHITEBOX_ACTIVE,
                                            self.tr('Activate'),
                                            True))
        ProcessingConfig.addSetting(Setting(self.name(),
                                            whiteboxUtils.WHITEBOX_EXECUTABLE,
                                            self.tr('prepair executable'),
                                            whiteboxUtils.whiteboxToolsPath(),
                                            valuetype=Setting.FILE))
        ProcessingConfig.addSetting(Setting(self.name(),
                                            whiteboxUtils.WHITEBOX_VERBOSE,
                                            self.tr('Log commands output'),
                                            False))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        ProcessingConfig.removeSetting(whiteboxUtils.WHITEBOX_ACTIVE)
        ProcessingConfig.removeSetting(whiteboxUtils.WHITEBOX_EXECUTABLE)
        ProcessingConfig.removeSetting(whiteboxUtils.WHITEBOX_VERBOSE)

    def isActive(self):
        return ProcessingConfig.getSetting(whiteboxUtils.WHITEBOX_ACTIVE)

    def setActive(self, active):
        ProcessingConfig.setSettingValue(whiteboxUtils.WHITEBOX_ACTIVE, active)

    def defaultVectorFileExtension(self, hasGeometry=True):
        return 'shp'

    def defaultRasterFileExtension(self):
        return 'tif'

    def supportedOutputRasterLayerExtensions(self):
        return ['tif', 'flt', 'sdat', 'rdc', 'dep']

    def supportedOutputVectorLayerExtensions(self):
        pass

    def supportsNonFileBasedOutput(self):
        return False

    def loadAlgorithms(self):
        self.algs = []
        folder = whiteboxUtils.descriptionPath()

        for descriptionFile in os.listdir(folder):
            if descriptionFile.endswith('txt'):
                try:
                    alg = WhiteboxAlgorithm(os.path.join(folder, descriptionFile))
                    if alg.name().strip() != '':
                        self.algs.append(alg)
                    else:
                        QgsMessageLog.logMessage(self.tr('Could not load WhiteBox Tools algorithm from file: {}'.format(descriptionFile)),
                                                 self.tr('Processing'), QgsMessageLog.CRITICAL)
                except Exception as e:
                    QgsMessageLog.logMessage(self.tr('Could not load WhiteBox Tools algorithm from file: {}\n{}'.format(descriptionFile, str(e))),
                                             self.tr('Processing'), QgsMessageLog.CRITICAL)

        for a in self.algs:
            self.addAlgorithm(a)

    def tr(self, string, context=''):
        if context == '':
            context = 'WhiteBoxAlgorithmProvider'
        return QCoreApplication.translate(context, string)
