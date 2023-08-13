# Use the base image
FROM python:latest

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set environment variables
ENV DB_NAME \
    DB_USER \
    DB_PASSWORD \
    DB_HOST \
    DB_PORT

# Install system dependencies
RUN apt-get update && apt-get install -y nginx

# Create a directory for your app
RUN mkdir /app

# Copy your application files
COPY ./app /app
COPY entrypoint.sh /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN python3 -m pip install Pillow
RUN pip3 install -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x ./entrypoint.sh

# Copy the Nginx configuration file
COPY ./nginx/nginx.conf /etc/nginx/sites-available/default

# Expose the port
EXPOSE 8000

# Start the application using the entrypoint script
CMD ["./entrypoint.sh"]
