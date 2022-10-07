// SPDX-License-Identifier: MIT

pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract coffeeChain is ERC721Full {
    address admin;

    constructor() public ERC721Full("coffeeToken", "BREW") {
        admin = msg.sender;
    }

    //--------Structs--------

    struct Node {
        string nodeName;
        string nodeType;
        string Latitude;
        string Longitude;
        bool exists;
    }

    struct Batch {
        uint256 value;
        bool state;
    }

    //--------Mappings--------

    mapping(address => Node) public Nodes;
    mapping(uint256 => Batch) public Batches;

    //--------Events--------

    event transfer(address transferFrom, address transferTo, uint256 tokenId);

    //--------Modifiers--------

    modifier onlyAdmin() {
        require(
            msg.sender == admin,
            "Access to this function requires admin rights."
        );
        _;
    }

    modifier adminOrNode() {
        require(
            msg.sender == admin || (Nodes[msg.sender].exists == true),
            "Access to this function requires admin or owner rights."
        );
        _;
    }

    modifier onlyNode() {
        require(
            Nodes[msg.sender].exists == true,
            "Access to this function requires owner rights."
        );
        _;
    }

    //--------Node and Batch Functions--------

    // adds a batch to the Batches mapping and mints the respective NFT token under the owner address. (requires admin or node rights)
    function addBatch(
        address owner,
        string memory tokenURI,
        uint256 value,
        bool readyForShipping
    ) public adminOrNode returns (uint256) {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);
        Batches[tokenId] = Batch(value, readyForShipping);
        return tokenId;
    }

    // adds a node to the Nodes mapping (requires admin rights)
    function addNode(
        address businessAddress,
        string memory name,
        string memory nodeType,
        string memory latitude,
        string memory longitude
    ) public onlyAdmin {
        Nodes[businessAddress] = Node(
            name,
            nodeType,
            latitude,
            longitude,
            true
        );
    }

    // transfers a batch NFT from one address to another and transfers eth to owner, sets batch state to false after transfer (requires batch to be in the true state)
    function transferBatch(address payable owner, uint256 tokenId)
        public
        payable
    {
        require(Batches[tokenId].state == true, "batch still processing");
        require(msg.value == Batches[tokenId].value, "incorrect amount sent");
        safeTransferFrom(owner, msg.sender, tokenId);
        owner.transfer(msg.value);
        emit transfer(owner, msg.sender, tokenId);
        Batches[tokenId].state = false;
    }

    //--------Setters and Getters--------

    // changes batch to desired state.
    function setBatchState(bool state, uint256 tokenId) public adminOrNode {
        Batches[tokenId].state = state;
    }

    function getBatchState(uint256 tokenId) public view returns (bool) {
        return Batches[tokenId].state;
    }

    // sets batch value
    function setBatchValue(uint256 value, uint256 tokenId) public onlyNode {
        Batches[tokenId].value = value;
    }

    function getBatchValue(uint256 tokenId) public view returns (uint256) {
        return Batches[tokenId].value;
    }
}
