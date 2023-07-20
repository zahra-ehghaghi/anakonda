pipeline{
  agent any
  stages {
    stage("Prepare"){
      steps{
	sh "true"
      } 
    }

   stage("Build"){
     steps{
	 script{
		def anakondaImage = docker.build("anakonda:jenkins-pipeline-$BUILD_ID")
	}
     }
   }

   stage("Test"){
      steps{
        sh "true"
      }
    }

  }
}
