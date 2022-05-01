from brownie import Bounty, network, config
from scripts.deploy_bounty import deploy_bounty
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def fund(bounty_amount):
    bounty = Bounty[-1]
    account = get_account(None)
    bounty.fund_bounty({"from": account, "value": bounty_amount})
    print(
        f"You have funded your bounty with {Web3.fromWei(bounty_amount, 'ether')} ether."
    )


def view():
    bounty = Bounty[-1]
    account = get_account(None)
    (
        owner,
        bounty_name,
        bounty_link,
        bounty_amount,
        bounty_status,
    ) = bounty.view_bounty()
    print(
        f"The current status of this bounty is {bounty_status}. This bounty is called {bounty_name} and its owner is {owner}. They are offering {Web3.fromWei(bounty_amount, 'ether')} ether for its completion. You can find more info here {bounty_link}."
    )


def withdraw():
    bounty = Bounty[-1]
    account = get_account(None)
    bounty.withdraw_bounty({"from": account})


def main():
    deploy_bounty()
    fund(100000000000000000)
    view()
    withdraw()
    view()
