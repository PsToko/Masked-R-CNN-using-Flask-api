pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t localhost:5001/masked-rcnn-api:latest .'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push localhost:5001/masked-rcnn-api:latest'
            }
        }
    }
}