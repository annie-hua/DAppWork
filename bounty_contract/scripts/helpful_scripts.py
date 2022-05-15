from brownie import network, config, accounts
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
bounty_status_list = ["open", "awaiting claim", "closed", "canceled"]

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
