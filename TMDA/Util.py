# -*- python -*-

"""General purpose functions."""


import cPickle
import fileinput
import fnmatch
import os
import random
import re
import string
import time


EMPTYSTRING = ''
NL = '\n'
DOT = '.'
from string import whitespace as WHITESPACE


def gethostname():
    hostname = os.environ.get('QMAILHOST') or \
               os.environ.get('MAILHOST')
    if not hostname:
        import socket
        hostname = socket.getfqdn()
    return hostname


def getfullname():
    fullname = os.environ.get('QMAILNAME') or \
               os.environ.get('NAME') or \
               os.environ.get('MAILNAME')
    if not fullname:
        import pwd
        fullname = pwd.getpwuid(os.getuid())[4]
    if not fullname:
        fullname = ''
    return fullname


def getusername():
    username = os.environ.get('QMAILUSER') or \
               os.environ.get('USER') or \
               os.environ.get('LOGNAME')
    if not username:
        import pwd
        username = pwd.getpwuid(os.getuid())[0]
    if not username:
        username = '<unknown>'
    return username


def seconds(timeout):
    """Translate the defined timeout interval into seconds."""
    match = re.match("^([0-9]+)([YMwdhms])$", timeout)
    if not match:
        raise ValueError, 'Invalid timeout value: ' + timeout
    (num, unit) = match.groups()
    if unit == 'Y':                     # years --> seconds
        seconds = int(num) * 60 * 60 * 24 * 365
    elif unit == 'M':                   # months --> seconds
        seconds = int(num) * 60 * 60 * 24 * 30
    elif unit == 'w':                   # weeks --> seconds
        seconds = int(num) * 60 * 60 * 24 * 7
    elif unit == 'd':                   # days --> seconds
        seconds = int(num) * 60 * 60 * 24
    elif unit == 'h':                   # hours --> seconds
        seconds = int(num) * 60 * 60
    elif unit == 'm':                   # minutes --> seconds
        seconds = int(num) * 60
    else:                               # just seconds
        seconds = int(num)
    return seconds


def format_timeout(timeout):
    """Return a human readable translation of the timeout interval."""
    match = re.match("^([0-9]+)([YMwdhms])$", timeout)
    if not match:
        return timeout
    (num, unit) = match.groups()
    if unit == 'Y':
        timeout = num + " years"
    elif unit == 'M':
        timeout = num + " months"
    elif unit == 'w':
        timeout = num + " weeks"
    elif unit == 'd':
        timeout = num + " days"
    elif unit == 'h':
        timeout = num + " hours"
    elif unit == 'm':
        timeout = num + " minutes"
    else:
        timeout = num + " seconds"
    if int(num) == 1:
        timeout = timeout[:-1]
    return timeout


def unixdate(timesecs=None):
    """Return a date string in the format of the UNIX `date' command.  e.g,

    Thu Dec 27 17:54:04 MST 2001

    timesecs is optional, and if not given, the current time is used.
    """
    if not timesecs:
        timesecs = time.time()
    timetuple = time.localtime(timesecs)
    tzname = time.tzname[timetuple[-1]]
    asctime_list = string.split(time.asctime(timetuple))
    asctime_list.insert(len(asctime_list)-1, tzname)
    return string.join(asctime_list)


def make_msgid(timesecs=None, pid=None):
    """Return an rfc2822 compliant Message-ID string, composed of
    date + process id + random integer + 'TMDA' + FQDN  e.g:
    
    <20020204183548.40803.32317.TMDA@nightshade.la.mastaler.com>

    timesecs is optional, and if not given, the current time is used.

    pid is optional, and if not given, the current process id is used.
    """
    if not timesecs:
        timesecs = time.time()
    if not pid:
        import Defaults
        pid = Defaults.PID
    idhost = os.environ.get('QMAILIDHOST')
    if not idhost:
        idhost = gethostname()
    utcdate = time.strftime('%Y%m%d%H%M%S', time.gmtime(timesecs))
    randint = random.randrange(100000)
    message_id = '<%s.%s.%s.TMDA@%s>' % (utcdate, pid, randint, idhost)
    return message_id


