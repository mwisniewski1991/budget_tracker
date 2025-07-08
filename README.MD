# Budget Tracker

## Overview

A web application for tracking household income and expenses, designed to replace manual Excel-based financial tracking with an automated solution.

## Goal

Create and maintain a web app for tracking household income and expenses.

## Description

For many years, I've been tracking my income and expenses in Excel. It's time to automate this process. I decided to create a simple web app where I can input my income and expenses and see my current financial status.

## Tech Stack

### Backend
- **Python** - Main programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **WTForms** - Form handling and validation

### Database
- **PostgreSQL** - Primary database

### Development & Deployment
- **Pytest** - Testing framework
- **Docker** - Containerization
- **Nginx** - Web server
- **GitHub Actions** - CI/CD pipeline

## Project Structure

### Web Application
![Web Application GUI](readme_utils/webapp_gui1.png)

### Database Schema

The application uses the following database tables:

- **owners** - User accounts and ownership information
- **accounts** - Financial accounts (bank accounts, cash, etc.)
- **type_dict** - Dictionary tables with two types: income and expense
- **categories** - Main expense/income categories
- **subcategories** - Subcategories within main categories
- **incexp_header** - Main information about transactions (date, type, owner, account, source)
- **incexp_position** - Detailed transaction information (category, subcategory, amount, comment, connection)

## Getting Started

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 16.6 or higher
- Docker and Docker Compose (optional, for containerized setup)

### Installation & Setup

#### Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budget_tracker
   ```

2. **Create environment file**
   ```bash
   cp website/.env_example website/.env
   ```
   
   Edit `website/.env` file and update the database connection string:
   ```
   FLASK_SQLALCHEMY_DATABASE_URI=postgresql://user:password@database:5432/budget_tracker
   FLASK_DEFAULT_OWNER_ACCOUNT_IDS=1_01
   FLASK_SECRET_KEY=your_secret_key_here
   FLASK_DEFAULT_RESULTS_LIMIT=50
   ```

3. **Start the application using Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Open your browser and navigate to `http://localhost:81`
   - The application will be available through Nginx proxy
   - As a first step, add a new Owner. Next, create a new Account, and subsequently add an Income or Expense entry.