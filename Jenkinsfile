pipeline {
    agent any

    environment {
        DOCKER_HOST = 'tcp://docker:2375'
    }

    stages {

        stage('Test Docker') {
            steps {
                sh 'docker version'
                sh 'docker info'
            }
        }

    }
}