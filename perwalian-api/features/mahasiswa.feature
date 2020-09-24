Variable:
    paid status: enum true, false
    approve status: enum true, false

Feature: mahasiswa feature
    Scenario: create mahasiswa default
        Given provided mahasiswa 001
        Then mahasiswa 001 exists
    
    Fail Scenario: create mahasiswa fail
        Given provided mahasiswa 002
        Then mahasiswa 001 exists

    Scenario Outline: batas ambil sks menurut ipk
        Given provided mahasiswa 001
        When mahasiswa 001 ipk is <ipk>
        When mahasiswa 001 ambil sks <sks>
        Then mahasiswa 001 exists
        Then mahasiswa 001 ipk is <ipk>
        Then mahasiswa 001 ambil sks <sks>
        Example:
            | ipk   | sks   |
            | 4     | 24    |
            | 4     | 12    |
            | 4     | 0     |
            | 2     | 20    |
        Fail Example:
            | ipk   | sks   |
            | 2     | 24    |
            | 2     | 21    |

    Scenario Outline: sks range
        Given provided mahasiswa 001
        When mahasiswa 001 ipk is 4
        When mahasiswa 001 ambil sks <sks>
        Then mahasiswa 001 exists
        Then mahasiswa 001 ambil sks <sks>

        Example:
            | sks   |
            | 0     |
            | 12    |
            | 24    |
        Fail Example:
            | sks   |
            | -1    |
            | 25    |
    

    Scenario Outline: ipk range
        Given provided mahasiswa 001
        When mahasiswa 001 ipk is <ipk>
        Then mahasiswa 001 exists
        Then mahasiswa 001 ipk is <ipk>
        Example:
            | ipk   |
            | 0     |
            | 2     |
            | 4     |
        Fail Example:
            | ipk  |
            | -1.0 |
            | 5.0  |

    

    Scenario Outline: sks must correct for approve
        Given provided mahasiswa 001
        When mahasiswa 001 have paid true
        When mahasiswa 001 ipk is <ipk>
        When mahasiswa 001 ambil sks <sks>
        When mahasiswa 001 approve <approve>
        Then mahasiswa 001 exists
        Then mahasiswa 001 ipk is <ipk>
        Then mahasiswa 001 ambil sks <sks>
        Then mahasiswa 001 approve <approve>

        Example:
            | ipk   | sks   | approve   |
            | 4     | 24    | true      |
            | 2     | 20    | true      |
            | 4     | 24    | false     |

        Fail Example:
            | ipk   | sks   | approve   |
            | 2     | 24    | true      |


    Scenario: must have paid before approve
        Given provided mahasiswa 001
        When mahasiswa 001 have paid <paid status>
        When mahasiswa 001 approve <approve status>
        Then mahasiswa 001 exists
        Then mahasiswa 001 have paid <paid status>
        Then mahasiswa 001 approve <approve status>

        Variable Rejected:
            | paid status  | approve status  |
            | false        | true            |
