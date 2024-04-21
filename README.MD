# Parking Solution App

This application is designed to address the limited parking availability in Tirana, Albania, by facilitating communication between drivers. It allows users to register their cars and mark the location where they are parked. If a car blocks another, the affected driver can easily notify the blocker through the app, helping to resolve parking conflicts efficiently.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before setting up the project, you need to have Python installed on your computer. Additionally, you'll need a virtual environment to manage the project's dependencies.

### Installation

Follow these steps to set up and run the application:

#### Database Setup

- Create a database schema using the SQL script provided in `blocked_car.sql`. This script will give you the schema on **My SQL.**
- Change the name of the database *db_name*  on the files `car.py` and `user.py` with the name you save your database.

#### Environment Setup

1. Open a terminal in the main folder of the project.
2. Set up a virtual environment:
   ```bash
   python -m venv venv

3. Activate the virtual environment:
   
   3.1. On Windows:

       .\venv\Scripts\activate

   3.2. On Unix or MacOS:

       source venv/bin/activate


4. Install the required libraries using pip:

   ```bash
    pip install -r requirements.txt

5. Run the Application
   
   Start the application by running:
   ```bash
    python server.py


### Usage

Once the application is running, you can register your car and mark other cars as blocked if they obstruct your vehicle. This allows other drivers to receive notifications directly from the app when their car blocks another, facilitating quick resolution of parking issues.