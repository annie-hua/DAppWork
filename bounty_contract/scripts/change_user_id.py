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


def change_hunter_github_id(_hunter_github_id):
    bounty = Bounty[-1]
    account = get_account("oracle")
    bounty.change_hunter_github_id(_hunter_github_id, {"from": account})


def main():
    deploy_bounty(15552000)
    fund(10000000000000000)
    view()
    change_hunter_github_id("dog_the_bounty_hunter")
    view()
