# Ecomm Project

Ecomm is a comprehensive ecommerce website that brings together a rich set of features to create a seamless online shopping experience. Built with a user-friendly interface and robust functionality, Ecomm covers everything from product discovery to secure checkout. Moreover, it's been deployed using Amazon Elastic Container Service (ECS) and powered by an efficient CI/CD pipeline managed through Jenkins.

## Table of Contents

- [Description](#description)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Description

This project is built on the Django framework, focusing on backend development and showcasing a comprehensive set of features. These include robust user account management encompassing phone and email verification, password reset, and a versatile multi-address system. It also integrates a secure payment gateway, cart and favorites functionality, and a review and rating system for user feedback. Furthermore, the project utilizes external APIs to enhance its capabilities, demonstrating a holistic approach to ecommerce and user engagement.

The entire Django application has been containerized using a Dockerfile. It is seamlessly integrated with the Jenkins server, which employs the Jenkinsfile. This setup enables the automation of GitHub updates, triggering the build and subsequent pushing of the Docker image to the Elastic Container Registry. Finally, the image is automatically deployed to an ECS cluster through task execution, completing a streamlined deployment process.

## Getting Started

### Prerequisites

- Docker installed on the host system.
- Mysql database server (or Any database engine).

#### Only for complete CI/CD setup
- Jenkins setup with master and EC2-based slave configuration.
- Slave node configured with Docker and AWS CLI with proper IAM access.

### Local usage
> If you want to run project on local system

1. Build docker image
```
docker build -t <image_name>:latest .
```

2. Run the continer with this image
```
docker container run -p 8000:8000 -e DB_NAME=<Database_Name> -e DB_PASSWORD=<password> -e DB_USER=<user> -e DB_HOST=<host> <image_name>:latest
```

3. Container will be running at
```
localhost:8000
``` 

> If you want to run project with compler CI/CD


## Contributing
I welcome contributions from the community. To contribute for:
- HTML and CSS enhancments
- Add more testing scripts 
- Database transition optmization
- anything



