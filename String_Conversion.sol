import "https://github.com/Arachnid/solidity-stringutils/blob/master/src/strings.sol";
using strings for *;

    function parseLink(string gitlink) returns (string newLink){
       
        strings.slice memory stringSlice = "gitlink".toSlice();
        strings.slice memory delim = "".toSlice();
        string[] memory newLinkKinda = new string[](stringSlice.count(delimeterSlice));
        for (uint i = 0; i < strings.length; i++) {
           newLinkKinda[i] = stringSlice.split(delim).toString();
        }
        link = newLinkKinda[7:];
        
    
    }
