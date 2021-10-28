# Book Organizer
#### Video Demo: https://youtu.be/tu7T7vU5cFk
## Description:
BookOrganizer helps you keeping track of your read books and displays information about them. After creating your personal account you can start adding books to your online library. Various filters aid you if you have a longer reading history. Information you can enter about your read book when adding it to your library:
- title
- author
- pages
- rating
- month and year that you've read the book in

You can also search for specific books within your library if you want to lookup the rating for example.

## Setup Project in Editor
--Process may vary--

1. Install venv `python3 -m pip install virtualenv`
2. Setup venv `python3 -m virtualenv venv`
3. Activate venv `/ProjectDir/venv/Scripts/activate.bat`
4. Install Required Packages `pip install -r requirements.txt`

## Running the Application
1. Set Flask Application `set FLASK_APP=application.py`
2. Run `flask run`

## Features
- Login System (using a SQLite Database)
- Tracking your books and page-count
- various managing tools for your library

## Technologies
- Backend:
    - Flask
    - SQLite3

- Frontend:
    - TailwindCSS