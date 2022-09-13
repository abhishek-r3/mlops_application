pipeline {
    agent any
        stages {
            stage('Clone Repository') {
                /* Cloning the repository for web application */
                steps {
                    checkout scm
                }
            }
            stage('Verify') {
                steps{
                    sh 'ls'
                }
            }
            stage('Display Jenkins File') {
                steps{
                    sh 'cat Jenkinsfile'
                }
            }
            stage('Build Image') {
                steps{
                    sh "docker build --user='jenkins' -t drug-per-app:v1 src/app"
                }
            }
            stage('Run Docker Image'){
                steps {
                sh "docker run --user='jenkins' -d -p 5000:5000 --name drug-per-app drug-per-app:v1"
                }
            }
            stage("Testing"){
                steps {
                    echo 'Testing.....'

                }
            }
        }
}