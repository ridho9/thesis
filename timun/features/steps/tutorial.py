from timun import *


@given("echo")
def step1(ctx):
    print("Echo")


@then("this will {result}")
def step_impl_4(context, result):
    if result == "fail":
        raise Exception("Intentional fail")
    if result == "succeed":
        return
    raise Exception(f"no match '{result}'")
