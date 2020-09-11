Variable:
    paid status: enum true, false
    approve status: enum true, false

Feature: mahasiswa feature
    Scenario: create mahasiswa default
        Given prepare mahasiswa 001
        When create mahasiswa 001
        Then mahasiswa 001 exists
    
    Fail Scenario: create mahasiswa fail
        Given prepare mahasiswa 002
        When create mahasiswa 001
        Then mahasiswa 003 exists

    Scenario Outline: sks must correct for approve
        Given prepare mahasiswa 001
        Given mahasiswa 001 have paid true
        Given mahasiswa 001 ipk is <ipk>
        Given mahasiswa 001 ambil sks <sks>
        Given mahasiswa 001 approve <approve>
        When create mahasiswa 001
        Then mahasiswa 001 exists

        Example:
            | ipk   | sks   | approve   |
            | 4     | 24    | true      |
            | 2     | 20    | true      |
            # bisa tidak approve walaupun sks benar
            | 4     | 24    | false     |

        Fail Example:
            | ipk   | sks   | approve   |
            | 2     | 24    | true      |


    Scenario: must have paid before approve
        Given prepare mahasiswa 001
        Given mahasiswa 001 have paid <paid status>
        Given mahasiswa 001 approve <approve status>
        When create mahasiswa 001
        Then mahasiswa 001 exists

        Variable Rejected:
            | paid status  | approve status  |
            | false        | true            |


    Scenario Outline: ipk range
        Given prepare mahasiswa 001
        Given mahasiswa 001 ipk is <ipk>
        When create mahasiswa 001
        Then mahasiswa 001 exists
        Example:
            | ipk   |
            | 0     |
            | 2     |
            | 4     |
        Fail Example:
            | ipk  |
            | -1.0 |
            | 5.0  |

    
    Scenario Outline: sks range
        Given prepare mahasiswa 001
        Given mahasiswa 001 ipk is 4
        Given mahasiswa 001 ambil sks <sks>
        When create mahasiswa 001
        Then mahasiswa 001 exists

        Example:
            | sks   |
            | 0     |
            | 12    |
            | 24    |
        Fail Example:
            | sks   |
            | -1    |
            | 25    |
    
    Scenario Outline: batas ambil sks menurut ipk
        Given prepare mahasiswa 001
        Given mahasiswa 001 ipk is <ipk>
        Given mahasiswa 001 ambil sks <sks>
        When create mahasiswa 001
        Then mahasiswa 001 exists
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