# AWS_AddRemoveInstances_fromELB
go to the server on linux.
 save the file on the server as "addremoveinstfromelb.py"
 save the instance-ids in the file "instidsfile"
 
 then run the below command with your choice of operation(register/deregister)


./addremoveinstfromelb.py "ELB-Name" deregister instidsfile
