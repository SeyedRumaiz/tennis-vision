.PHONY: help venv install run infer black lint check clean clean-stubs clean-all

PYTHON ?= python3
PIP := $(PYTHON) -m pip

PYTHON_FILES := $(shell find . -name '*.py' -not -path './.venv/*' -not -path './*/__pycache__/*')

help:
	@echo "Available targets:"
	@echo "  help         Show this help message"
	@echo "  venv         Create a local Python virtual environment at .venv"
	@echo "  install      Install project dependencies into .venv"
	@echo "  run          Execute the main tennis analysis pipeline"
	@echo "  infer        Run the YOLO inference helper script"
	@echo "  black        Format Python code with Black"
	@echo "  lint         Run lint checks with Flake8"
	@echo "  check        Syntax check all Python sources"
	@echo "  clean        Remove generated videos, caches, and temporary files"
	@echo "  clean-stubs  Remove tracker stub pickle files"
	@echo "  clean-all    Remove generated artifacts and the virtual environment"

venv:
	$(PYTHON) -m venv .venv

install: venv
	. .venv/bin/activate && $(PIP) install --upgrade pip
	. .venv/bin/activate && $(PIP) install ultralytics opencv-python pandas numpy torch torchvision black flake8

run:
	. .venv/bin/activate && $(PYTHON) main.py

infer:
	. .venv/bin/activate && $(PYTHON) yolo_inference.py

black:
	. .venv/bin/activate && $(PYTHON) -m black $(PYTHON_FILES)

lint:
	. .venv/bin/activate && $(PYTHON) -m flake8 $(PYTHON_FILES)

check:
	$(PYTHON) -m py_compile $(PYTHON_FILES)

clean:
	rm -rf output_videos/*.avi tracker_stubs/*.pkl runs/detect/* runs/track/*
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

clean-stubs:
	rm -f tracker_stubs/*.pkl

clean-all: clean clean-stubs
	rm -rf .venv
