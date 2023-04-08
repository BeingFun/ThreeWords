MAKE := python
all:
	$(MAKE) ./scripts/compile.py && $(MAKE) ./scripts/deploy.py
compile:
	$(MAKE) ./scripts/clr_compile.py && $(MAKE) ./scripts/compile.py
deploy:
	$(MAKE) ./scripts/clr_deploy.py && $(MAKE) ./scripts/deploy.py
clr_all:
	$(MAKE) ./scripts/clr_deploy.py
	$(MAKE) ./scripts/clr_running.py
	$(MAKE) ./scripts/clr_compile.py  # if clr_compile not at last, use ROOT_PATH cause make new *.pyc file
clr_deploy:
	$(MAKE) ./scripts/clr_deploy.py
clr_compile:
	$(MAKE) ./scripts/clr_compile.py
clr_running:
	$(MAKE) ./scripts/clr_running.py
test:
	$(MAKE) ./scripts/test.py # TODO
