from timun import *


@given("my number is {number:d}")
def given_my_number(ctx, number):
    ctx["number"] = number


@when("I {operation} {number:d}")
def when_i_add(ctx, operation: str, number: int):
    operation = operation.lower()
    if operation == "add":
        ctx["number"] += number
    elif operation == "subtract":
        ctx["number"] -= number
    elif operation == "multiply":
        ctx["number"] *= number
    elif operation == "divide":
        ctx["number"] /= number
    else:
        raise Exception(f"invalid operation '{operation}'")


@then("my number should be {number:d}")
def then_my_number_should_be(ctx, number):
    assert ctx["number"] == number


@then("fail my number should be {number:d}")
def fail_then_my_number_should_be(ctx, number):
    assert ctx["number"] != number
