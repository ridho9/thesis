from timun.parser import *
from timun.model import *


def test_parse_step_1():
    input = create_input("file", "given name\nrest")

    expect = Step(StepType.GIVEN, "name", 0)
    res_input = (["rest"], 1, "file")

    assert parse_step(input) == (expect, res_input)


def test_parse_step_2():
    input = create_input("file", "when name\nrest")

    expect = Step(StepType.WHEN, "name", 0)
    res_input = (["rest"], 1, "file")

    assert parse_step(input) == (expect, res_input)


def test_parse_step_3():
    input = create_input("file", "then name\nrest")

    expect = Step(StepType.THEN, "name", 0)
    res_input = (["rest"], 1, "file")

    assert parse_step(input) == (expect, res_input)


def test_parse_step_4():
    input = create_input("file", "rest")

    try:
        parse_step(input)
    except Exception as e:
        assert isinstance(e, ParserError)


def test_parse_step_5():
    input = create_input("file", "    \n  \n   given name\nrest")

    expect = Step(StepType.GIVEN, "name", 2)
    res_input = (["rest"], 3, "file")

    assert parse_step(input) == (expect, res_input)


def test_parse_steps_1():
    input = create_input("file", "given 1\nthen 2")

    expect = [Step(StepType.GIVEN, "1", 0), Step(StepType.THEN, "2", 1)]
    res_input = ([], 2, "file")

    assert parse_steps(input) == (expect, res_input)


def test_parse_steps_2():
    input = create_input("file", "\ngiven 1\nthen 2")

    expect = [Step(StepType.GIVEN, "1", 1), Step(StepType.THEN, "2", 2)]
    res_input = ([], 3, "file")

    assert parse_steps(input) == (expect, res_input)


def test_parse_steps_3():
    input = create_input("file", "\nrest")

    try:
        parse_steps(input)
    except Exception as e:
        assert isinstance(e, ParserError)


def test_parse_scenario_1():
    content = """\
        scenario: 1
            given a
            when b
            then c\
    """

    input = create_input("file", content)

    expect = Scenario(
        ScenarioType.SCENARIO,
        "1",
        [
            Step(StepType.GIVEN, "a", 1),
            Step(StepType.WHEN, "b", 2),
            Step(StepType.THEN, "c", 3),
        ],
        0,
    )
    res_input = ([], 4, "file")

    assert parse_scenario_like(input, ScenarioType.SCENARIO) == (expect, res_input)


def test_parse_scenario_2():
    content = """\
        scenario: 1
    """

    input = create_input("file", content)

    try:
        parse_scenario_like(input, ScenarioType.SCENARIO)
    except Exception as e:
        assert isinstance(e, ParserError)


def test_parse_background_1():
    content = """\
        background: 1
            given a
            when b
            then c\
    """

    input = create_input("file", content)

    expect = Scenario(
        ScenarioType.BACKGROUND,
        "1",
        [
            Step(StepType.GIVEN, "a", 1),
            Step(StepType.WHEN, "b", 2),
            Step(StepType.THEN, "c", 3),
        ],
        0,
    )
    res_input = ([], 4, "file")

    assert parse_scenario_like(input, ScenarioType.BACKGROUND) == (expect, res_input)


def test_parse_feature_1():
    content = """\
    feature: feature 1
        scenario: 1
            given a
            when b
            then c\
    """

    input = create_input("file", content)

    expect_scenario = Scenario(
        ScenarioType.SCENARIO,
        "1",
        [
            Step(StepType.GIVEN, "a", 2),
            Step(StepType.WHEN, "b", 3),
            Step(StepType.THEN, "c", 4),
        ],
        1,
    )
    expect = Feature([], "feature 1", None, [expect_scenario], 0, "file")
    res_input = ([], 5, "file")

    assert parse_feature(input) == (expect, res_input)


def test_parse_fail_scenario_1():
    content = """\
        fail scenario: 1
            given a
            when b
            then c\
    """

    input = create_input("file", content)

    expect = Scenario(
        ScenarioType.FAIL_SCENARIO,
        "1",
        [
            Step(StepType.GIVEN, "a", 1),
            Step(StepType.WHEN, "b", 2),
            Step(StepType.THEN, "c", 3),
        ],
        0,
    )
    res_input = ([], 4, "file")

    assert parse_fail_scenario(input) == (expect, res_input)


def test_parse_scenarios_family_1():
    content = """\
        scenario: 1
            given a
            when b
            then c\
    """

    input = create_input("file", content)

    expect = Scenario(
        ScenarioType.SCENARIO,
        "1",
        [
            Step(StepType.GIVEN, "a", 1),
            Step(StepType.WHEN, "b", 2),
            Step(StepType.THEN, "c", 3),
        ],
        0,
    )

    res_input = ([], 4, "file")

    assert parse_scenario_family(input) == (expect, res_input)


def test_parse_scenarios_family_2():
    content = """\
        fail scenario: 1
            given a
            when b
            then c\
    """

    input = create_input("file", content)

    expect = Scenario(
        ScenarioType.FAIL_SCENARIO,
        "1",
        [
            Step(StepType.GIVEN, "a", 1),
            Step(StepType.WHEN, "b", 2),
            Step(StepType.THEN, "c", 3),
        ],
        0,
    )

    res_input = ([], 4, "file")

    assert parse_scenario_family(input) == (expect, res_input)


def test_parse_scenarios_1():
    content = """\
        scenario: 1
            given a
            when b
            then c\
    """

    input = create_input("file", content)

    expect = [
        Scenario(
            ScenarioType.SCENARIO,
            "1",
            [
                Step(StepType.GIVEN, "a", 1),
                Step(StepType.WHEN, "b", 2),
                Step(StepType.THEN, "c", 3),
            ],
            0,
        )
    ]
    res_input = ([], 4, "file")

    assert parse_scenarios(input) == (expect, res_input)
