// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Bounty {
    address public owner_address;
    address public oracle;
    address public hunter_address;
    string public bounty_name;
    string public bounty_link;
    uint256 public bounty_amount;
    uint256 bounty_creation_time;
    uint256 bounty_lockup_seconds;

    enum BOUNTY_STATE {
        OPEN,
        CLOSED,
        WITHDRAWN
    }
    BOUNTY_STATE public bounty_state;

    constructor(
        string memory _bounty_name,
        string memory _bounty_link,
        uint256 _bounty_lockup_seconds,
        address _owner_address
    ) {
        owner_address = _owner_address;
        bounty_name = _bounty_name;
        bounty_link = _bounty_link;
        bounty_state = BOUNTY_STATE.OPEN;
        oracle = 0xFd1A5a86f7017E600b84087f4f0071565f42C1B7;
        bounty_creation_time = block.timestamp;
        bounty_lockup_seconds = _bounty_lockup_seconds;
    }

    function view_bounty()
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
        return (
            owner_address,
            bounty_name,
            bounty_link,
            bounty_amount,
            bounty_state,
            bounty_creation_time,
            bounty_lockup_seconds,
            hunter_address
        );
    }

    modifier onlyOwner() {
        require(msg.sender == owner_address);
        _;
    }

    function withdraw_bounty() public payable onlyOwner {
        require(
            bounty_state == BOUNTY_STATE.OPEN,
            "This bounty is already closed."
        );
        require(
            block.timestamp > bounty_creation_time + bounty_lockup_seconds,
            "Bounties must be open for at least the lockup duration before they can be closed and have their funds withdrawn by the owner."
        );
        payable(msg.sender).transfer(address(this).balance);
        bounty_amount = address(this).balance;
        bounty_state = BOUNTY_STATE.WITHDRAWN;
    }

    function fund_bounty() public payable onlyOwner {
        require(
            bounty_state == BOUNTY_STATE.OPEN,
            "This bounty is already closed."
        );
        bounty_amount = address(this).balance;
    }

    modifier onlyOracle() {
        require(msg.sender == oracle);
        _;
    }

    function close_bounty(address _bounty_winner) public payable onlyOracle {
        require(
            bounty_state == BOUNTY_STATE.OPEN,
            "This bounty is already closed."
        );
        payable(_bounty_winner).transfer(address(this).balance);
        bounty_amount = address(this).balance;
        bounty_state = BOUNTY_STATE.CLOSED;
    }

    function change_hunter_address(address _hunter_address) public onlyOracle {
        require(
            bounty_state == BOUNTY_STATE.OPEN,
            "This bounty is either closed or withdrawn."
        );
        hunter_address = _hunter_address;
        bounty_state = BOUNTY_STATE.CLOSED;
    }
}
