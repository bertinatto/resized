APP=resized

.PHONY: clean
clean:
	@sudo rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec sudo rm -fr {} +
	@find . -name '*.pyc' -exec sudo rm -f {} +
	@find . -name '*.pyo' -exec sudo rm -f {} +

.PHONY: test
test:
	@make clean
	@py.test --verbose tests/
	@py.test --flake8 $(APP)

.PHONY: start-compose
start-compose:
	@docker-compose up

.PHONY: start-oc
start-oc:
	@sh bin/occtl.sh start $(APP)

.PHONY: stop-oc
stop-oc:
	@sh bin/occtl.sh stop $(APP)
	@make clean

.PHONY: start-k8
start-k8:
	@sh bin/k8ctl.sh start $(APP)

.PHONY: stop-k8
stop-k8:
	@sh bin/k8ctl.sh stop $(APP)
	@make clean
