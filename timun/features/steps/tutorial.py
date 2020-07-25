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


@then("this will succeed")
def step_impl_4(context):
    pass


@then("this will fail")
def step_imple_5(context):
    assert False
