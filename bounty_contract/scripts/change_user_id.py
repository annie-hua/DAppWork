from brownie import Bounty, network, config
from scripts.deploy_bounty import deploy_bounty
from scripts.fund_and_withdraw_bounty import (
    fund,
    view,
    withdraw,
    seconds_to_days,
    bounty_status_list,
)
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3
import time

# will add a python function here that will call the "change_user_id" solidity function


def main():
    deploy_bounty(15552000)
    fund(100000000000000000)
    view()
    withdraw()
    view()
