#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def thing(CurrentThing, accounts):
    thing = CurrentThing.deploy({'from': accounts[0]})
    thing.test_mint(accounts[0], 10 ** 18)
    return thing


@pytest.fixture(scope="module")
def npc(NPC, accounts, thing):
    nft = NPC.deploy(thing, {'from': accounts[0]})
    thing.set_nft_addr(nft, {'from': accounts[0]}) 
    return nft

@pytest.fixture(scope="module")
def npc_minted(npc, accounts):
    npc.mint(accounts[0])
    return npc

@pytest.fixture(scope="module")
def root():
    return ""
