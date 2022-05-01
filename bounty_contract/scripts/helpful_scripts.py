from brownie import network, config, accounts
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

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
