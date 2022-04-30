#!/usr/bin/python3
import brownie


def test_sender_balance_decreases(accounts, thing):
    sender_balance = thing.balanceOf(accounts[0])
    amount = sender_balance // 4

    thing.transfer(accounts[1], amount, {'from': accounts[0]})

    assert thing.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, thing):
    receiver_balance = thing.balanceOf(accounts[1])
    amount = thing.balanceOf(accounts[0]) // 4

    thing.transfer(accounts[1], amount, {'from': accounts[0]})

    assert thing.balanceOf(accounts[1]) == receiver_balance + amount


def test_total_supply_not_affected(accounts, thing):
    total_supply = thing.totalSupply()
    amount = thing.balanceOf(accounts[0])

    thing.transfer(accounts[1], amount, {'from': accounts[0]})

    assert thing.totalSupply() == total_supply


def test_returns_true(accounts, thing):
    amount = thing.balanceOf(accounts[0])
    tx = thing.transfer(accounts[1], amount, {'from': accounts[0]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, thing):
    amount = thing.balanceOf(accounts[0])
    receiver_balance = thing.balanceOf(accounts[1])

    thing.transfer(accounts[1], amount, {'from': accounts[0]})

    assert thing.balanceOf(accounts[0]) == 0
    assert thing.balanceOf(accounts[1]) == receiver_balance + amount


def test_transfer_zero_things(accounts, thing):
    sender_balance = thing.balanceOf(accounts[0])
    receiver_balance = thing.balanceOf(accounts[1])

    thing.transfer(accounts[1], 0, {'from': accounts[0]})

    assert thing.balanceOf(accounts[0]) == sender_balance
    assert thing.balanceOf(accounts[1]) == receiver_balance


def test_transfer_to_self(accounts, thing):
    sender_balance = thing.balanceOf(accounts[0])
    amount = sender_balance // 4

    thing.transfer(accounts[0], amount, {'from': accounts[0]})

    assert thing.balanceOf(accounts[0]) == sender_balance


def test_insufficient_balance(accounts, thing):
    balance = thing.balanceOf(accounts[0])

    with brownie.reverts():
        thing.transfer(accounts[1], balance + 1, {'from': accounts[0]})


def test_transfer_event_fires(accounts, thing):
    amount = thing.balanceOf(accounts[0])
    tx = thing.transfer(accounts[1], amount, {'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]
