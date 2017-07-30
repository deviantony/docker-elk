#!groovy

node {

  ansiColor('xterm') {

    stage('Checkout') {
        echo 'Getting source code...'
        checkout scm
    }

    stage('Build Docker') {
        echo 'Building docker images...'
        sh "${env.DOCKER} build -t ${env.REGISTRY}/log-gateway log-gateway"
    }

    stage('Test') {
        echo 'Testing...'
        sh "${env.DOCKER} run --rm ${env.REGISTRY}/log-gateway test"
    }
  }
}