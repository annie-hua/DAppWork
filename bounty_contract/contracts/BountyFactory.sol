// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;

import "./Bounty.sol";

contract BountyFactory is Bounty {
    Bounty[] public bountyArray;
    event RequestedBountyIndex(uint256 bountyIndex);

    constructor()
        Bounty("Bounty Factory Contract", "Not Applicable", 0, msg.sender)
    {}

    function createBountyContract(
        string memory _bounty_name,
        string memory _bounty_link,
        uint256 _bounty_lockup_seconds,
        address _owner_address
    ) public returns (uint256 bountyIndex) {
        Bounty bounty = new Bounty(
            _bounty_name,
            _bounty_link,
            _bounty_lockup_seconds,
            _owner_address
        );
        bountyArray.push(bounty);
        bountyIndex = bountyArray.length - 1;
        emit RequestedBountyIndex(bountyIndex);
    }

    function bfViewBounty(uint256 _bountyIndex)
        public
        view
        returns (
            address,
            string memory,
            string memory,
            uint256,
            BOUNTY_STATE,
            uint256,
            uint256,
            string memory,
            address
        )
    {
        return Bounty(address(bountyArray[_bountyIndex])).view_bounty();
    }

    function bfViewBountyArrayLength()
        public
        view
        returns (uint256 _bountyArrayLength)
    {
        return bountyArray.length;
    }

    function bfViewBountyArray()
        public
        view
        returns (Bounty[] memory _bountyArray)
    {
        return bountyArray;
    }

    function bfReturnBountyAddress(uint256 _bountyIndex)
        public
        view
        returns (address)
    {
        return address(bountyArray[_bountyIndex]);
    }

    // This function will initiate the chainlink job, it will take as an input the pull request API link and the pull request index. It will also check to make sure there is enough LINK token in the contract so Chainlink oracle will be paid

    // function bf
}
