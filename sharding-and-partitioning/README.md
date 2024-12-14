# Social Media Database Project

This project demonstrates various MySQL partitioning techniques for a social media application.

## Prerequisites

- MySQL Server
- Python 3.7+

## Setup Instructions

1. Install MySQL Server:
   - Ubuntu: `sudo apt-get update && sudo apt-get install mysql-server`
   - macOS (using Homebrew): `brew install mysql`
   - Windows: Download and install from the official MySQL website

2. Start the MySQL service:
   - Ubuntu: `sudo systemctl start mysql`
   - macOS: `brew services start mysql`
   - Windows: MySQL service should start automatically after installation

3. Secure your MySQL installation:
   ```
   sudo mysql_secure_installation
   ```
   Follow the prompts to set a root password and other security settings.

4. Log in to MySQL:
   ```
   mysql -u root -p
   ```
   Enter the password you set during the secure installation.

5. Create a new user for your project:
   ```sql
   CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON *.* TO 'your_username'@'localhost';
   FLUSH PRIVILEGES;
   ```
   Replace 'your_username' and 'your_password' with your desired credentials.

6. Exit MySQL and clone this repository:
   ```
   git clone https://github.com/yourusername/social-media-db.git
   cd social-media-db
   ```

7. Set up the database:
   ```
   python src/database/run.py
   ```

## Usage

1. Copy the `.env.local` file and create a `.env` file.
2. Add your credentials to the `.env` file.

## Running the FastAPI Server

1. Make sure you have installed all the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```
   uvicorn src.main:app --reload
   ```

3. The server will start running on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Project Structure

- `src/`: Contains Python scripts for interacting with the database.
  - `src/database`: Contains `run.py` for setting up database and `remove.py` for deleting all databases.
  - `scr/controllers`: Contains implmentation of **Sharding** and **Vertical Partitioning**.
  - `src/routes`: All the routes are declared here.
- `requirements.txt`: Lists the required Python packages.
