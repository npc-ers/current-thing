import brownie
import pytest
from brownie import a


def test_admin_can_set_new_current_thing(thing, root):
    new_thing = "New Current Thing"
    thing.new_current_thing(new_thing, {"from": a[0]})
    assert thing.current_thing() == new_thing


def test_admin_can_advance_epoch(thing, root):
    new_thing = "New Current Thing"
    epoch = thing.current_epoch()
    thing.new_current_thing(new_thing, {"from": a[0]})
    assert thing.current_epoch() == epoch + 1


def test_user_cannot_trigger_new_epoch(thing, root):
    new_thing = "Thing"
    with brownie.reverts():
        thing.new_current_thing(new_thing, {"from": a[1]})


@pytest.mark.skip()
def test_user_can_claim_on_new_epoch(thing, root):
    new_thing = "New Current Thing"
    epoch = thing.current_epoch()
    amount = 10**18
    thing.new_current_thing(new_thing, amount, {"from": a[0]})
    thing.claim_bonus(epoch, root, 0, [root] * 10, {"from": a[1]})
    assert thing.balanceOf(a[1]) == amount


@pytest.mark.skip()
def test_user_cannot_reclaim_on_new_epoch(thing, root):
    new_thing = "New Current Thing"
    epoch = thing.current_epoch()
    amount = 10**18
    thing.new_current_thing(new_thing, amount, root, {"from": a[0]})
    thing.claim_bonus(epoch, root, 0, [root] * 10, {"from": a[1]})
    with brownie.reverts():
        thing.claim_bonus(epoch, root, 0, [root] * 10, {"from": a[1]})
