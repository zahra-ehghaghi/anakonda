pipeline{
  agent any
  stages {
    stage("Prepare"){
      steps{
	load "jenkins/config.groovy"
	dir(pwd(tmp: true)){
	  git(
 		url: "$ANAKONDA_API_CI_CONFIG_GIT_URL",
		branch: "$ANAKONDA_API_CI_CONFIG_GIT_BRANCH",
		credentialsId: "$ANAKONDA_API_CI_CONFIG_GIT_CREDENTIAL",
		changelog: true,
		poll: true
	     )
	  load "config.groovy"
	  sh  "env"
	}
	
      } 
    }

   stage("Build"){
     steps{
	 script{
                gitBranch = sh(script: "git  rev-parse --abbrev-ref HEAD", returnStdout:true).trim()
                gitTag = sh(script: "git tag --points-at HEAD", returnStdout: true).trim()
		gitCommit = sh(script: "git rev-parse HEAD", returnStdout:true).trim()
		anakondaImage = docker.build("${ANAKONDA_API_DOCKER_REGISTERY_ADDRESS}/${ANAKONDA_API_IMAGE_NAME}:jenkins-pipeline-$BUILD_ID",
		"--build-arg GIT_BRANCH=${gitBranch}  --build-arg GIT_COMMIT=${gitCommit} --build-arg BUILD_TAG=${BUILD_TAG}  --build-arg GIT_TAG=${gitTag}  --build-arg BUILD_ID=${BUILD_ID}  .")
	}
     }
   }
   stage("Test"){
      steps{
	script {
       	docker.image("${ANAKONDA_API_MYSQL_IMAGE}").withRun("--name anakonda-mysql-$BUILD_ID  -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=test -e MYSQL_USER=anakonda -e  MYSQL_PASSWORD=anakonda"){
          mysql -> 
		anakondaImage.inside("--name anakonda-app-$BUILD_ID --link ${mysql.id} -e  ANAKONDA_API_DATABASE_URI=mysql+pymysql://anakonda:anakonda@anakonda-mysql-${BUILD_ID}:3306/test -e ANAKONDA_API_ENV=test -e ANAKONDA_API_DEBUG=1 --entrypoint='' ${ANAKONDA_API_CONTAINER_EXTRA_ARGS}  "){
		   i = 1
		   retry(5) {
			sh "sleep $i"
			i *=2
                        sh "flask db upgrade"
    		   }
                  coverageStatus = sh(
			script:	"coverage run -m pytest --junit-xml=anakonda-pytest-${BUILD_ID}.xml",
			returnStatus: true 
		      )
		   if("$ANAKONDA_API_REPORT_UNIT_TEST_RESULTS" == "true"){
   		        junit "anakonda-pytest-${BUILD_ID}.xml"
		  }
		   sh "coverage html"
		   sh "coverage xml"
		  if("$ANAKONDA_API_REPORT_CODE_COVERAGE" == "true"){
	              cobertura(
	     	           autoUpdateHealth: true,
			   autoUpdateStability: true,
			   coberturaReportFile: "coverage.xml"
		      )
                  }
		  if("$ANAKONDA_API_ARCHIVE_ATRIFACTS" == "true"){
		     archiveArtifacts(
		         artifacts: "*.xml,htmlcov/**/*",
		         fingerprint: true
		  )
		 }
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
         if("$ANAKONDA_API_LATEST_IMAGE_RELEASE" == "true"){
              anakondaImage.push("latest")
	 }
         if("$ANAKONDA_API_BRANCH_IMAGE_RELEASE" == "true"){
              anakondaImage.push(gitBranch)
         }
          if (gitTag != ""){
	    if (gitTag.startsWith("v")){
	       gitTag = gitTag.minus("v")
	       anakondaFullVersion = gitTag
	       version = gitTag.split("\\.")
  	       anakondaMajorVersion = version[0]
	       anakondaMajorMinorVersion = version[0]+ "." + version[1]
               if("$ANAKONDA_API_TAG_IMAGE_RELEASE" == "true"){
		       anakondaImage.push(anakondaFullVersion)
		}
               if("$ANAKONDA_API_VERSION_IMAGE_RELEASE" == "true"){
                 anakondaImage.push(anakondaMajorVersion)
	         anakondaImage.push(anakondaMajorMinorVersion)
	      }
	   }
         }
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
