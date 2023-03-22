pipeline {
    agent any
    

    stages {
        stage('Install Dependencies') {
            steps {
                bat '''pip install -r requirements.txt'''
            }
        }

        stage('Build') {
            steps {
                bat '''python gpt2.py "Alan Turing theorized that computers would one day become"'''
            }
        }
    }
}
