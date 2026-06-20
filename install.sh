#!/usr/bin/env bash

# ==========================================================

# Blockchain Project Installer

# ==========================================================

set -e

PROJECT_NAME="blockchain_project"
PYTHON_MIN_VERSION="3.10"

echo "=================================================="
echo " Blockchain Project Setup"
echo "=================================================="
echo ""

# ----------------------------------------------------------

# Check Python

# ----------------------------------------------------------

if ! command -v python3 &> /dev/null
then
echo "[ERROR] Python3 not found."
exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

echo "[INFO] Python Version: $PYTHON_VERSION"

# ----------------------------------------------------------

# Create Virtual Environment

# ----------------------------------------------------------

if [ ! -d "venv" ]; then
echo "[INFO] Creating virtual environment..."
python3 -m venv venv
else
echo "[INFO] Virtual environment already exists."
fi

# ----------------------------------------------------------

# Activate Environment

# ----------------------------------------------------------

echo "[INFO] Activating virtual environment..."

source venv/bin/activate

# ----------------------------------------------------------

# Upgrade Package Tools

# ----------------------------------------------------------

echo "[INFO] Upgrading pip tools..."

python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install --upgrade wheel

# ----------------------------------------------------------

# Install Requirements

# ----------------------------------------------------------

if [ ! -f "requirements.txt" ]; then
echo "[ERROR] requirements.txt not found."
exit 1
fi

echo "[INFO] Installing dependencies..."

pip install -r requirements.txt

# ----------------------------------------------------------

# Create Runtime Directories

# ----------------------------------------------------------

echo "[INFO] Creating project directories..."

mkdir -p logs
mkdir -p data
mkdir -p data/blocks
mkdir -p data/wallets
mkdir -p data/backups
mkdir -p data/mempool
mkdir -p docs

# ----------------------------------------------------------

# Environment File

# ----------------------------------------------------------

if [ ! -f ".env" ]; then

cat <<EOF > .env
FLASK_ENV=development
HOST=0.0.0.0
PORT=5000

MINING_DIFFICULTY=4
MINING_REWARD=50

DATABASE_URL=sqlite:///blockchain.db
EOF

echo "[INFO] Created .env file"

else
echo "[INFO] Existing .env found"
fi

# ----------------------------------------------------------

# Initialize Database File

# ----------------------------------------------------------

if [ ! -f "blockchain.db" ]; then
touch blockchain.db
fi

# ----------------------------------------------------------

# Verify Critical Packages

# ----------------------------------------------------------

echo "[INFO] Verifying installation..."

python - <<EOF
import flask
import requests
import ecdsa
import sqlalchemy

print("Flask:", flask.**version**)
print("Requests:", requests.**version**)
print("ECDSA: OK")
print("SQLAlchemy:", sqlalchemy.**version**)
print("Dependency verification successful.")
EOF

# ----------------------------------------------------------

# Run Tests If Present

# ----------------------------------------------------------

if [ -d "tests" ]; then
echo "[INFO] Running test discovery..."
pytest tests || true
fi

# ----------------------------------------------------------

# Success Message

# ----------------------------------------------------------

echo ""
echo "=================================================="
echo " Installation Complete"
echo "=================================================="
echo ""
echo "Activate environment:"
echo ""
echo "    source venv/bin/activate"
echo ""
echo "Run node:"
echo ""
echo "    python api/node.py"
echo ""
echo "Run demo:"
echo ""
echo "    python demo.py"
echo ""
echo "Run tests:"
echo ""
echo "    pytest tests"
echo ""
echo "=================================================="
