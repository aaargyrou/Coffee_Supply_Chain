pragma solidity 0.5.17;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract supplyChain is ERC721Full {
    constructor(string memory name, string memory token)
        public
        ERC721Full(name, token)
    {}

    //--------Structs--------

    struct manufacturer {
        string name;
        string documentationURI;
    }

    struct product {
        string name;
        string productKey;
        string productURI;
        uint256 price;
        uint256 manufacturerId;
        uint256 GTIN;
    }

    //--------Mappings--------

    mapping(uint256 => manufacturer) public manufacturers;
    mapping(uint256 => product) public products;

    //--------Events--------

    /*
    event sendProduct()
    event closeSale()
    */

    //--------Functions--------

    // function to allow users to add themselves or their company as a manufacturer on the contract.
    function addManufacturer(
        string memory name,
        string memory documentationURI,
        address owner
    ) public returns (uint256) {
        uint256 manufacturerId = totalSupply();
        _mint(owner, manufacturerId);
        _setTokenURI(manufacturerId, documentationURI);

        manufacturers[manufacturerId] = manufacturer(name, documentationURI);

        return manufacturerId;
    }

    /*

    // allow a manufacturer to add a product (needs some way to ensure only the manufacturer with their account can use this function)
    function addProduct(
        string memory name,
        string memory productKey,
        string memory productURI,
        uint256 price,
        uint256 manufacturerId,
        uint256 GTIN) {}

    // allow a manufacturer to update the sale pric of a product
    function updatePrice()

    // call function to view the price of a specific product
    function requestQuote()

    // function for two adresses to initiate the sale of a product
    function initiateSale()
    */
}
