# -*- python -*-
#
# Copyright (C) 2001,2002 Jason R. Mastaler <jason@mastaler.com>
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

"""Shared TMDA errors and messages."""


# exception classes
class TMDAError(Exception):
    """Base class for all TMDA exceptions."""
    pass

class ConfigError(TMDAError):
    """tmdarc errors."""
    pass

class DeliveryError(TMDAError):
    """Delivery module errors."""
    pass

class MissingEnvironmentVariable(TMDAError):
    """An essential environment variable is not defined."""
    def __init__(self, varname):
        TMDAError.__init__(self)
        self.varname = varname
        print 'Missing environment variable:', self.varname
