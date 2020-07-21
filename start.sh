#!/bin/sh
Gravalog ()
{
        MSG=${1}
        COD_ERROR=${2}
        if [ $COD_ERROR -ne 0 ]
        then
        STATUS="ERROR: "
        DATELOG=`date +%m-%d-%Y" "%H:%M:%S`   
        echo "[${DATELOG}] - ${STATUS} error during execution of ${MSG}. ERROR CODE: ${COD_ERROR}" 
        exit 1
		fi
}


python3 1.getRepo.py
Gravalog "1.getRepo.py" $?
python3 2.getAttrib.py
Gravalog "2.getAttrib.py" $?
python2 3.gender_classifier.py
Gravalog "3.gender_classifier.py" $?
python3 4.Summary.py
Gravalog "4.Summary.py" $?
