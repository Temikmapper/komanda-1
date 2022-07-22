node {
    stage 'Test'
        sh 'python3 -m venv venv'
        sh 'source venv/bin/activate'
        sh 'pip3 install -r komanda/requirements/local.txt'
        sh 'cd komanda'
        sh 'python3 manage.py test expenses goals'

    // stage 'Deploy'
    //     sh './deployment/deploy_prod.sh'
}