pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t host.docker.internal:5001/masked-rcnn-api:latest .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push host.docker.internal:5001/masked-rcnn-api:latest
                '''
            }
        }
    }
}