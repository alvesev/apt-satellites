#!/bin/bash

#
#  Copyright 2013 Alex Vesev
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


PS4="CMD:${0}:pid=\${$}: "
#set -x

../src/apt-compare-versions --quiet -l "9.0.7-1~bpo70" -r "9.0.7-1~bpo70+1"
echo "    Have exit value from quiet command: ${?}"

../src/apt-compare-versions --quiet -l "9.0.7-1" -r "9.0.7-1"
echo "    Have exit value from quiet command: ${?}"

../src/apt-compare-versions --quiet -l "9.0.7-1~bpo70+1" -r "9.0.7-1~bpo70"
echo "    Have exit value from quiet command: ${?}"
