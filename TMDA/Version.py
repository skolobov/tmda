# -*- python -*-
#
# Copyright (C) 2001,2002,2003 Jason R. Mastaler <jason@mastaler.com>
#
# This file is part of TMDA.
#
# TMDA is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.  A copy of this license should
# be included in the file COPYING.
#
# TMDA is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with TMDA; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Various versioning information."""


import sys


# TMDA version
TMDA = "0.89+"

# TMDA version codename
CODENAME = "Northern Dancer"

# Python version
PYTHON = sys.version.split()[0]

# Platform identifier
try:
    from platform import platform
    PLATFORM = platform()
except ImportError:
    try:
        from distutils.util import get_platform
        PLATFORM = get_platform()
    except ImportError:
        PLATFORM = sys.platform

# Summary of all the version identifiers
# e.g, TMDA/0.86+ "Carry Back" (Python/2.3.2 on Darwin-6.8-Power_Macintosh-powerpc-32bit)
ALL = 'TMDA/%s "%s" (Python/%s on %s)' % (TMDA, CODENAME, PYTHON, PLATFORM)
