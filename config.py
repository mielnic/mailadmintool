###########################
# CONFIGS                 #
###########################

services = [
        'postfix',
        'dovecot',
        'spamassassin',
        'spamass-milter',
        'fail2ban',
        'opendmarc',
        'apache2',
        'mysql']

config_files ={
    'helo' : '/etc/postfix/helo_access',
    'rbl' : '/etc/postfix/rbl_override',
    'header_checks' : '/etc/postfix/header_checks',
    'body_checks' : '/etc/postfix/body_checks',
    'spamassassin' : '/etc/spamassassin/local.cf'
}

log_files = {
    'mail' : '/var/log/mail.log',
    'f2b' : '/var/log/fail2ban.log',
}

depth = '1000'