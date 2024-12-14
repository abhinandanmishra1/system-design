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
   \`\`\`
   sudo mysql_secure_installation
   \`\`\`
   Follow the prompts to set a root password and other security settings.

4. Log in to MySQL:
   \`\`\`
   mysql -u root -p
   \`\`\`
   Enter the password you set during the secure installation.

5. Create a new user for your project:
   \`\`\`sql
   CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON *.* TO 'your_username'@'localhost';
   FLUSH PRIVILEGES;
   \`\`\`
   Replace 'your_username' and 'your_password' with your desired credentials.

6. Exit MySQL and clone this repository:
   \`\`\`
   git clone https://github.com/yourusername/social-media-db.git
   cd social-media-db
   \`\`\`

7. Install Python dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

8. Set up the database:
   \`\`\`
   mysql -u your_username -p < sql/init.sql
   mysql -u your_username -p social_media < sql/vertical_partitioning.sql
   mysql -u your_username -p social_media < sql/horizontal_partitioning.sql
   \`\`\`

## Usage

1. Update the database connection details in the Python files (`src/*.py`) with your MySQL username and password.

2. Run the Python scripts to interact with the database:
   \`\`\`
   python src/basic_implementation.py
   python src/vertical_partitioned_db.py
   python src/sharded_db.py
   \`\`\`

## Running the FastAPI Server

1. Make sure you have installed all the required dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

2. Run the FastAPI server:
   \`\`\`
   python src/main.py
   \`\`\`

3. The server will start running on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

4. Use the following endpoints:
   - POST `/posts`: Create a new post
   - GET `/posts/{post_id}`: Retrieve a specific post by ID

Example usage with curl:

Create a new post:
\`\`\`
curl -X POST "http://localhost:8000/posts" -H "Content-Type: application/json" -d '{"user_id": 1, "content": "Hello, World!", "media_url": "http://example.com/image.jpg", "media_type": "image"}'
\`\`\`

Retrieve a post:
\`\`\`
curl "http://localhost:8000/posts/1"
\`\`\`

## Project Structure

- `sql/`: Contains SQL scripts for setting up the database and implementing partitioning.
- `src/`: Contains Python scripts for interacting with the database.
- `requirements.txt`: Lists the required Python packages.
- `README.md`: This file, containing setup and usage instructions.

## Best Practices and Considerations

1. Always use transactions when inserting across multiple tables.
2. Implement proper error handling and rollback mechanisms.
3. Consider using connection pools for better performance.
4. Implement proper monitoring and logging.
5. Use appropriate indexes for frequent queries.
6. Consider implementing a caching layer (e.g., Redis) for frequently accessed data.
7. Implement proper backup strategies for each shard.
8. Consider using proxy layers for routing queries to appropriate shards.

## Troubleshooting

If you encounter any issues during setup or execution, please check the following:

1. Ensure MySQL is running: `sudo systemctl status mysql` (Ubuntu) or `brew services list` (macOS)
2. Verify your MySQL user has the necessary permissions
3. Check that the database and tables were created successfully
4. Ensure your Python environment has all required packages installed

For further assistance, please open an issue in the GitHub repository.

