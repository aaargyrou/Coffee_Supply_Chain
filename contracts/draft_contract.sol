// SPDX-License-Identifier: MIT

pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract coffeeChain is ERC721Full {
    constructor() public ERC721Full("coffeeToken", "BREW") {
        address admin = msg.sender;
    }

    //--------Structs--------

    struct Node {
        string nodeName;
        string nodeType;
        string Latitude;
        string Longitude;
    }

    struct Batch {
        string batchURI;
    }
    //--------Mappings--------

    mapping(address => Node) public Nodes;
    mapping(uint256 => Batch) public Batches;

    //--------Modifiers--------
    /*
    modifier isAdmin{
        _;
    }
    modifier isPrimaryProduction{
       require(allNodes[msg.sender].nodeType == , "not authorised");
       _;
    }
    modifier isStorage{
       _;
    }
    modifier isRoaster{
       _;
    }
    modifier isRetail{
       _;
    }
*/

    //--------Events--------

    event transfer(address transferFrom, address transferTo, uint256 tokenId);

    //--------Functions--------

    function addBatch(address owner, string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);
        Batches[tokenId] = Batch(tokenURI);
        return tokenId;
    }

    function addNode(
        address payable businessAddress,
        string memory name,
        string memory nodeType,
        string memory latitude,
        string memory longitude
    ) public {
        Nodes[businessAddress] = Node(name, nodeType, latitude, longitude);
    }

    function transferBatch(
        address owner,
        address to,
        uint256 tokenId
    ) public {
        safeTransferFrom(owner, to, tokenId);
        emit transfer(owner, to, tokenId);
    }
}
