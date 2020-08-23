from timun import *


@given("my number is {number:d}")
def given_my_number(ctx, number):
    ctx["number"] = number


@when("I add {number:d}")
def when_i_add(ctx, number):
    ctx["number"] += number


@then("my number should be {number:d}")
def then_my_number_should_be(ctx, number):
    assert ctx["number"] == number
