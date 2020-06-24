# Notes and Thoughts on Failures in Gherkin

Masalah yang dihadapi saat ini adalah BDD framework yang ada pada saat ini tidak dapat
menentukan case yang seharusnya tidak boleh terjadi. BDD framework seperti Gherkin juga tidak
memiliki cara untuk mendeskripsikan step `Then` yang seharusnya fail.

Misal:
```
Feature: keranjang
  Scenario: menambahkan barang ke dalam keranjang
    Given user telah login
    When user memasukkan 1 barang
    Then ada 1 barang di dalam keranjang
```

Pada feature gherkin diatas ada beberapa hal yang dapat kita temukan

1.  Scenario tersebut memiliki initial state (given) dimana user telah login,
    bagaimana jika kita ingin mengecek apakah jika user belum login.
    Kita dapat menambahan scenario lainnya seperti:

    ```
    Feature: keranjang
      Scenario: menambahkan barang ke dalam keranjang
        Given user telah login
        When user memasukkan 1 barang
        Then sukses ada 1 barang di dalam keranjang
      Scenario: user belum login menambahkan barang ke dalam keranjang
        Given user belum login
        When user memasukkan 1 barang
        Then gagal ada 1 barang di dalam keranjang
    ```

    Kita dapat memanfaatkan fitur scenario outline untuk memperpendek scenario ini

    ```
    Feature: keranjang
      Scenario Outline: menambahkan barang ke dalam keranjang
        Given user <login state> login
        When user memasukkan 1 barang
        Then <result state> ada 1 barang di dalam keranjang

        Examples:
          | login state | result state |
          | sudah       | sukses       |
          | belum       | gagal        |
    ```

    Dengan begini, masalah duplikasi state tadi telah terselesaikan. Namun solusi ini memerlukan kita untuk 
    mendefinisikan table pada scenario outline secara manual

2.  Kita ingin membuat agar table example tadi dapat dibuat dengan otomatis, namun sebelum itu,
    pada gherkin 
    biasa, tidak ada cara untuk mendeskripsikan step `Then` yang harus gagal.
    Tentu saja kita dapat menggunakan `Then ada barang di dalam keranjang` dan `Then tidak ada barang di dalam keranjang`
    untuk mendeskripsikan step yang sukses dan step yang gagal, namun deskripsi step di atas mengharuskan
    kita untuk membuat 2 fungsi step yaitu `ada barang di dalam keranjang` dan `tidak ada barang di dalam keranjang`.

    Sebuah step `Then` dianggap berhasil jika pada saat fungsinya dijalankan tidak ada error/exception.
    Sementara pada end state negatif biasanya ditandai oleh adanya error, exception, atau fungsi fail pada context dipanggil.

    Kita dapat berandai dan memisalkan bahwa ada step negatif dari `Then` yaitu `Then Fail`, kita dapat menulis ulang
    skenario gherkin yang gagal menjadi

    ```
    Scenario: user belum login saat memasukkan barang
      Given user belum login
      When user memasukkan 1 barang
      Then Fail ada 1 barang di dalam keranjang
    ```

    Fungsi step untuk `ada 1 barang di dalam keranjang` dapat melemparkan exception, dan kita tidak harus menulis
    1 fungsi step tambahan. 
    
    Lalu jika diperhatikan kembali, pada alur aplikasi biasanya, jika user belum login maka tentu saja tidak ada
    keranjang yang akan dimasukkan barang, maka mungkin saja pada eksekusi sebelumnya, akan ada exception pada
    step `When`, yang menyebabkan scenario dianggap gagal. Kita dapat berandai lagi bahwa ada keyword yang
    dapat mendeskripsikan bahwa scenario ini harus memiliki kegagalan, baik di step `When` maupun `Then`.
    Dengan fitur yang kita andaikan tadi, kita dapat menulis kembali scenario gherkin sebelumnya menjadi

    ```
    Fail Scenario: user belum login saat memasukkan barang
      Given user belum login
      When user memasukkan 1 barang
      Then ada 1 barang di dalam keranjang
    ```

    atau

    ```
    Scenario: user belum login saat memasukkan barang
      Given user belum login
      When user memasukkan 1 barang
      Then ada 1 barang di dalam keranjang
      Should Fail
    ```

4.  Kita dapat menggabungkan fitur fail scenario dengan scenario outline untuk mengubah gherkin pada poin satu menjadi
    ```
    Feature: keranjang
      Scenario Outline: menambahkan barang ke dalam keranjang
        Given user <login state> login
        When user memasukkan 1 barang
        Then ada 1 barang di dalam keranjang

        Examples:
          | login state | 
          | sudah       |
        Fail Examples:
          | login state | 
          | belum       |
    ```

    Contoh lainnya

    ```
    Feature: keranjang
      Scenario Outline: menambahkan barang ke dalam keranjang
        Given user sudah login
        When user memasukkan <buah masuk> ke dalam keranjang
        Then ada <buah expect> di dalam keranjang
      
        Examples:
          | buah masuk | buah expect |
          | apel       | apel        |
        Fail Examples:
          | buah masuk | buah expect |
          | nanas      | apel        |
    ```

Dalam menulis deskripsi gherkin, alangkah baiknya jika kita hanya perlu mendeskripsikan scenario scenario yang
harusnya terjadi (positif / sukses),
dan somehow, sistem dapat mengetahui (infer) skenario yang seharusnya tidak boleh terjadi.