from venv import create
from brownie import Bounty, BountyFactory, network, config, Contract
from scripts.deploy_bounty_factory import deploy_bounty_factory
from scripts.fund_and_withdraw_bounty import fund
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    bounty_status_list,
    seconds_to_days,
)
from web3 import Web3
import time
import json

with open("./build/contracts/Bounty.json") as f:
    data = json.load(f)

bounty_abi = data["abi"]

owner_address = get_account(None)


def create_bounty_with_factory(
    _bounty_name, _bounty_link, _bounty_lockup_seconds, _owner_address
):
    bounty_factory = BountyFactory[-1]
    account = get_account(None)
    bounty_factory.createBountyContract(
        _bounty_name,
        _bounty_link,
        _bounty_lockup_seconds,
        _owner_address,
        {"from": account},
    )


def view_bounty_through_factory(_bounty_index):
    bounty_factory = BountyFactory[-1]
    account = get_account(None)
    (
        owner,
        bounty_name,
        bounty_link,
        bounty_amount,
        bounty_status,
        bounty_creation_time,
        bounty_lockup_seconds,
        hunter_github_id,
        hunter_address,
    ) = bounty_factory.bfViewBounty(_bounty_index, {"from": account})
    print(
        f"The current status of this bounty is {bounty_status_list[bounty_status]}. This bounty is called {bounty_name} and its owner is {owner}. They are offering {Web3.fromWei(bounty_amount, 'ether')} ether for its completion. You can find more info here {bounty_link}. This bounty was created on {time.ctime(bounty_creation_time)}. If you are the bounty owner, and would like to close this bounty (which would result in you withdrawing all of your funds), you must wait {bounty_lockup_seconds/seconds_to_days} days since the bounty creation date, specifically until {time.ctime(bounty_creation_time + bounty_lockup_seconds)}, to do so."
    )


def fund_to_specific_bounty(_bounty_index, _bounty_amount):
    bounty_factory = BountyFactory[-1]
    bounty_address = bounty_factory.bfReturnBountyAddress(_bounty_index)
    bounty_contract = Contract.from_abi("current_bounty", bounty_address, bounty_abi)
    account = get_account(None)
    bounty_contract.fund_bounty({"from": account, "value": _bounty_amount})


def main():
    deploy_bounty_factory()
    create_bounty_with_factory(
        "Treasure",
        "https://github.com/PatrickAlphaC/storage_factory/blob/main/StorageFactory.sol",
        15552000,
        owner_address,
    )
    view_bounty_through_factory(0)
    fund_to_specific_bounty(0, 100000000000000000)
    view_bounty_through_factory(0)
