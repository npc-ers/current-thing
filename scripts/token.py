#!/usr/bin/python3

from brownie import Token, accounts


def main():
    thing = CurrentThing.deploy(18, 1e21, {'from': accounts[0]})
    nft = NPC.deploy(thing, {'from': accounts[0]})
    thing.setNFT(nft, {"from": accounts[0]})

