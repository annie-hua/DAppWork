from contextlib import closing
from click import confirm
from brownie import Bounty, BountyFactory, network, config, Contract
from scripts.helpful_scripts import get_account, fund_with_link
from scripts.view_bounty_array import (
    view_bounty_factory_array_length,
    view_bounty_array_contents,
)
import json
import pandas as pd
from web3 import Web3
import time
import datetime

pd.set_option("display.max_columns", None)

i = 0
bounty_state_list = ["open", "closed", "withdrawn"]

with open("./build/contracts/BountyFactory.json") as f:
    bounty_factory_json = json.load(f)

bounty_factory_abi = bounty_factory_json["abi"]

with open("./build/contracts/Bounty.json") as f:
    bounty_json = json.load(f)

bounty_abi = bounty_json["abi"]

bounty_factory_contract_address = "0x1FE94CDA16AAF50f300fE78AC97A3d677452bA2a"
bounty_factory_contract = Contract.from_abi(
    "Bounty_Factory_Contract", bounty_factory_contract_address, bounty_factory_abi
)

account = get_account(0)


def pull_request_converter(_pull_request_link):
    first_list = _pull_request_link.split("//")
    first_addition = first_list[0] + "//api." + first_list[1]
    second_list = first_addition.split(".com")
    second_addition = second_list[0] + ".com/repos" + second_list[1]
    third_list = second_addition.split("pull")
    parsed_pull_request = third_list[0] + "issues" + third_list[1]
    return parsed_pull_request


