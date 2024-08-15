# Flask App with MySQL

This project demonstrates a Flask application connected to a MySQL database, all containerized using Docker. It provides a simple web interface for managing data stored in MySQL.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [Database Initialization](#database-initialization)
- [Build and Start the Containers](#build-and-start-the-containers)
- [Running the Application](#running-the-application)
- [Stopping and Removing Containers](#stopping-and-removing-containers)
- [License](#license)

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shahid199578/Banking-Management.git
   cd Banking-Management
   ```

2. For installation instructions, please refer to [docker-compose.md](docker-compose.md).

3. Ensure Docker and Docker Compose are installed on your system. You can follow the [official Docker installation guide](https://docs.docker.com/get-docker/) if needed.

## Docker Setup

This project includes a `docker-compose.yml` file to define and run the application and MySQL as services.

## Environment Variables

The application requires the following environment variables to connect to the MySQL database:

- `MYSQL_HOST`: The hostname of the MySQL server (default is `db`).
- `MYSQL_DATABASE`: The name of the database (default is `flask_app`).
- `MYSQL_USER`: The MySQL user (default is `root`).
- `MYSQL_PASSWORD`: The MySQL user password (set to `Shahid`).
  
> Note: If you want to change the MySQL user password, you should also need to update the password in the following line in app/__init__.py:
>
> ```python
> app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Shahid@db/flask_app'
> 
These variables are defined in the `docker-compose.yml` file.

## Database Initialization

The `create_database_and_tables.sql` script is automatically executed when the MySQL container starts for the first time.

## Build and Start the Containers

To build and start the Docker containers, run:

```bash
docker-compose up --build -d
```

This command will create and start the services defined in the `docker-compose.yml` file, rebuilding the images if there have been any changes.



## Running the Application

Once the containers are up and running, the Flask application will be accessible at:

```
http://localhost:80
```

You can access the application in your web browser.

## Stopping and Removing Containers

To stop and remove the containers, run:

```bash
docker-compose down
```

This command will stop and remove the running containers along with the associated networks.
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

