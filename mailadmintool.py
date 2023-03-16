import subprocess
from os import system
from config import services, config_files, log_files, depth

##########################
# FUNCTIONS              #
##########################
#
# Tools
#
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def input_yesno(message):
    """Forces Y or N input"""
    while True:
        yesno = input(message).lower()
        if yesno == 'y':
            yesno = True
            break
        elif yesno == 'n':
            yesno = False
            break
        else:
            print('Must enter Y or N.')
    return yesno

def return_to_menu():
    """Manages wrong menu inputs"""
    system('clear')
    print()
    input(f'Invalid option.\nPress any key to return to menu.')

def edit(filename, tag, setting):
    """System files edit"""
    f = open(filename)
    lines = f.readlines()
    if not lines[len(lines) - 1].endswith('\n'):
        lines[len(lines) - 1] = lines[len(lines) - 1] + '\n'
    f.close()
    while True:
        print(f'------------------------------------\nEditing {filename}:\n------------------------------------\n')
        for i in range(len(lines)):
            if not (lines[i].startswith('#') or lines[i].startswith('\n')):
                print(lines[i], end='')
        option = input(f'\n a - add a {tag}\n {bcolors.FAIL}d - delete a {tag}{bcolors.ENDC}\n w - Write\n q - Quit\n \n -> ').lower()
        if option == 'a':
            new_line = input(f'Enter the {tag} to be added: ').lower()
            lines.append(f'{new_line} {setting}\n')
        elif option == 'd':
            ok_lines = []
            ko_line = input(f'Enter the {tag} to be deleted: ').lower()
            for i in range(len(lines)):
                if not lines[i].startswith(ko_line):
                    ok_lines.append(lines[i])
            lines = ok_lines
        elif option == 'w':
            f = open(filename, 'w')
            f.writelines(lines)
            f.close()
            break
        elif option == 'q':
            break

def log_read(log):
    """Loads log file"""
    cmd = 'tail -' + depth + ' ' + log
    try:
        log_bin = subprocess.check_output(cmd, shell = True)
    except Exception:
         input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
    else:
        log_txt = log_bin.decode().splitlines(False)
    return log_txt
#
# Status
#
def status(services):
    """Queries relevant services status"""
    filtered = []
    for i in range(len(services)):
        cmd = 'systemctl status ' + services[i] + ' --no-pager'
        try:
            output_bin = subprocess.check_output(cmd, shell=True)
        except Exception:
            filtered.append(f"{bcolors.FAIL}{services[i]}: INACTIVE{bcolors.ENDC}")
        else:
            output = output_bin.decode().splitlines(False)
            for line in output:
                if 'Active' in line:
                    filtered.append(f"{bcolors.OKGREEN}{services[i]}{bcolors.ENDC}: {line.strip()}")
    return filtered

def netstat():
    """Monitors relevant ports"""
    filtered = []
    cmd = 'netstat -lnpt'
    try:
        netstat_bin = subprocess.check_output(cmd, shell = True)
    except Exception:
        input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
    else:
        netstat_txt = netstat_bin.decode().splitlines(False)
        for i in range(len(netstat_txt)):
            line = " ".join(netstat_txt[i].split())
            if 'master' in line or 'dovecot' in line:
                filtered.append(line)
    return filtered

def queue():
    """Queue management"""
    cmd1 = 'postqueue -p'
    cmd2 = 'postqueue -f'
    try:
        queue_bin = subprocess.check_output(cmd1, shell = True)
    except Exception:
        input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
    else:
        queue_txt = queue_bin.decode()
        while True:
            system('clear')
            print(queue_txt)
            option = input(f'\n {bcolors.WARNING}f - flush queue{bcolors.ENDC}\n q - Quit\n \n -> ').lower()
            if option == 'f':
                try:
                    flush_bin = subprocess.check_output(cmd2, shell=True)
                except Exception:
                    input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
                break
            elif option == 'q':
                break


# Postfixadmin

def postfixadmin_exe(message, cmd):
    """Executes postfixadmin command"""
    ok = input_yesno(message)
    if ok == True:
        try:
            output_bin = subprocess.check_output(cmd, shell=True)
        except Exception:
            input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
        else:
            output = output_bin.decode()
            print(output)
            input('Press any key to return to menu.')

def postfixadmin_add():
    """Postfixadmin add mailbox"""
    print(f"{bcolors.OKBLUE}ADD NEW USER:{bcolors.ENDC}")
    user = input('New User email: ')
    name = input('New User full name: ')
    pw = input('Password: ')
    cmd = 'postfixadmin-cli mailbox add ' + user + ' --password ' + pw + ' --password2 ' + pw + ' --name ' + name + ' --quota --active y --welcome-mail n --email-other'
    postfixadmin_exe('Save new User? (y/n): ', cmd)

