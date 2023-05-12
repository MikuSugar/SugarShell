#!/usr/bin/env python3
# encoding=utf-8
import os
import signal
import sys

from math import ceil  # 导入向上取整函数

ssh_config_file = '~/.ssh/config'

title = '''
                                  _          _ _ 
 ___ _   _  __ _  __ _ _ __   ___| |__   ___| | |
/ __| | | |/ _` |/ _` | '__| / __| '_ \ / _ \ | |
\__ \ |_| | (_| | (_| | |    \__ \ | | |  __/ | |
|___/\__,_|\__, |\__,_|_|    |___/_| |_|\___|_|_|
           |___/                                 
                                            v0.2.6
'''


def signal_handler(signal, frame):
    print()
    print('GoodBye %s' % (os.environ['USER']))
    sys.exit(0)


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
    signal.signal(signal.SIGINT, signal_handler)
    entry_id = 0
    entry_list, status_code = parse_config()

    if not entry_list and status_code == 1:
        return

    print(title)
    print('Hello %s, Welcome to use SugarShell~ :)' % (os.environ['USER']))

    # 定义每页显示的主机数
    per_page = 15
    # 计算总页数
    total_pages = ceil(len(entry_list) / per_page)
    # 初始化当前页数为1
    current_page = 1

    # 显示第一页的内容
    show(entry_id, entry_list, current_page, per_page)

    select = ''

    while select != 'q':
        select = input('\n# ')

        if select == 'q':
            print('GoodBye %s' % (os.environ['USER']))
            break

        if select == 's':
            # 显示当前页的内容
            show(entry_id, entry_list, current_page, per_page)
        elif select == 'n':
            # 如果有下一页，就显示下一页的内容，并更新当前页数
            if current_page < total_pages:
                current_page += 1
                show(entry_id, entry_list, current_page, per_page)
            else:
                print('This is the last page.')
        elif select == 'p':
            # 如果有上一页，就显示上一页的内容，并更新当前页数
            if current_page > 1:
                current_page -= 1
                show(entry_id, entry_list, current_page, per_page)
            else:
                print('This is the first page.')
        else:
            try:
                entry_name, entry_addr, pw = entry_list[int(select)]
                print('connect %s' % entry_addr)
                if len(pw) <= 0:
                    os.system('ssh %s' % entry_name)
                else:
                    os.system('sshpass -p %s ssh %s' % (pw, entry_name))
            except (ValueError, IndexError):
                print('You must press a number between 0 and %d' % (len(entry_list) - 1))


def show(entry_id, entry_list, current_page, per_page):
    # 根据当前页数和每页显示的主机数，计算开始和结束的索引
    start_index = (current_page - 1) * per_page
    end_index = min(current_page * per_page - 1, len(entry_list) - 1)

    print(
        '+-----+------------------------------+------------------------------------------+---------------+')
    print(
        '| id  | name                         | address                                  | is_sshpass    |')
    print(
        '+-----+------------------------------+------------------------------------------+---------------+')
    for i in range(start_index, end_index + 1):
        # 遍历当前页的主机列表，并打印出来
        entry_id = i
        entry_name, entry_addr, pw = entry_list[i]
        print('| %-3d | %-28s | %-40s | %-13s |' % (entry_id, entry_name, entry_addr, len(pw) > 0))

    print(
        '+-----+------------------------------+------------------------------------------+---------------+')
    print('''
Tips: Press a number betwwen 0 and %d to select the host to connect,or "q" to quit,or "s" to show current page,
or "n" to go to next page,or "p" to go to previous page.''' % (len(entry_list) - 1))
    return entry_id


if __name__ == '__main__':
    ssh_helper()
