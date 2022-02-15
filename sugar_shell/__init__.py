#!/usr/bin/env python3
# encoding=utf-8
import os

ssh_config_file = '~/.ssh/config'


def parse_config():
    entry_list = []
    entry_name = host_name = user_name = pw = ''

    conf = os.path.expanduser(ssh_config_file)

    if not os.path.exists(conf):
        print('No such file exists: "%s"!' % conf)
        return entry_list, 1

    fp = open(conf, 'r')

    for line in fp:
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        if line.startswith('Host '):
            if entry_name:
                entry_address = '%s@%s' % (user_name, host_name)
                entry_list.append((entry_name, entry_address, pw))
                pw = ''

            entry_name = line.split()[1]

            if entry_name == '*':
                entry_name = ''

        elif line.startswith('HostName '):
            host_name = line.split()[1]
        elif line.startswith('User '):
            user_name = line.split()[1]
        elif line.startswith("Password "):
            pw = line.split()[1]

    if entry_name:
        entry_address = '%s@%s' % (user_name, host_name)
        entry_list.append((entry_name, entry_address, pw))

    fp.close()

    return entry_list, 0


def ssh_helper():
    entry_id = 0
    entry_list, status_code = parse_config()

    if not entry_list and status_code == 1:
        return

    print('Hello %s, Welcome to use SugarShell~ :)' % (os.environ['USER']))

    entry_id = show(entry_id, entry_list)

    select = ''

    while select != 'q':
        select = input('\n# ')

        if select == 'q':
            print('GoodBye %s' % (os.environ['USER']))
            break

        if select == 's':
            show(entry_id, entry_list)
        else:
            try:
                entry_name, entry_addr, pw = entry_list[int(select)]
                print('connect %s' % entry_addr)
                if len(pw) <= 0:
                    os.system('ssh %s' % entry_name)
                else:
                    os.system('sshpass -p %s ssh %s' % (pw, entry_name))
            except (ValueError, IndexError):
                print('You must press a number between 0 and %d' % entry_id)


def show(entry_id, entry_list):
    print(
        '+-----+------------------------------+------------------------------------------+---------------+')
    print(
        '| id  | name                         | address                                  | is_sshpass    |')
    print(
        '+-----+------------------------------+------------------------------------------+---------------+')
    for entry_id, entry in enumerate(entry_list):
        entry_name, entry_addr, pw = entry
        print('| %-3d | %-28s | %-40s | %-13s |' % (entry_id, entry_name, entry_addr, len(pw) > 0))
    print(
        '+-----+------------------------------+------------------------------------------+---------------+')

    print('''
Tips: Press a number betwwen 0 and %d to select the host to connect, or "q" to quit, "s" to show.''' % entry_id)
    return entry_id
