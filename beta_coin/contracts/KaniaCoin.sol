
pragma solidity ^0.4.22;
 
import "openzeppelin-solidity/contracts/token/ERC20/MintableToken.sol";
 
contract KaniaCoin is MintableToken {

	string public constant name = "KaniaCoin";
	string public constant symbol = "KC";
	uint8 public constant decimals = 18;

}
