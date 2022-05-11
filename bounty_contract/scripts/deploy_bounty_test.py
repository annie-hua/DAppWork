from brownie import BountyTest, network, config
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_bounty_test(_bounty_lockup_duration):
    account = get_account(None)

    bounty = BountyTest.deploy(
        "Treasure",
        "https://github.com/PatrickAlphaC/smartcontract-lottery/blob/main/scripts/deploy_lottery.py",
        _bounty_lockup_duration,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {bounty.address}")
    return bounty


def main():
    deploy_bounty_test()
