"""
transaction.py

Wallets, Transactions and Digital Signatures
for the Blockchain Project.

Functional-style implementation.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict, field
from typing import Dict, Any

from ecdsa import (
    SigningKey,
    VerifyingKey,
    SECP256k1,
    BadSignatureError,
)


# ==========================================================
# DATA MODELS
# ==========================================================

@dataclass
class Wallet:
    private_key: SigningKey
    public_key: VerifyingKey


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float

    public_key: str = ""
    signature: str = ""

    timestamp: float = field(default_factory=time.time)


# ==========================================================
# WALLET FUNCTIONS
# ==========================================================

def create_wallet() -> Wallet:
    """
    Create a new wallet.
    """

    private_key = SigningKey.generate(
        curve=SECP256k1
    )

    public_key = private_key.verifying_key

    return Wallet(
        private_key=private_key,
        public_key=public_key
    )


def export_private_key(
    wallet: Wallet
) -> str:

    return wallet.private_key.to_string().hex()


def export_public_key(
    wallet: Wallet
) -> str:

    return wallet.public_key.to_string().hex()


def load_private_key(
    private_key_hex: str
) -> SigningKey:

    return SigningKey.from_string(
        bytes.fromhex(private_key_hex),
        curve=SECP256k1
    )


def load_public_key(
    public_key_hex: str
) -> VerifyingKey:

    return VerifyingKey.from_string(
        bytes.fromhex(public_key_hex),
        curve=SECP256k1
    )


def get_wallet_address(
    wallet: Wallet
) -> str:
    """
    Address = SHA256(public_key)
    """

    public_key_hex = export_public_key(
        wallet
    )

    return hashlib.sha256(
        public_key_hex.encode()
    ).hexdigest()


# ==========================================================
# TRANSACTION FUNCTIONS
# ==========================================================

def create_transaction(
    sender: str,
    receiver: str,
    amount: float,
    public_key: str = ""
) -> Transaction:

    return Transaction(
        sender=sender,
        receiver=receiver,
        amount=amount,
        public_key=public_key
    )


def transaction_to_dict(
    tx: Transaction
) -> Dict[str, Any]:

    return {
        "sender": tx.sender,
        "receiver": tx.receiver,
        "amount": tx.amount,
        "public_key": tx.public_key,
        "timestamp": tx.timestamp
    }


def calculate_transaction_hash(
    tx: Transaction
) -> str:

    payload = json.dumps(
        transaction_to_dict(tx),
        sort_keys=True
    )

    return hashlib.sha256(
        payload.encode()
    ).hexdigest()


def sign_transaction(
    tx: Transaction,
    private_key_hex: str
) -> str:

    private_key = load_private_key(
        private_key_hex
    )

    tx_hash = calculate_transaction_hash(
        tx
    )

    signature = private_key.sign(
        tx_hash.encode()
    )

    tx.signature = signature.hex()

    return tx.signature


def verify_transaction_signature(
    tx: Transaction
) -> bool:

    if not tx.signature:
        return False

    try:

        public_key = load_public_key(
            tx.public_key
        )

        tx_hash = calculate_transaction_hash(
            tx
        )

        return public_key.verify(
            bytes.fromhex(tx.signature),
            tx_hash.encode()
        )

    except (
        BadSignatureError,
        ValueError,
        Exception
    ):
        return False


def validate_transaction(
    tx: Transaction
) -> bool:

    if tx.amount <= 0:
        return False

    if tx.sender == tx.receiver:
        return False

    return verify_transaction_signature(
        tx
    )


# ==========================================================
# SERIALIZATION
# ==========================================================

def serialize_transaction(
    tx: Transaction
) -> Dict[str, Any]:

    return asdict(tx)


def deserialize_transaction(
    data: Dict[str, Any]
) -> Transaction:

    return Transaction(
        sender=data["sender"],
        receiver=data["receiver"],
        amount=data["amount"],
        public_key=data.get(
            "public_key",
            ""
        ),
        signature=data.get(
            "signature",
            ""
        ),
        timestamp=data.get(
            "timestamp",
            time.time()
        )
    )


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def create_signed_transaction(
    sender_wallet: Wallet,
    receiver_address: str,
    amount: float
) -> Transaction:

    tx = create_transaction(
        sender=get_wallet_address(
            sender_wallet
        ),
        receiver=receiver_address,
        amount=amount,
        public_key=export_public_key(
            sender_wallet
        )
    )

    sign_transaction(
        tx,
        export_private_key(
            sender_wallet
        )
    )

    return tx


# ==========================================================
# DEMO
# ==========================================================

if __name__ == "__main__":

    alice = create_wallet()
    bob = create_wallet()

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=50
    )

    print("=" * 50)

    print("Alice Address:")
    print(get_wallet_address(alice))

    print("\nBob Address:")
    print(get_wallet_address(bob))

    print("\nTransaction Hash:")
    print(
        calculate_transaction_hash(tx)
    )

    print("\nSignature:")
    print(tx.signature)

    print("\nValid Transaction:")
    print(
        validate_transaction(tx)
    )

    print("=" * 50)