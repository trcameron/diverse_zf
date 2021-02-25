#####################################################
#			Zero Forcing Diversity Make File		
#####################################################
include make.inc
	
python_test:
	$(NAUTY)/geng $(SIZE) | python3 python/zero_forcing_ip.py
