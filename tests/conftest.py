#!/usr/bin/python3

import pytest
from brownie import (
    NPC,
    CurrentThing,
    ERC721TokenReceiverImplementation,
    Indoctrinator,
    accounts,
    Vote
)


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def thing(CurrentThing, deployer):
    thing = CurrentThing.deploy({"from": deployer})
    thing.mint(deployer, 10**18, {"from": deployer})
    return thing


@pytest.fixture(scope="module")
def npc(NPC, deployer, thing):
    nft = NPC.deploy({"from": deployer})
    thing.admin_set_npc_addr(nft, {"from": deployer})
    return nft


@pytest.fixture(scope="module")
def npc_minted(npc, deployer):
    npc.mint(deployer)
    return npc


@pytest.fixture(scope="module")
def root():
    return ""


@pytest.fixture(scope="module")
def deployer():
    return accounts[0]


@pytest.fixture(scope="module")
def alice():
    return accounts[1]


@pytest.fixture(scope="module")
def bob():
    return accounts[2]


@pytest.fixture(scope="module")
def charlie():
    return accounts[3]


@pytest.fixture(scope="module")
def token(npc):
    return npc


@pytest.fixture(scope="module")
def minted(npc, alice):
    npc.mint(alice)
    return npc


@pytest.fixture(scope="module")
def minted_token_id():
    return 0


@pytest.fixture(scope="module")
def premint():
    return 100


@pytest.fixture(scope="module")
def minter(npc, deployer, thing, premint, accounts, alice):
 
    minter = Indoctrinator.deploy({"from": deployer})
    npc.set_minter(minter, {"from": deployer})
    minter.admin_set_nft_addr(npc, {"from": deployer})
    minter.premint(accounts[0])

    thing.admin_set_minter(minter, {"from": deployer})
    minter.admin_set_token_addr(thing, {"from": deployer})

    return minter


@pytest.fixture(scope="module")
def token_metadata():
    return {"name": "NPC-ers", "symbol": "NPC"}


@pytest.fixture(scope="module")
def tokenReceiver(deployer):
    return ERC721TokenReceiverImplementation.deploy({"from": deployer})


@pytest.fixture(scope="module")
def staker(npc, thing, alice):
    return Vote.deploy({'from': alice})


