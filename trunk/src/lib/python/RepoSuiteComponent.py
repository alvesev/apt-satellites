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


class RepoSuiteComponent:
    name = 'default'
    architecturesPool = ['i386', 'amd64', 'all', 'source']

    def __init__(self, newName = '', newArchPool = []):
        if newName:     self.name = newName
        if newArchPool: self.architecturesPool = newArchPool

        if not type(newName) == type(''):
            raise Exception("New name must be a string but it is not.")
        if not type(newArchPool) == type([]):
            raise Exception("New architectures pool must be a list but it is not.")
