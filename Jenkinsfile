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
		anakondaImage = docker.build("anakonda:jenkins-pipeline-$BUILD_ID")
	}
     }
   }

   stage("Test"){
      steps{
       	docker.image.("mysql:8").withRun("--name anakonda-mysql-$BUILD_ID -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABSE=test -e MYSQL_USER=anakonda -e  MYSQL_PASSWORD=anakonda"){
          mysql -> 
		anakondaImage.inside("--name anakonda-app-$BUILD_ID --link ${mysql.id} -e  ANAKONDA_API_DATABASE_URI=mysql+pymysql://anakonda:anakonda@anakonda-mysql-${BUILD_ID}:3306/test -e ANAKONDA_API_ENV=test -e ANAKONDA_API_DEBUG=1 --entrypoint=''"){
		   i = 1
		   retry(10) {
			sh "sleep $i"
			i *=2
                        sh "flask db upgrade"
    		   }
                   sh "coverage run"
         	}
	
	}
      }
    }

  }
}
