"""
demo.py

End-to-End Blockchain Demonstration

Features Demonstrated:
- Wallet Creation
- Address Generation
- Initial Funding
- Transaction Creation
- Digital Signatures
- Mempool Management
- Block Mining
- Mining Rewards
- Balance Updates
- Chain Validation
- Blockchain Inspection

Run:

    python demo.py
"""

from blockchain.transaction import (
    create_wallet,
    get_wallet_address,
    create_signed_transaction,
)

from blockchain.chain import (
    create_blockchain,
)


# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

def print_separator():
    print("\n" + "=" * 80 + "\n")


def print_wallet_info(name, wallet):
    print(f"{name} Address:")
    print(get_wallet_address(wallet))
    print()


def print_balances(
    blockchain,
    alice_address,
    bob_address,
    miner_address
):
    print("\nCurrent Balances")
    print("-" * 40)

    print(
        f"Alice : "
        f"{blockchain.get_balance(alice_address)}"
    )

    print(
        f"Bob   : "
        f"{blockchain.get_balance(bob_address)}"
    )

    print(
        f"Miner : "
        f"{blockchain.get_balance(miner_address)}"
    )


# ==========================================================
# MAIN DEMO
# ==========================================================

def main():

    print_separator()

    print("BLOCKCHAIN PROJECT DEMONSTRATION")

    print_separator()

    # ======================================================
    # CREATE BLOCKCHAIN
    # ======================================================

    blockchain = create_blockchain(
        difficulty=4,
        mining_reward=50.0
    )

    print("Blockchain created.")

    print(
        f"Difficulty: "
        f"{blockchain.difficulty}"
    )

    print(
        f"Mining Reward: "
        f"{blockchain.mining_reward}"
    )

    # ======================================================
    # CREATE WALLETS
    # ======================================================

    print_separator()

    print("CREATING WALLETS")

    alice = create_wallet()
    bob = create_wallet()
    miner = create_wallet()

    alice_address = (
        get_wallet_address(alice)
    )

    bob_address = (
        get_wallet_address(bob)
    )

    miner_address = (
        get_wallet_address(miner)
    )

    print_wallet_info(
        "Alice",
        alice
    )

    print_wallet_info(
        "Bob",
        bob
    )

    print_wallet_info(
        "Miner",
        miner
    )

    # ======================================================
    # INITIAL FUNDING
    # ======================================================

    print_separator()

    print("INITIAL FUNDING")

    blockchain.set_balance(
        alice_address,
        100.0
    )

    print(
        "Alice funded with 100 coins."
    )

    print_balances(
        blockchain,
        alice_address,
        bob_address,
        miner_address
    )

    # ======================================================
    # CREATE TRANSACTION
    # ======================================================

    print_separator()

    print(
        "ALICE SENDS 25 COINS TO BOB"
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=bob_address,
        amount=25.0
    )

    added = blockchain.add_transaction(
        tx
    )

    print(
        f"Transaction Added: "
        f"{added}"
    )

    print(
        f"Mempool Size: "
        f"{len(blockchain.get_pending_transactions())}"
    )

    # ======================================================
    # MINE BLOCK
    # ======================================================

    print_separator()

    print("MINING BLOCK")

    block = (
        blockchain.mine_pending_transactions(
            miner_address
        )
    )

    if block:

        print(
            f"Block #{block.index} mined."
        )

        print(
            f"Hash: {block.hash}"
        )

        print(
            f"Nonce: {block.nonce}"
        )

    else:

        print(
            "No transactions to mine."
        )

    # ======================================================
    # BALANCE CHECK
    # ======================================================

    print_separator()

    print("UPDATED BALANCES")

    print_balances(
        blockchain,
        alice_address,
        bob_address,
        miner_address
    )

    # ======================================================
    # CHAIN VALIDATION
    # ======================================================

    print_separator()

    print("CHAIN VALIDATION")

    valid = (
        blockchain.is_chain_valid()
    )

    print(
        f"Blockchain Valid: "
        f"{valid}"
    )

    # ======================================================
    # CHAIN INFO
    # ======================================================

    print_separator()

    print("BLOCKCHAIN INFO")

    print(
        f"Chain Length: "
        f"{blockchain.get_chain_length()}"
    )

    print(
        f"Pending Transactions: "
        f"{len(blockchain.get_pending_transactions())}"
    )

    print(
        f"Connected Peers: "
        f"{len(blockchain.get_peers())}"
    )

    # ======================================================
    # PRINT CHAIN
    # ======================================================

    print_separator()

    print("BLOCKCHAIN CONTENTS")

    blockchain.print_chain()

    # ======================================================
    # EXPORT CHAIN
    # ======================================================

    print_separator()

    print("BLOCKCHAIN JSON EXPORT")

    chain_json = blockchain.to_json()

    print(
        chain_json[:1000]
    )

    print("\n...output truncated...\n")

    print_separator()

    print(
        "DEMO COMPLETED SUCCESSFULLY"
    )

    print_separator()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()