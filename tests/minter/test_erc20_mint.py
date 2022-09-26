import brownie


def test_mint_yields_tokens(minter, alice, thing):
    assert thing.balanceOf(alice) == 0
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    assert thing.balanceOf(alice) == 1000 * 10**18


def test_mint_yields_tokens_proportionally(minter, alice, thing):
    assert thing.balanceOf(alice) == 0
    minter.mint(5, {"from": alice, "value": minter.mint_price(5, alice)})
    expected = minter.erc20_drop_quantity()
    assert thing.balanceOf(alice) == 5 * expected


def test_disable_coin_mint(minter, alice, thing, deployer):
    assert thing.balanceOf(alice) == 0
    minter.admin_update_erc20_drop_live(False, {"from": deployer})

    assert minter.is_erc20_drop_live() == False
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    assert thing.balanceOf(alice) == 0


def test_can_update_quantity_of_drop(minter, alice, npc, deployer, thing):
    assert thing.balanceOf(alice) == 0
    new_qty = minter.erc20_drop_quantity() * 2
    minter.admin_update_erc20_drop_quantity(new_qty, {"from": deployer})
    assert minter.erc20_drop_quantity() == new_qty
    minter.mint(2, {"from": alice, "value": minter.mint_price(2, alice)})
    assert thing.balanceOf(alice) == new_qty * 2


def test_admin_can_mint_erc20(minter, alice, thing, deployer):
    assert thing.balanceOf(alice) == 0
    quantity = 10**18
    minter.admin_mint_erc20(alice, quantity, {"from": deployer})

    assert thing.balanceOf(alice) == quantity


def test_rando_cannot_disable_coin_mint(minter, alice, thing):
    with brownie.reverts():
        minter.admin_update_erc20_drop_live(False, {"from": alice})


def test_rand_cannot_update_quantity(minter, alice):
    with brownie.reverts():
        minter.admin_update_erc20_drop_quantity(1, {"from": alice})


def test_rando_cannot_mint_admin_erc20(minter, alice):
    with brownie.reverts():
        minter.admin_mint_erc20(alice, 10**18, {"from": alice})
