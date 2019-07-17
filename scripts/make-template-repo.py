# create template repo for github classroom from
# nbgrader directory

import os
import fnmatch
import argparse

def get_notebooks(nbgrader_dir, assignment):
    # get the list of notebooks for this assignment
    # assumes assignemnts have been released (i.e. are in release dir)
    print("Getting notebooks")
    release_dir = nbgrader_dir + '/release/' + assignment
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

def init_template(repo_name):
    # create a new directory for this assignment and initialize as git repo
    try:
        os.mkdir(repo_name)
        
        print("Initializing git repo")
    except FileExistsError as fee:
        print("directory {} already exists".format(repo_name))

def push_to_github(template_dir):
    # push the repo to the github classroom
    print("pushing to github repo")

if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('nbgrader_dir', help='Top level nbgrader directory')
    parser.add_argument('assignment', help='Assignment name, e.g., "2019-01-31-stability" or "hw1-rootfinding"')
    parser.add_argument('--org_name', help='name of GitHub organization')
    parser.add_argument('--repo_name', help='desired name of github repo')
    args = parser.parse_args()

    notebooks = get_notebooks(args.nbgrader_dir, args.assignment)
    init_template(args.repo_name)
