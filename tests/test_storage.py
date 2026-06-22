"""
tests/test_storage.py

Persistence & Storage Integration Tests (V2)
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

sys.path.insert(0, PROJECT_ROOT)

from blockchain.chain import create_blockchain
from blockchain.wallet_manager import WalletManager
from blockchain.transaction import create_wallet, get_wallet_address, create_signed_transaction
from blockchain.storage import (
    reset_storage,
    load_blockchain,
    load_wallets,
    load_mempool,
    storage_status,
)


# ==========================================================
# CLEAN STORAGE FIXTURE
# ==========================================================

@pytest.fixture(autouse=True)
def clean_storage():
    reset_storage()
    yield
    reset_storage()


# ==========================================================
# TEST 1: BLOCKCHAIN PERSISTENCE
# ==========================================================

def test_blockchain_persistence():

    chain = create_blockchain()

    # create a funded wallet
    wallet = create_wallet()
    address = get_wallet_address(wallet)

    chain.set_balance(address, 100)

    # add transaction
    tx = create_signed_transaction(
        sender_wallet=wallet,
        receiver_address="receiver",
        amount=10
    )

    chain.add_transaction(tx)

    # mine block
    miner = get_wallet_address(create_wallet())
    chain.mine_pending_transactions(miner)

    # reload from disk
    new_chain = create_blockchain()

    assert new_chain.get_chain_length() == chain.get_chain_length()


# ==========================================================
# TEST 2: WALLET PERSISTENCE (SYSTEM LEVEL)
# ==========================================================

def test_wallet_persistence():

    manager = WalletManager()

    address = manager.create_new_wallet()
    wallet_data = manager.get_wallet(address)

    assert wallet_data is not None

    # simulate restart
    new_manager = WalletManager()

    assert new_manager.get_wallet(address) is not None
    assert new_manager.wallet_count() == 1


# ==========================================================
# TEST 3: MEMPOOL PERSISTENCE
# ==========================================================

def test_mempool_persistence():

    chain = create_blockchain()

    wallet = create_wallet()
    address = get_wallet_address(wallet)

    chain.set_balance(address, 100)

    tx = create_signed_transaction(
        sender_wallet=wallet,
        receiver_address="receiver",
        amount=5
    )

    chain.add_transaction(tx)

    # ensure mempool stored
    assert len(load_mempool()) == 1

    # reload chain
    new_chain = create_blockchain()

    assert len(new_chain.get_pending_transactions()) == 1


# ==========================================================
# TEST 4: STORAGE RESET
# ==========================================================

def test_storage_reset():

    manager = WalletManager()
    manager.create_new_wallet()

    chain = create_blockchain()

    wallet = create_wallet()
    address = get_wallet_address(wallet)

    chain.set_balance(address, 50)

    # trigger reset
    reset_storage()

    status = storage_status()

    assert status["blockchain_exists"] is False
    assert status["wallets_exists"] is False
    assert status["mempool_exists"] is False


# ==========================================================
# TEST 5: FULL SYSTEM RELOAD INTEGRITY
# ==========================================================

def test_full_system_reload_integrity():

    manager = WalletManager()
    address = manager.create_new_wallet()

    chain = create_blockchain()

    wallet = create_wallet()
    sender = get_wallet_address(wallet)

    chain.set_balance(sender, 100)

    tx = create_signed_transaction(
        sender_wallet=wallet,
        receiver_address=address,
        amount=20
    )

    chain.add_transaction(tx)

    chain.mine_pending_transactions(address)

    # simulate full restart
    new_manager = WalletManager()
    new_chain = create_blockchain()

    assert new_manager.get_wallet(address) is not None
    assert new_chain.get_chain_length() >= 2
    assert new_chain.is_chain_valid()