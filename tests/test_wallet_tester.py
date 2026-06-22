"""
tests/test_wallet_manager.py
"""

import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)

from blockchain.wallet_manager import (
    WalletManager,
)

from blockchain.storage import (
    reset_storage,
)

from blockchain.transaction import (
    create_wallet,
    export_private_key,
)


# ==========================================================
# CLEAN STORAGE
# ==========================================================

@pytest.fixture(autouse=True)
def clean_storage():

    reset_storage()

    yield

    reset_storage()


# ==========================================================
# CREATE WALLET
# ==========================================================

def test_create_wallet():

    manager = WalletManager()

    address = (
        manager.create_new_wallet()
    )

    assert address is not None

    assert (
        manager.wallet_count()
        == 1
    )

    assert (
        manager.get_wallet(address)
        is not None
    )


# ==========================================================
# WALLET COUNT
# ==========================================================

def test_wallet_count():

    manager = WalletManager()

    manager.create_new_wallet()
    manager.create_new_wallet()

    assert (
        manager.wallet_count()
        == 2
    )


# ==========================================================
# LIST WALLETS
# ==========================================================

def test_list_wallets():

    manager = WalletManager()

    manager.create_new_wallet()
    manager.create_new_wallet()

    wallets = (
        manager.list_wallets()
    )

    assert (
        len(wallets)
        == 2
    )


# ==========================================================
# GET WALLET
# ==========================================================

def test_get_wallet():

    manager = WalletManager()

    address = (
        manager.create_new_wallet()
    )

    wallet = (
        manager.get_wallet(
            address
        )
    )

    assert wallet is not None

    assert (
        wallet["address"]
        == address
    )


# ==========================================================
# DELETE WALLET
# ==========================================================

def test_delete_wallet():

    manager = WalletManager()

    address = (
        manager.create_new_wallet()
    )

    result = (
        manager.delete_wallet(
            address
        )
    )

    assert result is True

    assert (
        manager.wallet_count()
        == 0
    )


# ==========================================================
# DELETE UNKNOWN WALLET
# ==========================================================

def test_delete_unknown_wallet():

    manager = WalletManager()

    result = (
        manager.delete_wallet(
            "fake_address"
        )
    )

    assert result is False


# ==========================================================
# IMPORT WALLET
# ==========================================================

def test_import_wallet():

    wallet = create_wallet()

    private_key = (
        export_private_key(
            wallet
        )
    )

    manager = WalletManager()

    address = (
        manager.import_wallet(
            private_key
        )
    )

    assert (
        manager.get_wallet(
            address
        )
        is not None
    )

    assert (
        manager.wallet_count()
        == 1
    )


# ==========================================================
# PERSISTENCE
# ==========================================================

def test_wallet_persistence():

    manager = WalletManager()

    address = (
        manager.create_new_wallet()
    )

    manager.save()

    new_manager = (
        WalletManager()
    )

    assert (
        new_manager.get_wallet(
            address
        )
        is not None
    )

    assert (
        new_manager.wallet_count()
        == 1
    )