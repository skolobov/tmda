# -*- python -*-

"""TMDA configuration variable defaults."""


import os
import stat
import string
import sys

import Util


##############################
# General system-wide defaults
##############################

TMDA_VERSION = "0.40"
TMDA_HOMEPAGE = "<http://tmda.sf.net/>"

PYTHON_VERSION = string.split(sys.version)[0]
# e.g, "TMDA v0.35/Python 2.1.1 (irix646)"
DELIVERY_AGENT = 'TMDA ' + 'v' + TMDA_VERSION + '/Python ' + PYTHON_VERSION \
                 + ' (' + sys.platform + ')'

# General exit status codes which should be understood by all MTAs.
# Defined so we can raise exit codes within TMDA modules without
# having to create an MTA instance.
EX_OK = 0                               
EX_TEMPFAIL = 75

# If the file /etc/tmdarc exists, read it before ~/.tmdarc.
# Make site-wide configuration changes to this file.
GLOBAL_TMDARC = '/etc/tmdarc'
if os.path.exists(GLOBAL_TMDARC):
    try:
        execfile(GLOBAL_TMDARC)
    except IOError:
        pass                            # just skip it if we can't open it
    
# Look for the user-config-file in the environment first then default
# to ~/.tmdarc.
TMDARC = os.environ.get('TMDARC')
if not TMDARC:TMDARC = os.path.expanduser("~/.tmdarc")

# Read-in the user's configuration file.
if not os.path.exists(TMDARC):
    print "Can't open configuration file:",TMDARC
    sys.exit(EX_TEMPFAIL)
execfile(TMDARC)

# Check for proper file permissions before proceeding.
statinfo = os.stat(TMDARC)
permbits = stat.S_IMODE(statinfo[stat.ST_MODE])
mode = int(oct(permbits))

# ALLOW_MODE_640
# Set this variable to 1 if you want to allow mode 640 .tmdarc files.
# Default is 0 (turned off)
if not vars().has_key('ALLOW_MODE_640'):
    ALLOW_MODE_640 = 0

if ALLOW_MODE_640 and mode in (400, 600, 640):
    pass
elif mode not in (400, 600):
    print TMDARC,"must be permission mode 400 or 600!"
    sys.exit(EX_TEMPFAIL)
else:
    pass

############################
# User configurable settings
############################

# Only compute defaults for unset variables to speed startup.

# DATADIR
# Top-level directory which TMDA uses to store its files and
# directories.  TMDA should be free to create files and directories
# under DATADIR if need be.  Make sure to include a trailing "/".
# Default is ~/.tmda/
if not vars().has_key('DATADIR'):
    DATADIR = os.path.expanduser("~/.tmda/")

# MAIL_TRANSFER_AGENT
# Defines which mail transfer agent (MTA) software you are running.
# Possible choices are "exim", "postfix" or "qmail"
# Default is qmail
if not vars().has_key('MAIL_TRANSFER_AGENT'):
    MAIL_TRANSFER_AGENT = "qmail"

# LOCAL_DELIVERY_AGENT
# The full path to the program used to deliver a sucessful message to
# your mailbox.  Only necessary if you are NOT running qmail!
# Tested LDAs include maildrop and procmail.
# This variable may also contain arguments which will be passed to the command.
# e.g, LOCAL_DELIVERY_AGENT = "/usr/bin/procmail -p ~/.procmailrc"
# No default
if not vars().has_key('LOCAL_DELIVERY_AGENT'):
    LOCAL_DELIVERY_AGENT = None
if MAIL_TRANSFER_AGENT != 'qmail' and not LOCAL_DELIVERY_AGENT:
    print "Not running qmail: you must define LOCAL_DELIVERY_AGENT in",TMDARC
    sys.exit(EX_TEMPFAIL)

# RECIPIENT_DELIMITER
# A single character which specifies the separator between user names
# and address extensions (e.g, user-ext).
# The default under qmail is `-', while the default for Sendmail and
# friends is likely `+'.
# Default is "-"
if not vars().has_key('RECIPIENT_DELIMITER'):
    RECIPIENT_DELIMITER = "-"

