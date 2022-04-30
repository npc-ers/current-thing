from brownie import *
import brownie

def test_current_thing_sets(npc_minted):
    thing_init = npc_minted.currentThing(0)
    npc_minted.supportCurrentThing(0, "New Thing")
    assert npc_minted.currentThing(0) != thing_init

def test_staking_current_thing_increases_balance(npc_staked, thing, accounts):
    init_bal = thing.balanceOf(accounts[0])
    init_time = chain.time()

    chain.mine(timedelta=10000)
    assert chain.time() - init_time > 0
    assert thing.balanceOf(accounts[0]) > init_bal


def test_new_epoch_earns_no_inflation(npc_staked, thing, accounts):
    chain.mine(timedelta=10000)
    init_bal = thing.balanceOf(accounts[0])
    thing.newCurrentThing("Thing 2", {"from": accounts[0]})
    final_bal = thing.balanceOf(accounts[0])
    chain.mine(timedelta=10000)
    assert thing.balanceOf(accounts[0]) == final_bal

def test_staked_cannot_transfer(npc_staked, accounts):
    with brownie.reverts("Token is Staked"):
        npc_staked.transferFrom(accounts[0], accounts[1], 0)
    assert npc_staked.ownerOf(0) == accounts[0]

def test_can_transfer_new_epoch(npc_staked, accounts, thing):
    thing.newCurrentThing("Thing 2", {'from': accounts[0]})
    npc_staked.transferFrom(accounts[0], accounts[1], 0)
    assert False
    assert npc_staked.ownerOf(0) == accounts[1]

