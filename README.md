# Restaurant Booking System CLI app(Milestone Project 3)
![](readme/mockup.png)

## Table of contents

* [Purpose](#purpose)

* [UX Design](#UX-Design)
  * [User Stories](#User-Stories)
  * [Structure](#Structure)

* [Features](#Features)
  * [Existing Features](#Existing-Features)
  * [Feature Considerations](#Feature-Considerations)

* [Technologies](#Technologies)
  * [Languages](#Languages)
  * [Programs, frameworks, libraries](#Programs,-frameworks,-libraries)

* [Deployment](#Deployment)

* [Testing](#Testing)
  * [User Story Testing](#User-Story-Testing)
  * [Manual Testing](#Manual-Testing)
  * [Unit Testing](#Unit-Testing)
  * [Automated Testing](#Automated-Testing)

* [Credits](#Credits)

# Purpose
This project is a CLI app - Restaurant [Booking System](https://my-wicked-booking-sys.herokuapp.com/). The app provides all the essential features, such as creating, editing and viewing reservations, additionally it allows to log in a member of staff and holds a database of staff members and customers, also it involves some basic data science to generates statictics reports.

The core purposes of the app:
- optimise a process of booking tables and keeping track of reservations.
- collect and store customers' data for future marketing purposes.
- provide staticstical insights into an enterprise current state.  

The website is built using Python, with little HTML and CSS, as a Milestone Project#3 for the Code Institute's Full Stack Developer course.  

[The live website is available here](https://my-wicked-booking-sys.herokuapp.com/)
___
# UX Design
## User stories
### As a **business owner**

- I want to manage reservations eficiently.
- I want to keep track of history.
- I want a staff database, and ability to see who added the booking, so in case something about a reservation is unclear, it could be clearly confirmed with a person who added it, without spending time trying to find out who it was.
- I want a customers database for marketing purposes
- I want  to receive insights from statistic reports for business decisions.


### As a **first time user**

- I want to understand easily how to use the app.
- I want to be able to understand where in the program I am and what options are available.
- I want to be able to go to the start menu at any point or go back if I chose the wrong option.
- I want to easily access contact information of another members of staff.
- I want to easily access customers' information to confirm a reservation or make changes.
- I want to be able to easily find, add, confirm, reschedule and cancel a reservation.
- I want to be remided of bookings to confirm.


### As a **frequent user**

- I want to be able to navigate fast.
- I want to be sure my account is secured with password.
- I want to be able to change my password.

___

## Structure

![](readme/structure.png)

Throughout all the app the user is guided with clear instructions and can return one step back or to the start menu at any point.
___

# Features
## Existing Features

- **Log in**

Allows the user to log in by checking a password or create a new user. The data of exising users is stored in Google Spreadsheets. A member od staff record consisits of a name, a passsword and a contact(phone), in case there is a need to contact any member of staff to clarify something about bookings they added.

- **Start Menu**

The Start Menu is an entry point to the program, it allows to choose between 3 main sections: Bookings, Customers and Staff. At any point of the ptogram further on the user can go straight back to the Start Menu if they need.

- **Bookings Menu**

The Bookings Menu includes options related to bookings: View bookings, Add booking and Edit bookings.

- **View Bookings Menu**

The View Bookings Menu includes four options of viewing: "Today", "Tomorrow", "a Week" and "All time". Bookings for "Today" are printed in a special format with signs "\/", if a booking was confirmed, and "--", if a booking needs to be confirmed, and a customer's contact below to do so. Bookings data is obtained from Google Spreadsheet db.

- **Add Booking**

This section requests to input a customer's name, if the customer doesn't exist, it offers to create a new customer (y/n choice) or try to search a customer by name again. Having found or created a customer, Add Booking function requests a date, time and a number of people and writes it to Google Spreadcheets. The booking entry also has an attribute "created by", so even if any doubts or questions regarding a booking arise, it is possible to easily contact a person created it for clarification.

- **Edit Bookings**

The Edit Bookings Menu offers to Confirm, Reschedule or Cancel a booking. 

- **Confirm**

The Confirm function picks all bookings for today that are not confirmed and prints them out one by one with a customer's contact information. Having contacted a customer the user can choose between "Confirmed" (if the booking is successfully confirmed), "Skip"(if they weren't able to contact the customer) or "Cancel"(if the booking was cancelled as a result of contacting the customer).

- **Reschedule**

The Reschedule function allows to change any aspect of the booking: date, time and number of people.

- **Cancel**

The Cancel function cancels a chosen booking. A cancelled booking remains in the database for analitics purposes, it receives an attribute "cancelled". 

- **Customers Menu**

The Customers Menu includes options related to customers: View customers and Stats. A new customer function is not on the menu, bacause there is no need to create a customer without a booking, therefore it gets created with a new booking.

- **View Customers**

Allows to search customers by name or view the full list of existing customers if needed.

- **Stats**

Generates a pdf report about basic business data, such as Age groups of customers, number of bookings per customer and a percentage of cancelled bookings. It is saved to Google Drive and could be accessed by the link below the terminal.

- **Staff Menu**

The Staff Menu includes options related to customers: View Staff Info and Edit Staff Info.

- **View Staff Info**

Allows to search members of staff by name or view the full list if needed.

- **Edit Staff Info**

Allows to change the user's password or a contact number, to make sure contact information is always up to date.

- **Data Validation**

Date, time, phone, email and number data is validated throughout the app to ensure only correct format valid data in written to the database.

- **Database**

Google Spreadsheet API is used as a database for the app. There are three worksheets to organise data: "bookings", "customers" and "staff".

## Feature Considerations

### Email or SMS reminders

Customers will be able to receive reminders of upcoming bookings by a chanel of their choice.

### Congratulations

Customers birthdates are collected so birthday greetings could be sent, as well as promo offers for the date. Unfortunately, it was not possible under Heroku limitations. However could be achieved by setting up [IronMQ](https://elements.heroku.com/addons/iron_mq) service.

# Technologies
## Languages
- Python, HTML, CSS
## Programs, frameworks, libraries
- [Gitpod](https://gitpod.io/) IDE to develop the app.
- [GitHub](https://GitHub.com/) to host the source code 
- [Heroku](https://www.heroku.com/) to deploy and host the live app.
- Git to provide version control (to commit and push code to the repository). 
- [Google Spreadsheets API](https://developers.google.com/sheets/api) to store data.
- [Google Drive](https://developers.google.com/drive) to write an app to process requests to Spreadsheets.
- [Pandas](https://pandas.pydata.org/) and [Matplotlib](https://matplotlib.org/) for statistic reports.
- [Pytest](https://docs.pytest.org/en/7.1.x/) Pytest for unit-testing.
- [TinyJPG](https://tinyjpg.com/) to optimise images for readme. 
- [Favicon.io](https://www.favicon.io/) to create the website favicon.
- [Techsini](https://tecnisih.com) to create the Mockup image in this README.
- [W3C HTML Markup Validator](https://validator.w3.org/) to validate HTML code.
- [W3C Jigsaw CSS Validator](https://jigsaw.w3.org/css-validator/) to validate CSS code.
- [Markdown Tables Generator](https://www.tablesgenerator.com/) to generate tables for the readme file.
- [PEP 8](http://pep8online.com/) to validate python code.
- Code Institute's Python Template to generate the workspace for the project.
___

# Deployment

## Heroku

### Steps for deployment:

1. Fork or clone this repository.
2. Log into your account on Heroku.
3. Create a new Heroku app.
4. Navigate to `Settings` tab.
5. Set up config vars.
5. Set the buildbacks to `python` and `NodeJS` in that order.
6. Configure GitHub integration in the `Deploy` tab.
6. Click `Deploy branch`.