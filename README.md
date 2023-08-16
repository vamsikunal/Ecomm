# Ecomm Project

Ecomm is a comprehensive e-commerce website that brings together a rich set of features to create a seamless online shopping experience. Built with a user-friendly interface and robust functionality, Ecomm covers everything from product discovery to secure checkout. Moreover, it's been deployed using Amazon Elastic Container Service (ECS) and powered by an efficient CI/CD pipeline managed through Jenkins.

## Table of Contents

- [Description](#description)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Description

This project is built on the Django framework, focusing on backend development and showcasing a comprehensive set of features. These include robust user account management encompassing phone and email verification, password reset, and a versatile multi-address system. It also integrates a secure payment gateway, cart and favorites functionality, and a review and rating system for user feedback. Furthermore, the project utilizes external APIs to enhance its capabilities, demonstrating a holistic approach to e-commerce and user engagement.

The entire Django application has been containerized using a Dockerfile. It is seamlessly integrated with the Jenkins server, which employs the Jenkinsfile. This setup enables the automation of GitHub updates, triggering the build and subsequent pushing of the Docker image to the Elastic Container Registry. Finally, the image is automatically deployed to an ECS cluster through task execution, completing a streamlined deployment process.

## Getting Started

### Prerequisites

- Docker installed on the host system.
- Mysql database server (or Any database engine).

#### Only for complete CI/CD and Cloud setup
- AWS CLI on local system
- Jenkins setup with master and EC2-based slave configuration.
- Slave node configured with Docker and AWS CLI with proper IAM access.

### Local usage
####  If you want to run project on local system

1. Build docker image
```
docker build -t <image_name>:latest .
```

2. Run the container with this image
```
docker container run -p 8000:8000 -e DB_NAME=<Database_Name> -e DB_PASSWORD=<password> -e DB_USER=<user> -e DB_HOST=<host> <image_name>:latest
```

3. Container will be running at.
```
localhost:8000
``` 

#### If you want to run project with complete CI/CD and cloud support

> Host on ECS 

1. Create a ECR registry

2. Build docker image locally
```
docker build -t <image_name>:latest .
```
3. Tag the image with ecr registry name. (PS - aws cli should be configured on local system)
```
docker tag <image_name>:latest <erc_repo_link>:latest.
```
4. Push the image on AWS ECR.
```
docker push <erc_repo_link>:latest.
```
5. Set up an ECS cluster for container management.

6. Create an ECS task on the console, utilizing an ECR image and providing essential environment variables are
```  
DB_USER, DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT(optional, default=3306), DB_ENGINE(optional, default = mysql)
```
7. Deploy the ECS task as a service on the ECS cluster for container execution and management.

> CI/CD automation with jenkins

1. Start by forking this repository and setting up your GitHub account credentials in Jenkins.

2. In the Jenkinsfile, update '<GITHUB_URL>' with the URL of your forked repository.

3. Configure text credentials in Jenkins to store ECR_REGISTRY, ECR_REGION, ECS_CLUSTER, ECS_TASK_DEFINITION, and ECS_SERVICE_NAME.

4. Create a Jenkins app pipeline, specifying the GitHub repository and the target branch.

5. For the build trigger you can use option "Github hook trigger for GITScm polling" for automatic build task for every push on github repo.

6. Configure github repo for webhook - select webhook on repo setting and create webhook, in payload url enter '<Jenkins_master_url>/github-webhook/' and select content type json and add the webhook.

7. Under the pipeline section in definition select Pipeline script form SCM, select SCM as git and provide all details.

8. Save the pipeline app.

#### AWS secret manager for database credential 

When specifying an ECS task, the inclusion of hard-coded database credentials gives rise to security concerns. To address this, AWS Secret Manager can be employed for the secure storage of these database credentials. 

* For that while creating RDS database check the option "Manage master credentials in AWS secrets manager" It will generate a secret in AWS secrets manager

* To get access of AWS secrets, manually add the JSON permissions to the task execution role (ECSTaskExecutionRole).

* In json add ACtion : "secretsmanager:GetSecretValue"
and in Resources : "arn_of_aws_secret_key"  
For more information : [Sensitive data form AWS Systems Manager](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-ssm-paramstore.html)

* In task definition add environment variable  (ps - Still need to pass DB_HOST ans DB_NAME as usual)
    ```
    key = 'DB_CRED', value type = 'ValueFrom', value = 'arn_of_aws_secret_key'
    ```

## Contributing
I'm open to contributions from the community. You can contribute by:
- Enhancing HTML and CSS elements
- Adding additional testing scripts
- Optimizing database transition processes
- Anything else you think can improve the project"


