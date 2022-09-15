import brownie
from brownie import ZERO_ADDRESS


def test_admin_set_minter_works(thing, alice):
    thing.admin_set_minter(alice, {"from": thing.owner()})
    assert thing.minter() == alice


def test_admin_set_owner_works(thing, alice):
    thing.admin_set_owner(alice, {"from": thing.owner()})
    assert thing.owner() == alice


def test_admin_can_set_nft_addr(thing):
    thing.admin_set_npc_addr(ZERO_ADDRESS, {"from": thing.owner()})


def test_rando_cannot_admin_set_owner(thing, charlie):
    with brownie.reverts():
        thing.admin_set_owner(charlie, {"from": charlie})


def test_rando_cannot_admin_set_minter(thing, charlie):
    with brownie.reverts():
        thing.admin_set_minter(charlie, {"from": charlie})


def test_rando_cannot_set_nft_addr(thing, charlie):
    with brownie.reverts():
        thing.admin_set_npc_addr(charlie, {"from": charlie})


def test_rando_cannot_mint(thing, charlie):
    with brownie.reverts():
        thing.mint(charlie, 10**18, {"from": charlie})
