# ⛓️ Blockchain Project (Python) — V2 Persistent System

A fully functional **single-node blockchain system built from scratch in Python**, featuring **Proof-of-Work mining, ECDSA-based wallets, signed transactions, persistent storage, and a REST API using Flask**.

This project demonstrates real-world blockchain fundamentals including transaction signing, block mining, chain validation, and disk-based persistence.

---

# 🚀 Features

## 🔗 Core Blockchain
- Proof-of-Work (PoW) mining system
- SHA-256 block hashing
- Genesis block creation & recovery
- Chain validation and integrity checks
- Mining reward system
- Account-based balance tracking

---

## 💰 Wallet System
- ECDSA key pair generation
- Secure wallet address derivation
- Wallet import/export support
- Persistent wallet storage (`wallets.json`)
- Wallet management via `WalletManager`

---

## 💳 Transactions
- Digitally signed transactions (ECDSA)
- Transaction validation (signature + balance + rules)
- Mempool for pending transactions
- Persistent mempool storage (`mempool.json`)

---

## ⛏️ Mining System
- Proof-of-Work difficulty system
- Block mining with rewards
- Automatic balance updates after mining
- Transaction bundling into blocks

---

## 💾 Persistence Layer (V2 Major Feature)
- Full system persistence across restarts
- JSON-based storage:
  - `blockchain.json`
  - `wallets.json`
  - `mempool.json`
- Automatic reload on startup
- Storage reset and status APIs

---

## 🌐 REST API (Flask Node)

### Wallet APIs
- POST `/wallet/create`
- GET `/wallets`
- GET `/wallet/<address>`

### Transaction APIs
- POST `/transaction`
- GET `/mempool`

### Blockchain APIs
- POST `/mine`
- GET `/chain`
- GET `/chain/validate`
- GET `/chain/export`

### Network APIs
- POST `/peer/register`
- GET `/peers`

### Storage APIs (V2 Feature)
- GET `/storage/status`
- POST `/storage/reset`

### Debug APIs
- GET `/stats`

---

# 🧪 Testing

The system is fully tested with **30 passing tests**:

## Blockchain Tests
- 17/17 passed

## Wallet System Tests
- 8/8 passed (`test_wallet_tester.py`)

## Storage & Persistence Tests
- 5/5 passed (`test_storage.py`)

### ✅ Total
30/30 tests passing


---

# 📁 Project Structure
blockchain_project/
│
├── blockchain/
│ ├── chain.py
│ ├── block.py
│ ├── transaction.py
│ ├── storage.py
│ └── wallet_manager.py
│
├── api/
│ └── node.py
│
├── data/
│ ├── blockchain.json
│ ├── wallets.json
│ └── mempool.json
│
├── tests/
│ ├── test_blockchain.py
│ ├── test_wallet_tester.py
│ └── test_storage.py
│
├── demo.py
├── requirements.txt
└── README.md


---

# ▶️ Running the Project

## Install dependencies
```bash
pip install -r requirements.txt

Start API server
python api/node.py

Server runs at:

http://127.0.0.1:5000
🔌 API Overview
Wallets
Create wallet
List wallets
Get wallet details
Transactions
Submit signed transactions
View mempool
Mining
Mine pending transactions
Receive mining rewards
Blockchain
View full chain
Validate chain integrity
Export chain JSON
System
View stats
Reset storage
Check persistence status
⚙️ How it works
Wallets are created using ECDSA key pairs
Transactions are signed using private keys
Transactions enter mempool after validation
Miners collect transactions into blocks
Proof-of-Work secures block creation
Blocks are appended to the chain
All state is persisted to disk (V2 feature)
⚠️ Limitations (Current Version)
Single-node system (no networking yet)
No distributed consensus (V3 feature)
No smart contracts
No Merkle trees (simplified implementation)
🚀 Future Improvements (V3 Roadmap)
Multi-node peer-to-peer network
Chain synchronization between nodes
Consensus algorithm (longest valid chain rule)
Node discovery system
Distributed mining simulation
Blockchain explorer UI
📜 License

Educational project for learning blockchain internals.

👨‍💻 Author

Built as a deep systems-learning project to understand blockchain architecture, cryptography, distributed systems, and persistence engineering.
