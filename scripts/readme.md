# Integration scripts

The scripts in this directory allow us to interface between nbgrader and GitHub Classroom.

All of the scripts assume that the current working directory is the nbgrader course dir.

To get help for any script, simply run `python script.py -h`.  

**make-template-repo.py**

When you create a GitHub Classroom assignment, you can provide a link to a template repository that contains information you want to provide to the students. In our case, we want to that repo to include any notebooks in the nbgrader `release` directory. This script copies notebooks from nbgrader/release, adds a readme and .gitignore, initializes a repository and pushes the repo to an (already existing) github repo.

The first argument allows you to just create the local repo, just push to github, or both.

Sample call: `make-template-repo.py create nbgrader-bootcamp assignment1`

```
usage: make-template-repo.py [-h] [--org_name ORG_NAME]
                             [{create,push,both}] nbgrader_dir assignment

positional arguments:
  {create,push,both}   Whether to {create} local repo, {push} to github, or
                       both
  nbgrader_dir         path to nbgrader directory
  assignment           assignment name, e.g., "2019-01-31-stability" or
                       "ea-04-bootcamp-spatial-data"

optional arguments:
  -h, --help           show this help message and exit
  --org_name ORG_NAME  name of GitHub Classroom organization; default = earth-
                       analytics-edu
```

**clone-all.py**

This script clones all of the student repositories for a given classroom and assignment, then copies the notebooks into the nbgrader 'submitted' directory.

Sample call: `clone-all.py --roster ../classroom_roster.csv --assignment assignment1 --classroom earth-analytics-edu`

```
usage: clone-all.py [-h] [--roster ROSTER] --assignment ASSIGNMENT --classroom
                    CLASSROOM [--clonedir CLONEDIR] [-n] [--skip-existing]

optional arguments:
  -h, --help            show this help message and exit
  --roster ROSTER       CSV file from which to read roster
  --assignment ASSIGNMENT
                        Assignment name, e.g., "2019-01-31-stability" or
                        "hw1-rootfinding"
  --classroom CLASSROOM
                        GitHub Classroom name
  --clonedir CLONEDIR   Destination directory
  -n, --dry-run         List repositories that would be cloned
  --skip-existing       Skip attempt to update repositories that have already
                        been cloned
```

**git-feedback.py**

This script collects all of the feedback reports from the nbgrader directory, copies them to the student repos, and pushes the repos to github. Note that the feedback repo is always called `feedback.html` in the student repo. Note the --dry-run option if you want to check things out before pushing.

Sample call: `git-feedback.py --roster ../classroom_roster.csv --assignment assignment1`

```
usage: git-feedback.py [-h] [--roster ROSTER] --assignment ASSIGNMENT
                       [--clonedir CLONEDIR] [-n]

optional arguments:
  -h, --help            show this help message and exit
  --roster ROSTER       CSV roster file
  --assignment ASSIGNMENT
                        Name of assignment, e.g., hw1-rootfinding
  --clonedir CLONEDIR   Destination directory
  -n, --dry-run         Print git statements but do not run
```
