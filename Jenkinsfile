#!groovy

node {

  ansiColor('xterm') {

    stage('Initialize') {
        echo 'Initializing...'
        def node = tool name: 'Node-8.1.4', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
        env.PATH = "${node}/bin:${env.PATH}"
    }

    stage('Checkout') {
        echo 'Getting source code...'
        checkout scm
    }

    dir('log-gateway') {
      stage('Dependencies') {
          echo 'Building dependencies...'
          sh 'npm install'
      }

      stage('Build') {
          echo 'Building TypeScript...'
          sh 'npm run build'
      }

      stage('Test') {
          echo 'Testing...'
          sh 'npm test'
      }
    }
  }
}