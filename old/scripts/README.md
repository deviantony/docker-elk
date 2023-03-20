## Basic Instructions for Generating HS Reports

< brief description >

### Installation

It is recommended to use a Python 3 virtual environment, e.g. anaconda.  The following steps will get you going quickly using miniconda.  These steps can be skipped if anaconda or miniconda are already install on your system.

#### 1. Installing Miniconda

- Navigate to the [miniconda](https://conda.io/miniconda.html) homepage and download the approproate installer.  For example, MacOSX would be:

    ```
    $ wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    ```

- Execute the installer

    ```
    $ bash Miniconda3-latest-MacOSX-x86_64.sh 
    ```

- Complete instructions can be found [here](https://conda.io/docs/user-guide/install/index.html)

#### 2. Installing Required Python Packages

- Create a virtual environment, replace "myenv" with you environment name

    ```
    $ conda create -y -n myenv python=3
    ```

- Activate the environment 

    ```
    $ source activate myenv
    ```

- Install prerequisites 
  
    ```
    (myenv)$ conda env update -n myenv -f environment.yml
    ```

### Generating Reports  

#### 1. Basic Usage

1. Collect Data

    ```
    $/.getdata.py
    ```

This operation performs the following tasks:
 - creates a date-stamped folder for output data
 - collects data from the HydroShare elasticsearch database
 - saves resource, users, and activity data as serialized pandas dataframes (\*.pkl) and comma separated files.

2. Deriving Standard User Metrics


#### 2. Working with the CMS

- With an activate python environment, launch the CUAHSI Metrics Shell (CMS)

    ```
    (myenv) $ ./cms.py
    ----------------------------------------
    CUAHSI Metrics Shell
    ----------------------------------------
    Enter a command or "help" to list options

    A directory for your session has been created at: 04.10.2018_2
    (CMS)
    ```

- You are now in CMS and are free to execute predefined commands.  To view these commands, type `help`.

    ```
    (CMS) help

    Documented commands (type help <topic>):
    ========================================
    calculate_session_stats  collect_hs_data  help  ll  q  rm  save_to_xls

    Undocumented commands:
    ======================
    change_working_dir  set_output_xls
    ```

- To learn more about these commands, type `help` followed by a function name

    ```
    (CMS) help calculate_session_stats

            Calculate session statistics from activity logs.

              usage: calculate_session_stats [a] [b]
              - a: start date, MM-DD-YYYY
              - b: end date, MM-DD-YYYY

    ```


#### 2. Basic Reporting Workflow

1. Collect metrics data from `http://usagemetrics.hydroshare.org/`, organize data in `Pandas` data frames, and save raw binary data.

    ```
    (CMS) collect_hs_data
    ```

2. view the data that was collected

    ```
    (CMS) ll
    total 148584
    -rw-r--r--  1 castro  staff  72529239 Apr 10 13:02 activity.pkl
    -rw-r--r--  1 castro  staff   1780419 Apr 10 13:02 combined-stats.pkl
    -rw-r--r--  1 castro  staff   1167828 Apr 10 13:00 resources.pkl
    -rw-r--r--  1 castro  staff    589196 Apr 10 13:00 users.pkl
    ```

<!--
3. To create custom figures, save these data to excel

    < todo >
-->

4. Create a standard set of figures using `matplotlib`

    ```
    (CMS) calculate_session_stats 01-01-2017 01-01-2018
    ```

    view outputs  

    ```
    (CMS) ll
    total 155696
    -rw-r--r--  1 castro  staff  72529239 Apr 10 13:12 activity.pkl
    -rw-r--r--  1 castro  staff     15545 Apr 10 13:50 activity_by_university.xlsx
    -rw-r--r--  1 castro  staff   1780419 Apr 10 13:12 combined-stats.pkl
    -rw-r--r--  1 castro  staff     28417 Apr 10 13:50 resource_actions_by_university_bar.png
    -rw-r--r--  1 castro  staff   1167828 Apr 10 13:10 resources.pkl
    -rw-r--r--  1 castro  staff     20031 Apr 10 13:50 sessions_by_month_bar.png
    -rw-r--r--  1 castro  staff     33466 Apr 10 13:50 sessions_by_month_line.png
    -rw-r--r--  1 castro  staff     26884 Apr 10 13:50 sessions_by_university_bar.png
    -rw-r--r--  1 castro  staff   3509742 Apr 10 13:50 stats.xlsx
    -rw-r--r--  1 castro  staff    589196 Apr 10 13:10 users.pkl
    ```
