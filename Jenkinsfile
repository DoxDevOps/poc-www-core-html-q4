pipeline {
  agent any
  stages {
    stage('Initializing') {
      steps {
        echo 'Initializing ...'
        sh 'echo "Working from $WORKSPACE"'
        sh '''echo "Your build number is: \\${BUILD_NUMBER} -> ${BUILD_NUMBER}"
echo "Your build number is: \\${REQUEST_ID} -> ${REQUEST_ID}"'''
      }
    }

    stage('Fetching Repos') {
      parallel {
        stage('Fetching API') {
          steps {
            echo 'Starting to fetch API from GitHub'
            echo 'Checking if BHT-EMR-API exists.'
            sh '[ -d "BHT-EMR-API" ] && echo "API already cloned." || git clone https://github.com/HISMalawi/BHT-EMR-API.git'
            echo 'Giving access to all users'
            sh 'cd $WORKSPACE && chmod 777 BHT-EMR-API'
            echo 'Fetching Tags'
            sh 'cd $WORKSPACE/BHT-EMR-API && git fetch --tags -f'
            echo 'Checking out to Latest Tag'
            sh '''#cd $WORKSPACE/BHT-EMR-API && git checkout v4.10.44
#$(git describe --tags `git rev-list --tags --max-count=1`)'''
            sh '#cd $WORKSPACE/BHT-EMR-API && git describe > HEAD'
          }
        }

        stage('Fetching Core') {
          steps {
            echo 'Starting to fetch Core from GitHub'
            echo 'Checking if BHT-Core exists.'
            sh '[ -d "BHT-Core" ] && echo "Core already cloned." || git clone https://github.com/HISMalawi/BHT-Core.git'
            echo 'Giving access to users'
            sh 'cd $WORKSPACE && chmod 777 BHT-Core'
            echo 'Fetching New Tags'
            sh 'cd $WORKSPACE/BHT-Core && git fetch --tags -f'
            echo 'Checking out to latest tag'
            sh '#cd $WORKSPACE/BHT-Core && git checkout $(git describe --tags `git rev-list --tags --max-count=1`)'
            echo 'creating apps folder in Core'
            sh '[ -d "$WORKSPACE/BHT-Core/apps" ] && echo "apps already exists." || cd $WORKSPACE/BHT-Core && mkdir apps'
            echo 'giving access rights to apps folder'
            sh 'cd $WORKSPACE/BHT-Core && chmod 777 apps'
          }
        }

      }
    }

    stage('Fetching Core Apps') {
      parallel {
        stage('Fetching ART') {
          steps {
            echo 'Starting to fetch ART from GitHub'
            echo 'Checking if BHT-Core-Apps-ART exists.'
            sh '[ -d "$WORKSPACE/BHT-Core/apps/ART" ] && echo "ART already cloned." || git clone https://github.com/HISMalawi/BHT-Core-Apps-ART.git $WORKSPACE/BHT-Core/apps/ART'
            echo 'Giving access to all user'
            sh 'cd $WORKSPACE/BHT-Core/apps && chmod 777 ART'
            echo 'Fetching new tags'
            sh 'cd $WORKSPACE/BHT-Core/apps/ART && git fetch --tags -f'
            echo 'Checking out to latest tag'
            sh '#cd $WORKSPACE/BHT-Core/apps/ART && git checkout $(git describe --tags `git rev-list --tags --max-count=1`)'
            sh '#cd $WORKSPACE/BHT-Core/apps/ART && git describe > HEAD'
          }
        }

        stage('Fetching OPD') {
          steps {
            echo 'Starting to fetch ART from GitHub'
            echo 'Checking if BHT-Core-Apps-OPD exists.'
            sh '[ -d "$WORKSPACE/BHT-Core/apps/OPD" ] && echo "OPD already cloned." || git clone https://github.com/HISMalawi/BHT-Core-Apps-OPD.git $WORKSPACE/BHT-Core/apps/OPD'
            echo 'Giving access to all user'
            sh 'cd $WORKSPACE/BHT-Core/apps && chmod 777 OPD'
            echo 'Fetching new tags'
            sh 'cd $WORKSPACE/BHT-Core/apps/OPD && git fetch --tags -f'
          }
        }

      }
    }

    stage('Shipping & Configurations') {
      parallel {
        stage('API') {
          steps {
            echo 'shipping & Configuring API'
            sh '''python3 api_shippingx.py



'''
          }
        }

        stage('Core, ART & OPD') {
          steps {
            echo 'Shipping & configuring Core & ART'
            sh '''python3 core_shippingx.py
python3 art_shippingx.py
#python3 opd_shippingx.py'''
          }
        }

      }
    }

  }
  environment {
    REQUEST_ID = 'true'
    CLUSTER_ID = '12345'
  }
}