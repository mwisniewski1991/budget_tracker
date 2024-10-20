# Budget Tracker

## Goal
Create and maintain a web app for tracking household income and expenses.

## Description
From many years I track my income and expenses in Excel. It's time to automate this process.\
I decided to create simple web app where I input my income and expenses and see my current financial status.


## Stack
- Python
    - Flask
    - SQLAlchemy
    - WTForms
- DB
    - PostgreSQL
- Others:
    - Docker
    - Nginx

## Project Details

### Web App
![webapp gui](readme_utils/webapp_gui1.png)


### Database
Tables:
- owners
- accounts
- type_dict
    - dictionary tables with two types income and expense
- categories
- subcategories
- incexp_header
    - main information about bills (date, type (income or expense), owner, account, source)
- incexp_position
    - detailed information about bill (category, subcategory, amount, comment, connection)




## What I learnt
- Proper desing of the database schema is very, very, very importany. After start project changes are difficult to implement.