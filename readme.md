# Flask App with MySQL

This project demonstrates a Flask application connected to a MySQL database, all containerized using Docker. It provides a simple web interface for managing data stored in MySQL.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [Stopping and Removing Containers](#stopping-and-removing-containers)
- [Database Initialization](#database-initialization)
- [License](#license)

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask_app.git
   cd flask_app
   ```

2. Ensure Docker and Docker Compose are installed on your system. You can follow the [official Docker installation guide](https://docs.docker.com/get-docker/) if needed.

## Docker Setup

This project includes a `docker-compose.yml` file to define and run the application and MySQL as services.

### Build and Start the Containers

To build and start the Docker containers, run:

```bash
docker-compose up --build -d
```

This command will create and start the services defined in the `docker-compose.yml` file, rebuilding the images if there have been any changes.

## Running the Application

Once the containers are up and running, the Flask application will be accessible at:

```
http://localhost:5000
```

You can access the application in your web browser.

## Environment Variables

The application requires the following environment variables to connect to the MySQL database:

- `MYSQL_HOST`: The hostname of the MySQL server (default is `db`).
- `MYSQL_DATABASE`: The name of the database (default is `flask_app`).
- `MYSQL_USER`: The MySQL user (default is `root`).
- `MYSQL_PASSWORD`: The MySQL user password (set to `Shahid`).

These variables are defined in the `docker-compose.yml` file.

## Stopping and Removing Containers

To stop and remove the containers, run:

```bash
docker-compose down
```

This command will stop the running containers and remove them along with the associated networks.

## Database Initialization

The `create_database_and_tables.sql` script is automatically executed when the MySQL container starts for the first time. Make sure this script contains the necessary SQL commands to create your database schema and any initial data required by the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
