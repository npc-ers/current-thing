import pytest
from brownie import *  # InterfaceChecker, accounts, exceptions


@pytest.mark.skip()
def test_supports_interface_direct(token):
    assert token.supportsInterface(
        0x0000000000000000000000000000000000000000000000000000000001FFC9A7
    )


@pytest.mark.skip()
def test_openzeppelin_recognizes_interface(minted, alice):
    checker = InterfaceChecker.deploy({"from": alice})

    checker.transferERC721(minted, alice, 1, {"from": alice})
    # assert checker.supportsInterface(token)
