Variable:
    operator: enum add, subtract, multiply, divide

Feature: example feature
    # Scenario: variable for operator
    #     Given my number is 1
    #     When I <operator> 1
    #     Then my number should be 2

    #     Variable Accepted:
    #     | operator  |
    #     | add       |

    # Scenario: succeed test
    #     Then this will succeed

    # Fail Scenario: this should pass
    #     Then this will fail
    Background: background
        Given echo


    Scenario: Calculator success add operation
        Given my number is 1
        When I add 1
        Then my number should be 2
    
    # Fail Scenario: Calculator fail add operation
    #     Given my number is 1
    #     When I add 1
    #     Then my number should be 3

    # Scenario Outline: scenario outline
    #     Given my number is <init>
    #     When I add <add>
    #     Then my number should be <expect>

    #     Example:
    #     | init  | add   | expect  |
    #     | 1     | 1     | 2       |
    #     | 2     | 1     | 3       |

    #     Fail Example:
    #     | init  | add   | expect  |
    #     | 1     | 1     | 3       |


# ==========================================================================

    # Fail Scenario: eee
    #     Given my number is 1
    #     When I <operator> 1
    #     Then my number should be 3

    #     # accept all variable should be fail
    #     # or this means that I REJECT THAT ANY VALUE IS SUCCESS
    #     Variable Rejected:
    #     | operator  |

    #     # Variable Reject:
    #     # | operator  |
    #     # | subtract  |
    #     # | multiply  |
    #     # | divide    |
    #     # | add       |

    # # Fail Scenario: fail example
    # #     Given my number is 1
    # #     When I add 1
    # #     Then my number should be 3

    # Scenario Outline: scenario outline
    #     Given my number is <init>
    #     When I add <add>
    #     Then my number should be <expect>

    #     Example:
    #     | init  | add   | expect  |
    #     | 1     | 1     | 2       |
    #     | 2     | 1     | 3       |

    #     Fail Example:
    #     | init  | add   | expect  |
    #     | 1     | 1     | 3       |
