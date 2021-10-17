pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '**']], 
                extensions: [], userRemoteConfigs: [[credentialsId: 'sjng1234_github_ssh_key', 
                url: 'git@github.com:sjng1234/SPM_G5.git']]])
            }
        }
        stage('Code_Analysis') {
            steps {
                sh '''
                python3 -m venv env
                source env/bin/activate
                pip3 install flake8
                flake8 main.py
                '''
            }
        }

    }
}
