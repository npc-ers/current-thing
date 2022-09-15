import brownie


def test_set_base_uri(token, deployer):
    new_base_uri = "test"
    token.set_base_uri(new_base_uri, {"from": deployer})
    assert token.base_uri() == new_base_uri


def test_set_contract_uri(token, deployer):
    new_contract_uri = "test"
    token.set_contract_uri(new_contract_uri, {"from": deployer})
    assert token.contractURI() == new_contract_uri


def test_can_set_owner(token, deployer, alice):
    token.set_owner(alice, {"from": deployer})
    assert token.owner() == alice


def test_new_owner_can_set_old_owner(token, deployer, alice):
    token.set_owner(alice, {"from": deployer})
    token.set_owner(deployer, {"from": alice})
    assert token.owner() == deployer


def test_new_owner_can_set_old_owner(token, deployer, alice, bob):
    token.set_owner(alice, {"from": deployer})
    token.set_owner(bob, {"from": alice})
    assert token.owner() == bob


def test_rando_cannot_set_owner(token, alice):
    with brownie.reverts():
        token.set_owner(alice, {"from": alice})


def test_rando_cannot_set_minter(token, alice):
    with brownie.reverts():
        token.set_minter(alice, {"from": alice})


def test_rando_cannot_set_base_uri(token, alice):
    with brownie.reverts():
        token.set_base_uri("malware", {"from": alice})
    assert token.base_uri() != "malware"


def test_rando_cannot_set_contract_uri(token, alice):
    with brownie.reverts():
        token.set_contract_uri("malware", {"from": alice})
    assert token.base_uri() != "malware"