# SENDMAIL
# The path to the sendmail program, or sendmail compatibility
# interface.  Defaults to one of the two standard locations, but you
# can override it in case it is installed elsewhere.
if not vars().has_key('SENDMAIL'):
    if os.path.exists("/usr/sbin/sendmail"):
        SENDMAIL = "/usr/sbin/sendmail"
    elif os.path.exists("/usr/lib/sendmail"):
        SENDMAIL = "/usr/lib/sendmail"
    else:
        print "Can't find your sendmail program!"
        sys.exit(EX_TEMPFAIL)
elif not os.path.exists(SENDMAIL):
    print "Invalid SENDMAIL path:",SENDMAIL
    sys.exit(EX_TEMPFAIL)

# USEVIRTUALDOMAINS
# Set this variable to 0 if want to turn off TMDA's qmail virtualdomains
# support.  This should obviously only be done if you are not running
# any qmail virtualdomains, but it will improve performance.
# Default is 1 (turned on)
if not vars().has_key('USEVIRTUALDOMAINS'):
    USEVIRTUALDOMAINS = 1

# VIRTUALDOMAINS
# virtualdomains defaults to /var/qmail/control/virtualdomains, but
# this lets you override it in case it is installed elsewhere.  Used
# for virtualdomain processing in tmda-filter.
if not vars().has_key('VIRTUALDOMAINS'):
    VIRTUALDOMAINS = "/var/qmail/control/virtualdomains"

# BLACKLIST
# Filename which contains a list of e-mail addresses and/or
# substrings, one per line, which are considered unacceptable and
# therefore bounced if there is a match.
# Default is ~/.tmda/lists/blacklist
if not vars().has_key('BLACKLIST'):
    BLACKLIST = DATADIR + "lists/" + "blacklist"

# BOUNCE_BLACKLIST_CC
# An optional e-mail address which will be sent a copy of any message
# that bounces because of a BLACKLIST match.
# No default.
if not vars().has_key('BOUNCE_BLACKLIST_CC'):
    BOUNCE_BLACKLIST_CC = None

# BOUNCE_CONFIRM_CC
# An optional e-mail address which will be sent a copy of any message
# that triggers a confirmation request.
# No default.
if not vars().has_key('BOUNCE_CONFIRM_CC'):
    BOUNCE_CONFIRM_CC = None

# BOUNCE_REVOKED_CC
# An optional e-mail address which will be sent a copy of any message
# that bounces because of a REVOKED match.
# No default.
if not vars().has_key('BOUNCE_REVOKED_CC'):
    BOUNCE_REVOKED_CC = None

# BOUNCE_ENV_SENDER
# The envelope sender of the bounce message.
# Default is an empty envelope sender <>.
if not vars().has_key('BOUNCE_ENV_SENDER'):
    # Exim doesn't like -f ''
    if MAIL_TRANSFER_AGENT == 'exim':
        BOUNCE_ENV_SENDER = '<>'
    else:
        BOUNCE_ENV_SENDER = ''

# CONFIRM_ACCEPT_NOTIFY
# Set this variable to 0 if you do not want to generate confirmation
# acceptance notices.
# Default is 1 (turned on)
if not vars().has_key('CONFIRM_ACCEPT_NOTIFY'):
    CONFIRM_ACCEPT_NOTIFY = 1

# CONFIRM_MAX_MESSAGE_SIZE
# This is the largest size (in bytes) that a message can be before the
# its body is excluded from the confirmation request/acceptance
# notice.  Set this to None to allow any size message.
# Default is 50000
if not vars().has_key('CONFIRM_MAX_MESSAGE_SIZE'):
    CONFIRM_MAX_MESSAGE_SIZE = 50000

# CONFIRM_ACCEPT_TEMPLATE
# Full path to a custom template for confirmation acceptance notices.
# Default is confirm_accept.txt in ../templates/.
if not vars().has_key('CONFIRM_ACCEPT_TEMPLATE'):
    ca_template = '/templates/confirm_accept.txt'
    CONFIRM_ACCEPT_TEMPLATE = os.path.split(os.path.dirname
                                            (os.path.abspath
                                             (sys.argv[0])))[0] + ca_template 

