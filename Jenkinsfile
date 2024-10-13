pipeline {
    agent any

    triggers {
        cron('H/10 * * * *') // 每 10 分鐘執行一次
    }

    environment {
        GITLAB_CREDENTIALS = credentials('gitlab') // GitLab 認證
        PYTHON_ENV = "venv"  // 設定 Python 環境路徑
    }

    stages {
        stage('從gitlab拉取專案') {
            steps {
                script {
                    // 從 GitLab 拉取專案
                    git url: "$SOURCE_CODE_GIT_URL", credentialsId: 'gitlab'
                }
            }
        }

        stage('安裝套件') {
            steps {
                sh '''
                apt-get install python3-venv -y
                '''
            }
        }


        stage('設定python環境變數') {
            steps {
                sh '''
                python3 -m venv $PYTHON_ENV
                . $PYTHON_ENV/bin/activate
                pip install -r ${WORKSPACE}/requirements.txt
                '''
            }
        }


        stage('執行爬蟲腳本') {
            steps {
                sh '''
                . $PYTHON_ENV/bin/activate
                python3 yahoo_news_with_selenium.py
                '''
            }
        }
    }
    post {
        always {
            script {
                def buildResult = currentBuild.currentResult
                // 執行LINE NOTIFY腳本
                sh """
                echo "部署结果: ${buildResult}"
                sh ${WORKSPACE}/send_line_notify.sh $JOB_NAME $BUILD_NUMBER $BUILD_URL $GIT_BRANCH $GIT_COMMIT $WORKSPACE $LINE_NOTIFY_TOKEN ${buildResult}
                """
                // 讀取HTML模板內容
                def customHtmlTemplate = readFile('custom.html')
                // 寄送郵件
                emailext (
                    subject: "$JOB_NAME-#$BUILD_NUMBER-${buildResult}",
                    body: customHtmlTemplate,
                    mimeType: 'text/html',
                    to: "markhsu0704@gmail.com"
                )
            }

        }
    }
}
