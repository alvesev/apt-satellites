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


import sys
import os
import shutil
import re

from .AptConfGenerator import AptConfGenerator
from .AptSourcesListsGenerator import AptSourcesListsGenerator
from .SCmd import SCmd

class AptRepoGenerator:
    """
    This class is main entrance point for Apt repository generation actions. 
    """
    def __init__(self, aptRepo):
        if str(aptRepo.__class__.__name__) != 'AptRepo':
            raise Exception("Unexpected argument class '%s' among constructor arguments in file '%s'." % (str(aptRepo.__class__.__name__), __file__))
        self.repo = aptRepo

    def generateRepo(self):
      
        for suite in self.repo.repoSuitePool:
            prefix = 'INFO:%s:%s:' % (__file__, SCmd().lineno())
            sys.stderr.write("\n\n" + prefix + "For repository '%s' processing suite '%s'.\n" % (self.repo.repoId, suite.name))
            confFileNames = AptConfGenerator(suite, self.repo.dir).createFiles()
        
            self._organiseDirs(self.repo.dir, suite)
            os.chdir(self.repo.dir)
        
            for fileName in confFileNames['indexesConf']:
                self._generateAptContentsAndPackages(confFileNames['aptConf'], fileName)
            self._generateAptRelease(confFileNames['aptConf'], suite)
    
        self._signReleaseFile(suite)
        
        
        self.exportPublicKey()
        self.removeTemporaryFiles()
        
        sourcesGen = AptSourcesListsGenerator(self.repo)
        sourcesListFileName = '%s/%s.sources.list' % (self.repo.dir, self.repo.repoId)
        sourcesGen.dumpToFile(sourcesListFileName)


    def exportPublicKey(self):
        filePublicKey = '%s/%s.key.pub' % (self.repo.dir, self.repo.repoId)
        shellCmd = ['gpg', '--homedir', self.repo.dirGpgHome,
                                        '--armor',
                                        '--export', self.repo.gpgKeyId,
                                    ]
        SCmd().callShellCmd(__file__, SCmd().lineno(), shellCmd, filePublicKey)

    
    
    def removeTemporaryFiles(self):
        dirTop = self.repo.dir
        for parentDir, subDirs, files in os.walk(dirTop):  # @UnusedVariable
            for fileName in files:
                if re.match('^apt-.*\.conf$', fileName):
                    os.remove(fileName)
                if re.match('^packages-.*\.db$', fileName):
                    os.remove(fileName)
            break


#
# # 
# # # 
# # # #
  
        
    def _organiseDirs(self, dirRepo, suite):
        os.chdir(dirRepo)
        dirSuiteMetaData = dirRepo + '/dists' + '/' + suite.name
    
        if os.path.exists(dirSuiteMetaData):
            shutil.rmtree(dirSuiteMetaData)
    
        if not os.path.exists(dirSuiteMetaData):
            os.makedirs(dirSuiteMetaData)
        for component in suite.componentsPool.values():
            for arch in component.architecturesPool:
                if arch == 'source':
                    dirName = dirSuiteMetaData + '/' + component.name + '/' + arch
                else:
                    dirName = dirSuiteMetaData + '/' + component.name + '/' + 'binary-' + arch
                if not os.path.exists(dirName):
                    os.makedirs(dirName)

    def _generateAptContentsAndPackages(self, contentsConfName, indexesConfName):
        shellCmd = ['apt-ftparchive',
                        'generate',
                        '-c=%s' % contentsConfName,
                        indexesConfName
                        ]
        SCmd().callShellCmd(__file__, SCmd().lineno(), shellCmd)

    def _generateAptRelease(self, contentsConfName, suite):
        release = self._getAprReleaseFDirAndFileForSuite(suite)
        shellCmd = ['apt-ftparchive',
                        '-c=%s' % contentsConfName,
                        'release',
                        release['dir']
                        ]
        SCmd().callShellCmd(__file__, SCmd().lineno(), shellCmd, release['fileFull'])

    
    def _signReleaseFile(self, suite):
        release = self._getAprReleaseFDirAndFileForSuite(suite)
        releaseSignFile = '%s/%s.gpg' % (release['dir'], release['fileShort'])

        if os.path.isfile(releaseSignFile):
            os.remove(releaseSignFile)
    
        shellCmd = ['gpg', '--homedir', self.repo.dirGpgHome,
                                        '--output', releaseSignFile,
                                        '-ba', release['fileFull']
                    ]
        SCmd().callShellCmd(__file__, SCmd().lineno(), shellCmd)

    def _getAprReleaseFDirAndFileForSuite(self, suite):
        dirForReleaseFile = '%s/dists/%s' % (self.repo.dir, suite.name)
        fileReleaseShortName = 'Release'
        fileReleaseFullName = '%s/Release' % dirForReleaseFile
        return {'dir': dirForReleaseFile,
                    'fileShort': fileReleaseShortName,
                    'fileFull': fileReleaseFullName}
    