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


def test_can_update_nft_address(minter, deployer):
    minter.admin_set_nft_addr(ZERO_ADDRESS, {"from": deployer})
    assert minter.nft_addr() == ZERO_ADDRESS


def test_can_update_whitelist(minter, deployer, bob, npc):
    assert minter.mint_price(1, bob) > 0
    assert npc.balanceOf(bob) == 0
    minter.admin_add_to_whitelist(bob, {"from": deployer})
    assert minter.mint_price(1, bob) == 0
    minter.mint(1, {"from": bob})
    assert npc.balanceOf(bob) == 1


def test_cannot_reuse_whitelist(minter, deployer, bob, npc):
    assert minter.mint_price(1, bob) > 0
    assert npc.balanceOf(bob) == 0

    minter.admin_add_to_whitelist(bob, {"from": deployer})

    minter.mint(1, {"from": bob})
    assert npc.balanceOf(bob) == 1
    assert minter.mint_price(1, bob) > 0
    with brownie.reverts():
        minter.mint(1, {"from": bob})


def test_can_add_coupon(minter, deployer, alice, thing, npc):
    assert minter.mint_price(1, alice) > 0
    assert npc.balanceOf(alice) == 0

    minter.admin_update_coupon_token(thing, {"from": deployer})
    minter.admin_mint(alice, 10**18, {"from": deployer})

    assert minter.mint_price(1, alice) == 0
    minter.mint(1, {"from": alice})
    assert npc.balanceOf(alice) > 0


def test_cannot_reuse_coupon(minter, deployer, alice, thing, npc):
    assert minter.mint_price(1, alice) > 0
    assert npc.balanceOf(alice) == 0

    minter.admin_update_coupon_token(thing, {"from": deployer})
    minter.admin_mint(alice, 10**18, {"from": deployer})

    assert minter.mint_price(1, alice) == 0
    minter.mint(1, {"from": alice})
    assert npc.balanceOf(alice) > 0
    assert minter.mint_price(1, alice) > 0
    with brownie.reverts():
        minter.mint(1, {"from": alice})


def test_can_update_owner(minter, deployer, bob):
    minter.admin_new_owner(bob, {"from": deployer})
    assert minter.owner() == bob


def test_can_withdraw(minter, deployer):
    minter.mint(1, {"from": deployer, "value": minter.mint_price(1, deployer)})
    deployer_init = deployer.balance()
    minter_init = minter.balance()

    assert minter_init > 0

    minter.admin_withdraw(deployer, minter_init, {"from": deployer})
    assert deployer.balance() == deployer_init + minter_init


def test_rando_cannot_update_nft_address(minter, alice):
    with brownie.reverts():
        minter.admin_set_nft_addr(ZERO_ADDRESS, {"from": alice})


def test_rando_cannot_update_whitelist(minter, alice):
    with brownie.reverts():
        minter.admin_add_to_whitelist(alice, {"from": alice})


def test_rando_cannot_update_owner(minter, alice):
    with brownie.reverts():
        minter.admin_new_owner(alice, {"from": alice})


def test_rando_cannot_update_coupon(minter, alice):
    with brownie.reverts():
        minter.admin_update_coupon_token(ZERO_ADDRESS, {"from": alice})


def test_rando_cannot_withdraw(minter, alice):
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    balance = minter.balance()
    assert balance > 0
    with brownie.reverts():
        minter.admin_withdraw(alice, balance, {"from": alice})


def test_mint_yields_tokens(minter, alice, thing):
    assert thing.balanceOf(alice) == 0
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    assert thing.balanceOf(alice) == 1000 * 10**18


def test_mint_is_sequential(minter, alice, bob, charlie, token):
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    minter.mint(1, {"from": bob, "value": minter.mint_price(1, bob)})
    minter.mint(1, {"from": charlie, "value": minter.mint_price(1, charlie)})
    assert token.ownerOf(0) == alice
    assert token.ownerOf(1) == bob
    assert token.ownerOf(2) == charlie


def test_mint_multiple_is_sequential(minter, alice, bob, charlie, token):
    minter.mint(2, {"from": alice, "value": minter.mint_price(2, alice)})
    minter.mint(3, {"from": bob, "value": minter.mint_price(3, bob)})
    minter.mint(4, {"from": charlie, "value": minter.mint_price(4, charlie)})

    for i in range(2):
        assert token.ownerOf(i) == alice

    for i in range(2, 5):
        assert token.ownerOf(i) == bob

    for i in range(5, 9):
        assert token.ownerOf(i) == charlie


@pytest.mark.skip_coverage
def test_mint_at_limit(minter, alice):
    for i in range(399):
        minter.mint(10, {"from": alice, "value": minter.mint_price(10, alice)})

    with brownie.reverts():
        minter.mint(10, {"from": alice, "value": minter.mint_price(10, alice)})
