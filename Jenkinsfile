
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
            }
        }

        stage('Gemini AI Security Analysis') {
            when {
                not {
                    branch 'test/security-gate-blocking'
                }
            }
            steps {
                withCredentials([
                    string(
                        credentialsId: 'gemini-api-key',
                        variable: 'GEMINI_API_KEY'
                    )
                ]) {
                    bat '".jenkins-venv\\Scripts\\python.exe" security\\ai_analyzer.py'
                }
            }
        }

        stage('Inject Simulated HIGH Finding - TEST ONLY') {
            when {
                branch 'test/security-gate-blocking'
            }
            steps {
                writeFile file: 'reports/bandit-report.json', text: '''{
    "results": [
        {
            "test_id": "TEST001",
            "issue_severity": "HIGH",
            "issue_confidence": "HIGH",
            "issue_text": "SIMULATED TEST: Verify Jenkins blocks a high-severity finding.",
            "filename": "simulated_test.py",
            "line_number": 1
        }
    ]
}'''
                echo 'TEST ONLY: Injected a simulated HIGH-severity finding.'
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
            echo 'SECURITY PIPELINE PASSED: Docker image built.'
        }
        failure {
            echo 'SECURITY PIPELINE BLOCKED: Inspect the failed stage and reports.'
        }
        always {
            archiveArtifacts artifacts: 'reports/bandit-report.json,reports/ai-security-report.md', allowEmptyArchive: true
            echo 'Security reports archived. Pipeline execution completed.'
        }
    }
}
