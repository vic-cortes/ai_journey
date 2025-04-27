.PHONY: all clean build install create-migrations library install_all

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

# Alembic migrations
create-migrations: message 
ifndef message
	@echo "Please provide a message for the migration using 'make db-create-migrations message='<your message here>'"
else
	@echo "Creating migrations for Api"
	alembic revision --autogenerate -m "${message}"
endif

install_all:
	@echo "Installing all dependencies..."
	uv pip install -r requirements.lock
