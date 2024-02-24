import os
import random
import time
import json
# from testnets import swan, taiko
from testnet_tx import TestnetTx

PK = os.environ.get("HASH_MASH")

with open("testnets.json", "r", encoding="utf-8") as f:
    contracts = json.load(f)

with open("messages.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f.readlines()]

# swan
swan_msg = contracts.get("swan").get("MessageContract").get("contract")
swan_msg_abi = contracts.get("swan").get("MessageContract").get("abi")

swan_counter = contracts.get("swan").get("Counter").get("contract")
swan_counter_abi = contracts.get("swan").get("Counter").get("abi")

# taiko
taiko_counter = contracts.get("taiko").get("Counter").get("contract")
taiko_counter_abi = contracts.get("taiko").get("Counter").get("abi")

taiko_msg = contracts.get("taiko").get("MessageContract").get("contract")
taiko_msg_abi = contracts.get("taiko").get("MessageContract").get("abi")


def main() -> None:
    Swan = TestnetTx(rpc_url="https://saturn-rpc.swanchain.io", chain_id=2024, private_key=PK)
    Taiko = TestnetTx(rpc_url="https://rpc.katla.taiko.xyz", chain_id=167008, private_key=PK)

    while True:
        # interact with Counter.sol
        counter_method = random.choice(("setNumber", "increment", "decrement"))
        param_number = random.choice(range(1, 30))
        sleep_time_short = random.choice(range(30, 50))
        sleep_time_long = random.choice(range(420, 720))

        taiko_counter_resp = Taiko.call_contract_method(
            contract_addr=taiko_counter,
            abi=taiko_counter_abi,
            method_name=counter_method,
            params=param_number if counter_method == "setNumber" else None
        )
        print("TAIKO COUNTER:", *taiko_counter_resp)

        time.sleep(sleep_time_short)

        swan_counter_resp = Swan.call_contract_method(
            contract_addr=swan_counter,
            abi=swan_counter_abi,
            method_name=counter_method,
            params=param_number if counter_method == "setNumber" else None
        )

        print("SWAN COUNTER:", *swan_counter_resp)

        time.sleep(sleep_time_long)
        # interact with MessageContract.sol
        message_method = random.choice(("writeMessage", "readMessage"))
        message = random.choice(messages)

        taiko_msg_resp = Taiko.call_contract_method(contract_addr=taiko_msg,
                                                    abi=taiko_msg_abi,
                                                    method_name=message_method,
                                                    params=message if message_method == "writeMessage" else None
                                                    )
        print("TAIKO MSG:", *taiko_msg_resp)

        time.sleep(sleep_time_short)

        swan_msg_resp = Swan.call_contract_method(contract_addr=swan_msg,
                                                  abi=swan_msg_abi,
                                                  method_name=message_method,
                                                  params=message if message_method == "writeMessage" else None
                                                  )
        print("SWAN MSG:", *swan_msg_resp)

        time.sleep(sleep_time_long)


if __name__ == "__main__":
    main()