def make_date(timesecs=None, localtime=1):
    """Return an rfc2822 compliant Date string.  e.g,

    Fri, 30 Nov 2001 04:06:11 -0700 (MST)
    
    timesecs is optional, and if not given, the current time is used.

    Optional localtime is a flag that when true, returns a date
    relative to the local timezone instead of UTC.  This is the
    default.
    """
    if not timesecs:
        timesecs = time.time()
    if localtime:
        timetuple = time.localtime(timesecs)
        tzname = time.tzname[timetuple[-1]]
    else:
        timetuple = time.gmtime(timesecs)
        tzname = 'UTC'
    try:
        import email.Utils
        rfc2822date = email.Utils.formatdate(timesecs,localtime)
        rfc2822date_tzname = '%s (%s)' % (rfc2822date, tzname)
    except ImportError:
        # This except block can be removed once Python >= 2.2 is required.
        if localtime:
            # Calculate timezone offset, based on whether the local zone has
            # daylight savings time, and whether DST is in effect.
            if time.daylight and timetuple[-1]:
                offset = time.altzone
            else:
                offset = time.timezone
            hours, minutes = divmod(abs(offset), 3600)
            # Remember offset is in seconds west of UTC, but the timezone is in
            # minutes east of UTC, so the signs differ.
            if offset > 0:
                sign = '-'
            else:
                sign = '+'
            zone = '%s%02d%02d (%s)' % (sign, hours, minutes / 60, tzname)
        else:
            # Timezone offset is always -0000
            zone = '%s (%s)' % ('-0000', tzname)
        rfc2822date_tzname = '%s, %02d %s %04d %02d:%02d:%02d %s' % (
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][timetuple[6]],
            timetuple[2],
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][timetuple[1] - 1],
            timetuple[0], timetuple[3], timetuple[4], timetuple[5],
        zone)
    return rfc2822date_tzname


def file_to_dict(file, dict):
    """Process and add then each line of a textfile to a dictionary."""
    for line in fileinput.input(file):
        line = string.strip(line)
        # Comment or blank line?
        if line == '' or line[0] in '#':
            continue
        else:
            fields = string.split(line)
            key = fields[0]
            key = string.lower(key)
            value = fields[1]
            dict[key] = value
    return dict


def file_to_list(file, list):
    """Process and then append each line of file to list."""
    for line in fileinput.input(file):
        line = string.strip(line)
        # Comment or blank line?
        if line == '' or line[0] in '#':
            continue
        else:
            line = string.expandtabs(line)
            line = string.split(line, ' #')[0]
            line = string.strip(line)
            fields = string.split(line, None, 1)
            # preserve the case of second field
            f1 = string.lower(fields[0])
            try:
                f1 = string.join([f1] + [fields[1]])
            except IndexError:
                pass
            list.append(f1)
    return list


def writefile(contents, fullpathname):
    """Simple function to write contents to a file."""
    if os.path.exists(fullpathname):
        raise IOError, fullpathname + ' already exists'
    else:
        file = open(fullpathname, 'w')
        file.write(contents)
        file.close()
        

def append_to_file(str, fullpathname):
    """Append a string to a text file if it isn't already in there."""
    if os.path.exists(fullpathname):
        for line in fileinput.input(fullpathname):
            line = string.lower(string.strip(line))
            # Comment or blank line?
            if line == '' or line[0] in '#':
                continue
            else:
                if string.lower(string.strip(str)) == line:
                    fileinput.close()
                    return 0
    file = open(fullpathname, 'a+')
    file.write(string.strip(str) + '\n')
    file.close()


def pager(file):
    """Display file using a UNIX text pager such as less or more."""
    pager_list = []
    pager = os.environ.get('PAGER')
    if pager is None:
        # try to locate less or more if $PAGER is not set
        for prog in ('less', 'more'):
            path = os.popen('which ' + prog).read()
            if path != '':
                pager = path
                break
    for arg in pager.split():
        pager_list.append(arg)
    pager_list.append(file)
    os.spawnvp(os.P_WAIT, pager_list[0], pager_list)


def build_cdb(filename):
    """Build a cdb file from a text file."""
    import cdb
    try:
        cdbname = filename + '.cdb'
        cdb = cdb.cdbmake(cdbname, cdbname + '.tmp')
        match_list = []
        for line in file_to_list(filename, match_list):
            linef = line.split()
            key = linef[0]
            try:
                value = linef[1]
            except IndexError:
                value = ''
            cdb.add(key, value)
        cdb.finish()
    except:
        return 0
    else:
        return 1


def pickleit(object, file, bin=0):
    """Store object in a pickle file.
    Optional bin specifies whether to use binary or text pickle format."""
    fp = open(file, 'w')
    cPickle.dump(object, fp, bin)
    fp.close()
    return