# CONFIRM_REQUEST_TEMPLATE
# Full path to a custom template for confirmation requests.
# Default is confirm_request.txt in ../templates/.
if not vars().has_key('CONFIRM_REQUEST_TEMPLATE'):
    cr_template = '/templates/confirm_request.txt'
    CONFIRM_REQUEST_TEMPLATE = os.path.split(os.path.dirname
                                            (os.path.abspath
                                             (sys.argv[0])))[0] + cr_template 

# DATED_TEMPLATE_VARS
# Set this variable to 1 if you want to use 'dated' address variables
# in your templates.
# Default is 0 (turned off)
if not vars().has_key('DATED_TEMPLATE_VARS'):
    DATED_TEMPLATE_VARS = 0

# SENDER_TEMPLATE_VARS
# Set this variable to 1 if you want to use 'sender' address variables
# in your templates.
# Default is 0 (turned off)
if not vars().has_key('SENDER_TEMPLATE_VARS'):
    SENDER_TEMPLATE_VARS = 0

# COOKIE_TYPE
# The default cookie type is dated.  Possible values are:
#       dated   (can only be replied to for TIMEOUT)
#       sender  (can only be replied to by address)
#       bare    (untagged)
if not vars().has_key('COOKIE_TYPE'):
    COOKIE_TYPE = "dated"

# CRYPT_KEY
# Your encryption key should be unique and kept secret.
# Use the included "tmda-keygen" program to generate your key.
# No default.
if not vars().has_key('CRYPT_KEY'):
    print "Encryption key not found!"
    sys.exit(EX_TEMPFAIL)
else:
    # Convert key from hex back into raw binary.
    # Hex has only 4 bits of entropy per byte as opposed to 8.
    CRYPT_KEY = Util.unhexlify(CRYPT_KEY)

# FULLNAME
# Your full name.
# Default comes from your environment or the password file.
if not vars().has_key('FULLNAME'):
    FULLNAME = Util.getfullname()

# HMAC_BYTES
# An integer which determines the length of the HMACs used in TMDA's
# "cookies".  Read the `CRYPTO' file for more information.  Changing
# this value will will invalidate all previously generated HMACs.
# Default is 3 (24-bit HMACs)
if not vars().has_key('HMAC_BYTES'):
    HMAC_BYTES = 3

# HOSTNAME
# The right-hand side of your email address (after `@').
# Defaults to the fully qualified domain name of the localhost.
if not vars().has_key('HOSTNAME'):
    HOSTNAME = Util.gethostname()

# LOGFILE
# Filename which delivery statistics should be written to.
# Default is 0 (no logging)
if not vars().has_key('LOGFILE'):
    LOGFILE = 0

# MESSAGE_FROM_STYLE
# Specifies how `From' headers should look on when tagging outgoing
# messages with tmda-inject.  There are three valid values:
#
#     "address"
#           Just the address - king@grassland.com
#
#     "parens"
#           king@grassland.com (Elvis Parsley)
#
#     "angles"
#           "Elvis Parsley" <king@grassland.com>
#
# Default is "angles".
if not vars().has_key('MESSAGE_FROM_STYLE'):
    MESSAGE_FROM_STYLE = "angles"

# TIMEOUT
# The timeout interval for 'dated' addresses.  The available units are
# (Y=years, M=months, w=weeks, d=days, h=hours, m=minutes, s=seconds).
# Default is 5d (5 days).
if not vars().has_key('TIMEOUT'):
    TIMEOUT = "5d"

# TIMEZONE
# A string representing a valid timezone on your system.  e.g,
#
# TIMEZONE = "MST7MDT"
# TIMEZONE = "Pacific/Auckland"
#
# This setting might be useful when you want dates represented (in
# logfiles, mail headers, etc.) in a timezone other than the default
# timezone of the machine running TMDA.
# Default is the timezone of the local host.
if not vars().has_key('TIMEZONE'):
    TIMEZONE = None
# The time module gets the timezone name when first imported, and it
# can't be changed by later setting TZ in the environment.  Thus, we
# must set TZ first, or else the time-zone as hour offset from UTC
# will be incorrect.
else:
    os.environ['TZ'] = TIMEZONE

