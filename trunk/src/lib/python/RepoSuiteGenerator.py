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


import os
from .RepoSuite import RepoSuite
from .RepoSuiteComponent import RepoSuiteComponent

class RepoSuiteGenerator:

    _dirDebFilesPool = None

    def __init__(self):
        pass

    def getSuitePoolFromDir(self, dirDebFilesPool):
        self._acceptDirName(dirDebFilesPool)
        namesPool = self._evaluateSuiteNamesFromDebPoolDirectory()
        suitePool = []

        for suiteName, componentNamePool in  namesPool.items():
            suite = RepoSuite(suiteName)
            componentPool = [RepoSuiteComponent(val) for idx, val in enumerate(componentNamePool)]  # @UnusedVariable
            suite.addComponentPool(componentPool)
            suitePool.append(suite)
        return suitePool

    def _evaluateSuiteNamesFromDebPoolDirectory(self):
        namesPool = {}
        topDirLevel = self._dirDebFilesPool.count(os.path.sep)
        for parentDir, subDirs, files in os.walk(self._dirDebFilesPool):  # @UnusedVariable
            currentDirLevel = parentDir.count(os.path.sep)
            relativeDirLevel = currentDirLevel - topDirLevel
            if relativeDirLevel == 1:
                suiteName = os.path.basename(parentDir)
                componentsNames = subDirs
                namesPool[suiteName] = componentsNames
        self._validateNamesPool(namesPool)
        return namesPool

    def _validateNamesPool(self, namesPool):
        subMessage = "Is there correct structure for the deb-files pool directory named '%s'?" % self._dirDebFilesPool
        if not namesPool:
            raise Exception("Got void suite names pool. " + subMessage)
        for suiteName, componentNamePool in namesPool.items():
            if not componentNamePool:
                raise Exception("Got void value for component pool in suite '%s'. " % suiteName + subMessage)


    def _acceptDirName(self, dirName):
        if not os.path.isdir(dirName):
            raise Exception("Failed to find directory '%s' to be used as deb-files pool." % dirName)
        self._dirDebFilesPool =  os.path.abspath(dirName)
        self._dirDebFilesPool =  self._dirDebFilesPool.rstrip(os.path.sep)
