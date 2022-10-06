#!/usr/bin/python3

from brownie import NPC, CurrentThing, Indoctrinator, Wei, accounts, network
from brownie.network import priority_fee

if network.show_active() in ["goerli"]:
    priority_fee("2 gwei")


def main():
    if network.show_active() in ["rinkeby", "goerli"]:
        deployer = accounts.load("husky")
    elif network.show_active() == "mainnet":
        deployer = accounts.load("minnow")
    else:
        deployer = accounts[0]

    publish_flag = False

    # Deploy Token
    thing = CurrentThing.deploy({"from": deployer}, publish_source=publish_flag)

    # Deploy NFT
    nft = NPC.deploy({"from": deployer}, publish_source=publish_flag)
    thing.admin_set_npc_addr(nft, {"from": deployer})

    # Deploy Minter
    minter = Indoctrinator.deploy({"from": deployer}, publish_source=publish_flag)
    minter.admin_set_nft_addr(nft, {"from": deployer})
    minter.admin_set_token_addr(thing, {"from": deployer})
    thing.admin_set_minter(minter, {"from": deployer})
    nft.set_minter(minter, {"from": deployer})
