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

class ConfApt:

    fileName = None
    suite = None

    _contentFieldValues = {
            'Origin': 'default',
            'Label': 'default',
            'Suite': 'default',
            'Codename': 'distro',
            'Architectures': ['i386', 'amd64', 'all', 'source'], # XXX - There is no setter with new value type checks.
            'Components': ['main'], # XXX - There is no setter with new value type checks.
            'Description': 'no description'
        }

    _contentFieldTemplates = {
            'Origin': 'APT::FTPArchive::Release::Origin "%s";',
            'Label': 'APT::FTPArchive::Release::Label "%s";',
            'Suite': 'APT::FTPArchive::Release::Suite "%s";',
            'Codename': 'APT::FTPArchive::Release::Codename "%s";',
            'Architectures': 'APT::FTPArchive::Release::Architectures "%s";',
            'Components': 'APT::FTPArchive::Release::Components "%s";',
            'Description': 'APT::FTPArchive::Release::Description "%s";'
        }

    def __init__(self, newFileName, suite):
        self.fileName = newFileName
        self._evaluateFieldsFromSuite(suite)

    def getField(self, fieldName):
        if fieldName not in self._contentFieldValues:
            raise Exception("A field with name '%s' is not implemented in class '%s'." % (fieldName, self.__class__.__name__))
        return self._contentFieldValues[fieldName]

    def setField(self, fieldName, fieldValue):
        if fieldName not in self._contentFieldValues:
            raise Exception("A field with name '%s' is not implemented in class '%s'." % (fieldName, self.__class__.__name__))
        self._contentFieldValues[fieldName] = fieldValue

    def dumpContentToFile(self):
        try:
            fileHandle = open(self.fileName, 'w')
            fileHandle.write(self.generateContent())
            fileHandle.close()
        except:
            sys.stderr.write("Failed to write a content into the fileHandle '%s'.\n" % self.fileName)
            raise

    def generateContent(self):
        content = []
        for key in self._contentFieldTemplates.keys():
            content.append(self._contentFieldTemplates[key] % self._stringify(self._contentFieldValues[key]))
        return '\n'.join(content) + '\n'


    def _evaluateFieldsFromSuite(self, suite):
        archList = []
        for component in suite.componentsPool.values():
            archList = list( set(archList) | set(component.architecturesPool))

        self._contentFieldValues = {
            'Origin': suite.name,
            'Label': suite.name,
            'Suite': suite.name,
            'Codename': suite.name,
            'Architectures': ' '.join(archList),
            'Components': ' '.join(suite.componentsPool),
            'Description': 'Apt-Satellites Arg generated repo'
        }

    def _stringify(self, incomingObject):
        if type(incomingObject) == type(''): #Py2: isinstance(incomingObject, basestring), Py3: isinstance(incomingObject, str)
            return incomingObject
        return ' '.join(incomingObject)
