import brownie
import pytest

def test_contract_uri_exists(token):
    assert len(token.contractURI()) > 10


@pytest.mark.skip()
def test_contract_prereveal_is_initially_false(token):
    assert token.revealed() == False


@pytest.mark.skip()
def test_prereveal_token_uri_is_default(token, minter, alice, bob):
    default_uri = token.default_uri()
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    minter.mint(2, {"from": bob, "value": minter.mint_price(2, bob)})
    for i in range(3):
        assert token.tokenURI(i) == default_uri


def test_postreveal_token_uri_is_base_plus_id(token, minter, alice, bob, deployer):
    default_uri = token.default_uri()
    minter.mint(1, {"from": alice, "value": minter.mint_price(1, alice)})
    minter.mint(2, {"from": bob, "value": minter.mint_price(2, bob)})
    token.set_revealed(True, {"from": deployer})

    for i in range(3):
        assert token.tokenURI(i) == f"{token.base_uri()}{i}"
