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

class ConfAptIndexes:

    fileName = None
    suite = None
    component = None

    _miscParts = """
Dir {
  ArchiveDir ".";
  CacheDir ".";
};

Default {
  Packages::Compress ". gzip bzip2";
  Sources::Compress "gzip bzip2";
  Contents::Compress "gzip bzip2";
};

Default {
  Packages {
    Extensions ".deb";
  };
};
"""

    _binDirPartTemplate = """
BinDirectory "dists/__SUITE__/__COMPONENT__/binary-__ARCH__" {
  Packages "dists/__SUITE__/__COMPONENT__/binary-__ARCH__/Packages";
  Contents "dists/__SUITE__/Contents-__ARCH__";
  SrcPackages "dists/__SUITE__/__COMPONENT__/source/Sources";
};
"""

    _treePartTemplate = """
TreeDefault {
    Directory "pool/__SUITE__/__COMPONENT__/bin";
    SrcDirectory "pool/__SUITE__/__COMPONENT__/src";
}
Tree "dists/__SUITE__" {
  Sections "__COMPONENT__";
  Architectures "__ARCH_ALL__";
};
"""
    def __init__(self, fileName, suite, component):
        self.fileName = fileName
        self.suite = suite
        self.component = component

    def dumpContentToFile(self):
        try:
            fileHandle = open(self.fileName, 'w')
            fileHandle.write(self.generateContent())
            fileHandle.close()
        except:
            sys.stderr.write("Failed to write a content into the fileHandle '%s'.\n" % self.fileName)
            raise

    def generateContent(self):
        content = ''
        content +=  self._miscParts
        content += self._generatePartsFromTemplates()
        return content

    def _generatePartsFromTemplates(self):
        text = ''
        archPool = {}
        for arch in self.component.architecturesPool:
            archPool[arch] = arch
            text += self._generateSingleBinPartText(self.suite.name, self.component.name, arch)
        text += self._generateTreePartText(self.component, archPool)
        return text

    def _generateSingleBinPartText(self, suiteName, componentName, arch):
        if arch == 'source': return ''

        text = self._binDirPartTemplate
        text = text.replace('__SUITE__', suiteName)
        text = text.replace('__COMPONENT__', componentName)
        text = text.replace('__ARCH__', arch)
        return text

    def _generateTreePartText(self, component, archPool):

        text = self._treePartTemplate
        text = text.replace('__COMPONENT__', self.component.name)
        text = text.replace('__SUITE__', self.suite.name)
        text = text.replace('__ARCH_ALL__', ' '.join(archPool))
        return text
