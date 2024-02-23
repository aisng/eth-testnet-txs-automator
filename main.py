import os
import time
from testnet_tx import TestnetTx


contr_swan_msg = "0xAE3C20700f5D5F17BD4e5BaA3ce2fF220A15854D"
contr_swan_msg_abi = [{"inputs": [
    {
        "internalType": "string",
        "name": "newMessage",
        "type": "string"
    }
],
    "name": "writeMessage",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
},
    {
    "inputs": [],
    "name": "readMessage",
    "outputs": [
        {
            "internalType": "string",
            "name": "",
            "type": "string"
        }
    ],
    "stateMutability": "view",
    "type": "function"}]


def main() -> None:
    pk = os.environ.get("HASH_MASH")

    swan_testnet = TestnetTx(
        rpc_url="https://saturn-rpc.swanchain.io", chain_id=2024, private_key=pk)

    while True:
        tx1 = swan_testnet.call_contract_method(
            contract_addr=contr_swan_msg, abi=contr_swan_msg_abi, method_name="writeMessage", params="yohiva")
        print(tx1)
        time.sleep(3)


if __name__ == "__main__":
    main()
