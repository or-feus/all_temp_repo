import pytest

from main import User


# Unit Test
def test_check_money(user):
    cheap_price = 500
    expensive_price = 10000000

    can_buy = user._check_money_enough(price=cheap_price)

    assert can_buy

    can_buy = user._check_money_enough(price=expensive_price)
    assert not can_buy


def test_give_money_cheaper(user):
    price = 500
    pre_money = user._money

    user._give_money(money=price)

    assert user._money == pre_money - price


def test_give_money_expensive(user):
    price = 100000000

    with pytest.raises(Exception):
        user._give_money(money=price)


# Integration Test
def test_purchase_product_well(user):
    # 1. 유저가 돈을 잘 냈는가?
    # 2. 유저의 주머니에 상품이 있는가?

    product_id = 1
    pre_user_money = user._money
    user.belongs = []

    product = user.purchase_product(product_id=product_id)

    assert user.get_money() == pre_user_money - product.price
    assert user.get_belongs() == [product]


def test_purchase_product_expensive(user):
    product_id = 2  # price 500,000

    with pytest.raises(Exception):
        user.purchase_product(product_id=product_id)
