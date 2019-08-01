# create template repo for github classroom from
# nbgrader directory; creates in current working dir (fails if
# template dir already exists)

import os
import fnmatch
import argparse
import subprocess
import shutil

def get_notebooks(nbgrader_dir, assignment):
    # get the list of notebooks for this assignment
    # assumes assignemnts have been released (i.e. are in release dir)
    print("Getting notebooks")
    release_dir = os.path.join(nbgrader_dir,'release', assignment)
    notebooks = []
    for file in os.listdir(release_dir):
        if fnmatch.fnmatch(file, '*.ipynb'):
            print(file)
            notebooks.append(file)
    print("Found {} notebooks".format(len(notebooks)))
    return notebooks

def create_readme():
    # create a stub of a readme file for the template repo
    print("Creating readme")

def do_git_things(org_name,repo_name,no_push):
    # init the repo and push to the github classroom org:
    # git remote add origin git@github.com:earth-analytics-edu/repo_name.git
    # git push -u origin master

    repo_url = "git@github.com:{}/{}.git".format(org_name,repo_name)
    git = ['git', '-C', repo_name]

    # note that it is harmless to call git add, commit, push if no changes
    try:
        if not os.path.exists(os.path.join(repo_name,'.git')):
            print("initializing git repo")
            subprocess.check_call(git + ['init'])
        for file in os.listdir(repo_name):
            if fnmatch.fnmatch(file, '*.ipynb'):
                subprocess.check_call(git + ['add', file])
        subprocess.check_call(git + ['commit', '-mInitial commit'])
        subprocess.check_call(git + ['remote','add','origin',repo_url])
        if not no_push:
            print("pushing to github repo {}".format(repo_url))
            subprocess.check_call(git + ['push','-u','origin','master'])
    except subprocess.CalledProcessError:
        print('Skipping {}'.format(destdir))

if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('nbgrader_dir', help='path to nbgrader directory')
    parser.add_argument('assignment', help='assignment name, e.g., "2019-01-31-stability" or "hw1-rootfinding"')
    parser.add_argument('--org_name', help='name of GitHub Classroom organization')
    parser.add_argument('--repo_name', help='name of github repo; must already exist')
    parser.add_argument('-n', '--no_push', help='Do not push to github; maybe you want to add a readme first?', action='store_true')
    args = parser.parse_args()

    # notebooks = get_notebooks(args.nbgrader_dir, args.assignment)
    # cp notebooks to new dir and initialize as git repo
    try:
        os.mkdir(args.repo_name)
        print("Initializing git repo in {}".format(args.repo_name))
    except FileExistsError as fee:
        print("directory {} already exists; exiting".format(args.repo_name))

    # copy notebooks to repo
    print("Getting notebooks")
    release_dir = os.path.join(args.nbgrader_dir,'release', args.assignment)
    nbooks = 0
    for file in os.listdir(release_dir):
        if fnmatch.fnmatch(file, '*.ipynb'):
            nb = os.path.join(release_dir,file)
            print("copying {} to {}".format(nb,args.repo_name))
            shutil.copy(nb,args.repo_name)
            nbooks += 1
    print("Copied {} notebooks".format(nbooks))

    do_git_things(args.org_name,args.repo_name,args.no_push)
