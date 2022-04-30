from brownie import *

def test_current_thing_sets(npc_minted):
    thing_init = npc_minted.currentThing(0)
    npc_minted.setCurrentThing(0, "New Thing")
    assert npc_minted.currentThing(0) != thing_init
