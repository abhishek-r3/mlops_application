pipeline {
    agent any
        stages {

            stage('Clone Source Repository') {
                /* Cloning the repository for web application */
                steps {
                    checkout scm
                }
            }
	    stage('Verify The Clone') {
                steps{
                    sh 'ls'
                }
            }
            stage('Verify The Steps') {
                steps{
                    sh 'cat Jenkinsfile'
                }
            }
            
            stage('Build Docker Image') {
                steps{
                    sh "docker build -t drug-per-app:v1 src/app"
                }
            }
            stage('Run Docker Image And Expose API'){
                steps {
                sh "docker run -d -p 5000:5000 --name drug-per-app drug-per-app:v1"
                }
            }
            stage("Testing Application"){
                steps {
                    echo 'Testing.....'

                }
            }
        }
}