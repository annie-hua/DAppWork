from brownie import Bounty, BountyFactory, network, config
from scripts.deploy_bounty_factory import deploy_bounty_factory
from scripts.use_bounty_factory import create_bounty_with_factory, owner_address
from scripts.close_bounty import close
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

bountyIndex = 0
# This would be passed by the website depending on which bounty the user chooses to close
pullsIndex = 0
# This is currently hardcoded, in a later version, we aim to have script on the website pull the Github API and find the right index


def initiate_chainlink_job_and_close_bounty(bountyIndex, pullsIndex):
    pass


def main():
    initiate_chainlink_job_and_close_bounty(bountyIndex, pullsIndex)
