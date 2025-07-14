pipeline {
    agent any

    stages {
        stage('Code') {
            steps {
                echo 'This is Developing code'
                git url: "https://github.com/salilgupta332/Speedy-Bites.git" , branch: "main"
            }
        }
        stage('Build') {
            steps {
                echo 'This is Building code'
                sh  "docker build -t speedy-bites ."
            }
        }
        stage('Push to Docker hub') {
            steps {
                echo 'Pushing Image to Docker hub'
                withCredentials([usernamePassword(credentialsId:"dockerhub" , passwordVariable: "dockerHubPass" , usernameVariable: "dockerHubUser")]){
                    sh "docker tag speedy-bites ${env.dockerHubUser}/speedy-bites:latest"
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                    sh "docker push  ${env.dockerHubUser}/speedy-bites:latest"
                }
            }
        }
        
        stage("Deploy") {
            steps {
                echo 'This is Deploying code'
                sh "docker compose down && docker-compose up -d"
            }
        }
    }
}