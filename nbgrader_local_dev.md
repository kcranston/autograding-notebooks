# Setting up nbgrader for local dev

[nbgrader](https://github.com/jupyter/nbgrader) includes functionality for
creating assignments with autograded tests in Jupyter notebooks as well as
managing students, files, and grades for a Jupyter-based class. Most of the
nbgrader code is for the latter.

These notes are for getting a local setup to test the autograding functionality.
This involves running both instructor and student commands to create the
nbgrader workflow. Where possible, I've done everything using the command-line
interface, but almost everything can also be done with the notebook interface
in the browser.

## Installing nbgrader

**Which nbgrader?**

To simply test release version of nbgrader:

   `pip install nbgrader` (or conda)

To follow along with the implementation of partial credit, use my fork (as of May 2, the master branch is unchanged from base nbgrader):

   `pip install --upgrade git+https://github.com/kcranston/nbgrader.git`

If you want to make changes to nbgrader code and test on the fly, install from local git repo:

   `pip install -e /path_to_local_repo`

Once you have picked your pip command, simply follow the [official installation instructions](https://nbgrader.readthedocs.io/en/stable/user_guide/installation.html), including the three extensions. I use a virtual env for this.

## Setup nbgrader course locally

1. Use the quickstart command to create a course:

     `nbgrader quickstart course-name`.

     This will create a course directory called `course_name` with one assignment called `ps1`, some sample notebooks and a config.

1. Create the exchange directory (where we will release and submit assignments):

  `mkdir /tmp/exchange`

1. Edit the config:

   * add `c.Exchange.root = "/tmp/exchange"` after the `c.Exchange.course_id` line
   * delete the students (the line starting with `c.CourseDirectory.db_students `)

1. Add yourself as a student, using your the username on your local computer (`$USER`) as the student id:

  `nbgrader db student add studentid --last-name=lastname --first-name=firstname`

1. Create a student directory (create this anywhere but not inside the course directory, or the exchange directory):

  `mkdir student_dir`

1. Create a `nbgrader_config.py` file in the student dir. It only needs three lines:

  ```
  c = get_config()
  c.Exchange.root = '/tmp/exchange'
  c.Exchange.course_id = 'course-name'
  ```

## Edit assignment

* Start `jupyter notebook` from the top level of the course directory. You should see the 'Formgrader' tab at the top if
nbextensions were properly installed.

* In `source\ps1` there is a `problem1` notebook. Open this (or create a new one). You can have one or more notebooks per assignment.

* Once you have a notebook open, enable the nbgrader interface with
View -> Cell Toolbar -> Create Assignment. Now you should see a pulldown menu on the cells that allow you to specify whether the cell is a task or test and auto vs manually graded.

* save once you are done

## Autograding workflow

The basic workflow (see [nbgrader docs](https://nbgrader.readthedocs.io/en/stable/user_guide/philosophy.html) for an overview):

* (instructor) validate notebooks
* (instructor) assign notebooks (create the student version)
* (instructor) release notebooks (copy to exchange dir)  
* (student) fetch notebooks (from exchange dir)
* (student) do work, save notebooks
* (student) submit notebooks (to exchange dir)
* (instructor) collect notebooks (from exchange dir)
* (instructor) autograde notebooks
* (instructor) manually grade notebooks
* (instructor) generate feedback

From the command line, assuming assignment named `ps1`:

In `course_dir` (i.e. as instructor):

* `nbgrader validate source/ps1/*.ipynb`
* `nbgrader assign "ps1" --IncludeHeaderFooter.header=source/header.ipynb --create`
* `nbgrader release ps1`

In `student_dir` (i.e. as student):

* `nbgrader fetch ps1`
* _do work in notebook_
* `nbgrader submit ps1`

In `course_dir` (i.e. as instructor):
* `nbgrader collect ps1`
* `nbgrader autograde "ps1"`
