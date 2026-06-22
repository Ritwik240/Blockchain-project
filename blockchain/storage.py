"""
blockchain/storage.py

Persistence Layer for Blockchain V2

Features
--------
- Save blockchain to JSON
- Load blockchain from JSON
- Save wallets
- Load wallets
- Save mempool
- Load mempool
- Automatic directory creation

Data Files
----------
data/
├── blockchain.json
├── wallets.json
└── mempool.json
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

BLOCKCHAIN_FILE = os.path.join(
    DATA_DIR,
    "blockchain.json"
)

WALLETS_FILE = os.path.join(
    DATA_DIR,
    "wallets.json"
)

MEMPOOL_FILE = os.path.join(
    DATA_DIR,
    "mempool.json"
)


# ==========================================================
# DIRECTORY MANAGEMENT
# ==========================================================

def ensure_data_directory() -> None:
    """
    Create data directory if missing.
    """

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )


# ==========================================================
# GENERIC JSON HELPERS
# ==========================================================

def save_json(
    file_path: str,
    data: Any
) -> bool:
    """
    Save data to JSON file.
    """

    try:

        ensure_data_directory()

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        return True

    except Exception as error:

        print(
            f"[SAVE ERROR] {error}"
        )

        return False


def load_json(
    file_path: str,
    default: Any
) -> Any:
    """
    Load JSON data safely.
    """

    try:

        if not os.path.exists(
            file_path
        ):
            return default

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception as error:

        print(
            f"[LOAD ERROR] {error}"
        )

        return default


# ==========================================================
# BLOCKCHAIN STORAGE
# ==========================================================

def save_blockchain(
    blockchain_data: List[Dict]
) -> bool:
    """
    Save blockchain.
    """

    return save_json(
        BLOCKCHAIN_FILE,
        blockchain_data
    )


def load_blockchain() -> List[Dict]:
    """
    Load blockchain.
    """

    return load_json(
        BLOCKCHAIN_FILE,
        []
    )


# ==========================================================
# WALLET STORAGE
# ==========================================================

def save_wallets(
    wallet_data: Dict
) -> bool:
    """
    Save wallets.
    """

    return save_json(
        WALLETS_FILE,
        wallet_data
    )


def load_wallets() -> Dict:
    """
    Load wallets.
    """

    return load_json(
        WALLETS_FILE,
        {}
    )


# ==========================================================
# MEMPOOL STORAGE
# ==========================================================

def save_mempool(
    mempool_data: List[Dict]
) -> bool:
    """
    Save pending transactions.
    """

    return save_json(
        MEMPOOL_FILE,
        mempool_data
    )


def load_mempool() -> List[Dict]:
    """
    Load pending transactions.
    """

    return load_json(
        MEMPOOL_FILE,
        []
    )


# ==========================================================
# RESET STORAGE
# ==========================================================

def reset_storage() -> None:
    """
    Delete all saved blockchain data.
    """

    files = [
        BLOCKCHAIN_FILE,
        WALLETS_FILE,
        MEMPOOL_FILE
    ]

    for file_path in files:

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )


# ==========================================================
# STORAGE STATUS
# ==========================================================

def storage_status() -> Dict:
    """
    Return storage file information.
    """

    return {
        "blockchain_exists":
            os.path.exists(
                BLOCKCHAIN_FILE
            ),

        "wallets_exists":
            os.path.exists(
                WALLETS_FILE
            ),

        "mempool_exists":
            os.path.exists(
                MEMPOOL_FILE
            ),

        "data_directory":
            DATA_DIR
    }