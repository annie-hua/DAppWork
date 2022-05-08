// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Bounty.sol";

contract BountyFactory is Bounty {
    Bounty[] public bountyArray;

    function createBountyContract() public {
        Bounty bounty = new Bounty();
        bountyArray.push(bounty);
    }

    // function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber)
    //     public
    // {
    //     SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(
    //         _simpleStorageNumber
    //     );
    // }

    // function sfGet(uint256 _simpleStorageIndex) public view returns (uint256) {
    //     return
    //         SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]))
    //             .retrieve();
    // }
}
