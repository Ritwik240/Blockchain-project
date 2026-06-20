"""
block.py

Core Block implementation for the Blockchain Project.

Features:
- Block Data Structure
- SHA-256 Hashing
- Proof of Work (PoW)
- Serialization / Deserialization
- Compatible with chain.py, node.py, tests, and demo.py
"""

from __future__ import annotations

import hashlib
import json
import time

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from blockchain.transaction import (
    Transaction,
    serialize_transaction,
    deserialize_transaction
)


# ==========================================================
# BLOCK MODEL
# ==========================================================

@dataclass
class Block:
    """
    Basic block structure.
    """

    index: int

    transactions: List[Transaction]

    previous_hash: str

    timestamp: float = field(
        default_factory=time.time
    )

    nonce: int = 0

    hash: str = ""


# ==========================================================
# BLOCK FUNCTIONS
# ==========================================================

def block_to_dict(
    block: Block
) -> Dict[str, Any]:
    """
    Convert block to dictionary.
    """

    return {
        "index": block.index,
        "timestamp": block.timestamp,
        "previous_hash": block.previous_hash,
        "nonce": block.nonce,
        "hash": block.hash,
        "transactions": [
            serialize_transaction(tx)
            for tx in block.transactions
        ]
    }


def calculate_block_hash(
    block: Block
) -> str:
    """
    Calculate SHA256 hash of block contents.
    """

    block_data = {
        "index": block.index,
        "timestamp": block.timestamp,
        "previous_hash": block.previous_hash,
        "nonce": block.nonce,
        "transactions": [
            serialize_transaction(tx)
            for tx in block.transactions
        ]
    }

    encoded = json.dumps(
        block_data,
        sort_keys=True
    ).encode()

    return hashlib.sha256(
        encoded
    ).hexdigest()


def create_block(
    index: int,
    transactions: List[Transaction],
    previous_hash: str
) -> Block:
    """
    Create a new block.
    """

    return Block(
        index=index,
        transactions=transactions,
        previous_hash=previous_hash
    )


def mine_block(
    block: Block,
    difficulty: int
) -> str:
    """
    Proof-of-Work mining.
    """

    target = "0" * difficulty

    while True:

        block.hash = (
            calculate_block_hash(block)
        )

        if block.hash.startswith(
            target
        ):
            return block.hash

        block.nonce += 1


def verify_block(
    block: Block,
    difficulty: int
) -> bool:
    """
    Verify mined block.
    """

    expected_hash = (
        calculate_block_hash(block)
    )

    if block.hash != expected_hash:
        return False

    if not block.hash.startswith(
        "0" * difficulty
    ):
        return False

    return True


# ==========================================================
# SERIALIZATION
# ==========================================================

def serialize_block(
    block: Block
) -> Dict[str, Any]:

    return block_to_dict(block)


def deserialize_block(
    data: Dict[str, Any]
) -> Block:

    transactions = [
        deserialize_transaction(tx)
        for tx in data["transactions"]
    ]

    return Block(
        index=data["index"],
        transactions=transactions,
        previous_hash=data["previous_hash"],
        timestamp=data["timestamp"],
        nonce=data["nonce"],
        hash=data["hash"]
    )


# ==========================================================
# PERSISTENCE HELPERS
# ==========================================================

def save_block_to_file(
    block: Block,
    filepath: str
) -> None:
    """
    Save block as JSON.
    """

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            serialize_block(block),
            file,
            indent=4
        )


def load_block_from_file(
    filepath: str
) -> Block:
    """
    Load block from JSON file.
    """

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return deserialize_block(
        data
    )


# ==========================================================
# DEMO
# ==========================================================

if __name__ == "__main__":

    from blockchain.transaction import (
        create_wallet,
        create_signed_transaction,
        get_wallet_address
    )

    alice = create_wallet()
    bob = create_wallet()

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=50
    )

    block = create_block(
        index=1,
        transactions=[tx],
        previous_hash="0" * 64
    )

    print("Mining block...")

    mine_block(
        block,
        difficulty=4
    )

    print("\nBlock mined successfully.")
    print("Block Hash:")
    print(block.hash)

    print("\nVerification:")
    print(
        verify_block(
            block,
            difficulty=4
        )
    )