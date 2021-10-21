# 42_corona_tracker

This application tracks people who sat close to a recently infected student. It can be used to immediately notify students that may be at risk.

If the campus uses the security footage to find all contacts of an infected student, this program can help track the infected person in the security footage faster because of the listing of all sessions in the output file.

## Description


This program outputs overlapping logging times between an infected student and contacts of this student. See the example output below.

## Prerequisites

- Python version 3 or higher.
- PIP
- Venv (to create a virtual environment)

## Installation and setup

### __1. Create a 42 APP__ 

Login to intra and go to -> settings -> API -> register a new app (top right).

For website just type __placeholder__ and for Redirect URI type __https://placeholder.com__.

### __2. Clone this repo.__

```sh
git clone https://github.com/hilmi-yilmaz/codam_corona_tracker.git
```

### 3. __Insert data__

Insert __UID__ and __SECRET__ of your 42 APP into the __config.yaml__ file between quotes.

Insert your campus ID in the __config.yaml__ file.

### 4. __Create a virtual environment using venv__
If you don't have venv module install, install like:

```sh
pip install virtualenv
```

Create a virtual environment:

```sh
python3 -m venv ENV
```

Activate the environment

```sh
source ENV/bin/activate
```

### 5. __Install packages__
Install required packages

```sh
pip install -r requirements.txt
```

Everything is setup now and you can use the program.

## Usage

Run:

```sh
python3 run.py login_name date_infected how_many_days_to_check
```

- login_name: the intra login name of the infected person
- date_infected: the date the person got infected in the format day-month-year (e.g. 15-01-2021).
- how_many_days_to_check: how many days to check. (The more, the longer the programs runs.)

It will give you the hosts the infected student set on. You have to enter the hosts you want to check.

## Output

The program outputs the following statistics:

- Summary of total overlapping login times.
- Sessions that contributed to overlapping time.
- Student that sat on an infected host (the host that the infected person left).
- Sessions of infected student.
- Sessions of contact persons.

## Example

If you run:

```sh
python3 run.py hyilmaz 19-09-2021 2
```

the program will output the data for 18-09-2021 and 17-09-2021 (2 days).

### Example output

```
hyilmaz tested positive on 2021-10-13. Checking overlaps between 2021-10-11 (00:00:00) and 2021-10-13 (00:00:00).

############################################################
#                                                          #
#         Summary of total overlapping login times         #
#                                                          #
############################################################

Ji-Won          logged in for a total of 2:51:02    hours next to hyilmaz
Thor            logged in for a total of 7:54:05    hours next to hyilmaz
Eustorgo        logged in for a total of 6:42:43    hours next to hyilmaz
Karel           logged in for a total of 4:51:04    hours next to hyilmaz

#############################################################################################
#                                                                                           #
#         Table containing sessions that contributed to overlapping time (hyilmaz)         #
#                                                                                           #
#############################################################################################

session_id      login           host                 begin_time      end_time        date            host_infected_person      overlap        
--------------------------------------------------------------------------------------------------------------------------------------
13212057        Ji-Won          f1r3s11.codam.nl     15:06:09        18:51:15        2021-10-11      f1r3s12.codam.nl          2:51:02        
13220952        Thor            f1r1s16.codam.nl     19:21:03        21:51:03        2021-10-12      f1r1s17.codam.nl          0:42:05        
13219716        Thor            f1r1s16.codam.nl     15:54:02        18:33:03        2021-10-12      f1r1s17.codam.nl          2:39:01        
13215438        Thor            f1r1s16.codam.nl     07:33:04        15:30:31        2021-10-12      f1r1s17.codam.nl          4:32:59        
13217034        Eustorgo        f1r1s18.codam.nl     12:02:25        19:09:08        2021-10-12      f1r1s17.codam.nl          3:26:58        
13217034        Eustorgo        f1r1s18.codam.nl     12:02:25        19:09:08        2021-10-12      f1r1s17.codam.nl          3:15:45        
13211618        Karel           f1r3s13.codam.nl     13:06:07        18:30:49        2021-10-11      f1r3s12.codam.nl          4:51:04        

#####################################################
#                                                   #
#         Student that sat on infected host         #
#                                                   #
#####################################################

mairlijn        sat on f1r3s12.codam.nl (infected person session id = 13211161) after 17:35:57 hours passed.

################################################
#                                              #
#         Sessions of infected student         #
#                                              #
################################################

Sessions of hyilmaz
	-------------------------
	Session ID : 13219627
	Host       : f1r1s17.codam.nl
	Begin_at   : 15:42:10
	End_at     : 20:03:08
	Date       : 2021-10-12
	-------------------------
	Session ID : 13216479
	Host       : f1r1s17.codam.nl
	Begin_at   : 10:45:11
	End_at     : 15:18:10
	Date       : 2021-10-12
	-------------------------
	Session ID : 13211161
	Host       : f1r3s12.codam.nl
	Begin_at   : 10:39:34
	End_at     : 17:57:11
	Date       : 2021-10-11

################################################
#                                              #
#         Sessions of contact students         #
#                                              #
################################################

Sessions of Ji-Won
	-------------------------
	Session ID : 13212057
	Host       : f1r3s11.codam.nl
	Begin_at   : 15:06:09
	End_at     : 18:51:15
	Date       : 2021-10-11

Sessions of Thor    
	-------------------------
	Session ID : 13220952
	Host       : f1r1s16.codam.nl
	Begin_at   : 19:21:03
	End_at     : 21:51:03
	Date       : 2021-10-12
	-------------------------
	Session ID : 13219716
	Host       : f1r1s16.codam.nl
	Begin_at   : 15:54:02
	End_at     : 18:33:03
	Date       : 2021-10-12
	-------------------------
	Session ID : 13215438
	Host       : f1r1s16.codam.nl
	Begin_at   : 07:33:04
	End_at     : 15:30:31
	Date       : 2021-10-12

Sessions of Eustorgo
	-------------------------
	Session ID : 13217034
	Host       : f1r1s18.codam.nl
	Begin_at   : 12:02:25
	End_at     : 19:09:08
	Date       : 2021-10-12

Sessions of Karel   
	-------------------------
	Session ID : 13211618
	Host       : f1r3s13.codam.nl
	Begin_at   : 13:06:07
	End_at     : 18:30:49
	Date       : 2021-10-11
```

## Roadmap
1. Add evaluations (need more permissions for the 42 API).

## Contribute

If you find any bugs or problems with this program, feel free to file a new issue.

## License

[MIT](https://opensource.org/licenses/MIT)
