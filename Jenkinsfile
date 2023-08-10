pipeline

    agent {label 'jenkins-slave'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DATABASE_CREDENTIALS = credentials('database-cred')
    }

    stages{

        stage('gitclone'){
            steps{
                git branch: 'main', credentialsId: 'github_credentials', url: 'https://github.com/vamsikunal/ecomm'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t kunal1904/ecomm:latest .'
            }
        }

        stage('Docker login') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage('Push') {
            steps {
                sh 'docker push kunal1904/ecomm:latest'
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }