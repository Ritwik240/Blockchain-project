"""
api/node.py

Blockchain Node REST API (V2 Final)
"""

from __future__ import annotations

from flask import request, jsonify
import os
import sys

# ==========================================================
# PROJECT ROOT SETUP
# ==========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from api import create_app

from blockchain.chain import create_blockchain
from blockchain.block import serialize_block
from blockchain.transaction import create_signed_transaction

from blockchain.wallet_manager import WalletManager
from blockchain.storage import storage_status, reset_storage


# ==========================================================
# APP INITIALIZATION
# ==========================================================

app = create_app()

blockchain = create_blockchain(
    difficulty=4,
    mining_reward=50.0
)

wallet_manager = WalletManager()


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online",
        "service": "blockchain-node",
        "chain_length": blockchain.get_chain_length(),
        "pending_transactions": len(blockchain.get_pending_transactions())
    })


# ==========================================================
# WALLET ENDPOINTS
# ==========================================================

@app.route("/wallet/create", methods=["POST"])
def create_wallet_endpoint():

    address = wallet_manager.create_new_wallet()

    wallet = wallet_manager.get_wallet(address)

    return jsonify({
        "success": True,
        "address": address,
        "public_key": wallet["public_key"]
    })


@app.route("/wallets", methods=["GET"])
def get_wallets():

    return jsonify({
        "wallets": list(wallet_manager.list_wallets().keys())
    })


@app.route("/wallet/<address>", methods=["GET"])
def get_wallet(address):

    wallet = wallet_manager.get_wallet(address)

    if wallet is None:
        return jsonify({
            "success": False,
            "message": "Wallet not found"
        }), 404

    return jsonify({
        "success": True,
        "wallet": wallet
    })


# ==========================================================
# BALANCE
# ==========================================================

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):

    return jsonify({
        "address": address,
        "balance": blockchain.get_balance(address)
    })


# ==========================================================
# TRANSACTION
# ==========================================================

@app.route("/transaction", methods=["POST"])
def create_transaction_endpoint():

    data = request.get_json()

    required = ["sender", "receiver", "amount"]

    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    for field in required:
        if field not in data:
            return jsonify({
                "success": False,
                "message": f"Missing field: {field}"
            }), 400

    sender = data["sender"]
    receiver = data["receiver"]
    amount = float(data["amount"])

    sender_wallet = wallet_manager.restore_wallet(sender)

    if sender_wallet is None:
        return jsonify({
            "success": False,
            "message": "Sender wallet not found"
        }), 404

    tx = create_signed_transaction(
        sender_wallet=sender_wallet,
        receiver_address=receiver,
        amount=amount
    )

    success = blockchain.add_transaction(tx)

    if not success:
        return jsonify({
            "success": False,
            "message": "Transaction rejected"
        }), 400

    return jsonify({
        "success": True,
        "message": "Transaction added to mempool"
    })


# ==========================================================
# MEMPOOL
# ==========================================================

@app.route("/mempool", methods=["GET"])
def get_mempool():

    transactions = []

    for tx in blockchain.get_pending_transactions():
        transactions.append(
            serialize_block(tx) if hasattr(tx, "serialize") else tx.__dict__
        )

    return jsonify({
        "pending_transactions": transactions
    })


# ==========================================================
# MINING
# ==========================================================

@app.route("/mine", methods=["POST"])
def mine_block():

    data = request.get_json()

    if not data or "miner_address" not in data:
        return jsonify({
            "success": False,
            "message": "miner_address required"
        }), 400

    block = blockchain.mine_pending_transactions(
        data["miner_address"]
    )

    if block is None:
        return jsonify({
            "success": False,
            "message": "No transactions to mine"
        }), 400

    return jsonify({
        "success": True,
        "block": serialize_block(block)
    })


# ==========================================================
# CHAIN
# ==========================================================

@app.route("/chain", methods=["GET"])
def get_chain():

    return jsonify({
        "length": blockchain.get_chain_length(),
        "chain": blockchain.export_chain()
    })


@app.route("/chain/validate", methods=["GET"])
def validate_chain():

    return jsonify({
        "valid": blockchain.is_chain_valid()
    })


@app.route("/chain/export", methods=["GET"])
def export_chain():

    return blockchain.to_json()


# ==========================================================
# PEERS
# ==========================================================

@app.route("/peer/register", methods=["POST"])
def register_peer():

    data = request.get_json()

    if not data or "peer" not in data:
        return jsonify({"success": False}), 400

    blockchain.add_peer(data["peer"])

    return jsonify({
        "success": True,
        "peer": data["peer"]
    })


@app.route("/peers", methods=["GET"])
def get_peers():

    return jsonify({
        "peers": blockchain.get_peers()
    })


# ==========================================================
# STORAGE (NEW V2 FEATURE)
# ==========================================================

@app.route("/storage/status", methods=["GET"])
def storage_status_endpoint():

    return jsonify(storage_status())


@app.route("/storage/reset", methods=["POST"])
def reset_storage_endpoint():

    global blockchain
    global wallet_manager

    reset_storage()

    blockchain = create_blockchain(
        difficulty=4,
        mining_reward=50.0
    )

    wallet_manager = WalletManager()

    return jsonify({
        "success": True
    })


# ==========================================================
# STATS
# ==========================================================

@app.route("/stats", methods=["GET"])
def stats():

    return jsonify({
        "difficulty": blockchain.difficulty,
        "mining_reward": blockchain.mining_reward,
        "chain_length": blockchain.get_chain_length(),
        "mempool_size": len(blockchain.get_pending_transactions()),
        "peer_count": len(blockchain.get_peers()),
        "wallet_count": wallet_manager.wallet_count()
    })


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )