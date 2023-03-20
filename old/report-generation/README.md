# Basic Script Usage

## 1. Collect Data

Collect metric data from elasticseach. This will create a working directory for the rest of the scripts, e.g. 09.13.2018

    $ ./collect_data.py 
    
    Metrics will be saved into: 09.13.2018
    --> downloading user metrics
    --> total number of records = 2925
    --> ...
    --> ...

## 2. Users

Generate HydroShare user plots via `users.py`. See help documentation:

    $ ./users.py --help
    usage: users.py [-h] --working-dir WORKING_DIR [--step STEP]
                    [--active-range ACTIVE_RANGE] [--figure-title FIGURE_TITLE]
                    [--filename FILENAME] [--st ST] [--et ET] [-t] [-a] [-n] [-r]
    
    
    optional arguments:
      -h, --help            show this help message and exit
      --working-dir WORKING_DIR
                            path to directory containing elasticsearch data
      --step STEP           timestep to use in aggregation in days
      --active-range ACTIVE_RANGE
                            number of days that qualify a user as active
      --figure-title FIGURE_TITLE
                            title for the output figure
      --filename FILENAME   filename for the output figure
      --st ST               start time MM-DD-YYYY
      --et ET               start time MM-DD-YYYY
      -t                    plot total users line
      -a                    plot active users line
      -n                    plot new users line
      -r                    plot returning users line


### 2.1 Create HydroShare Users Overview (active = 30 days)

    $ ./users.py --working-dir=09.13.2018 --active-range=30 --filename=hs-users-all-30.png -tan 
    --> calculating total users
    --> calculating active users
    --> calculating new users
    --> making figure...
    --> saving figure as 09.13.2018/hs-users-all-30.png

### 2.2 Create HydroShare Users Overview (active = 180 days)

    $ ./users.py --working-dir=09.13.2018 --active-range=180 --filename=hs-users-all-180.png -tan 
    --> calculating total users
    --> calculating active users
    --> calculating new users
    --> making figure...
    --> saving figure as 09.13.2018/hs-users-all-180.png

### 2.3 Create HydroShare Active Users Overview (active = 180 days)
    
    $ ./users.py --working-dir=09.13.2018 --active-range=180 --filename=hs-users-active-180.png -anr 
    --> calculating active users
    --> calculating new users
    --> calculating returning users
    --> making figure...
    --> saving figure as 09.13.2018/hs-users-all-30.png



## 3. Organizations

Generate HydroShare organization plots via `organizations.py`. See help documentation:

    $ ./organizations.py --help 
    usage: organizations.py [-h] --working-dir WORKING_DIR [--st ST] [--et ET]
                        [--title TITLE] [--filename FILENAME] [--agg AGG] [-a]
                        [-u] [-i] [-c]

    optional arguments:
      -h, --help            show this help message and exit
      --working-dir WORKING_DIR
                            path to directory containing elasticsearch data
      --st ST               reporting start date MM-DD-YYYY
      --et ET               reporting end date MM-DD-YYYY
      --title TITLE         title for the output figure
      --filename FILENAME   filename for the output figure
      --agg AGG             data aggregation (e.g. D, M, Y, #D, #M, #Y)
      -a                    plot all distinct organizations
      -u                    plot distinct US organizations
      -i                    plot distinct international organizations
      -c                    plot distinct cuahsi members
    
### 3.1 Plot Summary of all Organizations

    $ ./organizations.py --working-dir=09.13.2018 --agg=3M --filename="hs_all_organizations.png" -a
    --> calculating distinct organizations
    --> making figure...
    --> saving figure as 09.13.2018/hs_all_organizations.png

### 3.2 Plot Summary of US, International, and CUAHSI Member Organizations


    $ ./organizations.py --working-dir=09.13.2018 --agg=3M --filename="hs_us_int_cuahsi_organizations.png" -uic
    --> calculating distinct US universities
    --> calculating CUAHSI members
    --> calculating distinct international universities
    --> making figure...
    --> saving figure as 09.13.2018/hs_us_int_cuahsi_organizations.png


## 4. User Types

Generate HydroShare user type plots using `users-pie.py`:

    $ ./users-pie.py --help
    usage: users-pie.py [-h] --working-dir WORKING_DIR
                        [--figure-title FIGURE_TITLE] [--filename FILENAME]
                        [--st ST] [--et ET] [--exclude EXCLUDE] [-p]
    
    optional arguments:
      -h, --help            show this help message and exit
      --working-dir WORKING_DIR
                            path to directory containing elasticsearch data
      --figure-title FIGURE_TITLE
                            title for the output figure
      --filename FILENAME   output figure name
      --st ST               start time MM-DD-YYYY
      --et ET               start time MM-DD-YYYY
      --exclude EXCLUDE     comma separated list of user types to exclude
      -p                    plot pie chart of user types
     
### 4.1 Plot Pie Chart of Users by Type

    $ ./users-pie.py --working-dir=09.13.2018 --filename=hs_users_minus_other_and_unspecified.png --exclude=Other,Unspecified -p
    --> building user types pie-chart
    --> not reporting Other: 817 users
    --> not reporting Unspecified: 1887 users
    --> total number of users reporting: 221
    --> making user types pie chart...
    --> saving figure as hs_users_minus_other_and_unspecified.png
            
            
        
    
    

