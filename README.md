
![amfoss-cms-cover](https://user-images.githubusercontent.com/21276922/51844359-12628580-233b-11e9-891a-d4d826bd1d6e.png)

# amFOSS CMS

amFOSS Club Management System (CMS) is django-based web-app which lays framework for the amfoss website, the amfoss webapp, and the amfoss app. 


## :minidisc: Installation Instructions
The portal is primarily a django based application, and to set it up we require to have 
python environment with django and other project dependencies installed. Though one can
work with the project without an virtual environment,  it is recommended to use one so 
as to avoid conflicts with other projects.

1. Make sure that you have `Python 3` and `pip` installed. 
   Install `virtualenvwrapper`, and add it to your terminal path.
   
    ```
       $ sudo pip install virtualenvwrapper
       $ echo 'export WORKON_HOME=~/Envs' >> ~/.bashrc
       $ echo 'mkdir -p $WORKON_HOME' >> ~/.bashrc   
       $ echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc   
    ```
    
2. Clone the repository, and create a virtual environment for the project, 
   and work on the newly set up environment.
   
    ```
        $ git clone <repository-url>
        $ cd amfoss-portal
        $ mkvirtualenv --python=python3 amfoss
        $ workon amfoss
    ```
    
3. Install the project dependencies from `requirements.txt`
    ```
        $ pip install -r requirements.txt
    ```

You have now successfully set up the project on your environment.

### After Setting Up
From now when you start your work, run ``workon amfoss`` inside the project repository and you can work with the django application as usual - 

* `python manage.py migrate` - set up database
* `python manage.py createsuperadmin` - create admin user
* `python manage.py runserver`  - run the project locally

*Make sure you pull new changes from remote regularly.*


## :rocket: Data Models

### :tada: Activities
The activity app tracks the activities of the club members.

1. **Certificates** - carries certificates recieved by club members, also allows to upload them as attachments.
2. **Courses** - records courses completed by club members, includes link to certificate.
3. **Honours** - records achievements and honours recieved by club members, includes link to project, certificate.
4. **Projects** - holds projects of the club, club teams and club members
5. **Publications** - records publications made by club members
6. **Talks** - records talks given by club members

### :postbox: Blog
The blog app manages the blog of the club

1. **External Posts** - manages external posts published by club members by including them through links
2. **Posts** - contains posts published by club members, with tags and categories.

### :pencil: Pages
The pages app manages the content and templates for the foss-website. 

*Opitionally, it can also be used as a fallback to amfoss-webapp. It can used to server a minimal read-only version of the amfoss-webapp*

### :girl: Members
The members app manages the profile and data of the club members

1. **Attendance** - records and tracks attendance of club members inside FOSSLab
2. **Leave Records** - records and manages the leave requests of club members
3. **Mentor Groups** - manages mentor-menteee relationship of club members
4. **Profiles** - manages the member profile
5. **Responsibilities** - manages the various responsibilities held by a group of members
6. **Teams** - manages the various internal teams inside the club

### :incoming_envelope: Status
The status app manages the reporting system in the club

1. **Status** - holds status updates posted by members, under different threads, for various subjects. 
2. **Tasks** -  records and accounts different tasks assigned to the club members 

## :satellite: Integrations

1. **Attendance Module** - the amFOSS attendance module is a raspberry-pi which live records the attendance of club members when they are in the FOSSLab. The AmFOSS CMS fetches attendance details from it and logs it.
2. **Telegram Bot** - the amFOSS Telegram Bot is the bot assistant of the AmFOSS Telegram group. The AmFOSS CMS triggers the bot to send notifications, statistics etc. to the group.
3. **Daily Status Updates** - all members of the club are required to send status updates daily ellaborating the work they did to a automatically generated status-update thread in the Google Groups. The AmFOSS CMS fetches the status updates, and logs them.
4. **GitHub** - Integrates with GitHub to actively track the FOSS contributions made by club members

## :wrench: Tech Stack

* **Framework:** Django 2.1, Python 3
* **API:** Graphene (GraphQL), Graphene-JWT

## :gem: Contributors
Developed with :hearts: by the amFOSS WebTeam from 2018.

1. [Ashwin S Shenoy](https://github.com/aswinshenoy) - Core Developer, Maintainer

Contributors are welcomed :)

## :black_nib: License
This repository is licensed under  GNU General Public License V3. Though it was tailor-made for amFOSS, you are welcome to adapt it, make it yours. Just make sure that you credit us too.
