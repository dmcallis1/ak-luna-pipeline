pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
        disableConcurrentBuilds()
    }
    environment {
        /*
            Change these environment variables based on your specific project
        */

        // Assumes you have defined a Jenkins environment variable 'PATH+EXTRA'
        PROJ = "/bin:/usr/local/bin:/usr/bin"

        // Link to VCS project containing network list
        PIPELINESCM = "git@github.com:dmcallis1/epic-pl-demo.git"

        // Comma-seperated e-mail list
        EMAIL = "dmcallis@akamai.com"

        // Path to pipeline project on the Jenkins server
        PIPELINEPATH = "/var/lib/jenkins/pipeline/epic-pl-demo"
    }
    stages {
     stage('Clone NL project') {
            steps {

              dir("${env.PIPELINEPATH}") {
                git "${env.PIPELINESCM}"
              }

              slackSend(botUser: true, message: "${env.JOB_NAME} - Cloning pipeline repo: ${env.PIPELINESCM}", color: '#1E90FF')
            }
        }
        stage('Reconcile pipeline') {
            steps {

                dir("${env.PIPELINEPATH}") {

                    sh "pwd"

                }
                slackSend(botUser: true, message: "${env.JOB_NAME} - reconciling pipeline project.", color: '#1E90FF')
            }
        }
    post {
        success {
            slackSend(botUser: true, message: "${env.JOB_NAME} - Pipeline project reconciled successfully.", color: '#008000')
        }
        failure {
            slackSend(botUser: true, message: "${env.JOB_NAME} - Pipeline reconciliation failed!", color: '#FF0000')
        }
    }
}
