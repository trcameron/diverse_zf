#####################################################
#			Zero Forcing Diversity Make File		
#####################################################
include make.inc
	
python_test:
	$(NAUTY)/geng $(SIZE) | $(PYTHON) python/zero_forcing_ip.py
	
diameter_test:
	$(NAUTY)/geng $(SIZE) | $(PYTHON) python/diverse_zf_ip.py