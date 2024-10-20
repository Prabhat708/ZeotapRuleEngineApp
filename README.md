# Zeotap Rule Engine App
ZeotapRuleEngineApp is a Django-powered application that allows users to create, manage, and apply rules for eligibility checks based on inputs such as age, salary, department, and experience. The app is designed to be flexible, supporting both predefined rules and custom rule creation, making it suitable for various rule-based decision-making processes.

# Features
Add and Manage Custom Rules: Define your own eligibility rules or use predefined ones.
Flexible Input System: Users can input details like age, salary, department, and experience, and evaluate them against rules.
Eligibility Checks: Run custom or predefined rules to determine eligibility based on the provided data.
Rule Storage: Rules are stored in a database for reuse, and new rules can be added dynamically.
Simple Web Interface: The app provides an intuitive web interface to add new rules, modify existing ones, and run checks.
# Live Demo
Check out the live version of the app here: [Zeotap Rule Engine App](https://prabhat21.pythonanywhere.com/).

# Project Structure
The project follows the typical Django MVC (Model-View-Controller) pattern. Below is an overview of the project structure:

graphical
ZeotapRuleEngineApp/
│
├── db.sqlite3             # SQLite database to store rules and user input
├── manage.py              # Django's management script
├── ruleengine/            # Main Django app
│   ├── migrations/        # Django migrations for database changes
│   ├── static/            # Static files (CSS, JS)
│   ├── templates/         # HTML templates for web pages
│   ├── models.py          # Database models for rules and inputs
│   ├── views.py           # Views to handle rule logic and render templates
│   ├── forms.py           # Django forms for data input and rule creation
│   ├── urls.py            # URL routing for the application
│   └── admin.py           # Admin panel configuration
│
└── requirements.txt       # List of dependencies

# How to Use
# Adding a Rule:

Navigate to the "Add Rule" section.
Define the rule conditions (e.g., age > 25 and salary > 50000).
Save the rule to the database for future use.
# Checking Eligibility:

Enter user data (age, salary, department, experience).
Select a predefined rule or a custom rule you’ve added.
Run the eligibility check to see if the user qualifies based on the rule.

# Technologies Used
Backend: Python, Django
Database: SQLite
Frontend: HTML/CSS (with Django templates)
Hosting: PythonAnywhere (live demo)
