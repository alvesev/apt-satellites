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

from lib.python.RepoSuiteGenerator import RepoSuiteGenerator

class AptRepo:

    repoId = None
    dir = None
    repoSuitePool = None
    dirGpgHome = None
    gpgKeyId = None

    _dirDebFilesPool = None

    def __init__(self, dirRepoLocation, dirGpgHome, gpgKeyId):
        self.dir = dirRepoLocation
        self.dirGpgHome = dirGpgHome
        self.gpgKeyId = gpgKeyId

        self.repoId = os.path.basename(self.dir)

        self._dirDebFilesPool = self.dir + '/pool'
        self.repoSuitePool = RepoSuiteGenerator().getSuitePoolFromDir(self._dirDebFilesPool)
