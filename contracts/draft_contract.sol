// SPDX-License-Identifier: MIT
pragma solidity 0.8.14;

contract coffeeChain {
    constructor() {
        address admin = msg.sender;
    }

    //--------Structs--------

    struct Node {
        string nodeName;
        string nodeType;
        string Latitude;
        string Longitude;
    }
    //--------Mappings--------

    mapping(address => Node) public allNodes;

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

    event transfer(address transferFrom, address transferTo, string date);

    event newPrimaryProduction(
        string coffeeType,
        string growingConditions,
        string growingSeason,
        string dateOfHarvest,
        string shippingDate
    );

    event newStorageBatch(
        string inputBatches,
        string storageTemp,
        string dateStored,
        string dateDispatched
    );

    event newRoastingBatch(
        string inputBatches,
        string dryingTemp,
        string roastingTemp,
        string roastTime,
        string dateOfRoast
    );

    event newPackagedUnit(
        string inputBatches,
        string packagedFor,
        string productURI
    );

    //--------Functions--------

    function addNode(
        address payable businessAddress,
        string memory name,
        string memory nodeType,
        string memory latitude,
        string memory longitude
    ) public {
        allNodes[businessAddress] = Node(name, nodeType, latitude, longitude);
    }

    function sendPrimaryProduction(
        address payable businessAddress,
        address recieverAddress,
        string memory coffeeType,
        string memory growingConditions,
        string memory growingSeason,
        string memory dateOfHarvest,
        string memory shippingDate
    ) public {
        emit newPrimaryProduction(
            coffeeType,
            growingConditions,
            growingSeason,
            dateOfHarvest,
            shippingDate
        );
    }

    function sendStoredGoods(
        address payable businessAddress,
        address recieverAddress,
        string memory inputBatches,
        string memory storageTemp,
        string memory dateStored,
        string memory dateDispatched
    ) public {
        emit newStorageBatch(
            inputBatches,
            storageTemp,
            dateStored,
            dateDispatched
        );
    }

    function sendRoastedCoffee(
        address payable businessAddress,
        address recieverAddress,
        string memory inputBatches,
        string memory dryingTemp,
        string memory roastingTemp,
        string memory roastTime,
        string memory dateOfRoast
    ) public {
        emit newRoastingBatch(
            inputBatches,
            dryingTemp,
            roastingTemp,
            roastTime,
            dateOfRoast
        );
    }

    function sendUnits(
        address payable businessAddress,
        address recieverAddress,
        string memory inputBatches,
        string memory packagedFor,
        string memory productURI
    ) public {
        emit newPackagedUnit(inputBatches, packagedFor, productURI);
    }
}
