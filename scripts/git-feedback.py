#!/usr/bin/env python3

import glob
import pandas
import os
import shutil
import subprocess

def read_roster(filename):
    return pandas.read_csv(filename, index_col=['User ID'], usecols=[1,5])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--roster', help='CSV roster file', default='CSCI-3656-001-20190205.csv')
    parser.add_argument('--assignment', help='Name of assignment, e.g., hw1-rootfinding', required=True)
    args = parser.parse_args()
    roster = read_roster(args.roster)
    assignment = args.assignment
    for username, address in roster['Email'].items():
        try:
            (source,) = glob.glob(os.path.join('feedback', username, assignment, '*.html'))
        except ValueError: # Lack of feedback usually means student did not submit homework
            print(f'No feedback for {username}')
            continue
        destdir = os.path.join('submitted', username, assignment)
        dest = os.path.join(destdir, 'feedback.html')
        if os.path.exists(destdir):
            shutil.copyfile(source, dest)
        else:
            print('Destination directory does not exist: {}'.format(destdir))
        git = ['git', '-C', destdir]
        try:
            subprocess.check_call(git + ['add', os.path.basename(dest)])
            subprocess.check_call(git + ['commit', '-mAdd feedback'])
            subprocess.check_call(git + ['push'])
        except subprocess.CalledProcessError:
            print('Skipping {}'.format(destdir))
