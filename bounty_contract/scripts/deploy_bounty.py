from brownie import Bounty, network, config
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_bounty():
    account = get_account(None)

    bounty = Bounty.deploy(
        "Treasure",
        "https://github.com/PatrickAlphaC/smartcontract-lottery/blob/main/scripts/deploy_lottery.py",
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {bounty.address}")
    return bounty


def main():
    deploy_bounty()
