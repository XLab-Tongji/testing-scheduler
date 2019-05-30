# get the absolute path of this shell file.

#run the testcase_target with command line
#sudo python $basepath/src/test_parser.py --filepath=$basepath/test/test_case/stress/tc_stress_01.yaml

#sudo python $basepath/src/test_parser.py --filepath=$basepath/test/test_case/stress/tc_stress_02.yaml

#sudo python $basepath/src/test_parser.py --filepath=$basepath/test/test_case/stress/tc_stress_03.yaml

sudo python /home/serveradmin/testing-scheduler/server/src/test_parser.py --filepath=/home/serveradmin/testing-scheduler/server/test/test_case/stress/$1
