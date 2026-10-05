pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Program Files\\Python311\\python.exe'
        GIT_EXE = 'C:\\Program Files\\Git\\cmd\\git.exe'
        DOCKER_EXE = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        IMAGE_NAME = 'ai-security-gate'
    }

    stages {

        stage('Verify Tools') {
            steps {
                bat '"%PYTHON%" --version'
                bat '"%GIT_EXE%" --version'
                bat '"%DOCKER_EXE%" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m venv .jenkins-venv'
                bat '".jenkins-venv\\Scripts\\python.exe" -m pip install --upgrade pip'
                bat '".jenkins-venv\\Scripts\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Automated Tests') {
            steps {
                bat '".jenkins-venv\\Scripts\\python.exe" -m unittest discover -s tests -v'
            }
        }

        stage('Bandit Security Scan') {
            steps {
                bat 'if not exist reports mkdir reports'

                bat '".jenkins-venv\\Scripts\\python.exe" -m bandit -r app security -f json -o reports/bandit-report.json --exit-zero'

                echo 'Bandit security scan completed.'
            }
        }

        stage('Gemini AI Security Analysis') {
            steps {
                echo 'Starting Gemini AI security analysis...'

                bat '".jenkins-venv\\Scripts\\python.exe" security\\gemini_analysis.py'

                echo 'Gemini AI security analysis completed.'
            }
        }

        stage('Security Gate') {
            steps {
                bat '".jenkins-venv\\Scripts\\python.exe" security\\security_gate.py'
            }
        }

        stage('AI Risk Assessment') {
            steps {
                bat '".jenkins-venv\\Scripts\\python.exe" security\\ai_risk.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER_EXE%" build -t %IMAGE_NAME% .'
            }
        }
    }

    post {

        success {
            echo 'SECURITY PIPELINE PASSED: Docker image built successfully.'
        }

        failure {
            echo 'SECURITY PIPELINE BLOCKED: Inspect the failed stage and security reports.'
        }

        always {
            archiveArtifacts artifacts: 'reports/bandit-report.json,reports/ai-security-report.md',
                             allowEmptyArchive: true

            echo 'Security reports archived. Pipeline execution completed.'
        }
    }
}