def pythonic_dappwork_ui():
    i = 1
    while i == 1:
        print(
            "\nWelcome to DappWork, the decentralized marketplace for programming-related gig work!"
        )

        user_choice = 0

        options = [1, 2, 3, 4, 5]

        while int(user_choice) not in options:

            user_choice = input(
                "\nPlease select from the following options (Type One of the Numbers Below):\n\n1. List all Existing Bounties\n2. Create a New Bounty\n3. Close a Bounty\n4. Withdraw a Bounty\n5. Close DappWork\n\n"
            )

            if int(user_choice) not in options:
                print(
                    f'\nInvalid Entry: You entered "{user_choice}", please make sure to select one of the numbers listed above instead.'
                )

            if int(user_choice) == 5:

                print(
                    "\nYou selected to close DappWork. Goodbye and have a nice day!\n"
                )

            # This is for the list all existing bounties option
            while int(user_choice) == 1:

                print(
                    "\nYou selected to list all existing bounties. Please see below:\n"
                )

                total_number_of_bounties = (
                    bounty_factory_contract.bfViewBountyArrayLength()
                )

                list_of_bounties = []

                for bounty_index in range(total_number_of_bounties):

                    (
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount,
                        bounty_state,
                        bounty_creation_time_in_seconds,
                        bounty_lockup_seconds,
                        hunter_address,
                    ) = bounty_factory_contract.bfViewBounty(bounty_index)

                    bounty_amount_in_eth = Web3.fromWei(bounty_amount, "ether")

                    bounty_state = bounty_state_list[bounty_state]

                    bounty_creation_time = time.ctime(bounty_creation_time_in_seconds)

                    lockup_end_date = time.ctime(
                        bounty_creation_time_in_seconds + bounty_lockup_seconds
                    )

                    current_bounty_info = [
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount_in_eth,
                        bounty_state,
                        bounty_creation_time,
                        lockup_end_date,
                        hunter_address,
                    ]

                    list_of_bounties.append(current_bounty_info)

                df_list_of_bounties = pd.DataFrame(
                    list_of_bounties,
                    columns=[
                        "Owner",
                        "Name",
                        "Github Issue Link",
                        "Reward Amount (ETH)",
                        "Status",
                        "Creation Time",
                        "Lockup End Date",
                        "Winner",
                    ],
                )

                print(
                    "\nPlease note that if you are a bounty hunter, in order to receive the bounty, you must submit a pull request to the repo that has the open issue associated with said bounty and this pull request must get merged. You MUST ensure that the comment body of your pull request is in the following format '{Github Issue Link for Bounty}, {Your ETH Address}'. Also, do NOT update your pull request in any way after it has been merged as this will result in your pull request being ineligible to earn a bounty."
                )

                print(df_list_of_bounties)

                print("\nYou will now be returned to the main menu.")

                user_choice = 0

            # This is for the create a new bounty option
            while int(user_choice) == 2:

                print(
                    "\nYou selected to create a bounty. Please input the requested information about your bounty:"
                )

                owner = account

                bounty_name = input(
                    "\nPlease enter the title you'd like to assign to this bounty: "
                )
                bounty_link = input(
                    "\nPlease copy and paste the the github open issue link that is associated with this bounty: "
                )
                bounty_amount = float(
                    input(
                        "\nPlease enter how much in ETH you will fund your bounty with as a reward: "
                    )
                )

                bounty_amount_in_wei = Web3.toWei(bounty_amount, "ether")

                bounty_lockup_options = [3, 6, 9, 12]

                bounty_lockup_user_choice = 0

                while bounty_lockup_user_choice == 0:

                    bounty_lockup_user_choice = int(
                        input(
                            "\nPlease let us know how long you'd like to lock up your bounty for(Type One of the Numbers Below):\n\n3. 3 months\n6. 6 months\n9. 9 months\n12. 12 months\n\n"
                        )
                    )

                    if int(bounty_lockup_user_choice) not in bounty_lockup_options:
                        print(
                            f'\nInvalid Entry: You entered "{bounty_lockup_user_choice}", please make sure to select one of the numbers listed above instead.\n'
                        )

                        bounty_lockup_user_choice = 0

                bounty_lockup_seconds = (
                    bounty_lockup_user_choice * 30 * 24 * 60 * 60
                )  # converting months to seconds

                confirm_bounty_options = ["y", "n"]

                confirm_bounty_creation = "maybe"

                while confirm_bounty_creation not in confirm_bounty_options:

                    confirm_bounty_creation = input(
                        f'\nBased on your responses, you would like to create a bounty named "{bounty_name}" that has a Github issue link of "{bounty_link}". If someone completes your bounty, you will reward them {bounty_amount} ETH. If {bounty_lockup_user_choice} months pass without anyone completing your bounty, then you will be able to close the bounty and withdraw your funds.\n\nIf you would like to continue and create the bounty enter "y". If you would like to cancel this and go back to the main menu, enter "n".\n'
                    )

                    if confirm_bounty_creation == "y":

                        print("\n")

                        tx = bounty_factory_contract.createBountyContract(
                            bounty_name,
                            bounty_link,
                            bounty_lockup_seconds,
                            owner,
                            {"from": account},
                        )
                        tx.wait(1)
                        bounty_number = tx.events[0]["bountyIndex"]
                        bounty_address = bounty_factory_contract.bfReturnBountyAddress(
                            bounty_number
                        )
                        new_bounty_contract = Contract.from_abi(
                            "new_bounty", bounty_address, bounty_abi
                        )
                        new_bounty_contract.fund_bounty(
                            {"from": account, "value": bounty_amount_in_wei}
                        )
                        print(
                            f"Congrats! You just created bounty number {bounty_number} and funded it with {bounty_amount} ETH.\n\nYou will now be returned to the main menu."
                        )

                        user_choice = 0

                    else:
                        print(
                            '\nYou entered "n" so you will now be returned to the main menu.'
                        )

                        user_choice = 0

            # This is for the close bounty option
            while int(user_choice) == 3:

                print(
                    "\nYou selected to close a bounty. You can find the list of currently open bounties below:\n"
                )

                total_number_of_bounties = (
                    bounty_factory_contract.bfViewBountyArrayLength()
                )

                list_of_bounties = []

                for bounty_index in range(total_number_of_bounties):

                    (
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount,
                        bounty_state,
                        bounty_creation_time_in_seconds,
                        bounty_lockup_seconds,
                        hunter_address,
                    ) = bounty_factory_contract.bfViewBounty(bounty_index)

                    bounty_amount_in_eth = Web3.fromWei(bounty_amount, "ether")

                    bounty_state = bounty_state_list[bounty_state]

                    bounty_creation_time = time.ctime(bounty_creation_time_in_seconds)

                    lockup_end_date = time.ctime(
                        bounty_creation_time_in_seconds + bounty_lockup_seconds
                    )

                    current_bounty_info = [
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount_in_eth,
                        bounty_state,
                        bounty_creation_time,
                        lockup_end_date,
                        hunter_address,
                    ]

                    list_of_bounties.append(current_bounty_info)

                df_list_of_bounties = pd.DataFrame(
                    list_of_bounties,
                    columns=[
                        "Owner",
                        "Name",
                        "Github Issue Link",
                        "Reward Amount (ETH)",
                        "Status",
                        "Creation Time",
                        "Lockup End Date",
                        "Winner",
                    ],
                )

                print(df_list_of_bounties)

                closing_bounty_index = int(
                    input(
                        "\nPlease enter the row number of bounty you'd like to close:\n\n"
                    )
                )

                closing_bounty_row = df_list_of_bounties.iloc[closing_bounty_index]

                confirm_close_bounty = "maybe"

                confirm_close_bounty_options = ["y", "n"]

                while confirm_close_bounty not in confirm_close_bounty_options:

                    confirm_close_bounty = input(
                        f"You selected to close the following bounty:\n\n{closing_bounty_row}\n\nIf you'd like to continue, please enter 'y'. If you'd like to cancel and return to the main menu enter 'n'.\n\n"
                    )

                    if confirm_close_bounty not in confirm_close_bounty_options:

                        print(
                            f'\nInvalid Entry: You entered "{confirm_close_bounty}", please make sure to enter one of the options listed above instead.\n'
                        )

                        confirm_close_bounty = "maybe"

                if confirm_close_bounty == "y":

                    print("\n")

                    fund_with_link(bounty_factory_contract_address)

                    print("\nYou successfully funded the contract with 0.1 LINK!")

                    pull_request_link = input(
                        "\nPlease make sure that the body of the pull request comment is in the following format '{Github Issue Link for Bounty}, {Your ETH Address}'. Also, do NOT update your pull request in any way after it has been merged as this will result in your pull request being ineligible to earn a bounty.\n\nIn order to close this bounty, please provide us with a Github link of your pull request that has been merged:\n\n"
                    )
                    parsed_pull_request_link = pull_request_converter(pull_request_link)
                    print("\n")
                    tx = bounty_factory_contract.requestPullRequestBody(
                        parsed_pull_request_link,
                        {"from": account},
                    )
                    tx.wait(5)
                    pull_request_body = bounty_factory_contract.bfViewPullRequestBody(
                        {"from": account}
                    )
                    pull_request_body_components = pull_request_body.split(", ")

                    bounty_issue_link = pull_request_body_components[0]

                    bounty_hunter_eth_address = pull_request_body_components[1]

                    if bounty_issue_link == closing_bounty_row["Github Issue Link"]:
                        oracle_account = get_account("oracle")
                        closing_bounty_address = (
                            bounty_factory_contract.bfReturnBountyAddress(
                                closing_bounty_index
                            )
                        )
                        closing_bounty_contract = Contract.from_abi(
                            "closing_bounty", closing_bounty_address, bounty_abi
                        )
                        closing_bounty_contract.close_bounty(
                            bounty_hunter_eth_address, {"from": oracle_account}
                        )

                        print(
                            "\nCongrats! You just closed this bounty and the bounty hunter will be sent the reward. Thank you for using DappWork!"
                        )

                    else:
                        print(
                            "Error: The pull request you provided either has a comment body that has a Github issue link that does not match the Github issue link of the bounty you are wanting to close, or there is some other problem with it."
                        )

                    user_choice = 0

            # This is for the withdraw
            while int(user_choice) == 4:

                print(
                    "\nYou selected to withdraw a bounty. You can find the list of currently open bounties below:\n"
                )

                total_number_of_bounties = (
                    bounty_factory_contract.bfViewBountyArrayLength()
                )

                list_of_bounties = []

                for bounty_index in range(total_number_of_bounties):

                    (
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount,
                        bounty_state,
                        bounty_creation_time_in_seconds,
                        bounty_lockup_seconds,
                        hunter_address,
                    ) = bounty_factory_contract.bfViewBounty(bounty_index)

                    bounty_amount_in_eth = Web3.fromWei(bounty_amount, "ether")

                    bounty_state = bounty_state_list[bounty_state]

                    bounty_creation_time = time.ctime(bounty_creation_time_in_seconds)

                    lockup_end_date = time.ctime(
                        bounty_creation_time_in_seconds + bounty_lockup_seconds
                    )

                    current_bounty_info = [
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount_in_eth,
                        bounty_state,
                        bounty_creation_time,
                        lockup_end_date,
                        hunter_address,
                    ]

                    list_of_bounties.append(current_bounty_info)

                df_list_of_bounties = pd.DataFrame(
                    list_of_bounties,
                    columns=[
                        "Owner",
                        "Name",
                        "Github Issue Link",
                        "Reward Amount (ETH)",
                        "Status",
                        "Creation Time",
                        "Lockup End Date",
                        "Winner",
                    ],
                )

                print(df_list_of_bounties)

                withdrawing_bounty_index = int(
                    input(
                        "\nPlease enter the row number of bounty you'd like to withdraw. Please note you can only withdraw a bounty that you are the owner of and which has a lockup end date that has passed. If you select a bounty whose lockup period has not ended, the transaction will fail.:\n\n"
                    )
                )

                withdrawing_bounty_row = df_list_of_bounties.iloc[
                    withdrawing_bounty_index
                ]

                withdrawing_bounty_lockup_end_date = withdrawing_bounty_row[
                    "Lockup End Date"
                ]

                confirm_withdraw_bounty = "maybe"

                confirm_withdraw_bounty_options = ["y", "n"]

                while confirm_withdraw_bounty not in confirm_withdraw_bounty_options:

                    confirm_withdraw_bounty = input(
                        f"You selected to withdraw the following bounty:\n\n{withdrawing_bounty_row}\n\nIf you'd like to continue, please enter 'y'. If you'd like to cancel and return to the main menu enter 'n'.\n\n"
                    )

                    if confirm_withdraw_bounty not in confirm_withdraw_bounty_options:

                        print(
                            f'\nInvalid Entry: You entered "{confirm_close_bounty}", please make sure to enter one of the options listed above instead.\n'
                        )

                        confirm_close_bounty = "maybe"

                    withdrawing_bounty_address = (
                        bounty_factory_contract.bfReturnBountyAddress(
                            withdrawing_bounty_index
                        )
                    )
                    withdrawing_bounty_contract = Contract.from_abi(
                        "withdrawing_bounty", withdrawing_bounty_address, bounty_abi
                    )
                    withdrawing_bounty_contract.withdraw_bounty({"from": account})
                    print(
                        f"You just withdrew bounty number {withdrawing_bounty_index} and you should receive the bounty reward back into your wallet.\n\nYou will now be returned to the main menu."
                    )

        i = 0


def main():
    pythonic_dappwork_ui()
