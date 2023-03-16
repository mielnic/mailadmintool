## MailAdminTool

MailAdminTool is a python script that I use to help me manage mailservers based on Postfix/Dovecot. It is not intended for complete mailserver administration, but rather as a simple and quick helper to perform common tasks.

__It works for:__

* Postfix
* Dovecot
* Postfixadmin
* Spamassassin
* OpenDMARC
* Fail2Ban
* Ubuntu/Debian

Although it can be easily adapted to other "suite" combinations.

## Functions

* __Status:__ Check relevant services status & TCP open ports, view and flush mail queue.
* __Users:__ Add and delete users, and reset passwords.
* __Filters:__ Manages filtering rules: Postfix __HELO & RBL__ whitelisting, Postfix __Header & Body Checks__ rules and Spamassassin __custom rules__. It will automatically run postmap and reload the service if required. Header & Body Checks rules are set to __DISCARD__, not REJECT.  Files are edited in a line editor, so multiline rules (Spamassassin) must be added one line at a time. Comments (__#__) and empty lines in config files are __not shown__, but not modified nor deleted.
* __logs:__ They are just filters of relevant information from mail.log 'n' last lines (configurable in config file), except Fali2Ban (parses it's own log) and Postfix, where performs a __pflogsumm (required)__ report.

## Usage

Edit config.py and setup your file locations, adjust "depth" variable to the desired number of lines for log analysys, and un with admin privileges.
