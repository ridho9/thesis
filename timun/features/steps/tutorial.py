from timun import *


@given("we have behave installed")
def step_impl(context):

    # raise Exception(5)
    print("aaaaaaaaaa")
    pass


@when("we implement a test")
def step_impl_2(context):
    assert True is not False


@then("behave will test it for us!")
def step_impl_3(context):
    assert context["failed"] is False

