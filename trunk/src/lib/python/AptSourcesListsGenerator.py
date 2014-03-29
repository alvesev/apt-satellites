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
import sys

class AptSourcesListsGenerator:

    _serverPath = 'localhost/pub'
    _serverProtocol = 'ftp'

    _netSectionHeader = """###
##    Network address: %s
#
"""
    _localSectionHeader = """###
##    File system's local path: %s
#
"""

    def __init__(self, aptRepo):
        self._suitePool = aptRepo.repoSuitePool
        self._dirRepo = aptRepo.dir
        self._repoId = aptRepo.repoId

    def generateContent(self):
        netUrl =  self._serverProtocol + '://' 
        netUrl += self._serverPath + '/' + self._repoId
        localUrl = 'file://' + os.path.abspath(self._dirRepo)

        netSection = self._netSectionHeader % netUrl
        localSection = self._localSectionHeader % localUrl

        for suite in self._suitePool:
            nextStringNetwork = netUrl + '  ' + suite.name + ' '
            nextStringLocal = localUrl + '  ' + suite.name + ' '

            for component in suite.componentsPool.values():
                nextStringNetwork += ' ' + component.name
                nextStringLocal +=  ' ' + component.name

            netSection += '# deb      ' + nextStringNetwork + '\n'
            netSection += '# deb-src  ' + nextStringNetwork + '\n'
            localSection += '# deb      ' + nextStringLocal + '\n'
            localSection += '# deb-src  ' + nextStringLocal + '\n'

        return netSection + '\n' + localSection

    def dumpToFile(self, fileName):
        try:
            fileHandle = open(fileName, 'w')
            fileHandle.write(self.generateContent())
            fileHandle.close()
        except:
            sys.stderr.write("Failed to write a content into the fileHandle '%s'.\n" % fileName)
            raise


