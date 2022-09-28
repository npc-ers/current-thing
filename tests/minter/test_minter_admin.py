import brownie
from brownie import ZERO_ADDRESS


def test_can_update_nft_address(minter, deployer):
    minter.admin_set_nft_addr(ZERO_ADDRESS, {"from": deployer})
    assert minter.nft_addr() == ZERO_ADDRESS


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


def test_admin_can_mint_nft(minter, alice, npc, deployer):
    assert npc.balanceOf(alice) == 0
    minter.admin_mint_nft(alice, {"from": deployer})
    assert npc.balanceOf(alice) == 1


def test_admin_can_update_mint_price(minter, alice, deployer):
    new_price = 10**18
    assert minter.mint_price(1, alice) != new_price
    minter.admin_update_mint_price(new_price, {"from": deployer})
    assert minter.mint_price(1, alice) == new_price


def test_rando_cannot_update_whitelist(minter, alice):
    with brownie.reverts():
        minter.admin_update_whitelist_max(0, {"from": alice})


def test_rando_cannot_mint_admin_nft(minter, alice):
    with brownie.reverts():
        minter.admin_mint_nft(alice, {"from": alice})


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


def test_rando_cannot_set_token_addr(minter, alice):
    with brownie.reverts():
        minter.admin_set_token_addr(ZERO_ADDRESS, {"from": alice})


def test_rando_cannot_set_mint_price(minter, alice):
    with brownie.reverts():
        minter.admin_update_mint_price(0, {"from": alice})
