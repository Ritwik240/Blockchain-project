"""
blockchain/__init__.py

Blockchain Package Exports
"""

# ==========================================================
# TRANSACTIONS & WALLETS
# ==========================================================

from .transaction import (
    Wallet,
    Transaction,
    create_wallet,
    get_wallet_address,
    export_private_key,
    export_public_key,
    load_private_key,
    load_public_key,
    create_transaction,
    create_signed_transaction,
    calculate_transaction_hash,
    sign_transaction,
    verify_transaction_signature,
    validate_transaction,
    serialize_transaction,
    deserialize_transaction,
)

# ==========================================================
# BLOCKS
# ==========================================================

from .block import (
    Block,
    create_block,
    calculate_block_hash,
    mine_block,
    verify_block,
    serialize_block,
    deserialize_block,
    save_block_to_file,
    load_block_from_file,
)

# ==========================================================
# BLOCKCHAIN
# ==========================================================

from .chain import (
    Blockchain,
    create_blockchain,
)

# ==========================================================
# PACKAGE VERSION
# ==========================================================

__version__ = "1.0.0"

# ==========================================================
# PUBLIC EXPORTS
# ==========================================================

__all__ = [

    # Wallet
    "Wallet",
    "create_wallet",
    "get_wallet_address",
    "export_private_key",
    "export_public_key",
    "load_private_key",
    "load_public_key",

    # Transaction
    "Transaction",
    "create_transaction",
    "create_signed_transaction",
    "calculate_transaction_hash",
    "sign_transaction",
    "verify_transaction_signature",
    "validate_transaction",
    "serialize_transaction",
    "deserialize_transaction",

    # Block
    "Block",
    "create_block",
    "calculate_block_hash",
    "mine_block",
    "verify_block",
    "serialize_block",
    "deserialize_block",
    "save_block_to_file",
    "load_block_from_file",

    # Blockchain
    "Blockchain",
    "create_blockchain",
]