# This is named part 1 as there needs to be a gap to allow for the bounty hunter to view the bounty, submit a pull request, and then have it merged on GitHub

from brownie import Bounty, BountyFactory, network, config
from scripts.deploy_bounty_factory import deploy_bounty_factory
from scripts.use_bounty_factory import create_bounty_with_factory, owner_address
from scripts.use_bounty_factory import (
    view_bounty_through_factory,
    fund_to_specific_bounty,
)
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    bounty_status_list,
    seconds_to_days,
)


def main():
    deploy_bounty_factory()
    bountyIndex = create_bounty_with_factory(
        "First Bounty",
        "https://github.com/amicable-alpaca/DappWorkTest/issues/1",
        15552000,
        owner_address,
    )
    view_bounty_through_factory(bountyIndex)
    fund_to_specific_bounty(bountyIndex, 100000000000000000)
    view_bounty_through_factory(bountyIndex)
    bountyIndex = create_bounty_with_factory(
        "Second Bounty",
        "https://github.com/amicable-alpaca/DappWorkTest/issues/2",
        15552000,
        owner_address,
    )
    view_bounty_through_factory(bountyIndex)
    fund_to_specific_bounty(bountyIndex, 100000000000000000)
    view_bounty_through_factory(bountyIndex)
