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
                    sh 'whoami'
                }
            }
            stage("Fix the permission issue") {
                agent any
                steps {
                    sh "sudo chown root:jenkins /run/docker.sock"
                }
            }
            stage('Build Image') {
                steps{
                    sh "sudo docker build --user='jenkins' -t drug-per-app:v1 src/app"
                }
            }
            stage('Run Docker Image'){
                steps {
                sh "sudo docker run --user='jenkins' -d -p 5000:5000 --name drug-per-app drug-per-app:v1"
                }
            }
            stage("Testing"){
                steps {
                    echo 'Testing.....'

                }
            }
        }
}