#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def thing(CurrentThing, accounts):
    return CurrentThing.deploy(18, 1e21, {'from': accounts[0]})


@pytest.fixture(scope="module")
def npc(NPC, accounts):
    return NPC.deploy({'from': accounts[0]})

@pytest.fixture(scope="module")
def npc_minted(npc, accounts):
    npc.mint(accounts[0])
    return npc


