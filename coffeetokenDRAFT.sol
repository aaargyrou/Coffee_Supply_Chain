pragma solidity 0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract coffeeChain is ERC721Full {
    constructor() public ERC721Full("CoffeeChainToken", "COF") {}

    // --------Structs--------
    struct Node {
        string nodeName;
        string nodeType;
        string Latitude;
        string Longitude;
    }

    // --------Mappings--------

    mapping(address => Node) public allNodes;



    // --------Functions--------    
    function addNode(
        address payable businessAddress,
        string memory name,
        string memory nodeType,
        string memory latitude,
        string memory longitude
    ) public {
        Nodes[businessAddress] = Node(name, nodeType, latitude, longitude);
    }

    function registerCoffee(
        address owner,
        string memory tokenURI
        ) public {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);
    }

    function transferCoffee(
        address owner, 
        address newOwner
        uint256 tokenId
        ) public {
        require(owner == ownerOf(tokenId));
        transferFrom(owner, newOwner, tokenId);
        }

    function getNode(address businessAddress) public view returns (Node) {
        return Nodes[businessAddress];
    }
    
    function getCoffeeBag(uint256 tokenId) public view returns (CoffeeBag) {
        return coffeeBag[tokenId];
    }
}