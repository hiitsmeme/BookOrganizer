# Book Organizer
#### Video Demo: https://youtu.be/tu7T7vU5cFk
## Description:
BookOrganizer helps you keeping track of your read books and displays information about them. 

After creating your personal account you are directed to the dashboard (index.html). Here general information about your account is displayed. The main menu is on the left (layout_home.html). 

Clicking on the library button will direct you to your online library (library.html) where all the books you've added will be listed in descending order. In the library the user has the option to filter the books that should be displayed. Filter options include the rating, the month and the year the user has read the book in. Of course you can delete a book from the library as well. 

Clicking the add button will direct you to a form (add.html) where you can enter the information of a new book you want to add to you library.You can enter various information about a book you want to add to your library. The most important ones are the title, author, page count (which will update on your dashboard) and your rating of the book.

Clicking on the search button will lead you to a form where you can search for specific books within your library if you want to lookup the rating for example. You are able to search by title or author or both.

Technologies
- Backend:
    - Flask
    - SQLite3

- Frontend:
    - TailwindCSS

Features
- Login System (using a SQLite Database)
- Tracking your books and page-count
- various managing tools for your library


# Setup Project in Editor
--Process may vary--

1. Install venv `python3 -m pip install virtualenv`
2. Setup venv `python3 -m virtualenv venv`
3. Activate venv `/ProjectDir/venv/Scripts/activate.bat`
4. Install Required Packages `pip install -r requirements.txt`

# Running the Application
1. Set Flask Application `set FLASK_APP=application.py`
2. Run `flask run`
