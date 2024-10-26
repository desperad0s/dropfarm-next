#!/bin/bash

# Function to create directory and its parent directories
make_dir() {
    mkdir -p "$1"
    echo "Created directory: $1"
}

# Function to create file with parent directories
make_file() {
    mkdir -p "$(dirname "$1")"
    touch "$1"
    echo "Created file: $1"
}

# Root level files (don't overwrite existing .env and .gitignore)
make_file "docker-compose.yml"
make_file "README.md"

# Backend structure
make_dir "backend/app/api/endpoints"
make_dir "backend/app/core"
make_dir "backend/app/models"
make_dir "backend/app/services"
make_dir "backend/app/schemas"
make_dir "backend/app/utils"

# Backend files
make_file "backend/Dockerfile"
make_file "backend/requirements.txt"
make_file "backend/pytest.ini"

make_file "backend/app/main.py"
make_file "backend/app/__init__.py"

make_file "backend/app/api/__init__.py"
make_file "backend/app/api/router.py"
make_file "backend/app/api/deps.py"
make_file "backend/app/api/endpoints/__init__.py"
make_file "backend/app/api/endpoints/auth.py"
make_file "backend/app/api/endpoints/automation.py"
make_file "backend/app/api/endpoints/status.py"

make_file "backend/app/core/__init__.py"
make_file "backend/app/core/auth.py"
make_file "backend/app/core/config.py"
make_file "backend/app/core/browser.py"
make_file "backend/app/core/recorder.py"
make_file "backend/app/core/player.py"

make_file "backend/app/models/__init__.py"
make_file "backend/app/models/routine.py"
make_file "backend/app/models/user.py"

make_file "backend/app/services/__init__.py"
make_file "backend/app/services/automation.py"
make_file "backend/app/services/monitoring.py"

make_file "backend/app/schemas/__init__.py"
make_file "backend/app/schemas/routine.py"
make_file "backend/app/schemas/user.py"

make_file "backend/app/utils/__init__.py"
make_file "backend/app/utils/helpers.py"

# Test structure
make_dir "tests/backend/test_api"

make_file "tests/backend/__init__.py"
make_file "tests/backend/conftest.py"
make_file "tests/backend/test_api/test_automation.py"

echo "Project structure created successfully!"