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
               gitBranch = sh(script: "git branch --show-current", returnStdout:true).trim()
		if (gitBranch == ""){
		 	gitBranch="$BRANCH_NAME"
		}
		gitCommit = sh(script: "git rev-parse HEAD", returnStdout:true).trim()
		anakondaImage = docker.build("192.168.56.10/anakonda:jenkins-pipeline-$BUILD_ID",
		"--build-arg GIT_BRANCH=${gitBranch}  --build-arg GIT_COMMIT=${gitCommit} --build-arg BUILD_TAG=${BUILD_TAG} --build-arg BUILD_ID=${BUILD_ID} .")
	}
     }
   }

   stage("Test"){
      steps{
	script {
       	docker.image("mysql:8").withRun("--name anakonda-mysql-$BUILD_ID  -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABSE=test -e MYSQL_USER=anakonda -e  MYSQL_PASSWORD=anakonda"){
          mysql -> 
		anakondaImage.inside("--name anakonda-app-$BUILD_ID --link ${mysql.id} -e  ANAKONDA_API_DATABASE_URI=mysql+pymysql://anakonda:anakonda@anakonda-mysql-${BUILD_ID}:3306/test -e ANAKONDA_API_ENV=test -e ANAKONDA_API_DEBUG=1 --entrypoint=''"){
		   i = 1
		   retry(5) {
			sh "sleep $i"
			i *=2
                        sh "flask db upgrade 2"
    		   }
                  coverageStatus = sh(
			script:	"coverage run -m pytest --junit-xml=anakonda-pytest-${BUILD_ID}.xml",
			returnStatus: true 
		      )
	           juint "anakonda-pytest-${BUILD_ID}.xml"
		   sh "coverage html"
		   sh "coverage xml"
	           cobertura(
			autoUpdateHealth: true,
			autoUpdateStability: true,
			coberturaReportFile: "coverage.xml"
		   )
		  archiveArtifacts(
		    artifacts: "*.xml,htmlcov/**/*",
		    fingerprint: true
		  )
	           if (coverageStatus != 0){
                	sh "false"  
	           }  
         	}
	  }
	} 
      }
    }
   stage("Release"){
      steps{
	script {
          anakondaImage.push("latest")
        }
      }
   }
  }
  post{
   always{ 
    deleteDir()
   }
  }
}
