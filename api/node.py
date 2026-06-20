"""
api/node.py

Blockchain Node REST API

Features
--------
- Health Check
- Wallet Creation
- Submit Transactions
- View Mempool
- Mine Blocks
- View Blockchain
- Check Balances
- Register Peers
- View Peers
- Replace Chain (Consensus)
- Export Blockchain

Run:
    python api/node.py
"""

from __future__ import annotations

from flask import request, jsonify

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from api import create_app

from blockchain.chain import (
    create_blockchain
)

from blockchain.transaction import (
    create_wallet,
    get_wallet_address,
    create_signed_transaction,
)

from blockchain.block import (
    serialize_block
)


# ==========================================================
# APP INITIALIZATION
# ==========================================================

app = create_app()

blockchain = create_blockchain(
    difficulty=4,
    mining_reward=50.0
)

wallet_store = {}


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route(
    "/",
    methods=["GET"]
)
def health_check():

    return jsonify({
        "status": "online",
        "service": "blockchain-node",
        "chain_length": blockchain.get_chain_length(),
        "pending_transactions": len(
            blockchain.get_pending_transactions()
        )
    })


# ==========================================================
# WALLET ENDPOINTS
# ==========================================================

@app.route(
    "/wallet/create",
    methods=["POST"]
)
def create_wallet_endpoint():

    wallet = create_wallet()

    address = get_wallet_address(
        wallet
    )

    wallet_store[address] = wallet

    return jsonify({
        "success": True,
        "address": address
    })


@app.route(
    "/wallets",
    methods=["GET"]
)
def get_wallets():

    return jsonify({
        "wallets": list(
            wallet_store.keys()
        )
    })


# ==========================================================
# BALANCE ENDPOINTS
# ==========================================================

@app.route(
    "/balance/<address>",
    methods=["GET"]
)
def get_balance(address):

    balance = blockchain.get_balance(
        address
    )

    return jsonify({
        "address": address,
        "balance": balance
    })


# ==========================================================
# TRANSACTION ENDPOINTS
# ==========================================================

@app.route(
    "/transaction",
    methods=["POST"]
)
def create_transaction_endpoint():

    data = request.get_json()

    required_fields = [
        "sender",
        "receiver",
        "amount"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"Missing field: {field}"
            }), 400

    sender = data["sender"]
    receiver = data["receiver"]
    amount = float(
        data["amount"]
    )

    if sender not in wallet_store:

        return jsonify({
            "success": False,
            "message": "Sender wallet not found."
        }), 404

    transaction = (
        create_signed_transaction(
            sender_wallet=wallet_store[
                sender
            ],
            receiver_address=receiver,
            amount=amount
        )
    )

    success = blockchain.add_transaction(
        transaction
    )

    if not success:

        return jsonify({
            "success": False,
            "message":
            "Transaction validation failed."
        }), 400

    return jsonify({
        "success": True,
        "message":
        "Transaction added to mempool."
    })


@app.route(
    "/mempool",
    methods=["GET"]
)
def get_mempool():

    transactions = []

    for tx in blockchain.get_pending_transactions():

        transactions.append(
            tx.serialize()
            if hasattr(tx, "serialize")
            else tx.__dict__
        )

    return jsonify({
        "pending_transactions":
        transactions
    })


# ==========================================================
# MINING
# ==========================================================

@app.route(
    "/mine",
    methods=["POST"]
)
def mine_block_endpoint():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message":
            "Miner address required."
        }), 400

    miner_address = data.get(
        "miner_address"
    )

    if not miner_address:

        return jsonify({
            "success": False,
            "message":
            "miner_address missing."
        }), 400

    block = (
        blockchain.mine_pending_transactions(
            miner_address
        )
    )

    if block is None:

        return jsonify({
            "success": False,
            "message":
            "No transactions available."
        }), 400

    return jsonify({
        "success": True,
        "block":
        serialize_block(block)
    })


# ==========================================================
# BLOCKCHAIN
# ==========================================================

@app.route(
    "/chain",
    methods=["GET"]
)
def get_chain():

    return jsonify({
        "length":
        blockchain.get_chain_length(),
        "chain":
        blockchain.export_chain()
    })


@app.route(
    "/chain/validate",
    methods=["GET"]
)
def validate_chain():

    valid = blockchain.is_chain_valid()

    return jsonify({
        "valid": valid
    })


@app.route(
    "/chain/export",
    methods=["GET"]
)
def export_chain():

    return blockchain.to_json()


# ==========================================================
# PEERS
# ==========================================================

@app.route(
    "/peer/register",
    methods=["POST"]
)
def register_peer():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False
        }), 400

    peer = data.get(
        "peer"
    )

    if not peer:

        return jsonify({
            "success": False
        }), 400

    blockchain.add_peer(peer)

    return jsonify({
        "success": True,
        "peer": peer
    })


@app.route(
    "/peers",
    methods=["GET"]
)
def get_peers():

    return jsonify({
        "peers":
        blockchain.get_peers()
    })


# ==========================================================
# CONSENSUS
# ==========================================================

@app.route(
    "/consensus/replace",
    methods=["POST"]
)
def replace_chain():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False
        }), 400

    return jsonify({
        "success": True,
        "message":
        "Consensus endpoint ready."
    })


# ==========================================================
# DEBUG ENDPOINTS
# ==========================================================

@app.route(
    "/stats",
    methods=["GET"]
)
def network_stats():

    return jsonify({
        "difficulty":
        blockchain.difficulty,

        "mining_reward":
        blockchain.mining_reward,

        "chain_length":
        blockchain.get_chain_length(),

        "mempool_size":
        len(
            blockchain.get_pending_transactions()
        ),

        "peer_count":
        len(
            blockchain.get_peers()
        ),

        "wallet_count":
        len(
            wallet_store
        )
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