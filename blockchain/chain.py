"""
chain.py

Blockchain implementation with:

- Genesis Block
- Proof of Work (PoW)
- Mempool
- Account-based balance tracking
- Transaction validation
- Mining rewards
- Chain validation
- Peer management
- Longest-chain consensus
- Persistence support

Compatible with:
    transaction.py
    block.py
"""

from __future__ import annotations

import json
from typing import Dict, List, Set, Optional

from blockchain.storage import (
    save_blockchain,
    load_blockchain,
    save_mempool,
    load_mempool,
)

from blockchain.block import (
    Block,
    create_block,
    mine_block,
    verify_block,
    serialize_block,
    deserialize_block,
)

from blockchain.transaction import (
    Transaction,
    validate_transaction,
    serialize_transaction,
    deserialize_transaction,
)

# ==========================================================
# BLOCKCHAIN
# ==========================================================

class Blockchain:

    def __init__(
        self,
        difficulty: int = 4,
        mining_reward: float = 50.0
    ):

        self.difficulty = difficulty
        self.mining_reward = mining_reward

        self.chain: List[Block] = []
        self.mempool: List[Transaction] = []

        self.peers: Set[str] = set()

        # Simple account-based balance model
        self.balances: Dict[str, float] = {}

        self.load_or_create_blockchain()

   # ======================================================
   # GENESIS BLOCK
   # ======================================================

    def create_genesis_block(self) -> None:
        genesis_block = create_block(
            index=0,
            transactions=[],
            previous_hash="0" * 64
            )
        
        genesis_block.hash = (
            "0" * 64
            )
        
        self.chain.append(
            genesis_block
            )


    def load_or_create_blockchain(self) -> None:
        
        stored_chain = load_blockchain()
        if stored_chain:
            self.chain = [
                deserialize_block(block)
                for block in stored_chain
                ]
            
        else:
            self.create_genesis_block()
            save_blockchain(self.export_chain())
            
        stored_mempool = load_mempool()
        if stored_mempool:
            self.mempool = [
                deserialize_transaction(tx)
                for tx in stored_mempool
                ]
        else:
            self.mempool = []

    # ======================================================
    # BLOCK ACCESS
    # ======================================================

    def get_latest_block(self) -> Block:

        return self.chain[-1]

    def get_chain_length(self) -> int:

        return len(self.chain)

    # ======================================================
    # PEERS
    # ======================================================

    def add_peer(
        self,
        peer_url: str
    ) -> None:

        self.peers.add(peer_url)

    def remove_peer(
        self,
        peer_url: str
    ) -> None:

        self.peers.discard(peer_url)

    def get_peers(self) -> List[str]:

        return list(self.peers)

    # ======================================================
    # BALANCES
    # ======================================================

    def get_balance(
        self,
        address: str
    ) -> float:

        return self.balances.get(
            address,
            0.0
        )

    def set_balance(
        self,
        address: str,
        amount: float
    ) -> None:

        self.balances[address] = amount

    def update_balances(
        self,
        transactions: List[Transaction]
    ) -> None:

        for tx in transactions:

            if tx.sender != "SYSTEM":

                self.balances[
                    tx.sender
                ] = (
                    self.get_balance(
                        tx.sender
                    )
                    - tx.amount
                )

            self.balances[
                tx.receiver
            ] = (
                self.get_balance(
                    tx.receiver
                )
                + tx.amount
            )

    # ======================================================
    # MEMPOOL
    # ======================================================

    def add_transaction(
        self,
        transaction: Transaction
    ) -> bool:

        if not validate_transaction(
            transaction
        ):
            return False

        sender_balance = (
            self.get_balance(
                transaction.sender
            )
        )

        if sender_balance < transaction.amount:
            return False

        self.mempool.append(transaction)
        save_mempool(
            [
                serialize_transaction(tx)
                for tx in self.mempool
            ]
        )

        return True

    def get_pending_transactions(
        self
    ) -> List[Transaction]:

        return self.mempool

    def clear_mempool(
        self
    ) -> None:

        self.mempool.clear()
        save_mempool([])

    # ======================================================
    # MINING
    # ======================================================

    def mine_pending_transactions(
        self,
        miner_address: str
    ) -> Optional[Block]:

        if len(self.mempool) == 0:
            return None

        reward_transaction = Transaction(
            sender="SYSTEM",
            receiver=miner_address,
            amount=self.mining_reward
        )

        block_transactions = (
            self.mempool.copy()
        )

        block_transactions.append(
            reward_transaction
        )

        new_block = create_block(
            index=len(self.chain),
            transactions=block_transactions,
            previous_hash=(
                self.get_latest_block().hash
            )
        )

        mine_block(
            new_block,
            self.difficulty
        )

        self.chain.append(
            new_block
        )

        save_blockchain(
            self.export_chain()
        )

        self.update_balances(
            block_transactions
        )

        self.clear_mempool()
        return new_block

        

    # ======================================================
    # CHAIN VALIDATION
    # ======================================================

    def is_chain_valid(
        self
    ) -> bool:

        if len(self.chain) == 0:
            return False

        for i in range(
            1,
            len(self.chain)
        ):

            current = self.chain[i]
            previous = self.chain[i - 1]

            if not verify_block(
                current,
                self.difficulty
            ):
                return False

            if (
                current.previous_hash
                != previous.hash
            ):
                return False

        return True

    # ======================================================
    # CONSENSUS
    # ======================================================

    def replace_chain(
        self,
        incoming_chain: List[Block]
    ) -> bool:

        if (
            len(incoming_chain)
            <= len(self.chain)
        ):
            return False

        self.chain = incoming_chain

        save_blockchain(
            self.export_chain()
            )

        return True

    # ======================================================
    # SERIALIZATION
    # ======================================================

    def export_chain(
        self
    ) -> List[Dict]:

        return [
            serialize_block(block)
            for block in self.chain
        ]

    def export_balances(
        self
    ) -> Dict[str, float]:

        return self.balances

    def to_json(
        self
    ) -> str:

        data = {
            "difficulty": self.difficulty,
            "mining_reward": self.mining_reward,
            "balances": self.balances,
            "chain": self.export_chain()
        }

        return json.dumps(
            data,
            indent=4
        )

    # ======================================================
    # IMPORT
    # ======================================================

    @staticmethod
    def from_json(
        json_data: str
    ) -> "Blockchain":

        data = json.loads(
            json_data
        )

        blockchain = Blockchain(
            difficulty=data[
                "difficulty"
            ],
            mining_reward=data[
                "mining_reward"
            ]
        )

        blockchain.chain = [
            deserialize_block(block)
            for block in data["chain"]
        ]

        blockchain.balances = data[
            "balances"
        ]

        return blockchain

    # ======================================================
    # DEBUG
    # ======================================================

    def print_chain(self) -> None:

        print("\n")

        for block in self.chain:

            print("=" * 60)

            print(
                f"Block #{block.index}"
            )

            print(
                f"Hash: {block.hash}"
            )

            print(
                f"Previous: "
                f"{block.previous_hash}"
            )

            print(
                f"Transactions: "
                f"{len(block.transactions)}"
            )

            print("=" * 60)


