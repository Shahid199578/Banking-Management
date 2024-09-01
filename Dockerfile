FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install MySQL client
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Expose the port that Flask runs on
EXPOSE 5000
# Command to run on container start
# If using wait-for-it, adjust the CMD to include the wait-for-it script
CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["db:3306", "--", "flask", "run", "--host=0.0.0.0"]

