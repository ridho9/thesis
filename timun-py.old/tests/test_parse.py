from timun import parse
from timun.model import *


def test_parse_step1():
    case = "given aaa"
    expect = Step(StepType.GIVEN, "aaa")
    rest = ""
    assert parse.parse_step(case) == (expect, rest)


def test_parse_step2():
    case = "bbb aaa"
    expect = None
    rest = "bbb aaa"
    assert parse.parse_step(case) == (expect, rest)


def test_parse_step3():
    case = "when aaa"
    expect = Step(StepType.WHEN, "aaa")
    rest = ""
    assert parse.parse_step(case) == (expect, rest)


def test_parse_step4():
    case = "then aaa"
    expect = Step(StepType.THEN, "aaa")
    rest = ""
    assert parse.parse_step(case) == (expect, rest)


def test_parse_step5():
    case = "then aaa\nthen bbb"
    expect = Step(StepType.THEN, "aaa")
    rest = "then bbb"
    assert parse.parse_step(case) == (expect, rest)


def test_parse_steps_1():
    case = """
    given aaa
    then bbb
    ccc"""

    rest = "ccc"
    result = [Step(StepType.GIVEN, "aaa"), Step(StepType.THEN, "bbb")]
    assert parse.parse_steps(case) == (result, rest)


def test_parse_steps_2():
    case = """ccc"""

    rest = "ccc"
    result = []
    assert parse.parse_steps(case) == (result, rest)


def test_scenario_1():
    case = """\
    scenario: scenario 1
        given aaa
        when bbb"""
    result = Scenario(
        "scenario 1", [Step(StepType.GIVEN, "aaa"), Step(StepType.WHEN, "bbb")]
    )
    rest = ""
    assert parse.parse_scenario(case) == (result, rest)


def test_background_scenario_1():
    case = """\
    background: background 1
        given aaa
        when bbb"""
    result = Scenario(
        "background 1", [Step(StepType.GIVEN, "aaa"), Step(StepType.WHEN, "bbb")]
    )
    rest = ""
    assert parse.parse_background_scenario(case) == (result, rest)