# USERNAME
# The left-hand side of your e-mail address (before `@').
# Defaults to your UNIX username.
if not vars().has_key('USERNAME'):
    USERNAME = Util.getusername()

# BARE_FILE
# Filename which contains a list of e-mail addresses, one per line,
# which will receive untagged (no cookie added) messages.
# Default is ~/.tmda/lists/bare
if not vars().has_key('BARE_FILE'):
    BARE_FILE = DATADIR + "lists/" + "bare"

# DATED_FILE
# Filename which contains a list of e-mail addresses, one per line,
# which will receive messages with a dated cookie added to your
# address.
# Default is ~/.tmda/lists/dated
if not vars().has_key('DATED_FILE'):
    DATED_FILE = DATADIR + "lists/" + "dated"

# EXP_FILE
# Filename which contains a list of explicit to/from pairs, one per
# line.  If mail is destined for `to', your address will be changed
# to `from'.  For example,
#
#  xemacs-announce@xemacs.org jason@xemacs.org
#  domreg@internic.net        hostmaster@mastaler.com
#
# Default is ~/.tmda/lists/exp
if not vars().has_key('EXP_FILE'):
    EXP_FILE = DATADIR + "lists/" + "exp"

# EXT_FILE
# Filename which contains a list of e-mail address/extension pairs,
# one per line, which will receive messages with the extension added
# to the username of your address.  For example,
#
#  xemacs-beta@xemacs.org list-xemacs-beta
#  qmail@list.cr.yp.to    list-qmail
#
# Default is ~/.tmda/lists/ext
if not vars().has_key('EXT_FILE'):
    EXT_FILE = DATADIR + "lists/" + "ext"

# KEYWORD_FILE
# Filename which contains a list of e-mail address/keyword pairs, one
# per line, which will receive messages with a keyword cookie added to
# your address.  For example,
#
#  broker@schwab.com schwab
#  tmda-*@libertine.org lists-tmda
#
# Default is ~/.tmda/lists/keyword
if not vars().has_key('KEYWORD_FILE'):
    KEYWORD_FILE = DATADIR + "lists/" + "keyword"

# REVOKED_FILE
# Filename which contains a list of recipient e-mail addresses, one
# per line, which have been "revoked" and will therefore bounce.
# Default is ~/.tmda/lists/revoked
if not vars().has_key('REVOKED_FILE'):
    REVOKED_FILE = DATADIR + "lists/" + "revoked"
    
# SACRED_FILE
# Filename which contains a list of sacred keywords, the presence
# of which automatically zaps the mail into your mailbox.
# Default is ~/.tmda/lists/sacred
if not vars().has_key('SACRED_FILE'):
    SACRED_FILE = DATADIR + "lists/" + "sacred"

# SENDER_FILE
# Filename which contains a list of e-mail addresses, one per line,
# which will receive messages with a sender cookie added to your
# address.
# Default is ~/.tmda/lists/sender
if not vars().has_key('SENDER_FILE'):
    SENDER_FILE = DATADIR + "lists/" + "sender"

# WHITELIST
# Filename which contains a list of e-mail addresses and/or
# substrings, one per line, which are considered trusted contacts and
# therefore allowed directly into your mailbox if there is a match.
# Default is ~/.tmda/lists/whitelist
if not vars().has_key('WHITELIST'):
    WHITELIST = DATADIR + "lists/" + "whitelist"

# WHITELIST_AUTO_APPEND
# If you set this variable to 1, once a sender confirms a message their
# e-mail address will be automatically appended to WHITELIST.
# Default is 0 (turned off)
if not vars().has_key('WHITELIST_AUTO_APPEND'):
    WHITELIST_AUTO_APPEND = 0

# WHITELIST_TO_BARE
# Set this variable to 0 if you don't want addresses in your WHITELIST
# to automatically receive untagged (no cookie added) messages.
# Default is 1 (turned on)
if not vars().has_key('WHITELIST_TO_BARE'):
    WHITELIST_TO_BARE = 1

###################################
# END of user configurable settings
###################################
