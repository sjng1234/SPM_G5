pipeline {
    agent any

    stages {
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
