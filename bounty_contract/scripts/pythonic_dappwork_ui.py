from click import confirm
from brownie import Bounty, BountyFactory, network, config, Contract
from scripts.helpful_scripts import get_account
from scripts.view_bounty_array import (
    view_bounty_factory_array_length,
    view_bounty_array_contents,
)
import json
import pandas as pd

i = 0

with open("./build/contracts/BountyFactory.json") as f:
    bounty_factory_json = json.load(f)

bounty_factory_abi = bounty_factory_json["abi"]

with open("./build/contracts/Bounty.json") as f:
    bounty_json = json.load(f)

bounty_abi = bounty_json["abi"]

bounty_factory_contract_address = "0xCe8C2F0cD1864174D9b581fa97138EC8945dDD2c"
bounty_factory_contract = Contract.from_abi(
    "Bounty_Factory_Contract", bounty_factory_contract_address, bounty_factory_abi
)

account = get_account(0)


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
                        bounty_creation_time,
                        bounty_lockup_seconds,
                        hunter_address,
                    ) = bounty_factory_contract.bfViewBounty(bounty_index)

                    current_bounty_info = [
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount,
                        bounty_state,
                        bounty_creation_time,
                        bounty_lockup_seconds,
                        hunter_address,
                    ]

                    list_of_bounties.append(current_bounty_info)

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

                bounty_amount_in_wei = bounty_amount * 1000000000000000000  # 18 zeros

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

                for bounty_index in range(total_number_of_bounties):

                    (
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount,
                        bounty_state,
                        bounty_creation_time,
                        bounty_lockup_seconds,
                        hunter_address,
                    ) = bounty_factory_contract.bfViewBounty(bounty_index)

                    current_bounty_info = [
                        owner,
                        bounty_name,
                        bounty_link,
                        bounty_amount,
                        bounty_state,
                        bounty_creation_time,
                        bounty_lockup_seconds,
                        hunter_address,
                    ]

                    print(current_bounty_info)

                input(
                    "\nPlease select from the list of bounties which one you'd like to close:\n"
                )

        i = 0


def main():
    pythonic_dappwork_ui()