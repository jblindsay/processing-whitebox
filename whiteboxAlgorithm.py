# -*- coding: utf-8 -*-

"""
***************************************************************************
    whiteboxAlgorithm.py
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
from qgis.PyQt.QCore import QCoreApplication
from qgis.core import QgsProcessingAlgorithm
from processing.core.parameters import getParameterFromString

pluginPath = os.path.dirname(__file__)


class WhiteboxAlgorithm(QgsProcessingAlgorithm):

    def __init__(self, descriptionFile):
        super().__init__()

        self.descriptionFile = descriptionFile
        self._name = ''
        self._displayName = ''
        self._group = 'WhiteboxTools'
        self._groupId = 'whiteboxtools'
        self._shortHelp = ''

        self.params = []

        self.defineCharacteristicsFromFile()

    def createInstance(self):
        return self.__class__(self.descriptionFile)

    def name(self):
        return self._name

    def displayName(self):
        return self._displayName

    def group(self):
        return self._group

    def groupId(self):
        return self._groupId

    def shortHelpString(self):
        return self._shortHelp

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'whiteboxtools.png'))

    def tr(self, text):
        return QCoreApplication.translate("WhiteboxAlgorithm", text)

    def defineCharacteristicsFromFile(self):
        with open(self.description_file) as lines:
            line = lines.readline().strip('\n').strip()
            self._name = line

            line = lines.readline().strip('\n').strip()
            self._displayName = line

            line = lines.readline().strip('\n').strip()
            self._shortHelp = line

            line = lines.readline().strip('\n').strip()
            while line != '':
                self.params.append(getParameterFromString(line))
                line = lines.readline().strip('\n').strip()

    def processAlgorithm(self, parameters, context, feedback):
        arguments = [whiteboxUtils.whiteboxToolsPath()]

        for param in self.parameterDefinitions():
            if param.isDestination():
                continue

            if isinstance(param, (QgsProcessingParameterRasterLayer, QgsProcessingParameterFeatureSource)):
                pass
            else:
                arguments.append('--{}="{}"'.format(param.name(),
                                                    self.parameterAsInt(parameters, param.name(), context)))

        for out in self.destinationParameterDefinitions():
            pass
