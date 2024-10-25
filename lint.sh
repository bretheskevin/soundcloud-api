#!/bin/bash
CONTAINER_NAME="soundcloud-api-web-1"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'


print_header() {
    echo -e "\n${YELLOW}=== $1 ===${NC}\n"
}

docker_exec() {
    docker exec -i $CONTAINER_NAME $@
}

if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "Container $CONTAINER_NAME is not running!"
    echo "Please start the container with: docker-compose up -d"
    exit 1
fi

print_header "Running Black (Code Formatting)"
docker_exec black .

print_header "Running isort (Import Sorting)"
docker_exec isort .

print_header "Running MyPy (Type Checking)"
docker_exec mypy .

print_header "Running Flake8 (Style Guide)"
docker_exec flake8 .

print_header "Running Pylint"
docker_exec pylint app/

echo -e "\n${GREEN}All linting checks completed!${NC}"
