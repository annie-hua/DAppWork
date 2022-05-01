from brownie import Bounty, network, config
from scripts.deploy_bounty import deploy_bounty
from scripts.fund_and_withdraw_bounty import fund, view, withdraw
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def close(_bounty_winner):
    bounty = Bounty[-1]
    account = get_account("oracle")
    bounty.close_bounty(_bounty_winner, {"from": account})


def main():
    deploy_bounty()
    fund(10000000000000000)
    view()
    close("0x51e001d1Aa1F0bB281eF011CD5B4D221E6fe1a0f")
    view()
