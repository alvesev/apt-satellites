#!/usr/bin/python -B

#
#  Copyright 2013-2014 Alex Vesev
#
#  This file is part of Apt Satellites.
#
#  Apt Satellites is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Apt Satellites is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Apt Satellites.  If not, see <http://www.gnu.org/licenses/>.
#
##


from .ConfApt import ConfApt
from .ConfAptIndexes import ConfAptIndexes

class AptConfGenerator:

    dirConfLocation = None
    aptConfFileName = None
    indexesConfFileNamePool = None
    suite = None

    def __init__(self, suite, dirConfLocation):
        self.suite = suite
        self.dirConfLocation = dirConfLocation
        self.aptConfFileName = dirConfLocation + '/' + 'apt-conf-' + self.suite.name + '.conf'
        self.indexesConfFileNamePool = []

    def createFiles(self):
        self.createConfAptFile()
        self.createConfAptIndexesFile()
        return self.getFilesNamesPool()

    def getFilesNamesPool(self):
        return {'aptConf': self.aptConfFileName,
                'indexesConf': self.indexesConfFileNamePool}

    def createConfAptFile(self):
        confApt = ConfApt(self.aptConfFileName, self.suite)
        confApt.dumpContentToFile()

    def createConfAptIndexesFile(self):
        for component in self.suite.componentsPool.values():
            fileName = self.dirConfLocation + '/' + 'apt-indexes_' + self.suite.name + '_' + component.name + '.conf'
            confAptIndexes = ConfAptIndexes(fileName, self.suite, component)
            confAptIndexes.dumpContentToFile()
            self.indexesConfFileNamePool.append(fileName)
