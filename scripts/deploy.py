#!/usr/bin/python3

from brownie import CurrentThing, NPC, accounts, network


def main():
    if network.show_active() in ['rinkeby']:
        deployer = accounts.load('husky')
    else:
        deployer = accounts[0]

    ver = False
    thing = CurrentThing.deploy({'from': deployer}, publish_source=ver)
    nft = NPC.deploy(thing, {'from': deployer}, publish_source=ver)
    thing.set_nft_addr(nft, {"from": deployer})

