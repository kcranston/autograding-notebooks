---
tags: tool-development
---

# Autograding Documentation 

## How to Create a good notebook  
* this might end up in nbgrader repo / docs!! 

## Overview of autograding workflow

We are using nbgrader and GitHub Classroom for the workflow. These two platforms are not integrated, so there are a set of [integration scripts](https://github.com/earthlab/autograding-notebooks/tree/master/scripts) that move information between them. There are also a few steps that need to be repeated in both places (adding assignments, adding students). At a high level, the workflow to set up the first assignment in a new course is as follows. Details of course and assignment setup are in the next sections.

* [_nbgrader_] Create a new local nbgrader course directory
* [_github classroom_] Create a new GitHub Classroom. Add the students via their github usernames. 
* [_nbgrader_] Create a new assignment and add one or more notebooks for the assignment to the nbgrader directory
* Put the nbgrader repo onto GitHub as a private repo
* [_nbgrader_] Validate the notebook(s) and create the student version.
* Create a template repository in the GitHub organization. Use the `make_template_repo.py` script to 1) create a local template repo from the nbgrader directory and 2) link to the GitHub remote. 
* [_github classroom_] Make a new assignment for the course, adding the template repository. 
* Provide the assignment link to the students and have them complete the assignment and then submit by pushing their changes to GitHub.
* [_github classroom_] After all students have linked their github accounts, download the student roster as a csv file. 
* [_nbgrader_] Import the students into the database from the csv roster.
* After the assignment deadline, use the `clone-all.py` script to clone all of the student repos to the instructor computer and move the completed notebook to the nbgrader directory. 
* [_nbgrader_] Grade the notebooks (autograding and manual grading) and generate the feedback reports.
* Use the `git-feedback.py` script to push the feedback reports to the student repositories on GitHub.


## How to Setup Course To use with Nbgrader and Github Classroom

The steps below only have to be done once for every course. 

### Step 1: JupyterHub (Optional)

