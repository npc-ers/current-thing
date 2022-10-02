import brownie
import pytest
from brownie import ZERO_ADDRESS


def test_minter_can_mint(minter, npc, alice):
    assert npc.balanceOf(alice) == 0
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    assert npc.balanceOf(alice) == 1


def test_non_minter_cannot_mint(npc, alice):
    with brownie.reverts():
        npc.mint(alice, {"from": alice})


def test_cannot_mint_with_too_little(minter, alice):
    price = minter.mint_price(1, alice)
    with brownie.reverts():
        minter.mint(1, {"from": alice, "value": price - 1})


def test_can_mint_with_overpay(minter, alice, npc):
    price = minter.mint_price(1, alice)
    assert npc.balanceOf(alice) == 0

    minter.mint(1, {"from": alice, "value": price + 1})

    assert npc.balanceOf(alice) == 1


def test_can_mint_quantity(minter, alice, npc):
    mint_num = 10
    price = minter.mint_price(mint_num, alice)
    assert npc.balanceOf(alice) == 0
    minter.mint(mint_num, {"from": alice, "value": price})
    assert npc.balanceOf(alice) == mint_num


def test_can_update_whitelist(minter, deployer, bob, npc):
    assert minter.mint_price(1, bob) > 0
    assert npc.balanceOf(bob) == 0
    minter.admin_add_to_whitelist(bob, {"from": deployer})
    assert minter.mint_price(1, bob) == 0
    minter.mint(1, {"from": bob})
    assert npc.balanceOf(bob) == 1


def test_cannot_reuse_whitelist(minter, deployer, bob, npc):
    qty = minter.whitelist_max()
    assert minter.mint_price(qty, bob) > 0
    assert npc.balanceOf(bob) == 0

    minter.admin_add_to_whitelist(bob, {"from": deployer})

    minter.mint(qty, {"from": bob})
    assert npc.balanceOf(bob) == qty
    assert minter.mint_price(qty, bob) > 0
    with brownie.reverts():
        minter.mint(1, {"from": bob})


def test_can_add_coupon(minter, deployer, alice, thing, npc):
    qty = minter.whitelist_max()
    assert minter.mint_price(qty, alice) > 0
    assert npc.balanceOf(alice) == 0

    # Use $THING as a stand-in for a standard token
    minter.admin_update_coupon_token(thing, {"from": deployer})
    minter.admin_mint_erc20(alice, 10**18, {"from": deployer})

    assert minter.mint_price(qty, alice) == 0
    minter.mint(qty, {"from": alice})
    assert npc.balanceOf(alice) > 0


def test_cannot_reuse_coupon(minter, deployer, alice, thing, npc):
    qty = minter.whitelist_max()
    assert minter.mint_price(qty, alice) > 0
    assert npc.balanceOf(alice) == 0

    minter.admin_update_coupon_token(thing, {"from": deployer})
    minter.admin_mint_erc20(alice, 10**18, {"from": deployer})

    assert minter.mint_price(qty, alice) == 0
    minter.mint(qty, {"from": alice})
    assert npc.balanceOf(alice) > 0
    assert minter.mint_price(qty, alice) > 0
    with brownie.reverts():
        minter.mint(qty, {"from": alice})


def test_mint_is_sequential(minter, alice, bob, charlie, token):
    init_id = token.totalSupply()
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    minter.mint(1, {"from": bob, "value": minter.mint_price(1, bob)})
    minter.mint(1, {"from": charlie, "value": minter.mint_price(1, charlie)})
    assert token.ownerOf(init_id + 0) == alice
    assert token.ownerOf(init_id + 1) == bob
    assert token.ownerOf(init_id + 2) == charlie


def test_mint_multiple_is_sequential(minter, alice, bob, charlie, token):
    init_id = token.totalSupply()
    minter.mint(2, {"from": alice, "value": minter.mint_price(2, alice)})
    minter.mint(3, {"from": bob, "value": minter.mint_price(3, bob)})
    minter.mint(4, {"from": charlie, "value": minter.mint_price(4, charlie)})

    for i in range(2):
        assert token.ownerOf(i + init_id) == alice

    for i in range(2, 5):
        assert token.ownerOf(i + init_id) == bob

    for i in range(5, 9):
        assert token.ownerOf(i + init_id) == charlie


def test_can_mint_under_max_whitelist(minter, deployer, bob, npc):
    assert minter.mint_price(1, bob) > 0
    assert npc.balanceOf(bob) == 0
    minter.admin_add_to_whitelist(bob, {"from": deployer})
    assert minter.mint_price(1, bob) == 0
    minter.mint(1, {"from": bob})
    assert npc.balanceOf(bob) == 1

    max_mint = minter.whitelist_max()
    assert minter.mint_price(max_mint, bob) == minter.min_price()
    assert minter.mint_price(max_mint - 1, bob) == 0

    minter.mint(max_mint, {"from": bob, "value": minter.min_price()})

    assert npc.balanceOf(bob) == 1 + minter.whitelist_max()


def test_cannot_mint_over_limit(minter, bob, deployer):
    minter.admin_add_to_whitelist(bob, {"from": deployer})
    with brownie.reverts():
        minter.mint(minter.whitelist_max() + 1, {"from": bob})


def test_can_change_mint_cap(minter, bob, deployer, npc):
    minter.admin_add_to_whitelist(bob, {"from": deployer})
    max_mint = minter.whitelist_max()
    assert minter.mint_price(max_mint + 1, bob) > 0
    minter.admin_update_whitelist_max(max_mint + 1, {"from": deployer})

    assert minter.whitelist_max() == max_mint + 1
    assert minter.mint_price(max_mint + 1, bob) == 0
    minter.mint(max_mint + 1, {"from": bob})
    assert npc.balanceOf(bob) == max_mint + 1


def test_dropping_mint_cap_hits_prior_minters(minter, bob, deployer, npc):

    minter.admin_add_to_whitelist(bob, {"from": deployer})
    minter.mint(2, {"from": bob})
    assert minter.has_coupon(bob) == True
    assert minter.mint_price(1, bob) == 0

    minter.admin_update_whitelist_max(1, {"from": deployer})
    assert minter.has_coupon(bob) == False
    assert minter.mint_price(1, bob) > 0
    with brownie.reverts():
        minter.mint(1, {"from": bob})


def test_cannot_mint_to_null_addr(minter, deployer, npc):
    curr_tot = npc.totalSupply()
    with brownie.reverts():
        minter.admin_mint_nft(ZERO_ADDRESS, {"from": deployer})
    assert npc.totalSupply() == curr_tot


def test_adding_coupon_token_restricts_nonholder(minter, deployer, alice, thing, npc):
    qty = minter.whitelist_max()
    assert minter.mint_price(qty, alice) > 0
    assert npc.balanceOf(alice) == 0

    # Use $THING as a stand-in for a standard token
    minter.admin_update_coupon_token(thing, {"from": deployer})

    assert minter.mint_price(qty, alice) > 0
    with brownie.reverts():
        minter.mint(qty, {"from": alice})
    assert npc.balanceOf(alice) == 0


@pytest.mark.skip()
def test_mint_at_limit(minter, alice):
    for i in range(399):
        minter.mint(10, {"from": alice, "value": minter.mint_price(10, alice)})

    with brownie.reverts():
        minter.mint(10, {"from": alice, "value": minter.mint_price(10, alice)})
