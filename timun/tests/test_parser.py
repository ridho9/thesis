from timun.parser import *
from timun.model import *
import pytest


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

    with pytest.raises(ParserError):
        parse_step(input)


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

    with pytest.raises(ParserError):
        parse_steps(input)


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

    with pytest.raises(ParserError):
        parse_scenario_like(input, ScenarioType.SCENARIO)


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


def test_parse_table_line_1():
    content = "| name | age |"
    input = create_input("file", content)

    expect = ["name", "age"]
    res_input = ([], 1, "file")

    assert parse_table_line(input) == (expect, res_input)


def test_parse_table_line_2():
    content = "||"
    input = create_input("file", content)

    with pytest.raises(ParserError):
        parse_table_line(input)


def test_parse_table_1():
    content = """\
    | name  | age   |
    | a     | 1     |
    | b     | 2     |\
        """

    input = create_input("file", content)

    expect = [
        ["name", "age"],
        ["a", "1"],
        ["b", "2"],
    ]

    res_input = ([], 3, "file")

    assert parse_table_entries(input) == (expect, res_input)


def test_parse_table_2():
    content = """\
    | name  | age   |
    | a     | 1     |
    | b     | 2     |
    | c     |\
        """

    input = create_input("file", content)

    with pytest.raises(ParserError):
        parse_table_entries(input)


def test_parse_scenario_outline_1():
    content = """\
    scenario outline: s
        then then
        example:
            | a | b |
            | 1 | 2 |\
        """

    input = create_input("file", content)

    expect = ScenarioOutline(
        "s",
        [Step(StepType.THEN, "then", 1)],
        [("example", [["a", "b"], ["1", "2"]])],
        0,
    )
    res_input = ([], 5, "file")

    assert parse_scenario_outline(input) == (expect, res_input)


def test_parse_variable_line():
    content = "name: enum a, b, c"

    input = create_input("file", content)

    expect = Variable("name", "enum", ["a", "b", "c"], 0)
    res_input = ([], 1, "file")

    assert parse_variable_line(input) == (expect, res_input)


def test_parse_variable():
    content = """\
        variable:
            name: enum a, b, c
            name2: enum 1, 2, 3\
                """

    input = create_input("file", content)

    expect = VariableDeclaration(
        [
            Variable("name", "enum", ["a", "b", "c"], 1),
            Variable("name2", "enum", ["1", "2", "3"], 2),
        ],
        0,
        "file",
    )
    res_input = ([], 3, "file")

    assert parse_variable(input) == (expect, res_input)

