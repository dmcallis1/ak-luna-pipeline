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

        // Path to pipeline project on the Jenkins server
        PIPELINEPATH = "/var/lib/jenkins/pipeline/epic-pl-demo"

        // Path to pipeline sync project
        TOOLPATH = "/var/lib/jenkins/workspace/ak-luna-pipeline"

        // Comma-seperated e-mail list
        EMAIL = "dmcallis@akamai.com"


    }
    parameters {
      choice(name: 'SYNC_TARGET', choices: ['dev.epic-pl-demo', 'stage.epic-pl-demo', 'prod.epic-pl-demo'], description: 'The source property to compare.')
    }
    stages {
     stage('Clone Pipeine project') {
            steps {

                dir("${env.PIPELINEPATH}") {
                  git "${env.PIPELINESCM}"
                }

                slackSend(botUser: true, message: "${env.JOB_NAME} - Cloning pipeline repo: ${env.PIPELINESCM}", color: '#1E90FF')
            }
        }
        stage('Pull target metadata') {
               steps {
                 dir("/var/lib/jenkins/pipeline/compare") {
                     sh 'rm -rf $SYNC_TARGET/'
                     sh 'akamai pm import -p $SYNC_TARGET'
                 }

                  slackSend(botUser: true, message: "${env.JOB_NAME} - Pulling metadata snippets from: ${env.SYNC_TARGET}", color: '#1E90FF')
               }
        }
        stage('Sync snippets') {
               steps {
                 withEnv(["PATH+EXTRA=$PROJ"]) {
                   sh 'python3 $TOOLPATH/compareProject.py $PIPELINEPATH /var/lib/jenkins/pipeline/compare/$SYNC_TARGET/config-snippets'
                 }

                  slackSend(botUser: true, message: "${env.JOB_NAME} - Comparing and synchronizing metadata snippets...", color: '#1E90FF')
               }
        }
        stage('Reconcile project pipeline state') {
            steps {

                  dir("${env.PIPELINEPATH}") {
                    withEnv(["PATH+EXTRA=$PROJ"]) {
                      sh 'python3 $TOOLPATH/versionSync.py $PIPELINEPATH'
                    }
                  }
                  slackSend(botUser: true, message: "${env.JOB_NAME} - reconciling pipeline project state.", color: '#1E90FF')
            }
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
