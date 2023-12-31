pipeline {
    agent {
        label 'jenkins-slave'
    }

    environment {
        ECR_REGISTRY = credentials('ecr_registry')
        ECR_REGION = credentials('ecr_region')
        ECS_CLUSTER = credentials('ecs_cluster')
        ECS_TASK_DEFINITION = credentials('ecs_task_definition')
        ECS_SERVICE_NAME = credentials('ecs_service_name')
    }

    stages {
        stage('gitclone') {
            steps {
                git branch: 'main', credentialsId: 'github_credentials', url: '<GITHUB_URL>'
            }
        }

        stage('Connect ECR'){
            steps {
                // Connect to ECR
                sh 'aws ecr get-login-password --region ${ECR_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ecomm:latest .'
            }
        }

        stage('Run Python Tests') {
            steps {
                sh 'docker container run -e DB_NAME=ecomm.sqlite3 -e DB_ENGINE=django.db.backends.sqlite3 --name web -p 8000:8000 ecomm:latest'
                sh 'docker container exec web python manage.py test'
                sh 'docker contianer stop web'
                sh 'docker container rm web'
            }
        }

        stage('Push') {
            steps {
                // Push the image to ECR
                sh 'docker tag ecomm:latest ${ECR_REGISTRY}/ecomm:latest'

                sh 'docker push ${ECR_REGISTRY}/ecomm:latest'
            }
        }

        stage('Deploy to ECS') {
        steps {
            script {
                // Update ECS task definition with the new image
                def taskDefinition = sh(script: "aws ecs describe-task-definition --task-definition ${ECS_TASK_DEFINITION}", returnStdout: true).trim()
                def updatedTaskDefinition = taskDefinition.replaceAll(/"image":\s*".*"/, "\"image\": \"${ECR_REGISTRY}/ecomm:latest\"")

                sh "echo '${updatedTaskDefinition}' > updated-task-definition.json"

                // Register the updated task definition
                sh "aws ecs register-task-definition --cli-input-json file://updated-task-definition.json"

                sh "rm updated-task-definition.json"

                // Update the ECS service with the new task definition
                sh "aws ecs update-service --cluster ${ECS_CLUSTER} --service ${ECS_SERVICE_NAME} --task-definition ${ECS_TASK_DEFINITION}"
            }
        }
    }
    }
}
