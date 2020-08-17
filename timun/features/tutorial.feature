Feature: fail scenario

  Scenario: succeed test
      Then this will succeed

  Fail Scenario: this should pass
      Then this will fail

  Scenario Outline: scenario outline
    Given my number is <init>
    When I add <add>
    Then my number should be <expect>
    
    Example:
    | init  | add   | expect  |
    | 1     | 1     | 2       |
    | 2     | 1     | 3       |