from brownie import Bounty, BountyFactory, network, config
from scripts.deploy_bounty_factory import deploy_bounty_factory
from scripts.use_bounty_factory import create_bounty_with_factory, owner_address
from scripts.fund_and_withdraw_bounty import fund
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    bounty_status_list,
    seconds_to_days,
)

bounty_factory_array_contents = []


def view_bounty_factory_array_length():
    bounty_factory = BountyFactory[-1]
    account = get_account(None)
    bounty_factory_array_length = bounty_factory.bfViewBountyArrayLength(
        {"from": account}
    )
    print(
        f"The current status size of the bounty factory array is {bounty_factory_array_length}."
    )


def view_bounty_array_contents():
    bounty_factory = BountyFactory[-1]
    account = get_account(None)
    bounty_factory_array_contents = bounty_factory.bfViewBountyArray({"from": account})
    print(
        f"The contract address for the currently existing bounties are {bounty_factory_array_contents}."
    )


def main():
    deploy_bounty_factory()
    view_bounty_factory_array_length()
    view_bounty_array_contents()
    create_bounty_with_factory(
        "Treasure",
        "https://github.com/PatrickAlphaC/storage_factory/blob/main/StorageFactory.sol",
        15552000,
        owner_address,
    )
    view_bounty_factory_array_length()
    view_bounty_array_contents()
    create_bounty_with_factory(
        "Doggo",
        "https://github.com/PatrickAlphaC/storage_factory/blob/main/StorageFactory.sol",
        15552000,
        owner_address,
    )
    view_bounty_factory_array_length()
    view_bounty_array_contents()
