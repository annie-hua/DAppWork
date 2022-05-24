// SPDX-License-Identifier: MIT

pragma solidity 0.8.0;

import "./Bounty.sol";

contract BountyFactory is Bounty {
    Bounty[] public bountyArray;

    constructor()
        Bounty("Bounty Factory Contract", "Not Applicable", 0, msg.sender)
    {}

    function createBountyContract(
        string memory _bounty_name,
        string memory _bounty_link,
        uint256 _bounty_lockup_seconds,
        address _owner_address
    ) public {
        Bounty bounty = new Bounty(
            _bounty_name,
            _bounty_link,
            _bounty_lockup_seconds,
            _owner_address
        );
        bountyArray.push(bounty);
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
}
