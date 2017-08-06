#!groovy
@Library("jenkins-libs@master")
import main.groovy.docker.Compose

node {

  ansiColor('xterm') {
    stage('Checkout') {
        echo 'Getting source code'
        checkout scm
    }

    def currentBuildTag = "${env.BUILD_NUMBER}"
    def stableImageTag = "latest"
    def compose = new Compose(this, env.DOCKER, env.DOCKER_COMPOSE, env.REGISTRY)

    stage('Build Docker Images') {
        compose.buildImages(currentBuildTag)
    }

    try {
        saveImages(compose, currentBuildTag, stableImageTag)
        pushImages(compose, stableImageTag);
    } catch (e) {
    } finally {
        deleteImages(compose, currentBuildTag)
    }
  }
}

def saveImages(compose, oldTag, newTag) {
    stage('Save latest stable') {
        echo "Tagging images as ${newTag}"

        compose.tagImages(oldTag, newTag)
    }
}

def pushImages(compose, tag) {
    stage('Clean') {
        echo "Pushing the images"
        compose.pushImages(tag)
    }
}

def deleteImages(compose, tag) {
    stage('Clean') {
        echo "Deleting the images"
        compose.deleteImages(tag)
    }
}
