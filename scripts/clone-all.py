#!/usr/bin/env python3

# Script to clone all student repos from a given GitHub classroom course
# into a directory called `submitted` in the correct format for nbgrader
# Modifed from script received from @jedbrown to remove specific course and
# repo references

import pandas as pd
import os

def mkdir_p(path):
    dirname = os.path.dirname(path)
    if dirname:
        mkdir_p(dirname)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def clone_repo(url, dest, args):
    import subprocess
    if os.path.isdir(dest):
        if args.skip_existing:
            return
        cmd = ['git', '-C', dest, 'pull']
        cmdargs = []
    else:
        mkdir_p(os.path.dirname(dest))
        cmd = ['git', 'clone']
        cmdargs = [url, dest]
    if args.dry_run:
        cmd.append('--dry-run')
        print(cmd + cmdargs)
        return
    return subprocess.call(cmd + cmdargs)

if __name__ == '__main__':
    # argument parsing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--roster', help='CSV file from which to read roster', default='classroom_roster.csv')
    parser.add_argument('--assignment', help='Assignment name, e.g., "2019-01-31-stability" or "hw1-rootfinding"', required=True)
    parser.add_argument('--classroom', help='GitHub Classroom name', required=True)
    parser.add_argument('-n', '--dry-run', help='List repositories that would be cloned', action='store_true')
    parser.add_argument('--skip-existing', help='Skip attempt to update repositories that have already been cloned', action='store_true')
    args = parser.parse_args()

    # roster associates github usernames and student identifiers
    roster = pd.read_csv(args.roster, usecols=('identifier', 'github_username')).set_index('identifier')
    classroom = args.classroom

    # url format is git@github.com:classroom/assignment-github_username.git
    url_slug = "git@github.com:{}/{}".format(classroom, args.assignment)
    missing = []
    for identikey, (github_username,) in roster.iterrows():
        if clone_repo(url='{}-{}.git'.format(url_slug,github_username),
                      dest='submitted/{}/{}'.format(identikey, args.assignment),
                      args=args):
            missing.append((identikey, github_username))
    if len(missing)==0:
        print('All successful; no missing repos')
    else:
        print('Missing repositories: ', missing)
