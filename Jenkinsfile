#!groovy

node {

  ansiColor('xterm') {

    stage('Checkout') {
        echo 'Getting source code'
        checkout scm
    }

    def imageName = "${env.REGISTRY}/log-gateway"
    def currentBuildImage = "${imageName}:${env.BUILD_NUMBER}"
    def stableImageName = "${imageName}:latest"

    stage('Build Docker') {
        echo "Building docker image ${currentBuildImage}"
        sh "${env.DOCKER} build -t ${currentBuildImage} log-gateway"
    }

    try {
        testImage(currentBuildImage)

        saveImage(currentBuildImage, stableImageName)
    } catch (e) {

    } finally {
        deleteImage(currentBuildImage)
    }
  }
}

def testImage(image) {
    stage('Test') {
        echo "Testing image ${image}"
        sh "${env.DOCKER} run --rm ${image} test"
    }
}

def saveImage(oldImage, newImage) {
    stage('Save latest stable') {
        echo "Saving the image ${oldImage} as ${newImage}"
        sh "${env.DOCKER} tag ${oldImage} ${newImage}"
    }
}

def deleteImage(image) {
    stage('Clean') {
        echo "Deleting the image ${image}"
        sh "${env.DOCKER} rmi ${image}"
    }
}