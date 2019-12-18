#!/bin/bash

for WORKER in $(cat /usr/local/spark/conf/slaves)
do
    echo ${WORKER}
    ssh ubuntu@${WORKER} << 'EOF'

    # pip install imutils --user
    # pip install opencv-python==3.1.0.0 --user
    #sudo pip install vptree --user
    # pip install boto3 --user
    # sudo pip install pyspark
    # sudo pip install pandas==0.19.2

    exit
EOF
done