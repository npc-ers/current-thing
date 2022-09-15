#!/usr/bin/python3

from brownie import CurrentThing, NPC, Indoctrinator, accounts, network


def main():
    if network.show_active() in ['rinkeby']:
        deployer = accounts.load('husky')
    else:
        deployer = accounts[0]

    publish_flag = False

    thing = CurrentThing.deploy({'from': deployer}, publish_source=publish_flag)

    nft = NPC.deploy( {'from': deployer}, publish_source=publish_flag)
    thing.set_nft_addr(nft, {"from": deployer})

    minter = Indoctrinator.deploy({'from': deployer}, publish_source=publish_flag)
    minter.admin_set_nft_addr(nft, {'from': deployer})
    nft.set_minter(minter, {'from': deployer})

