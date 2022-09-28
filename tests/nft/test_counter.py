import brownie
import pytest
from brownie import ZERO_ADDRESS, accounts, exceptions


#
# Inquire initial count
#
def test_initialCount(npc, premint, minter):
    count = npc.totalSupply()
    assert premint == count


#
# Test increment
#


def test_token_by_index_accurate(npc, minter, alice, premint):
    assert npc.totalSupply() == premint
    quantity = 10
    price = minter.mint_price(quantity, alice)
    tx = minter.mint(quantity, {"from": alice, "value": price})
    my_tokens = []
    for i in range(quantity):
        my_tokens.append(npc.tokenByIndex(i))

    for i in range(len(tx.events)):
        if "seat_id" in tx.events[i]:
            assert tx.events[i]["seat_id"] in my_tokens


def test_increment(minted, premint):
    assert minted.totalSupply() == 1 + premint


def test_nonzero_owner_index(npc):
    with brownie.reverts():
        npc.tokenOfOwnerByIndex(ZERO_ADDRESS, 0)
