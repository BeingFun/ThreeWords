MAKE := python
all:
	$(MAKE) build.py && $(MAKE) deploy.py
compile:
	$(MAKE) build.py
deploy:
	$(MAKE) deploy.py
clr_all:
	$(MAKE) clr_compile.py && $(MAKE) clr_package.py && clr_running.py
clr_compile:
	$(MAKE) clr_compile.py
clr_package:
	$(MAKE) clr_package.py
clr_running:
	$(MAKE) clr_running.py # TODO 清理运行时文件
test:
	$(MAKE) test.py

