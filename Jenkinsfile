node {
    stage 'Test'
        sh """
            #!/bin/bash
            rm -rf venv
            python3 -m venv venv
            . venv/bin/activate
            pip3 install -r komanda/requirements/local.txt
            cd komanda
            python3 manage.py test expenses goals"""

    // stage 'Deploy'
    //     sh './deployment/deploy_prod.sh'
}