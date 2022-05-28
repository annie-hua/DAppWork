// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Bounty.sol";

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract BountyFactory is Bounty, ChainlinkClient {
    using Chainlink for Chainlink.Request;
    // using strings for *;
    Bounty[] public bountyArray;
    event RequestedBountyIndex(uint256 bountyIndex);

    string public pr_body;

    bytes32 private jobId;
    uint256 private fee;

    event RequestFirstId(bytes32 indexed requestId, string id);

    constructor()
        Bounty("Bounty Factory Contract", "Not Applicable", 0, msg.sender)
    {
        // For ETH Kovan Testnet
        setChainlinkToken(0xa36085F69e2889c224210F603D836748e7dC0088);
        setChainlinkOracle(0x74EcC8Bdeb76F2C6760eD2dc8A46ca5e581fA656);
        jobId = "7d80a6386ef543a3abb52817f6707e3b";

        // For MATIC Mumbai Testnet
        // setChainlinkToken(0x326C977E6efc84E512bB9C30f76E30c160eD06FB);
        // setChainlinkOracle(Unable to find a working one);
        // jobId = "Unable to find a working one";

        // For AVAX Fuji Testnet
        // setChainlinkToken(0x0b9d5D9136855f6FEc3c0993feE6E9CE8a297846);
        // setChainlinkOracle(Unable to find a working one);
        // jobId = "Unable to find a working one";

        // For BSC Testnet
        // setChainlinkToken(0x84b9b910527ad5c03a9ca831909e21e236ea7b06);
        // setChainlinkOracle(Unable to find a working one);
        // jobId = "Unable to find a working one";

        fee = (1 * LINK_DIVISIBILITY) / 10;
    }

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
            address
        )
    {
        return Bounty(address(bountyArray[_bountyIndex])).view_bounty();
    }

    function bfViewPullRequestBody()
        public
        view
        returns (string memory _pr_body)
    {
        return pr_body;
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

    function requestPullRequestBody(string memory _parsed_pull_request_link)
        public
        returns (bytes32 requestId)
    {
        Chainlink.Request memory req = buildChainlinkRequest(
            jobId,
            address(this),
            this.fulfill.selector
        );

        req.add("get", _parsed_pull_request_link);
        req.add("path", "body");
        return sendChainlinkRequest(req, fee);
    }

    function fulfill(bytes32 _requestId, string memory _pr_body)
        public
        recordChainlinkFulfillment(_requestId)
    {
        emit RequestFirstId(_requestId, _pr_body);
        pr_body = _pr_body;
    }
}
