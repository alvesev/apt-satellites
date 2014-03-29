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
import inspect
from subprocess import call

class SCmd:

    def callShellCmd(self, callOriginFile, callOriginLineno, shellCmd,
                        fileLog = None, verbose = True):
        """
        'fileLog' is used as 'stdout' collector, if the name is specified.
        """

        messagePrefix = 'INFO:%s:%s: ' % (callOriginFile, callOriginLineno)
        sys.stderr.write("\n" + messagePrefix + "Is going to execute '%s'.\n" % ' '.join(shellCmd) )
        shellExitCode = 0 # Shell's commands success exit code.
        if fileLog:
            fileHandle = open(fileLog, 'w')
            shellExitCode = call(shellCmd, stdout = fileHandle)
            fileHandle.flush()
            fileHandle.close()
            if verbose: sys.stderr.write(messagePrefix + "See job's output in '%s'\n" % fileLog)
        else:
            shellExitCode = call(shellCmd)

        if shellExitCode != 0: raise Exception("\n" + messagePrefix + "Shell command '%s' failed." % ' '.join(shellCmd))
        sys.stderr.write(messagePrefix + "Job done.\n")

    def lineno(self):
        """
        Example (Python 2): SCmd().callShellCmd(__file__, SCmd.lineno(), ..., ...)
        Example (Python 3): SCmd.callShellCmd(__file__, SCmd.lineno(), ..., ...)
        """
        return str(inspect.currentframe().f_back.f_lineno)
