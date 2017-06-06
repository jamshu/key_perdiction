#Actual case is train ,the test which is optional,which system work,and give feedback,no need of keyword for test
from graph_process import GraphProcess 
gf_train =GraphProcess(train_count=500,test_count=500,train=True)
# gf_test = GraphProcess(train_count=1,test_count=2,train=False)
gf_train.writeToExcel()
# gf_test.writeToExcel()