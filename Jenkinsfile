pipeline {
    agent any
        stages {
            stage('Clone Repository') {
                /* Cloning the repository for web application */
                steps {
                    checkout scm
                }
            }
            stage('Build Image') {
                steps{
                    sh 'sudo docker build -t drug-per-app:v1 src/app'
                }
            }
            stage('Run Docker Image'){
                steps {
                sh 'sudo docker run -d -p 5000:5000 --name drug-per-app drug-per-app:v1'
                }
            }
            Stage("Testing"){
                steps {
                    echo 'Testing.....'

                }
            }
        }
}