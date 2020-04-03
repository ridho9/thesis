# Variances

Salah satu penyebab masih adanya kelemahan keamanan dalam perangkat lunak walaupun telah melakukan
TDD/BDD adalah karena biasanya hanya skenario yang benar saja yang diuji,
sementara skenario yang gagal tidak diuji.
Biasanya programmer menganggap skenario yang seharusnya gagal telah diimplementasikan dengan benar,
dan karena pada siklus pengembangan biasa lebih menitikberatkan ke sisi fungsionalnya,
bagian keamanannya tidak diuji.

Contohnya adalah skenario gherkin di bawah:

```
Feature: keranjang
  Scenario: menambahkan barang ke dalam keranjang
    Given user telah login
    When user memasukkan 1 barang
    Then ada 1 barang di dalam keranjang
```

Skenario diatas menyatakan feature dimana user menambahkan item ke dalam keranjang.
Namun skenario diatas hanya menguji fungsionalitas saat skenario benar,
bagaimana dengan skenario saat tidak benar?

Programmer ingin menguji bahwa skenario harus gagal saat user belum login,
skenario gherkin berubah menjadi:

```
Feature: keranjang
  Scenario: menambahkan barang ke dalam keranjang
    Given user telah login
    When user memasukkan 1 barang
    Then ada 1 barang di dalam keranjang

  Fail Scenario: user belum login menambahkan barang ke dalam keranjang
    Given user belum login
    When user memasukkan 1 barang
    Then ada 1 barang di dalam keranjang
```

Dapat diperhatikan bahwa step dalam fail scenario mirip dengan fail scenario,
hanya saja berbeda pada bagian given dimana pada fail scenario user belum login.

Saat hanya ada kemungkinan dua _variansi_ skenario, maka tidaklah sulit