def unpickle(file):
    """Retrieve and return object from the file file."""
    fp = open(file, 'r')
    object = cPickle.load(fp)
    fp.close()
    return object


def findmatch(list, addrs):
    """Determine whether any of the passed e-mail addresses match a
    Unix shell-style wildcard pattern contained in list.  The
    comparison is case-insensitive.  Also, return the second half of
    the string if it exists (for exp and ext addresses only)."""
    for address in addrs:
        if address:
            address = string.lower(address)
            for p in list:
                stringparts = string.split(p)
                p = stringparts[0]
                # Handle special @=domain.dom syntax.
                try:
                    at = string.rindex(p, '@')
                    atequals = p[at+1] == '='
                except (ValueError, IndexError):
                    atequals = None
                if atequals:
                    p1 = p[:at+1] + p[at+2:]
                    p2 = p[:at+1] + '*.' + p[at+2:]
                    match = (fnmatch.fnmatch(address,p1)
                             or fnmatch.fnmatch(address,p2))
                else:
                    match = fnmatch.fnmatch(address,p)
                if match:
                    try:
                        return stringparts[1]
                    except IndexError:
                        return 1


def wraptext(text, column=70, honor_leading_ws=1):
    """Wrap and fill the text to the specified column.
    Adapted from Mailman's Utils.wrap().

    Wrapping is always in effect, although if it is not possible to
    wrap a line (because some word is longer than `column' characters)
    the line is broken at the next available whitespace boundary.
    Paragraphs are also always filled, unless honor_leading_ws is true
    and the line begins with whitespace.
    """
    wrapped = ''
    # first split the text into paragraphs, defined as a blank line
    paras = re.split('\n\n', text)
    for para in paras:
        # fill
        lines = []
        fillprev = 0
        for line in para.split(NL):
            if not line:
                lines.append(line)
                continue
            if honor_leading_ws and line[0] in WHITESPACE:
                fillthis = 0
            else:
                fillthis = 1
            if fillprev and fillthis:
                # if the previous line should be filled, then just append a
                # single space, and the rest of the current line
                lines[-1] = lines[-1].rstrip() + ' ' + line
            else:
                # no fill, i.e. retain newline
                lines.append(line)
            fillprev = fillthis
        # wrap each line
        for text in lines:
            while text:
                if len(text) <= column:
                    line = text
                    text = ''
                else:
                    bol = column
                    # find the last whitespace character
                    while bol > 0 and text[bol] not in WHITESPACE:
                        bol = bol - 1
                    # now find the last non-whitespace character
                    eol = bol
                    while eol > 0 and text[eol] in WHITESPACE:
                        eol = eol - 1
                    # watch out for text that's longer than the column width
                    if eol == 0:
                        # break on whitespace after column
                        eol = column
                        while eol < len(text) and \
                              text[eol] not in WHITESPACE:
                            eol = eol + 1
                        bol = eol
                        while bol < len(text) and \
                              text[bol] in WHITESPACE:
                            bol = bol + 1
                        bol = bol - 1
                    line = text[:eol+1] + '\n'
                    # find the next non-whitespace character
                    bol = bol + 1
                    while bol < len(text) and text[bol] in WHITESPACE:
                        bol = bol + 1
                    text = text[bol:]
                wrapped = wrapped + line
            wrapped = wrapped + '\n'
            # end while text
        wrapped = wrapped + '\n'
        # end for text in lines
    # the last two newlines are bogus
    return wrapped[:-2]


def maketext(templatefile, vardict):
    """Make some text from a template file.
    Adapted from Mailman's Utils.maketext().

    Reads the `templatefile' which should be a full pathname, and does
    string substitution by interpolating in the `localdict'.
    """
    fp = open(templatefile)
    template = fp.read()
    fp.close()
    import Defaults
    localdict = Defaults.__dict__.copy()
    localdict.update(vardict)
    text = template % localdict
    return text


def filter_match(filename, recip, sender=None):
    """Check if the give e-mail addresses match lines in filename."""
    import FilterParser 
    filter = FilterParser.FilterParser(checking=1)
    filter.read(filename)
    (actions, matchline) = filter.firstmatch(recip, [sender])
    # print the results
    checking_msg = 'Checking ' + filename
    print checking_msg
    print '-' * len(checking_msg)
    if recip:
        print 'To:',recip
    if sender:
        print 'From:',sender
    print '-' * len(checking_msg)
    if actions:
        print 'MATCH:', matchline
    else:
        print 'Sorry, no matching lines.'
