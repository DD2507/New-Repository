pipeline {
    agent any

    environment {
        IMAGE_NAME = "auto-rollback-app:v1"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'export KUBECONFIG=/var/jenkins_home/.kube/config && kubectl apply -f deployment.yaml'
                sh 'export KUBECONFIG=/var/jenkins_home/.kube/config && kubectl apply -f service.yaml'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'export KUBECONFIG=/var/jenkins_home/.kube/config && kubectl rollout status deployment/auto-rollback-app'
            }
        }
    }

    post {
        failure {
            sh 'export KUBECONFIG=/var/jenkins_home/.kube/config && kubectl rollout undo deployment/auto-rollback-app'
        }
    }
}