def postfixadmin_del():
    """Postfixadmin delete mailbox"""
    print(f"{bcolors.WARNING}DELETE USER:{bcolors.ENDC}")
    user = input('User email: ')
    cmd = 'postfixadmin-cli mailbox delete ' + user
    postfixadmin_exe(f'{bcolors.FAIL}Delete User? (y/n): {bcolors.ENDC}', cmd)

def postfixadmin_pwd():
    """Postfixadmin change password"""
    print(f"{bcolors.OKBLUE}CHANGE PASSWORD:{bcolors.ENDC}")
    user = input('User email: ')
    pw = input('Password: ')
    cmd = 'postfixadmin-cli mailbox update ' + user + ' --password ' + pw + ' --password2 ' + pw
    postfixadmin_exe('Update password? (y/n): ', cmd)


# Postmap

def postmap(filename):
    """Runs postmap and reloads posfix"""
    cmd1 = 'postmap ' + filename
    cmd2 = 'systemctl reload postfix'
    try:
        output_bin = subprocess.check_output(cmd1, shell=True)
    except Exception:
        input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
    try:
        output_bin = subprocess.check_output(cmd2, shell=True)
    except Exception:
        input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')

# Spamassassin

def spamass_restart():
    """Runs config check and restarts spamassassin"""
    cmd1 = 'spamassassin --lint'
    cmd2 = 'systemctl restart spamassassin'
    try:
        output_bin = subprocess.check_output(cmd1, shell=True)
    except Exception:
        input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
    try:
        output_bin = subprocess.check_output(cmd2, shell=True)
    except Exception:
        input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')

# Logs

def dovecot_log(log_txt):
    """Filters mail.log for dovecot errors"""
    for i in range(len(log_txt)):
        if 'dovecot' in log_txt[i] and ('Fatal' in log_txt[i] or 'Warning' in log_txt[i] or 'Error' in log_txt[i]):
            print(log_txt[i])

def postfix_log(log):
    """Prints pflogsumm"""
    cmd = 'pflogsumm ' + log + ' --problems-first --rej-add-from -q'
    try:
        log_bin = subprocess.check_output(cmd, shell = True)
    except Exception:
        input(f'{bcolors.WARNING} Command returned an error. Press any key to continue.{bcolors.ENDC}')
    else:
        log_txt = log_bin.decode()
    print(log_txt)

def opendmarc_log(log_txt):
    """Filters mail.log for OpenDMARC entries"""
    for i in range(len(log_txt)):
        if 'opendmarc' in log_txt[i]:
            print(log_txt[i])

def opendkim_log(log_txt):
    """Filters mail.log for OpenDKIM entries"""
    for i in range(len(log_txt)):
        if 'opendkim' in log_txt[i]:
            print(log_txt[i])

def spamd_log(log_txt):
    """Filters mail.log for spamd entries"""
    for i in range(len(log_txt)):
        if 'spamd' in log_txt[i]:
            print(log_txt[i])

def spf_log(log_txt):
    """Filters mail.log for SPF entries"""
    for i in range(len(log_txt)):
        if 'policyd-spf' in log_txt[i]:
            print(log_txt[i])

def f2b_log(log_txt):
    """Filters fail2ban.log for postfix ban/unban"""
    for i in range(len(log_txt)):
        if ('postfix' in log_txt[i]) and ('Ban' in log_txt[i] or 'Unban' in log_txt[i]):
            print(log_txt[i])

def search_log(log_txt, string):
    """Mail.log search"""
    for i in range(len(log_txt)):
        if string in log_txt[i]:
            print(log_txt[i])

# Menus

def menu_main():
    """Main menu display"""
    host_bin = subprocess.check_output('hostname', shell=True)
    host = host_bin.decode()
    return f"""
 ----------------------------------    
 MAIL ADMINISTRATION ON:
 {host} ---------------------------------
    
 1 - Status
 2 - Users
 3 - Filters
 4 - Logs
 5 - Exit
"""

def menu_status():
    """Status menu display"""
    host_bin = subprocess.check_output('hostname', shell=True)
    host = host_bin.decode()
    return f"""
 ----------------------------------    
 MAIL ADMINISTRATION ON:
 {host} 1 - STATUS
 ---------------------------------
    
 1 - Service Status
 2 - Netstat
 3 - Mail queue
 4 - Return to Main Menu
"""

