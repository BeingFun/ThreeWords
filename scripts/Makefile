MAKE := python
all:
	$(MAKE) build.py && $(MAKE) deploy.py
compile:
	$(MAKE) clr_compile.py && $(MAKE) build.py
deploy:
	$(MAKE) clr_package.py && $(MAKE) deploy.py
clr_all:
	$(MAKE) clr_compile.py && $(MAKE) clr_package.py && $(MAKE) clr_running.py
clr_compile:
	$(MAKE) clr_compile.py
clr_package:
	$(MAKE) clr_package.py
clr_running:
	$(MAKE) clr_running.py
test:
	$(MAKE) test.py # TODO
