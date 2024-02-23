import os
import random
import time
from testnets import swan
from testnet_tx import TestnetTx

PK = os.environ.get("HASH_MASH")

with open("messages.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f.readlines()]

contr_swan_msg = swan.get("contract")
contr_swan_msg_abi = swan.get("abi")


def main() -> None:
    Swan = TestnetTx(
        rpc_url="https://saturn-rpc.swanchain.io", chain_id=2024, private_key=PK)

    while True:
        msg = random.choice(messages)

        swan_msg_tx = Swan.call_contract_method(
            contract_addr=contr_swan_msg, abi=contr_swan_msg_abi, method_name="writeMessage", params=msg)

        if swan_msg_tx:
            print("MSG", swan_msg_tx)


if __name__ == "__main__":
    main()
