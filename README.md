# Blockchain Project

A complete educational blockchain implementation built in Python.

This project demonstrates the fundamental concepts behind blockchain technology including transactions, digital signatures, Proof-of-Work mining, chain validation, wallet management, and REST APIs.

---

# Features

## Wallet System

* ECDSA (SECP256k1) key generation
* Public/Private key management
* Address generation using SHA-256
* Digital signatures

## Transactions

* Signed transactions
* Signature verification
* Transaction validation
* Transaction serialization/deserialization

## Blocks

* SHA-256 block hashing
* Nonce-based Proof-of-Work
* Block verification
* JSON serialization

## Blockchain

* Genesis block creation
* Transaction mempool
* Mining rewards
* Account-based balances
* Chain validation
* Longest-chain consensus foundation
* Peer registry

## REST API

* Create wallets
* Submit transactions
* Mine blocks
* View blockchain
* View balances
* Register peers

## Testing

* Wallet tests
* Transaction tests
* Block tests
* Mining tests
* Chain validation tests

---

# Project Structure

```text
blockchain_project/
│
├── blockchain/
│   ├── __init__.py
│   ├── transaction.py
│   ├── block.py
│   └── chain.py
│
├── api/
│   ├── __init__.py
│   └── node.py
│
├── tests/
│   └── test_blockchain.py
│
├── data/
│   ├── blocks/
│   ├── wallets/
│   ├── mempool/
│   └── backups/
│
├── logs/
│
├── demo.py
├── requirements.txt
├── install.sh
├── create_structure.sh
├── .env
└── README.md
```

---

# Installation

## Clone Project

```bash
git clone <repository-url>
cd blockchain_project
```

## Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
bash install.sh
```

---

# Running the Demo

```bash
python demo.py
```

The demo performs:

1. Wallet creation
2. Initial funding
3. Transaction creation
4. Transaction validation
5. Mining
6. Reward distribution
7. Chain validation
8. Blockchain export

Expected output:

```text
Alice Balance: 75
Bob Balance: 25
Miner Balance: 50
```

---

# Running the API Node

Start the blockchain node:

```bash
python api/node.py
```

Default server:

```text
http://localhost:5000
```

---

# API Endpoints

## Health Check

```http
GET /
```

---

## Create Wallet

```http
POST /wallet/create
```

Response:

```json
{
    "success": true,
    "address": "wallet_address"
}
```

---

## View Wallets

```http
GET /wallets
```

---

## Check Balance

```http
GET /balance/<address>
```

---

## Submit Transaction

```http
POST /transaction
```

Request:

```json
{
    "sender": "address_1",
    "receiver": "address_2",
    "amount": 25
}
```

---

## View Mempool

```http
GET /mempool
```

---

## Mine Block

```http
POST /mine
```

Request:

```json
{
    "miner_address": "miner_wallet"
}
```

---

## View Blockchain

```http
GET /chain
```

---

## Validate Blockchain

```http
GET /chain/validate
```

---

## Register Peer

```http
POST /peer/register
```

Request:

```json
{
    "peer": "http://127.0.0.1:5001"
}
```

---

## View Peers

```http
GET /peers
```

---

# Running Tests

Execute all tests:

```bash
pytest tests/
```

Verbose output:

```bash
pytest tests/test_blockchain.py -v
```

Coverage:

```bash
pytest --cov=blockchain tests/
```

---

# Blockchain Workflow

```text
Wallet Creation
       │
       ▼
Create Transaction
       │
       ▼
Sign Transaction
       │
       ▼
Validate Transaction
       │
       ▼
Add To Mempool
       │
       ▼
Mine Block
       │
       ▼
Update Balances
       │
       ▼
Validate Chain
```

---

# Configuration

Settings are stored in:

```text
.env
```

Examples:

```env
BLOCKCHAIN_DIFFICULTY=4
MINING_REWARD=50
FLASK_PORT=5000
```

---

# Current Limitations

This project is intended for educational purposes.

Not yet implemented:

* Merkle Trees
* UTXO Model
* Persistent Storage
* SQLite Backend
* Real Peer-to-Peer Networking
* Automatic Peer Discovery
* Smart Contracts
* Distributed Consensus

---

# Future Improvements

Planned enhancements:

* Wallet persistence
* Blockchain persistence
* SQLite database support
* Merkle tree implementation
* UTXO transaction model
* Peer synchronization
* Longest-chain consensus
* Docker deployment
* Blockchain explorer
* Logging framework
* Authentication layer

---

# Technologies Used

* Python
* Flask
* ECDSA
* SHA-256
* PyTest
* JSON
* REST APIs

---

# Learning Objectives

This project demonstrates:

* Blockchain fundamentals
* Cryptographic signatures
* Hashing algorithms
* Proof-of-Work mining
* REST API development
* Distributed systems concepts
* Software testing practices

---

# License

This project is provided for educational and learning purposes.

Feel free to modify, extend, and experiment with the code.
