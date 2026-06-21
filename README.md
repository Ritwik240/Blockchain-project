# ⛓️ Blockchain Project (Python MVP)

A functional blockchain implementation built from scratch in Python, featuring proof-of-work mining, wallet generation using ECDSA, and a REST API using Flask.

This project demonstrates the core principles behind blockchain systems including transactions, mining, and chain validation.

---

## 🚀 Features

### Core Blockchain
- Proof-of-Work (PoW) mining
- SHA-256 block hashing
- Chain validation
- Genesis block creation
- Mining difficulty system

### Wallet System
- ECDSA-based key pair generation
- Wallet address creation
- In-memory wallet storage

### Transactions
- Signed transactions using private keys
- Transaction validation
- Mempool (pending transactions queue)

### REST API (Flask)
- Create wallet
- View wallets
- Submit transactions
- Mine blocks
- View blockchain
- Check balances
- Validate chain
- View network stats

### Testing
- Unit tests for blockchain logic
- Transaction validation tests
- Mining workflow tests
- Chain integrity tests

---

## Project Structure

```
blockchain_project/
│
├── blockchain/         # Core blockchain logic
├── api/                # Flask REST API node
├── tests/              # Unit tests
├── demo.py             # End-to-end blockchain demo
├── requirements.txt    # Dependencies
└── README.md
```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/blockchain-project.git
cd blockchain-project
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

##  Running the Project

### Start the API server
```bash
python -m api.node
```

Server runs at:
```
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

### Health Check
```
GET /
```

### Create Wallet
```
POST /wallet/create
```

### View Wallets
```
GET /wallets
```

### Send Transaction
```
POST /transaction
```

### Mine Block
```
POST /mine
```

### View Blockchain
```
GET /chain
```

### Validate Chain
```
GET /chain/validate
```

### Network Stats
```
GET /stats
```

---

## Run Tests

```bash
pytest -v
```

Expected output:
```
17 tests passed
```

---

## How it works (simplified)

1. A wallet is created using cryptographic key pairs (ECDSA)
2. Transactions are signed and validated
3. Valid transactions are added to a mempool
4. Miners collect transactions into a block
5. Proof-of-Work ensures computational difficulty
6. Block is added to the chain after validation

---

## Limitations (Current Version)

- No persistent storage (data resets on restart)
- Single-node system (no peer-to-peer networking)
- No smart contracts
- Basic consensus placeholder only

---

## Future Improvements

- Persistent storage (JSON / SQLite)
- Multi-node peer-to-peer networking
- Full consensus algorithm (longest chain rule)
- Merkle trees for transaction integrity
- Docker deployment
- Blockchain explorer UI

---

## License

This project is for educational purposes.

---

##  Author

Built as a learning project to understand blockchain internals from scratch.
