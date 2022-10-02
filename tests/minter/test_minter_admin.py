import brownie, pytest
from brownie import ZERO_ADDRESS, accounts
from brownie.test import given, strategy

def test_can_update_nft_address(minter, deployer):
    minter.admin_set_nft_addr(ZERO_ADDRESS, {"from": deployer})
    assert minter.nft_addr() == ZERO_ADDRESS


def test_can_update_owner(minter, deployer, bob):
    minter.admin_new_owner(bob, {"from": deployer})
    assert minter.owner() == bob


@pytest.mark.require_network("mainnet-fork")
def test_can_set_gnosis(minter):
    gnosis = accounts.at('0x8AaDe16ad409A19b0FF990B30a9a0E65d32DEa7D', force=True)
    accounts[0].transfer(gnosis, 10 ** 18)
    
    mint_price = minter.mint_price(1, gnosis)
    minter.mint(1, {'from': gnosis, 'value': mint_price})

    minter.admin_new_owner(gnosis, {'from': minter.owner()})
    
    init_bal = gnosis.balance()

    minter.withdraw({'from': gnosis})
    final_bal = gnosis.balance()

    assert final_bal == init_bal + mint_price
    

#@given(value=strategy('uint256', max_value=.008 * 10000 * 10 ** 18))
def test_can_withdraw(minter, deployer, alice, value = 0):
    withdraw_list = [
        "0xccBF601eB2f5AA2D5d68b069610da6F1627D485d",
        "0xAdcB949a288ec2500c1109f9876118d064c40dA6",
        "0xc59eae56D3F0052cdDe752C10373cd0B86451EB2",
        "0x84865Bb349998D6b813DB7Cc0F722fD0A94e6e27",
    ]
    withdraw_amts = [25, 25, 25, 15]

    funds = minter.mint_price(10, alice) + value
    minter.mint(10, {"from": alice, "value": funds })
    assert minter.balance() == funds

    init_bals = []
    for admin in withdraw_list:
        init_bals.append(accounts.at(admin, force=True).balance())

    init_bals.append(accounts.at(minter.owner(), force=True).balance())

    minter.withdraw({"from": deployer})
    for i in range(len(withdraw_list)):
        target_bal = funds * withdraw_amts[i] / 100
        final_bal = accounts.at(withdraw_list[i], force=True).balance() - init_bals[i]
        assert target_bal - final_bal < 10  # Give or take 10 wei

    assert accounts.at(minter.owner(), force=True).balance() > init_bals[i + 1]


def test_admin_can_mint_nft(minter, alice, npc, deployer):
    assert npc.balanceOf(alice) == 0
    minter.admin_mint_nft(alice, {"from": deployer})
    assert npc.balanceOf(alice) == 1


def test_admin_can_update_mint_price(minter, alice, deployer):
    new_price = 10**18
    assert minter.mint_price(1, alice) != new_price
    minter.admin_update_mint_price(new_price, {"from": deployer})
    assert minter.mint_price(1, alice) == new_price


def test_admin_can_update_whitelist_max(minter, deployer):
    minter.admin_update_whitelist_max(0, {"from": deployer})
    assert minter.whitelist_max() == 0


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


def test_rando_cannot_set_token_addr(minter, alice):
    with brownie.reverts():
        minter.admin_set_token_addr(ZERO_ADDRESS, {"from": alice})


def test_rando_cannot_set_mint_price(minter, alice):
    with brownie.reverts():
        minter.admin_update_mint_price(0, {"from": alice})
