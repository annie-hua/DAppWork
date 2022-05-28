from brownie import BountyFactory, network, config
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_bounty_factory():
    account = get_account(None)

    bounty_factory = BountyFactory.deploy(
        {"from": account},
        # publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {bounty_factory.address}")
    return bounty_factory


def main():
    deploy_bounty_factory()
