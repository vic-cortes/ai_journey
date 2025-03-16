.PHONY: all clean build install

all: build

build:
	@echo "Building the project..."

clean:
	@echo "Cleaning the project..."

install: library
	@echo "Installing the project..."
	uv pip install $(library)

compile-pip:
	@echo "Compiling the project..."
	uv pip freeze > requirements.txt 
	uv pip compile requirements.txt -o requirements.lock