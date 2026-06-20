"""
tests/test_blockchain.py

Unit Tests for Blockchain Project

Covers:
- Wallet Creation
- Transaction Signing
- Transaction Validation
- Block Mining
- Block Verification
- Blockchain Operations
- Chain Validation
- Balance Updates
- Mempool Behavior

Run:

    pytest tests/

or

    pytest tests/test_blockchain.py -v
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from blockchain.transaction import (
    create_wallet,
    get_wallet_address,
    create_signed_transaction,
    validate_transaction,
)

from blockchain.block import (
    create_block,
    mine_block,
    verify_block,
)

from blockchain.chain import (
    create_blockchain,
)


# ==========================================================
# WALLET TESTS
# ==========================================================

def test_wallet_creation():

    wallet = create_wallet()

    assert wallet is not None

    address = get_wallet_address(
        wallet
    )

    assert isinstance(
        address,
        str
    )

    assert len(address) == 64


def test_multiple_wallets_unique():

    wallet1 = create_wallet()
    wallet2 = create_wallet()

    address1 = get_wallet_address(
        wallet1
    )

    address2 = get_wallet_address(
        wallet2
    )

    assert address1 != address2


# ==========================================================
# TRANSACTION TESTS
# ==========================================================

def test_signed_transaction():

    sender = create_wallet()
    receiver = create_wallet()

    tx = create_signed_transaction(
        sender_wallet=sender,
        receiver_address=get_wallet_address(
            receiver
        ),
        amount=100
    )

    assert tx.signature != ""


def test_transaction_validation():

    sender = create_wallet()
    receiver = create_wallet()

    tx = create_signed_transaction(
        sender_wallet=sender,
        receiver_address=get_wallet_address(
            receiver
        ),
        amount=50
    )

    assert validate_transaction(
        tx
    ) is True


def test_invalid_transaction_amount():

    sender = create_wallet()
    receiver = create_wallet()

    tx = create_signed_transaction(
        sender_wallet=sender,
        receiver_address=get_wallet_address(
            receiver
        ),
        amount=-10
    )

    assert validate_transaction(
        tx
    ) is False


# ==========================================================
# BLOCK TESTS
# ==========================================================

def test_block_creation():

    block = create_block(
        index=1,
        transactions=[],
        previous_hash="0" * 64
    )

    assert block.index == 1

    assert block.previous_hash == (
        "0" * 64
    )


def test_block_mining():

    block = create_block(
        index=1,
        transactions=[],
        previous_hash="0" * 64
    )

    mine_block(
        block,
        difficulty=3
    )

    assert block.hash.startswith(
        "000"
    )


def test_block_verification():

    block = create_block(
        index=1,
        transactions=[],
        previous_hash="0" * 64
    )

    mine_block(
        block,
        difficulty=3
    )

    assert verify_block(
        block,
        difficulty=3
    ) is True


# ==========================================================
# BLOCKCHAIN TESTS
# ==========================================================

def test_genesis_block():

    blockchain = create_blockchain()

    assert (
        blockchain.get_chain_length()
        == 1
    )


def test_add_valid_transaction():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()

    alice_address = (
        get_wallet_address(
            alice
        )
    )

    bob_address = (
        get_wallet_address(
            bob
        )
    )

    blockchain.set_balance(
        alice_address,
        100
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=bob_address,
        amount=25
    )

    assert blockchain.add_transaction(
        tx
    ) is True


def test_reject_insufficient_balance():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=100
    )

    assert blockchain.add_transaction(
        tx
    ) is False


def test_mempool_size():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()

    alice_address = (
        get_wallet_address(
            alice
        )
    )

    blockchain.set_balance(
        alice_address,
        100
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=20
    )

    blockchain.add_transaction(
        tx
    )

    assert len(
        blockchain.get_pending_transactions()
    ) == 1


# ==========================================================
# MINING TESTS
# ==========================================================

def test_mining_creates_new_block():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()
    miner = create_wallet()

    alice_address = (
        get_wallet_address(
            alice
        )
    )

    blockchain.set_balance(
        alice_address,
        100
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=30
    )

    blockchain.add_transaction(
        tx
    )

    initial_length = (
        blockchain.get_chain_length()
    )

    blockchain.mine_pending_transactions(
        get_wallet_address(
            miner
        )
    )

    assert (
        blockchain.get_chain_length()
        == initial_length + 1
    )


def test_miner_receives_reward():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()
    miner = create_wallet()

    alice_address = (
        get_wallet_address(
            alice
        )
    )

    miner_address = (
        get_wallet_address(
            miner
        )
    )

    blockchain.set_balance(
        alice_address,
        100
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=20
    )

    blockchain.add_transaction(
        tx
    )

    blockchain.mine_pending_transactions(
        miner_address
    )

    assert (
        blockchain.get_balance(
            miner_address
        )
        == blockchain.mining_reward
    )


# ==========================================================
# BALANCE TESTS
# ==========================================================

def test_balance_updates_after_mining():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()
    miner = create_wallet()

    alice_address = (
        get_wallet_address(
            alice
        )
    )

    bob_address = (
        get_wallet_address(
            bob
        )
    )

    blockchain.set_balance(
        alice_address,
        100
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=bob_address,
        amount=40
    )

    blockchain.add_transaction(
        tx
    )

    blockchain.mine_pending_transactions(
        get_wallet_address(
            miner
        )
    )

    assert (
        blockchain.get_balance(
            alice_address
        )
        == 60
    )

    assert (
        blockchain.get_balance(
            bob_address
        )
        == 40
    )


# ==========================================================
# CHAIN VALIDATION TESTS
# ==========================================================

def test_chain_validity():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()
    miner = create_wallet()

    alice_address = (
        get_wallet_address(
            alice
        )
    )

    blockchain.set_balance(
        alice_address,
        100
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=10
    )

    blockchain.add_transaction(
        tx
    )

    blockchain.mine_pending_transactions(
        get_wallet_address(
            miner
        )
    )

    assert (
        blockchain.is_chain_valid()
        is True
    )


def test_chain_tampering_detection():

    blockchain = create_blockchain()

    alice = create_wallet()
    bob = create_wallet()
    miner = create_wallet()

    alice_address = (
        get_wallet_address(
            alice
        )
    )

    blockchain.set_balance(
        alice_address,
        100
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=get_wallet_address(
            bob
        ),
        amount=15
    )

    blockchain.add_transaction(
        tx
    )

    blockchain.mine_pending_transactions(
        get_wallet_address(
            miner
        )
    )

    blockchain.chain[1].nonce += 1

    assert (
        blockchain.is_chain_valid()
        is False
    )