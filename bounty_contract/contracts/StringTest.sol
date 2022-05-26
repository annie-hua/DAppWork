// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./strings.sol";

contract StringTest {
    string _input_text;

    function first_test(string memory _input_text)
        public
        pure
        returns (uint256 _number)
    {
        uint256 length = _input_text.strings.toSlice().len(); // 17
    }
}
