#####################################################
#			Zero Forcing Diversity Make File		#####################################################
include make.inc
	
python_test:
<<<<<<< HEAD
	$(NAUTY)/geng $(SIZE) | python3 python/zero_forcing_ip.py
=======
	$(NAUTY)/geng $(SIZE) | python3 python/zero_forcing_ip.py
	
uninstall:
	@rm -f boost_graph
	@rm -f graph6
>>>>>>> d131c3831bad97cccf6ceacd9f79067f49d8589c
