#!/usr/bin/env python3
# Script to copy nbgrader html feedback reports to feedback.html in student
# repos and push repos to github
# Based on script provided by @jedbrown
# Assumes that cwd is nbgrader course dir

import glob
import pandas as pd
import os
import shutil
import subprocess

def run_cmd(cmd,cmdargs,dry_run):
    if (dry_run):
        cmdargs.insert(1,'--dry-run')
        print(cmd+cmdargs)
    # note that commit when there aren't any changes will produce a
    # non-zero exit code (even with dry-run)
    subprocess.check_output(cmd + cmdargs)

def do_git_things(destdir, dest, dry_run):
    gitcmd = ['git', '-C', destdir]

    try:
        # add
        cmdargs = ['add', os.path.basename(dest)]
        run_cmd(gitcmd,cmdargs,dry_run)
        # commit
        cmdargs = ['commit', '-mAdd feedback.html']
        run_cmd(gitcmd,cmdargs,dry_run)
        # push
        cmdargs = ['push']
        run_cmd(gitcmd,cmdargs,dry_run)
    except subprocess.CalledProcessError as e:
        print(e.output)
        print('Skipping {}'.format(destdir))


def read_roster(filename):
    roster = pd.read_csv(args.roster, usecols=('identifier', 'github_username')).set_index('identifier')
    return roster

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--roster', help='CSV roster file', default='roster.csv')
    parser.add_argument('--assignment', help='Name of assignment, e.g., hw1-rootfinding', required=True)
    parser.add_argument('--clonedir', help='Destination directory', default='../cloned-repos')
    parser.add_argument('-n', '--dry-run', help='Print git statements but do not run', action='store_true')
    args = parser.parse_args()

    assignment = args.assignment
    clonedir = args.clonedir

    roster = read_roster(args.roster)
    for identikey, (github_username,) in roster.iterrows():
        try:
            #print("Looking in: {}".format(os.path.join('feedback', identikey, assignment)))
            (source,) = glob.glob(os.path.join('feedback', identikey, assignment, '*.html'),recursive=True)
        except ValueError: # Lack of feedback usually means student did not submit homework
            print("No feedback found for {}".format(identikey))
            continue
        slug = "{}-{}".format(assignment,github_username)
        destdir = os.path.join(clonedir, slug)
        dest = os.path.join(destdir, 'feedback.html')
        if os.path.exists(destdir):
            print("Copying feedback from {} to {}".format(source,dest))
            shutil.copyfile(source, dest)
        else:
            print('Destination directory does not exist: {}'.format(destdir))
        do_git_things(destdir, dest, args.dry_run)
