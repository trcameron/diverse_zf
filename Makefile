#####################################################
#			Zero Forcing Diversity Make File		
#####################################################
include make.inc
	
python_test:
	$(NAUTY)/geng $(SIZE) | $(PYTHON) python/zero_forcing_ip.py
	
wavefront:
	$(NAUTY)/geng $(SIZE) | $(PYTHON) python/wavefront.py