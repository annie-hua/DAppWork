from brownie import Bounty, network, config
from scripts.deploy_bounty import deploy_bounty
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3
import time

seconds_to_days = 86400
# seconds divided by 60 divided by 60 and then divided by 24 is the same as dividing by 86400

bounty_status_list = ["open", "awaiting claim", "closed", "canceled"]


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
        bounty_creation_time,
        bounty_lockup_seconds,
        user_id,
        hunter_address,
    ) = bounty.view_bounty()

    if bounty_status_list[bounty_status] == "awaiting claim":
        print(
            f"The current status of this bounty is {bounty_status_list[bounty_status]} and the one who completed the bounty has a github user ID of {user_id}. This bounty is called {bounty_name} and its owner is {owner}. They were offering {Web3.fromWei(bounty_amount, 'ether')} ether for its completion. You can find more info here {bounty_link}. This bounty was created on {time.ctime(bounty_creation_time)}."
        )
    elif bounty_status_list[bounty_status] == "canceled":
        print(
            f"The current status of this bounty is {bounty_status_list[bounty_status]}. This bounty was called {bounty_name} and its owner is {owner}. They were offering {Web3.fromWei(bounty_amount, 'ether')} ether for its completion. You can find more info here {bounty_link}. This bounty was created on {time.ctime(bounty_creation_time)}."
        )
    else:
        print(
            f"The current status of this bounty is {bounty_status_list[bounty_status]}. This bounty is called {bounty_name} and its owner is {owner}. They are offering {Web3.fromWei(bounty_amount, 'ether')} ether for its completion. You can find more info here {bounty_link}. This bounty was created on {time.ctime(bounty_creation_time)}. If you are the bounty owner, and would like to close this bounty (which would result in you withdrawing all of your funds), you must wait {bounty_lockup_seconds/seconds_to_days} days since the bounty creation date, specifically until {time.ctime(bounty_creation_time + bounty_lockup_seconds)}, to do so."
        )


def withdraw():
    bounty = Bounty[-1]
    account = get_account(None)
    bounty.withdraw_bounty({"from": account})


def main():
    deploy_bounty(15552000)
    fund(100000000000000000)
    view()
    withdraw()
    view()
