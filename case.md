# Test Cases Yemima Febe Yanti Marpaung - Project WeMine

### Test Case List:

| Test Case ID | Test Case Title / Description | Priority |
| :--- | :--- | :---: |
| **FO-01** | Sign in successfully using a valid active username | P1 |
| **FO-02** | Fail to sign in using a completely unregistered username | P1 |
| **FO-03** | Handle empty string or special character payload during sign in lookup | P2 |
| **FO-04** | Complete end-to-end authentication via Microsoft SSO login | P1 |
| **FO-05** | Fail to sign in using an invalid password on Microsoft SSO | P1 |
| **FO-06** | Complete first-time master data synchronization and trigger restart prompt | P1 |
| **FO-07** | Handle network timeout and recovery during master data synchronization | P1 |
| **FO-08** | Handle session token expiration and seamless re-auth in offline mode | P2 |
| **F1-01** | Retrieve exact maximum dynamic form schema up to 50 fields | P2 |
| **F1-02** | Restrict radio button field options to a maximum of 4 options | P2 |
| **F1-03** | Render dynamic form UI and persist local offline draft | P1 |
| **F1-04** | Validate dynamic fields and perform background media compression on low-spec devices | P2 |
| **F2-01** | Trigger automatic workflow task upon hazard report submission via API | P1 |
| **F2-02** | Enforce mandatory fields restriction on hazard report submission | P1 |
| **F2-03** | Dispatch real-time push notification targeting specific area users and PIC | P1 |
| **F2-04** | Complete PIC task resolution and add dynamic co-observers (+) | P1 |
| **F2-05** | Dispatch direct supervisor notification upon task resolution completion | P2 |

---

## Detail Skenario Pengujian

### Flow 0: Sign-In & Sinkronisasi Data

#### FO-01: Sign in successfully using a valid active username
- **Category:** Automation (API)
- **Pre-condition:** Akun pengguna aktif dan terdaftar di database tenant.
- **Test Step:** Kirim request `POST` ke endpoint `/user/who` dengan parameter payload `username` yang valid dan aktif.
- **Expected Result:** Server mengembalikan response HTTP `200 OK` beserta metadata tenant, konfigurasi, dan base endpoint yang sesuai.

#### FO-02: Fail to sign in using a completely unregistered username
- **Category:** Automation (API)
- **Pre-condition:** Username belum pernah terdaftar di sistem tenant manapun.
- **Test Step:** Kirim request `POST` ke endpoint `/user/who` menggunakan string `username` fiktif yang tidak ada di database.
- **Expected Result:** Server menolak request dengan status HTTP `404 Not Found` atau pesan error validasi tenant.

#### FO-03: Handle empty string or special character payload during sign in lookup
- **Category:** Automation (API)
- **Pre-condition:** Layanan backend `/user/who` aktif dan dapat diakses.
- **Test Step:** Kirim request `POST` ke endpoint `/user/who` dengan payload `username` berupa string kosong (`""`), spasi kosong, atau karakter injeksi khusus (`<script>`, SQL syntax).
- **Expected Result:** Sistem menolak request secara aman dengan status HTTP `400 Bad Request` tanpa mengalami *server crash* (HTTP 500).

#### FO-04: Complete end-to-end authentication via Microsoft SSO login
- **Category:** Automation (E2E)
- **Pre-condition:** Aplikasi terbuka, perangkat online, dan username terdaftar di sistem.
- **Test Step:** 
  1. Masukkan username valid $\rightarrow$ sistem memanggil endpoint `/user/who`.
  2. Alihkan ke layar Microsoft Identity Login.
  3. Masukkan kredensial password Microsoft yang benar $\rightarrow$ klik Sign In.
  4. Verifikasi pemanggilan endpoint profil `/user/me`.
- **Expected Result:** Autentikasi berhasil, sukses get token, profil pengguna dimuat dengan benar, dan aplikasi masuk ke halaman utama (*dashboard*).

#### FO-05: Fail to sign in using an invalid password on Microsoft SSO
- **Category:** Automation (E2E)
- **Pre-condition:** Aplikasi terbuka, perangkat online, dan menggunakan username yang valid.
- **Test Step:** 
  1. Masukkan username valid $\rightarrow$ lanjut ke layar Microsoft Login.
  2. Masukkan password yang salah secara sengaja $\rightarrow$ klik Sign In.
- **Expected Result:** Sistem Microsoft Identity menolak autentikasi dan menampilkan pesan error interaktif (*Incorrect password*) tanpa memberikan akses ke endpoint profil `/user/me`.

#### FO-06: Complete first-time master data synchronization and restart prompt
- **Category:** Manual
- **Pre-condition:** Pengguna baru melakukan login untuk pertama kalinya pada perangkat.
- **Test Step:** 
  1. Biarkan aplikasi memicu proses pengambilan data master dari endpoint `/tenant/master`.
  2. Pantau pergerakan *progress bar* unduhan untuk data lokasi, sublokasi, area, karyawan,