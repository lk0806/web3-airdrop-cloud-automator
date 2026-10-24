"""
modules/identity_generator.py
==============================
Generates a fresh, secure EVM Web3 Identity and Wallet for Autonomous Airdrop Farming.
Zero personal account pollution.
"""

import os
import sys
import json
from eth_account import Account

Account.enable_unaudited_hdwallet_features()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTITY_FILE = os.path.join(PROJECT_ROOT, "config", "airdrop_identity.json")

def generate_or_load_identity():
    os.makedirs(os.path.dirname(IDENTITY_FILE), exist_ok=True)
    if os.path.exists(IDENTITY_FILE):
        try:
            with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("address"):
                    return data
        except Exception:
            pass

    # Create brand new account
    acct, mnemonic = Account.create_with_mnemonic()
    identity = {
        "address": acct.address,
        "private_key": acct.key.hex(),
        "mnemonic": mnemonic,
        "burner_username": f"airdrop_hunter_{acct.address[2:8].lower()}",
        "created_at": str(Account),
        "status": "FRESH_ISOLATED_WALLET"
    }

    with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
        json.dump(identity, f, indent=2)

    print(f"[+] Brand New Isolated EVM Wallet Generated: {identity['address']}")
    return identity

if __name__ == "__main__":
    ident = generate_or_load_identity()
    print("Wallet Address:", ident["address"])
