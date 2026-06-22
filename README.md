⛓️ Blockchain Project (Python MVP → V2 Persistent System)

A fully functional blockchain system built from scratch in Python, evolving from a simple MVP into a persistent, API-driven blockchain architecture.

This project demonstrates core blockchain principles including cryptographic wallets, signed transactions, proof-of-work mining, and persistent storage.

🚀 V2 Major Upgrade (What Changed)

This version upgrades the system from an in-memory prototype to a fully persistent blockchain system.

Added in V2:
Persistent blockchain storage (blockchain.json)
Persistent wallet storage (wallets.json)
Persistent mempool (mempool.json)
WalletManager system for secure wallet handling
Storage layer for save/load/reset operations
REST API integration with persistence support
Full system recovery after restart
Storage status and reset endpoints
Expanded test suite (30 tests passing)
🚀 Features
⛓️ Core Blockchain
Proof-of-Work (PoW) mining
SHA-256 block hashing
Genesis block creation
Chain validation
Difficulty-based mining
Block integrity verification
👛 Wallet System
ECDSA key pair generation
Wallet address creation (SHA-256 of public key)
WalletManager with persistence
Import/export private keys
Wallet lookup and deletion
Automatic wallet saving
💸 Transactions
Digital signatures using ECDSA
Transaction validation
Balance verification before sending
Mempool for pending transactions
Secure signed transaction creation
🌐 REST API (Flask Node)
Wallet creation and management
Transaction submission
Mining endpoint
Blockchain viewer
Balance checking
Peer registration system
Storage status monitoring
Storage reset functionality
💾 Persistence Layer
Blockchain automatically saved to disk
Wallets persist across restarts
Mempool persistence
Automatic recovery on startup
Full system reset capability
🧪 Testing
Blockchain integrity tests
Transaction validation tests
Mining workflow tests
Wallet system tests (8 tests)
Storage persistence tests
Full system reload verification tests
📁 Project Structure

blockchain_project/
│
├── blockchain/
│ ├── chain.py
│ ├── block.py
│ ├── transaction.py
│ ├── storage.py (V2 - persistence layer)
│ └── wallet_manager.py (V2 - wallet system)
│
├── api/
│ └── node.py
│
├── tests/
│ ├── test_blockchain.py
│ ├── test_storage.py
│ └── test_wallet_tester.py
│
├── data/
│ ├── blockchain.json
│ ├── wallets.json
│ └── mempool.json
│
├── requirements.txt
└── README.md

⚙️ Installation
Clone repository:
git clone https://github.com/<your-username>/blockchain-project.git
cd blockchain-project
Create virtual environment:
python -m venv venv
source venv/bin/activate (Mac/Linux)
venv\Scripts\activate (Windows)
Install dependencies:
pip install -r requirements.txt
▶️ Running the Project

Start the API server:
python -m api.node

Server runs at:
http://127.0.0.1:5000

🔌 API Endpoints
Core
GET / → Health check
GET /chain → View blockchain
GET /chain/validate → Validate chain
Wallets
POST /wallet/create → Create wallet
GET /wallets → List wallets
GET /wallet/<address> → Get wallet details
Transactions
POST /transaction → Send transaction
GET /mempool → View pending transactions
Mining
POST /mine → Mine pending transactions
Network
POST /peer/register → Register peer
GET /peers → View peers
Storage (NEW in V2)
GET /storage/status → Check storage state
POST /storage/reset → Reset all data
🧠 How it works (Simplified)
Wallet is created using ECDSA key pair
Transactions are signed with private key
Valid transactions enter the mempool
Miner collects transactions into a block
Proof-of-Work secures the block
Block is added to chain
Data is persisted to disk automatically
⚠️ Limitations (Current Version)
Single-node system (no real networking yet)
No smart contracts
Basic consensus placeholder
No Merkle tree optimization
🚀 Future Improvements (V3+)
Peer-to-peer networking
Distributed consensus (longest chain rule)
Node discovery system
Chain synchronization across nodes
Smart contract layer
Docker deployment
Blockchain explorer UI
📌 Status

✔ 30/30 tests passing
✔ Fully persistent blockchain system
✔ Wallet + storage architecture complete
✔ REST API integrated
✔ V2 complete and stable

👨‍💻 Author

Built as a learning project to deeply understand blockchain systems from scratch, including cryptography, consensus basics, and system design principles.
