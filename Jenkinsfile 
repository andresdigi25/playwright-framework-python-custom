pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup & Test') {
            agent {
                docker {
                    // Using the official Playwright Python image.
                    // Ensure this image meets your requirements; you can also build a custom image if needed.
                    image 'mcr.microsoft.com/playwright/python:latest'
                    // The following args ensure that no extra entrypoint interferes.
                    args '--entrypoint=""'
                }
            }
            steps {
                // Upgrade pip and install your dependencies.
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                
                // Install Playwright browsers (if not already installed)
                sh 'playwright install'

                // Run your tests. Adjust options as needed.
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }
    }

    post {
        always {
            // Archive test results if available (optional)
            junit '**/test-results.xml'
        }
    }
}
