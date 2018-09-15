pragma solidity ^0.4.22;

import "openzeppelin-solidity/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "openzeppelin-solidity/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "./KaniaCoin.sol";

contract KaniaCoinICO is Ownable, TimedCrowdsale, MintedCrowdsale {
 function KaniaCoinICO(uint256 _startTime, uint256 _endTime, uint256 _rate, address _wallet, KaniaCoin _token) public
   Crowdsale(_rate, _wallet, _token)
   TimedCrowdsale(_startTime, _endTime) {}
}
