# Capstone (Final Project)

## **CS50's Web Programming with Python and JavaScript**

This is the final project. It is an amazon like application where vendors(from giant to small) and customers can participate in the trade.
Basic functionsalities included in this application:
* users and vendors have a separate login and register functionality
* users can subscribe to vendors
* vendors can add, edit and delete items
* vendors can edit their profile
* users can search through the website for either vendors or items
* users are presented with related items when viewing an item
* users can comment on items
* any user(anyone with a business idea) can open  avendor account
* there's a verified icon on verified vendors
* users can access a list of vendors. additionally in the list of vendors there's a filter functionality which filters vendors by vendor type, verified or not and subscribed or not

This Project is sufficiently distinct from previous ones. Previous projects focus on a simpler and less number of functionalities while this project constitutes several more or less complex functionalities like searching through the application for items and vendors. Additionally functionalities like **query result filtering** and listing items that are **trending**, **new**, **subscribed** and **upcoming** makes it more complex because they require a well designed database and smart queries.

This web application uses **Django** framework for backend with 7 models and **JavaScript** for frontend.

This web application is mobile responsive and uses bootstrap framework.

This project's source code includes 2 folders, a manage.py file which manages the whole application and an **sqlite database file** which holds the database. Below are the **main files** under those folders.

negade/:
* admin.py -> manages the content of the django admin panel.
* models.py -> stores the models of the application(7 models).
* urls.py -> stores the urls under this specific application.
* views.py -> A view function, or view for short, is a Python function that takes a Web request and returns a Web response([source](https://docs.djangoproject.com/en/3.1/topics/http/views/)). This file contains all the view functions that will later be requested to get a respective response.
* the *static* and *templates* subfolders are for HTML and CSS source files.

static/negade/:
* styles.css -> the styling code of the application
* index.js -> this is the front end source code where requests are made and responses are taken. And mainly it controls the client side activity of the application

templates/negade/:
* add_item.html -> contains an HTML form for adding a new item.
* edit_item.html -> contains an HTML form for editing an existing item.
* edit_page.html -> contains an HTML form for editing a vendor's home page and profile.
* index.html -> contains the structure of the applications main page holding list of items.
* item.html -> for displaying an item with its description, item's image, related items and related informations.
* layout.html -> contains main skeleton of the application from which all HTML files in this subdirectory extend.
* login.html -> contains users login form.
* register.html -> contains users register form.
* search.html -> for displaying search results.
* vendor_home.html -> for displaying vendors home page which contains posted items under it, link to add item page, link to edit profile page.
* vendor_login.html -> contains vendors login form.
* vendor_register.html -> contains vendors register form.
* vendor.html -> contains the structure of vendors official page with items under that vendor.
* vendors.html -> for displaying list of vendors with their description. additionally contains filter button to filter vendors list as users wish.

capstone/:
* contains the application configuration files like *settings.py* and *urls.py*.

#### How to run the application

* open cmd or terminal
* change directory to the project folder
* run this command -> `python manage.py runserver`
* open a browser 
* then go to the url -> 127.0.0.1:8000 (it is written on the terminal when server is started)