Update / create JupyterHub using the [hub-ops github repo](https://github.com/earthlab/hub-ops) with required environment / packages

* Give students access to the hub by adding their github usernames to the whitelist.

*NOTE: You do NOT need JupyterHub to run the grading workflow.*

### Step 2: Setup Your Local Python Environment

Next you need to setup your local environment. For the earth analytics courses we use Miniconda and an earth-analytics conda environment created specifically for our courses. 

1. Install [Miniconda - URL will be live after merge of open PR](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-git-bash-conda/)
1. Install the [Earth Lab earth-analytics-python conda environment](https://github.com/earthlab/earth-analytics-python-env)
1. Activate the `earth-analytics-python` conda environment that you just installed.
1. Install the [nbgrader extensions](https://nbgrader.readthedocs.io/en/stable/user_guide/installation.html#nbgrader-extensions):

```
jupyter nbextension install --sys-prefix --py nbgrader --overwrite
jupyter nbextension enable --sys-prefix --py nbgrader
jupyter serverextension enable --sys-prefix --py nbgrader
```

Note that the extensions will be available to use anytime you activate the `earth-analytics-python` environment. You could also use this workflow with another environment! This setup is for the earth-analytics courses specifically.

### Temporary nbgrader installation instructions

We have added some functionality to `nbgrader` to support partial credit. Until those changes have been merged, you will need to update nbgrader from github as follows:

`pip install --upgrade git+https://github.com/kcranston/nbgrader.git@partial_credit`


### Step 3. Setup GitHub Classroom 

Next, create a new github classroom within your organization for the course that you wish to teach using this url: https://classroom.github.com/classrooms/new. We are using the github.com/earth-analytics-edu organization.

*IMPORTANT: You need to be an admin / owner of the organization to create a classroom. This is the only step that requires you to be an owner for the organization.* 

Once you have a course setup within github classroom, you can add students to the classroom:

* Get list of students and their github usernames
* Add the students that you want to have access to your new classroom. On the classroom page, click the 'Settings' tab and then 'Roster management' in the sidebar. You can paste in a list of identifiers, one per line.

> [name=Karen Cranston]Would be good to use Canvas IDs for the identifers. Then will we have canvas and github ids associated for each student.  

### Step 4: Setup nbgrader repository

`nbgrader` requires a specific directory structure in order to work properly. See the [nbgrader philosophy](https://nbgrader.readthedocs.io/en/stable/user_guide/philosophy.html) for details. In order to use the autograding workflow, you need to set up your course using this directory structure. Note that there is **one** nbgrader directory for each course (not each assignment).

* Create an `nbgrader` directory on your local computer using the command 

`nbgrader quickstart course-name-here`

This is the directory that you will use to manage all assignments in your course. The course name does not have to match the name of the course that you used for your github classroom setup but we suggest that you do make the names the same to keep things simple.

In bash, `cd` to your local course directory. It is not yet a git repo. Initialize the `course-name-here` directory on your local computer as git repo using `git init`.

### OPTIONAL:

If you want to share your nbgrader repo with others (such as others who might be contributing to grading and teaching in your class), you may want to connect the local nbgrader repo to a remote repo on github. IMPORTANT: this is where student grades will be stored. Be sure to make this repository private! 

To share your nbgrader repo as a provide repo on github:

1. Create an nbgrader repo with the same name in your github organization. Be sure that it is PRIVATE as this is where grades will be stored. 

2. Setup `remotes` to connect your local repository to the github repository. *Note: you can copy the remote url from github.*

`git remote add origin https://github.com/your-org-name-here/your-class-name-here-nbgrader.git` 

> [name=Leah Wasser] this is confusing and needs some explanation. I thought i'm adding them to the classroom but here i'm adding them again? Any explanation you guys can add here would be really nice.

   * Add the students to nbgrader. See [docs](https://nbgrader.readthedocs.io/en/stable/user_guide/managing_the_database.html#managing-students). Easiest way is to wait until the students have accepted the first assignment and linked their github accounts. Then you can download the roster as csv from GitHub.

Once you have completed the steps above, you are ready to begin creating assignments for your course. 

## Create an Assignment

To create an assignment, you need to setup the assignment in both nbgrader locally and in GitHub Classroom (if you are using Classroom). There is no explicit link between nbgrader and github classroom, but the integration scripts assume that the assignment name is the same in both. 

### Step 1: nbgrader assignment setup

The instructions below are using the command line to set things up. You can also perform the same steps in the nbgrader interface wtihin jupyter notebooks. 

Command Line Steps

1. Add new assignment to nbgrader:
      `nbgrader db assignment add <assignment_name>`
2. Create the assignment notebook(s), including autograded test cells. Put notebook(s) in the `source` dir of the nbgrader repo: `nbgrader/source/<assignment_name>/*.ipynb`
3. Validate the assignment: 
`nbgrader validate source/<assignment_name>/*.ipynb`

*or click on the validate button in the notebook.*

4. Create the student version of the assignment using:
`nbgrader assign <assignment_name>` 

*(or click on the generate button in the nbgrader interface)*

When you create the student version of the notebook, nbgrader generates the necessarily files that the students need to complete the assignment in  `nbgrader/release/<assignment_name>`. If all worked well, these files should have the answers to the problems hidden from the students.

### Step 2: GitHub Classroom assignment setup

Once you have created the student version of the assignment, you are ready to create the GitHub classroom assignment and link a template repository. The template is the repo that GitHub Classroom uses to create the assignment repositories that you will share with the students.

1. On GitHub, create a repository for the template repo in your classroom organization. (earth-analytics-edu organization). Follow the [naming conventions in this document](https://hackmd.io/_4GDiG9wSwe6lBq18bDM7w#Naming-conventions).

1. Locally, create the template repo and push to github using the [make-template-repo](https://github.com/earthlab/autograding-notebooks/blob/master/scripts/make-template-repo.py) script. Sample call (see readme in [github](https://github.com/earthlab/autograding-notebooks/tree/master/scripts) for details): 
     `python make-template-repo.py both nbgrader-bootcamp assignment1 --org-name earth-analytics-edu`

> [name=Leah Wasser] that script `make-template-repo.py`  is not documented. can someone please add instructions here on how to call it? i'm happy to help document things but right now there is not documentation for how to call it


1. Create a new assignment in GitHub classroom and use the name of the template repo in the 'template repository' field. _The 'assignment title' on GitHub must be the same as the nbgrader assignment name. See Naming Conventions, at the bottom_. 

1. Once you create the assignment, GitHub will provide a student download link. Give this link to the students. 

1. Students click on the link, which generates a repo in the GitHub Classroom organization with their name in the repo name. 
1. To work locally on the assignment, or to work in the hub or some other cloud space, students clone their repo locally. Then they complete the assignment (either on a local installation of jupyter notebook or on the jupyterhub). They submit using `git push`.

> [name=Leah Wasser] I believe that the text below refers to the fact that we may 


    * (Later, we might want the students to work with forks and pull requests). 
    * The first time the students click on an assignment link, they will be asked to join the organization. Now you can link the student to their github account and download the roster as a csv file.
1. Add the students to nbgrader database: `nbgrader db student import students.csv`
> [name=Karen Cranston] I think there might be some re-formatting of the csv file needed between github export and nbgrader import.
7. Students submit assignments using `git commit` and `git push` to their repositories. 

### Step 3 - Grading assignments and returning feedback
1. Use the [clone-all.py](https://github.com/earthlab/autograding-notebooks/blob/master/scripts/clone-all.py) script to collect student repos and integrate notebooks into nbgrader repo. This takes the place of the nbgrader collect command. Sample call (see readme in [github](https://github.com/earthlab/autograding-notebooks/tree/master/scripts) for details):
  `clone-all.py --roster ../classroom_roster.csv --assignment assignment1 --classroom earth-analytics-edu`
3. Grade the notebooks using `nbgrader autograde <assignment_name>` and then do any manual grading. 
4. Generate the feedback reports using `nbgrader feedback <assignment_name>`. 
5. Keep updating the nbgrader repo via git push so that other instructors can see grades and reports. 
6. Push the html feedback reports to the student repos using the [git-feedback.py](https://github.com/earthlab/autograding-notebooks/blob/master/scripts/git-feedback.py) script. Sample call (see readme in [github](https://github.com/earthlab/autograding-notebooks/tree/master/scripts) for details):
  `git-feedback.py --roster ../classroom_roster.csv --assignment assignment1`

## Naming conventions

Based on discussion in [this issue](https://github.com/earthlab/autograding-notebooks/issues/6), these are the naming conventions for the various digital artifacts. Because so many of these names gets concatenated into repo names, general convention is to keep them short but descriptive. 

* **GitHub organization**: [earth-analytics-edu](https://github.com/earth-analytics-edu)
* **Classname**
  * _description_: The name of the class in GitHub Classroom, e.g. [class for bootcamp test](https://classroom.github.com/classrooms/45207559-ea-bootcamp-test). This does not affect any other names.
  * _format_:`ea-{classname}-nbgrader`, e.g. ea-bootcamp-nbgrader
* **Acronym**: 
  * _description_: a short form of the classname; used in repository names to prevent them from being too long and unwieldy and also to disambiguate repos for different courses
  * _format_: anything short, e.g. `ea` for 'earth-analytics' or `ea-bootcamp` for the bootcamp
* **Assignment {title/name}**
  * _description_: Name of the assignment, including week number to facilitate ordering. Set twice - once as `assignment title` in GitHub classroom and once as `assignment name` in nbgrader (_name must match in both locations!_) and then used as parameter for [nbgrader-classroom integration scripts](https://github.com/earthlab/autograding-notebooks/tree/master/scripts). 
  * _format_: `{acronym}-{week-number}-{assignment}`, e.g. `ea-02-spatial-vector-data`. Note inclusion of course acronym, because all assignments for all courses go into same github org. Also week number with leading zero.
* **Assignment repository prefix**
  * _description_: Required field when setting up a GitHub classroom assignment. This will be part of the student assignment repo name. Workflow assumes this is the same as Assignment. 
  * _format_: Same as Assignment, e.g. enter same text for `assignment title` and `assignment repository prefix` in GitHub classroom.
* **Template repository**
  * _description_: name used for repo created by [template repo script](https://github.com/earthlab/autograding-notebooks/blob/master/scripts/make-template-repo.py) and used as template for assignments
  * _format_: `{assignment}-template`, e.g. `ea-02-spatial-vector-data-template`
* **Student repositories**
  * _description_: auto-generated names based on other choices, above. Cannot be modified.
  * _format_: `{assignment}-{student-github-username}`, e.g. `ea-02-spatial-vector-data-lwasser`