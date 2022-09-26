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


def test_owner_can_mint(thing, deployer, alice, bob):
    assert thing.balanceOf(alice) == 0
    # Set unique minter/owner address to test
    thing.admin_set_owner(bob, {"from": deployer})
    thing.mint(alice, 10**18, {"from": bob})
    assert thing.balanceOf(alice) == 10**18


def test_minter_can_mint(thing, deployer, alice, bob):
    assert thing.balanceOf(alice) == 0
    # Set unique minter/owner address to test
    thing.admin_set_minter(bob, {"from": deployer})
    thing.mint(alice, 10**18, {"from": bob})
    assert thing.balanceOf(alice) == 10**18


def test_admin_can_update_image(thing, deployer):
    thing.admin_update_image("Test", {"from": deployer})
    assert thing.image() == "Test"


def test_rando_cannot_update_image(thing, alice):
    with brownie.reverts():
        thing.admin_update_image("Test", {"from": alice})


def test_rando_cannot_mint(thing, alice, bob):
    with brownie.reverts():
        thing.mint(alice, 10**18, {"from": bob})


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


def test_cannot_burn(thing, alice, deployer):
    thing.mint(alice, 10**18, {"from": deployer})
    assert thing.balanceOf(alice) == 10**18
    with brownie.reverts():
        thing.transfer(ZERO_ADDRESS, 10**18, {"from": alice})
    assert thing.balanceOf(alice) == 10**18
