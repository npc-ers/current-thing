# @version ^0.3.3

"""
@title Current Thing
@notice Based on the ERC-20 token standard as defined at
        https://eips.ethereum.org/EIPS/eip-20
"""

from vyper.interfaces import ERC20

implements: ERC20



event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256


interface NPC:
    def ownerOf(tokenId: uint256) -> address: view
 

name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
totalSupply: public(uint256)

balances: HashMap[address, uint256]
allowances: HashMap[address, HashMap[address, uint256]]

npc: public(NPC)
MAX_NFT_SUPPLY: constant(uint256) = 1000
owner: address

YEAR: constant(uint256) = 86400 * 365
EMISSION_RATE: constant(uint256) = 1_000_000 * 10 ** 18 / YEAR

currentThing: String[128]
epoch: public(uint256)
epoch_supporters: HashMap[uint256, HashMap[uint256, address]] # epoch -> id -> addr
epoch_timestamps: HashMap[uint256, HashMap[uint256, uint256]] # epoch -> id -> timestamp


@external
def __init__(_decimals: uint256, _total_supply: uint256):
    self.name = "Current Thing"
    self.symbol = "THING"
    self.decimals = _decimals
    self.balances[msg.sender] = _total_supply
    self.totalSupply = _total_supply
    self.owner = msg.sender
    log Transfer(ZERO_ADDRESS, msg.sender, _total_supply)


@view
@internal
def _calc_epoch_inflation(addr: address) -> uint256:
    inflation: uint256 = 0
    for i in range(MAX_NFT_SUPPLY):
        if self.epoch_timestamps[self.epoch][i] > 0:
             inflation += (block.timestamp - self.epoch_timestamps[self.epoch][i]) * EMISSION_RATE
    return inflation

@view
@external
def balanceOf(_owner: address) -> uint256:
    """
    @notice Getter to check the current balance of an address
    @param _owner Address to query the balance of
    @return Token balance
    """
    return self.balances[_owner] + self._calc_epoch_inflation(_owner)


@view
@external
def allowance(_owner : address, _spender : address) -> uint256:
    """
    @notice Getter to check the amount of tokens that an owner allowed to a spender
    @param _owner The address which owns the funds
    @param _spender The address which will spend the funds
    @return The amount of tokens still available for the spender
    """
    return self.allowances[_owner][_spender]


@external
def approve(_spender : address, _value : uint256) -> bool:
    """
    @notice Approve an address to spend the specified amount of tokens on behalf of msg.sender
    @dev Beware that changing an allowance with this method brings the risk that someone may use both the old
         and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
         race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
         https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
    @param _spender The address which will spend the funds.
    @param _value The amount of tokens to be spent.
    @return Success boolean
    """
    self.allowances[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True


@internal
def _transfer(_from: address, _to: address, _value: uint256):
    """
    @dev Internal shared logic for transfer and transferFrom
    """
    assert self.balances[_from] >= _value, "Insufficient balance"
    self.balances[_from] -= _value
    self.balances[_to] += _value
    log Transfer(_from, _to, _value)


@external
def transfer(_to : address, _value : uint256) -> bool:
    """
    @notice Transfer tokens to a specified address
    @dev Vyper does not allow underflows, so attempting to transfer more
         tokens than an account has will revert
    @param _to The address to transfer to
    @param _value The amount to be transferred
    @return Success boolean
    """
    self._transfer(msg.sender, _to, _value)
    return True


@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    """
    @notice Transfer tokens from one address to another
    @dev Vyper does not allow underflows, so attempting to transfer more
         tokens than an account has will revert
    @param _from The address which you want to send tokens from
    @param _to The address which you want to transfer to
    @param _value The amount of tokens to be transferred
    @return Success boolean
    """
    assert self.allowances[_from][msg.sender] >= _value, "Insufficient allowance"
    self.allowances[_from][msg.sender] -= _value
    self._transfer(_from, _to, _value)
    return True


@external
def setNFT(addr: address):
    assert msg.sender == self.owner
    self.npc = NPC(addr)

@external
def supportCurrentThing(tokenId: uint256, addr: address):
    self.epoch_supporters[self.epoch][tokenId] = addr
    self.epoch_timestamps[self.epoch][tokenId] = block.timestamp


@internal
def _commit_epoch_balances():
    for i in range(MAX_NFT_SUPPLY):
        addr: address = self.epoch_supporters[self.epoch][i]
        self.balances[addr] += (block.timestamp - self.epoch_timestamps[self.epoch][i]) * EMISSION_RATE


@external
def newCurrentThing(currentThing: String[128]):
    self._commit_epoch_balances()
    self.currentThing = currentThing
    self.epoch += 1
    
