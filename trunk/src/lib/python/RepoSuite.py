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
from .RepoSuiteComponent import RepoSuiteComponent

class RepoSuite:

    def __init__(self, name = 'default', codename = 'default',
            componentsPool = {},
            origin = 'default', label = 'default',
            description = 'default'):

        self.name = name
        self.codename = str(codename)
        if componentsPool: self.componentsPool = componentsPool
        else: self.componentsPool = {}
        self.origin = str(origin)
        self.label = str(label)
        self.description = str(description)

        if not type(componentsPool) == type({}):
            raise Exception("New components pool must be a dictionary but it is not.")

    def addComponentPool(self, newPool):
        try:
            for component in newPool:
                self.addComponent(component)
        except:
            sys.stderr.write("Failed to add component form pool: %s." % str(newPool))
            raise

    def addComponent(self, component):
        if not type(component) == type(RepoSuiteComponent()):
            raise Exception("New component type must be 'RepoSuiteComponent' but it is not.")
        self.componentsPool[component.name] = component

    def getComponentSingle(self, name):
        if type(name) == type(''):
            return self.componentsPool[name]
        else:
            raise Exception("Unexpected object's type.")

    def getComponentAll(self):
        return self.componentsPool

    def delComponent(self, someObject):
        if type(someObject) == type(''):
            del self.componentsPool[someObject]
        elif type(someObject) == type(RepoSuiteComponent()):
            del self.componentsPool[someObject.name]
        else:
            raise Exception("Unexpected object's type.")
