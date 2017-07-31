#!groovy
@Library("jenkins-libs@master")
import docker.Images

node {

  ansiColor('xterm') {
    
    stage('Checkout') {
        echo 'Getting source code'
        checkout scm
    }

    def imageName = "log-gateway"
    def currentBuildTag = "${env.BUILD_NUMBER}"
    def stableImageTag = "latest"
    def images = new Images(this, env.DOCKER, env.REGISTRY)

    stage('Build Docker') {
        images.buildDockerImages([imageName], currentBuildTag)
    }

    try {
        def currentBuildImageName = images.getFullImageName(imageName, currentBuildTag);
        testImage(currentBuildImageName)

        saveImage(images, imageName, currentBuildTag, stableImageTag)
    } catch (e) {

    } finally {
        deleteImage(currentBuildImageName)
    }
  }
}

def testImage(imageFullName) {
    stage('Test') {
        echo "Testing image ${imageFullName}"
        sh "${env.DOCKER} run --rm ${imageFullName} test"
    }
}

def saveImage(images, imageName, currentBuildTag, stableImageTag) {
    stage('Save latest stable') {
        def imageFullName = images.getFullImageName(imageName, currentBuildTag);
        def stableImageName = images.getFullImageName(imageName, stableImageTag);
        echo "Saving image ${imageFullName} as ${stableImageName}"

        images.tagDockerImages([imageName], currentBuildTag, stableImageTag)
    }
}

def deleteImage(images, imageName, currentBuildTag) {
    stage('Clean') {
        def imageFullName = images.getFullImageName(imageName, currentBuildTag);

        echo "Deleting the image ${imageFullName}"
        images.removeDockerImages([imageName], currentBuildTag)
    }
}