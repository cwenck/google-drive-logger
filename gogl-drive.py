#!/usr/bin/env python

import os
import subprocess

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def authorize_client():
    json_key = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/credentials.json', 'r'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    auth = gspread.authorize(credentials)
    print('Completed authorization.')
    return auth

def shell_cmd(cmd):
    """Cmd should be the command string to execute. The resulting output is returned.
    """
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    result = proc.stdout.read().replace('\n', '')
    return result


def disk_space():
    return shell_cmd('df -h | head -n2 | tail -n1 | cut -c30- | cut -d" " -f1')


def find_next_row(worksheet):
    """ Finds the first empty row of the worksheet.
    """
    val_list = worksheet.col_values(1)
    row_num = 1
    for row in val_list:
        if row == '':
            return row_num
        row_num += 1
    return None

def write_entry(worksheet):
    """ Trys to log the next entry in the worksheet.
    """
    row = find_next_row(worksheet)
    if row is None:
        print('Out of rows. Adding 100 more.')
        worksheet.add_rows(100)
        row = find_next_row(worksheet)
    print('Writing data to row ' + str(row) + '.')
    row_cells = worksheet.range('A' + str(row) + ':C' + str(row))
    row_cells[0].value = shell_cmd('date')
    row_cells[1].value = disk_space()
    row_cells[2].value = 'test'
    worksheet.update_cells(row_cells)
    print('Row written.')
    return True

#line = shell_cmd('date') + ',' + disk_space() + ',' + shell_cmd('uptime | cut -d" " -f11')

#print(line)


gc = authorize_client()
spread = gc.open_by_key('1k8ZSXOlcGadSFfU8uJLzDMi6Ksr88ZBP6hZe0MWM-18')
wks = spread.sheet1
#print('1min: ' + shell_cmd('uptime | cut -d" " -f10'))
#print('5min: ' + shell_cmd('uptime | cut -d" " -f11'))
#print('15min: ' + shell_cmd('uptime | cut -d" " -f12'))
write_entry(wks)
print('Done')
