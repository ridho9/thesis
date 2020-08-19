Feature: fail scenario
    Scenario Outline: scenario outline
        Given my number is <init>
        When I add <add>
        Then my number should be <expect>

        Example:
        | init  | add   | expect  |
        | 1     | 1     | 2       |
        | 2     | 1     | 3       |

        Fail Example:
        | init  | add   | expect  |
        | 1     | 1     | 3       |

        
    Scenario: succeed test
        Then this will succeed

    Fail Scenario: this should pass
        Then this will fail

    Scenario:
        Given my number is 1
        When I add 1
        Then my number should be 2

    Fail Scenario:
        Given my number is 1
        When I add 1
        Then my number should be 3