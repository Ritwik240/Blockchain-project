#!/usr/bin/env bash

echo "Creating blockchain project structure..."

mkdir -p blockchain_project

cd blockchain_project || exit

# Directories

mkdir -p blockchain
mkdir -p api
mkdir -p tests

mkdir -p data/blocks
mkdir -p data/wallets
mkdir -p data/mempool
mkdir -p data/backups

mkdir -p logs

# Blockchain files

touch blockchain/**init**.py
touch blockchain/transaction.py
touch blockchain/block.py
touch blockchain/chain.py

# API files

touch api/**init**.py
touch api/node.py

# Tests

touch tests/test_blockchain.py

# Root files

touch demo.py
touch requirements.txt
touch README.md
touch .env

echo "Project structure created successfully."
