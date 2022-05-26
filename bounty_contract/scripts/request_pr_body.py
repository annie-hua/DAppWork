# Written to test whether the Chainlink API request is working, which it is!

from brownie import Bounty, BountyFactory, network, config
from scripts.deploy_bounty_factory import deploy_bounty_factory
from scripts.use_bounty_factory import create_bounty_with_factory, owner_address
from scripts.close_bounty import close
from scripts.use_bounty_factory import (
    view_bounty_through_factory,
    fund_to_specific_bounty,
)
from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    bounty_status_list,
    seconds_to_days,
)


def start_chainlink_job(_parsed_pull_request_link):
    bounty_factory = BountyFactory[-1]
    tx = bounty_factory.requestPullRequestBody(_parsed_pull_request_link)
    return tx


def main():
    bf_contract_address = deploy_bounty_factory()
    fund_with_link(bf_contract_address)
    tx = start_chainlink_job(
        "https://api.github.com/repos/amicable-alpaca/DappWorkTest/issues/4"
    )
    tx.wait(1)
