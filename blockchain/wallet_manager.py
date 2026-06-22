"""
wallet_manager.py

Wallet Persistence Manager

Features
--------
- Create wallets
- Save wallets
- Load wallets
- Restore wallets
- Lookup by address
- List stored wallets

Uses:
    transaction.py
    storage.py
"""

from __future__ import annotations

from typing import Dict, Optional

from blockchain.transaction import (
    Wallet,
    create_wallet,
    get_wallet_address,
    export_private_key,
    export_public_key,
    load_private_key,
    load_public_key,
)

from blockchain.storage import (
    save_wallets,
    load_wallets,
)


# ==========================================================
# WALLET MANAGER
# ==========================================================

class WalletManager:

    def __init__(self):

        self.wallets: Dict[str, Dict] = {}

        self.load()

    # ======================================================
    # LOAD / SAVE
    # ======================================================

    def load(self) -> None:

        data = load_wallets()

        if data:
            self.wallets = data

    def save(self) -> bool:

        return save_wallets(
            self.wallets
        )

    # ======================================================
    # CREATE WALLET
    # ======================================================

    def create_new_wallet(self) -> str:

        wallet = create_wallet()

        address = get_wallet_address(
            wallet
        )

        self.wallets[address] = {
            "address": address,
            "private_key": export_private_key(
                wallet
            ),
            "public_key": export_public_key(
                wallet
            )
        }

        self.save()

        return address

    # ======================================================
    # IMPORT WALLET
    # ======================================================

    def import_wallet(
        self,
        private_key_hex: str
    ) -> str:

        private_key = load_private_key(
            private_key_hex
        )

        wallet = Wallet(
            private_key=private_key,
            public_key=private_key.verifying_key
        )

        address = get_wallet_address(
            wallet
        )

        self.wallets[address] = {
            "address": address,
            "private_key": export_private_key(
                wallet
            ),
            "public_key": export_public_key(
                wallet
            )
        }

        self.save()

        return address

    # ======================================================
    # GET WALLET
    # ======================================================

    def get_wallet(
        self,
        address: str
    ) -> Optional[Dict]:

        return self.wallets.get(
            address
        )
    
    def restore_wallet(
            self,
            address: str
            ) -> Optional[Wallet]:
        wallet_data = self.wallets.get(
            address
            )
        if not wallet_data:
            return None
        
        private_key = load_private_key(
            wallet_data["private_key"]
            )
        
        public_key = load_public_key(
            wallet_data["public_key"]
            )
        return Wallet(
            private_key=private_key,
            public_key=public_key
    )

    # ======================================================
    # LIST WALLETS
    # ======================================================

    def list_wallets(self) -> Dict[str, Dict]:

        return self.wallets

    # ======================================================
    # DELETE WALLET
    # ======================================================

    def delete_wallet(
        self,
        address: str
    ) -> bool:

        if address not in self.wallets:
            return False

        del self.wallets[address]

        self.save()

        return True

    # ======================================================
    # COUNT
    # ======================================================

    def wallet_count(self) -> int:

        return len(
            self.wallets
        )


# ==========================================================
# FACTORY
# ==========================================================

def create_wallet_manager() -> WalletManager:

    return WalletManager()


# ==========================================================
# DEMO
# ==========================================================

if __name__ == "__main__":

    manager = WalletManager()

    address = (
        manager.create_new_wallet()
    )

    print(
        "\nWallet Created:"
    )

    print(address)

    print(
        "\nStored Wallets:"
    )

    print(
        manager.wallet_count()
    )

    print(
        manager.list_wallets()
    )