def menu_user():
    """User menu display"""
    host_bin = subprocess.check_output('hostname', shell=True)
    host = host_bin.decode()
    return f"""
 ----------------------------------    
 MAIL ADMINISTRATION ON:
 {host} 2 - USERS
 ---------------------------------
    
 1 - Add User
 2 - Delete User
 3 - Reset Password
 4 - Return to Main Menu
"""

def menu_filter():
    """Filter menu display"""
    host_bin = subprocess.check_output('hostname', shell=True)
    host = host_bin.decode()
    return f"""
 ----------------------------------    
 MAIL ADMINISTRATION ON:
 {host} 3 - FILTERS
 ---------------------------------
    
 1 - Postfix HELO/EHELO Whitelist
 2 - Postfix RBL Override
 3 - Header Checks
 4 - Body Checks
 5 - Spamassassin Custom Rules
 6 - Return to Main Menu
"""

def menu_logs():
    """Filter menu display"""
    host_bin = subprocess.check_output('hostname', shell=True)
    host = host_bin.decode()
    return f"""
 ----------------------------------    
 MAIL ADMINISTRATION ON:
 {host} 4 - LOGS
 ---------------------------------
    
 1 - Dovecot (WARNING, ERROR, FAIL)
 2 - Postfix (pflogsumm)
 3 - OpenDMARC
 4 - OpenDKIM
 5 - SPF
 6 - Fail2Ban
 7 - Spamassassin
 8 - Mail.log search
 9 - Return to Main Menu
"""


if __name__ == '__main__':

    while True:
        system('clear')
        print(menu_main())
        item = input('Select option: ')
        if item == '1':
            while True:
                system('clear')
                print(menu_status())
                item = input('Select option: ')
                if item == '1':
                    status_list = status(services)
                    system('clear')
                    print('-------------------------------------')
                    print(*status_list, sep = "\n")
                    print('-------------------------------------')
                    input('Press any key to return to menu.')
                elif item == '2':
                    port_list = netstat()
                    system('clear')
                    print('-------------------------------------')
                    print(*port_list, sep = "\n")
                    print('-------------------------------------')
                    input('Press any key to return to menu.')
                elif item == '3':
                    system('clear')
                    queue()
                elif item == '4':
                    break
                else:
                    return_to_menu()
        elif item == '2':
            while True:
                system('clear')
                print(menu_user())
                item = input('Select option: ')
                if item == '1':
                    system('clear')
                    postfixadmin_add()
                elif item == '2':
                    system('clear')
                    postfixadmin_del()
                elif item == '3':
                    system('clear')
                    postfixadmin_pwd()
                elif item == '4':
                    break
                else:
                    return_to_menu()
        elif item == '3':
            while True:
                system('clear')
                print(menu_filter())
                item = input('Select option: ')
                if item == '1':
                    system('clear')
                    edit(config_files['helo'], 'host', 'OK')
                    postmap(config_files['helo'])
                elif item == '2':
                    system('clear')
                    edit(config_files['rbl'], 'domain', 'OK')
                    postmap(config_files['rbl'])
                elif item == '3':
                    system('clear')
                    edit(config_files['header_checks'], 'expression', 'DISCARD')
                    postmap(config_files['header_checks'])
                elif item == '4':
                    system('clear')
                    edit(config_files['body_checks'], 'expression', 'DISCARD')
                    postmap(config_files['body_checks'])
                elif item == '5':
                    system('clear')
                    edit(config_files['spamassassin'], 'rule', '')
                    spamass_restart()
                elif item == '6':
                    break
                else:
                    return_to_menu()
        elif item == '4':
            while True:
                system('clear')
                print(menu_logs())
                item = input('Select option: ')
                if item == '1':
                    system('clear')
                    log = log_read(log_files['mail'])
                    dovecot_log(log)
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '2':
                    system('clear')
                    postfix_log(log_files['mail'])
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '3':
                    system('clear')
                    log = log_read(log_files['mail'])
                    opendmarc_log(log)
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '4':
                    system('clear')
                    log = log_read(log_files['mail'])
                    opendkim_log(log)
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '5':
                    system('clear')
                    log = log_read(log_files['mail'])
                    spf_log(log)
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '6':
                    system('clear')
                    log = log_read(log_files['f2b'])
                    f2b_log(log)
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '7':
                    system('clear')
                    log = log_read(log_files['mail'])
                    spamd_log(log)
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '8':
                    system('clear')
                    string = input(f'\nEnter the search string: ')
                    log = log_read(log_files['mail'])
                    search_log(log, string)
                    input(f'\n{bcolors.WARNING}Press any key to return to menu.{bcolors.ENDC}')
                elif item == '9':
                    break
                else:
                    return_to_menu()
        elif item == '5':
            break
        else:
            return_to_menu()
