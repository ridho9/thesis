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
untuk menulis semua kemungkinannya. Namun bagaimana jika banyak variansi dari skenarionya?
Kita dapat menggunakan scenario outline yang telah didefinisikan pada `failure.md` sehingga
kode gherkin menjadi seperti:

```
Feature: keranjang
  Scenario Outline: menambahkan barang ke dalam keranjang
    Given user <login state> login
    When user memasukkan 1 barang
    Then ada 1 barang di dalam keranjang

    Examples:
    | login state   |
    | telah         |

    Fail Examples:
    | login state   |
    | belum         |
```

Terlihat panjang tetapi akan menghemat banyak tempat jika banyak state.

Sejauh ini yang disampaikan telah sedikit banyaknya dibahas pada bagian failure,
programmer dapat saja menuliskan semua kemungkinan state satu persatu,
namun programmer juga manusia yang dapat lupa, jadi sekarang pertanyaannya bagaimanakah
perbedaan-perbedaan state ini dapat didefinisikan dengan mudah.

Misal untuk sebuah webapp e-commerce, user memiliki 3 role "buyer" "seller" dan "admin",
dan programmer akan menulis kode testing untuk admin mengubah suatu setting web

```
Variables:
  role: enum(buyer seller admin)
Feature: Admin
  Scenario: admin mengubah setting website
    Given user dengan role <role> telah login
    When user merubah pengaturan website
    Then pengaturan website berubah

    Variables Accepted:
    | role    |
    | admin   |
```

Deklarasi variables diletakkan pada scope Feature karena agar dapat reusable.
Namun mungkin deklarasi `Variables` dapat diletakkan pada tingkat scenario.

Kita dapat membayangkan scenario diatas akan mencoba semua kemungkinan variable,
dan hanya mengecek apakah hanya kombinasi variables dalam bagian `Variables Accepted`
yang sukses, dan seluruh variable diluar kombinasi bernilai gagal. Bagian `Variables Accepted`
dapat diganti dengan `Variables Rejected` untuk mendapatkan kebalikannya.

Tipe variable yang ada adalah

- `enum`, berupa string string dengan beberapa pilihan
- `bool`, karena dapat dianggap berupa `enum(true false)`

Untuk apakah kita bisa menggunakan integer, sepertinya susah, karena integer banyaknya tidak terhingga,
dan jikapun kita dapat membatasi banyak integer yang digunakan, jumlah test yang dijalankan dapat menjadi
sangat banyak dalam waktu yang cepat.
