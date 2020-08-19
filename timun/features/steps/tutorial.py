from timun import *


@then("this will {result}")
def step_impl_4(context, result):
    if result == "fail":
        raise Exception("Intentional fail")
    if result == "succeed":
        return
    raise Exception(f"no match '{result}'")


@given("my number is {number:d}")
def given_my_number(ctx, number):
    ctx["number"] = number


@when("I add {number:d}")
def when_i_add(ctx, number):
    ctx["number"] += number


@then("my number should be {number:d}")
def then_my_number_should_be(ctx, number):
    assert ctx["number"] == number