# ==========================================================
# FACTORY
# ==========================================================

def create_blockchain(
        difficulty: int = 4,
        mining_reward: float = 50.0
        ) -> Blockchain:
    return Blockchain(
        difficulty=difficulty,
        mining_reward=mining_reward
        )


# ==========================================================
# DEMO
# ==========================================================

if __name__ == "__main__":

    from blockchain.transaction import (
        create_wallet,
        get_wallet_address,
        create_signed_transaction,
    )

    chain = create_blockchain()

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

    # Initial funds
    chain.set_balance(
        alice_address,
        100.0
    )

    tx = create_signed_transaction(
        sender_wallet=alice,
        receiver_address=bob_address,
        amount=25.0
    )

    print(
        "Transaction Added:",
        chain.add_transaction(tx)
    )

    mined_block = (
        chain.mine_pending_transactions(
            miner_address
        )
    )

    print(
        "Block Mined:",
        mined_block.index
    )

    print(
        "Chain Valid:",
        chain.is_chain_valid()
    )

    print(
        "Alice Balance:",
        chain.get_balance(
            alice_address
        )
    )

    print(
        "Bob Balance:",
        chain.get_balance(
            bob_address
        )
    )

    print(
        "Miner Balance:",
        chain.get_balance(
            miner_address
        )
    )