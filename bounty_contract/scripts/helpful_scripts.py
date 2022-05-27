from brownie import network, config, accounts, Contract
from web3 import Web3
import json

with open("./build/contracts/LinkToken.json") as f:
    data = json.load(f)

link_token_abi = data["abi"]

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
bounty_status_list = ["open", "closed", "withdrawn"]

seconds_to_days = 86400
# seconds divided by 60 divided by 60 and then divided by 24 is the same as dividing by 86400


DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account(_account_number):
    if (
        _account_number == None
        and network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):

        if _account_number == 1:

            return accounts[1]

        else:

            return accounts[0]

    else:

        if _account_number == "oracle":

            return accounts.add(config["wallets"]["oracle_key"])

        else:

            return accounts.add(config["wallets"]["from_key"])


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = get_account(0)
    link_token_contract_address = config["networks"][network.show_active()][
        "link_token"
    ]
    link_token_contract = Contract.from_abi(
        "link_token_contract", link_token_contract_address, link_token_abi
    )
    link_token_contract.transfer(contract_address, amount, {"from": account})
