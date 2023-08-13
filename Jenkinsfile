pipeline {
    agent {
        label 'jenkins-slave'
    }

    environment {
        ECR_REGISTRY = credentials('ecr_registry')
        ECR_REGION = credentials('ecr_region')
        ECS_CLUSTER = credentials('ecs_cluster')
    }

    stages {
        stage('gitclone') {
            steps {
                git branch: 'main', credentialsId: 'github_credentials', url: 'https://github.com/vamsikunal/ecomm'
            }
        }

        stage('Connect ECR'){
            steps {
                sh 'aws ecr get-login-password --region ${ECR_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${ECR_REGISTRY}/ecomm:latest .'
            }
        }

        stage('Push') {
            steps {
                sh 'docker push ${ECR_REGISTRY}/ecomm:latest'
            }
        }

        stage('Deploy to ECS') {
        steps {
            script {
                // Define the ECS service name and task definition name
                def ECS_SERVICE_NAME = 'ecomm-service'
                def ECS_TASK_DEFINITION = 'ecomm-task'

                // Update ECS task definition with the new image
                def taskDefinition = sh(script: "aws ecs describe-task-definition --task-definition ${ECS_TASK_DEFINITION}", returnStdout: true).trim()
                def updatedTaskDefinition = taskDefinition.replaceAll(/"image":\s*".*"/, "\"image\": \"${ECR_REGISTRY}/ecomm:latest\"")

                sh "echo '${updatedTaskDefinition}' > updated-task-definition.json"

                // Register the updated task definition
                sh "aws ecs register-task-definition --cli-input-json file://updated-task-definition.json"

                // Update the ECS service with the new task definition
                sh "aws ecs update-service --cluster ${ECS_CLUSTER} --service ${ECS_SERVICE_NAME} --task-definition ${ECS_TASK_DEFINITION}"
            }
        }
    }
    }
}
