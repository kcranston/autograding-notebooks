#!/usr/bin/env python3

# Script to clone all student repos from a given GitHub classroom course
# and then copy over the assignment files into the nbgrader `submitted` dir
# Modifed from script received from @jedbrown to remove specific course and
# repo references and to clone into separate directory (we are keeping the
# nbgrader repo under version control, so avoiding repos-within-repos)
# Assumes that cwd is nbgrader course dir

import pandas as pd
import os
import glob
import shutil
import subprocess

def mkdir_p(path):
    dirname = os.path.dirname(path)
    if dirname:
        mkdir_p(dirname)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def clone_repo(slug, username, args):
    clonedir = args.clonedir # directory containing git repos
    destdir = os.path.join(clonedir,slug) # path to repo

    if os.path.isdir(destdir):
        # if the repo already exists, pull (unless skip_existing)
        if args.skip_existing:
            return
        cmd = ['git', '-C', destdir, 'pull']
        cmdargs = []
    else:
        classroom = args.classroom
        assignment = args.assignment
        # url format is git@github.com:classroom/assignment-github_username.git
        url = "git@github.com:{}/{}.git".format(classroom, slug)
        # repo does not already exist; clone
        cmd = ['git', '-C', clonedir, 'clone']
        cmdargs = [url]
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
    parser.add_argument('--clonedir', help='Destination directory', default='../cloned-repos')
    parser.add_argument('-n', '--dry-run', help='List repositories that would be cloned', action='store_true')
    parser.add_argument('--skip-existing', help='Skip attempt to update repositories that have already been cloned', action='store_true')
    args = parser.parse_args()

    # roster associates github usernames and student identifiers
    roster = pd.read_csv(args.roster, usecols=('identifier', 'github_username')).set_index('identifier')
    classroom = args.classroom
    assignment = args.assignment

    missing = []
    clonedir = args.clonedir
    mkdir_p(clonedir)

    for identikey, (github_username,) in roster.iterrows():
        slug = "{}-{}".format(assignment,github_username)
        if clone_repo(
            slug = slug,
            username = github_username,
            args=args):
        #if clone_repo(url='{}-{}.git'.format(url_slug,github_username),
                      #dest='submitted/{}/{}'.format(identikey, assignment),
                      #args=args):
            missing.append((identikey, github_username))
        else:
            files = glob.glob(os.path.join(clonedir,slug,'*.ipynb'))
            dest = os.path.join('submitted',github_username,assignment)
            mkdir_p(dest)
            for f in files:
                print("copying {} to {}".format(f,dest))
                shutil.copy(f, dest)
    if len(missing)==0:
        print('All successful; no missing repos')
    else:
        print('Missing repositories: ', missing)
