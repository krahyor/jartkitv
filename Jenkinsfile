
pipeline {
    agent any  // ใช้ Jenkins node ที่มี Docker CLI

    environment {
        SONARQUBE = credentials('sonar-token')   // Jenkins Credentials สำหรับ SonarQube token
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'lab', url: 'https://github.com/krahyor/jartkitv.git'
            }
        }

        stage('Install Dependencies & Run Tests') {
            agent {
                docker {
                    image 'python:3.11'
                    args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'  // รันเป็น root + DinD
                }
            }
            steps {
                // ติดตั้ง dependencies
                sh 'python3.11 -m venv venv'
                sh './venv/bin/pip install --no-cache-dir --upgrade pip'
                sh './venv/bin/pip install --no-cache-dir -r requirements.txt'
                sh './venv/bin/pip install --no-cache-dir coverage'
                
                // รัน unit test และ generate coverage report (coverage.xml สำหรับ SonarQube)
                sh 'PYTHONPATH=. ./venv/bin/coverage run -m pytest ./tests/test_main.py'
                sh './venv/bin/coverage xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // ใช้ SonarScanner CLI Docker image (Linux compatible)
                    // -Dsonar.host.url=http://172.17.0.1:9001 <--- command check : ip addr show docker0
                    docker.image('sonarsource/sonar-scanner-cli').inside {
                        withSonarQubeEnv('sonarqube-7.2') {
                            sh '''
                                sonar-scanner \
                                    -Dsonar.projectKey=fastapi-jenkins \
                                    -Dsonar.sources=app \
                                    -Dsonar.host.url=http://172.17.0.1:9001 \
                                    -Dsonar.login=$SONARQUBE \
                                    -Dsonar.branch.name=lab
                            '''
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                // stop & remove container ถ้ามีอยู่
                sh '''
                if [ $(docker ps -aq -f name=app) ]; then
                    docker stop app
                    docker rm app
                fi
                '''

                // run container ใหม่
                sh 'docker run -d --name app -p 8000:8000 fastapi-app:latest uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline finished"
        }
    }
}