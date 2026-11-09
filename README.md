# Website Portofolio Nuno Mikael Nugroho

## Gambaran Umum
Website portofolio pribadi yang dibuat untuk mata kuliah Pemrograman Berbasis Platform, menampilkan latar belakang, keahlian, pengalaman, dan proyek saya sebagai mahasiswa Ilmu Komputer di Universitas Indonesia. Awalnya dibangun sebagai situs statis untuk Tugas Individu 1, kemudian dikembangkan menjadi aplikasi Django dinamis menggunakan pola Model-View-Template (MVT) untuk Tugas Individu 2, dan dilengkapi dengan fitur Create/Update/Delete, data delivery dalam format JSON, serta autentikasi untuk Tugas Individu 3. Pada tugas-tugas berikutnya ditambahkan hak akses berbasis peran (Tugas Individu 4), pembaruan halaman tanpa reload menggunakan AJAX (Tugas Individu 5), dan REST API dengan Django REST Framework yang dipakai langsung oleh halaman Projects dan Experience (Tugas Individu 6).

## Fitur
- **Tata letak responsif**
    menyesuaikan dari tampilan desktop ke mobile menggunakan CSS Grid dan media queries
- **Header navigasi sticky**
    dengan smooth scroll ke bagian-bagian halaman
- **Halaman Experience dinamis**
    mengambil data dari model `Experience`, menampilkan peran, kategori, dan status masih berlangsung/selesai
- **Halaman Projects dinamis**
    mengambil data dari model `Project`, dengan tata letak teks/gambar yang berselang-seling di setiap proyek untuk ritme visual
- **Create, Update, dan Delete**
    baik untuk Project maupun Experience, menggunakan `ModelForm` dan dilindungi login (`@login_required`)
- **Data delivery dalam format JSON**
    endpoint `/api/project/` mengembalikan data proyek dalam format JSON, dan halaman Projects mengambil datanya melalui proses serialization/deserialization
- **REST API dengan Django REST Framework**
    endpoint `/api/v1/projects/` dan `/api/v1/experiences/` mendukung GET, POST, PUT, PATCH, DELETE, serta endpoint star, dengan status HTTP yang sesuai (200, 201, 204, 400, 403, 404)
- **Serializer dengan validasi**
    `ProjectSerializer` dan `ExperienceSerializer` menulis daftar field secara eksplisit, membersihkan input teks dengan `strip_tags`, dan menyediakan field hitungan yang read-only (`star_count`, `is_starred`, `starred_by_names`)
- **Hak akses berbasis peran di API**
    pengunjung hanya membaca; pengguna biasa juga dapat memberi star; Editor juga dapat mengubah data (PUT/PATCH) pada Experience; pemilik (superuser) dapat membuat, mengubah, dan menghapus
- **Fitur star**
    pengguna yang login dapat memberi atau membatalkan star pada proyek dan pengalaman, diperbarui tanpa reload halaman
- **Pembaruan halaman tanpa reload (AJAX)**
    daftar, pencarian, tambah, ubah, star, dan hapus dilakukan lewat `fetch()` ke API, dengan pesan kesalahan dari API ditampilkan sebagai toast
- **Kolom pencarian**
    memfilter proyek dan pengalaman menggunakan `Q` objects Django dan parameter query `q`, dipanggil lewat AJAX dengan debouncing 300 ms
- **Modal edit untuk Experience**
    Editor dan pemilik dapat mengubah pengalaman langsung dari halaman lewat PATCH ke API
- **Lightbox penampil gambar**
    klik gambar proyek mana pun untuk melihatnya secara penuh, dibuat dengan CSS murni (selector `:target`, tanpa JavaScript)
- **Skills section**
    dengan pill berlabel ikon, dikelompokkan secara visual berdasarkan kategori
- **Mode gelap**
    gaya visual beda untuk menyesuaikan dengan preferensi pengunjung
- **Latar belakang CSS kustom untuk header, body, dan footer**
    latar belakang gambar/tekstur untuk header dan footer, latar belakang gradasi warna untuk body
- **Pengujian otomatis**
    test dengan `APITestCase` untuk setiap peran, validasi, star, dan perlindungan CSRF

## Fitur Tambahan (Tugas 6)
- **Filter tag pada halaman Projects**
    setiap tag pada kartu proyek dapat diklik untuk memfilter daftar (`/api/v1/projects/?tag=Django`). Pencocokan dilakukan pada tag utuh dan tidak membedakan huruf besar/kecil, sehingga `Java` tidak cocok dengan `JavaScript`. Filter dapat digabung dengan pencarian, menampilkan keterangan "Filtering by tag" dengan tombol hapus, dan tersimpan di URL (`/projects/?tag=Django`) agar tampilan terfilter dapat dibagikan. Mengklik tag yang sedang aktif akan menghapus filter.
- **Dropdown kategori pada halaman Experience**
    daftar kategori diambil dari pilihan pada model, lalu memfilter lewat `/api/v1/experiences/?category=research`. Filter dapat digabung dengan pencarian dan tersimpan di URL (`/experience/?category=research`).

Keduanya diuji dengan `APITestCase` (`test_filter_by_tag` dan `test_filter_by_category`).

## Dokumentasi API
Semua endpoint berada di bawah `/api/v1/` dan memakai `SessionAuthentication`, sehingga setiap permintaan yang mengubah data harus menyertakan header `X-CSRFToken`.

| Endpoint | Method | Fungsi | Siapa yang boleh |
|---|---|---|---|
| `/api/v1/projects/?q=&tag=` | GET | Daftar proyek (dapat dicari/difilter) | Semua |
| `/api/v1/projects/` | POST | Membuat proyek | Pemilik |
| `/api/v1/projects/<id>/` | GET | Detail proyek | Semua |
| `/api/v1/projects/<id>/` | PUT, PATCH, DELETE | Mengubah / menghapus proyek | Pemilik |
| `/api/v1/projects/<id>/star/` | POST | Memberi / membatalkan star | Pengguna yang login |
| `/api/v1/experiences/?q=&category=` | GET | Daftar pengalaman (dapat dicari/difilter) | Semua |
| `/api/v1/experiences/` | POST | Membuat pengalaman | Pemilik |
| `/api/v1/experiences/<id>/` | GET | Detail pengalaman | Semua |
| `/api/v1/experiences/<id>/` | PUT, PATCH | Mengubah pengalaman | Pemilik dan Editor |
| `/api/v1/experiences/<id>/` | DELETE | Menghapus pengalaman | Pemilik |
| `/api/v1/experiences/<id>/star/` | POST | Memberi / membatalkan star | Pengguna yang login |

## Menjalankan Test
```
python manage.py test main.tests_api --verbosity 2
python manage.py test main
```
Gunakan `python manage.py test main`, bukan `python manage.py test` tanpa nama app, agar skrip Selenium (jika ada) tidak ikut dijalankan.

## Tech Stack
- **Django**
    framework backend yang menangani routing, view, model, form, autentikasi, dan template (pola MVT)
- **Django REST Framework**
    serializer, permission class, dan API view berbasis fungsi (`@api_view`) untuk REST API di `/api/v1/`
- **HTML5**
    elemen semantik (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`), template inheritance dengan `base.html`
- **CSS3** 
    Grid layout, custom properties (CSS variables), media queries, `:target` untuk interaktivitas
- **JavaScript**
    `fetch()` dan `async`/`await` untuk memanggil API, debouncing pencarian, event delegation, dan escaping HTML sebelum data disisipkan ke halaman
- **Google Fonts**
    Space Grotesk

JavaScript digunakan sejak Tugas 5 untuk memuat dan memperbarui data halaman Projects dan Experience lewat API tanpa reload. Lightbox gambar tetap dibuat dengan CSS murni.

## Reflection  Tugas 1
1.  Yes, I used semantic HTML5 elements, specifically `<header>`, `<nav>`, `<main>`, `<section>`, and `<footer>`. I
    used`<section>` three times to group content thematically (profile, skills, and projects) each with an `id` used as an anchor target for navigation.

    `<article>` was not used, since none of the content is meant to be independently distributable outside the page. Each section is a dependent part of a single cohesive page rather than standalone syndicated content.
    `<aside>` was also not used, as all content presented (profile info, skills, and projects) is primary and directly relevant to the portfolio's purpose. There was no supplementary content I wanted to add to warrant using `<aside>`

2. The main challenge in building a responsive layout was reworking elements that are arranged side-by-side on desktop into a
    stacked layout on mobile, without breaking the logical reading order. For example, the hero photo is positioned beside the identity / details text on desktop via `grid-template-areas` but needed a deliberate reordering on mobile so it sits between the identity and details sections rather than in a confusing position. A similar challenge appeared in the projects section, where the desktop layout alternates text-left / image-right and image-left / text-right per project; this alternation doesn't translate meaningfully to a single-column mobile layout, so all project rows were unified into one consistent stacking order on mobile. Element sizing for certain images was also adjusted for smaller viewports.
    
    The general evaluation principle used was elements arranged horizontally on desktop were converted to vertical stacking on mobile, since horizontal space becomes too narrow to preserve readability. I tested it using the browser DevTools' Device Toolbar to verify layout behavior across breakpoints.

3. As a purely static site, a few limitations became apparent to me while trying to present content optimally:
    - Image lightbox
        Implemented using the CSS `:target` selector, which works but has real limitations, such as not being able to be closed by clicking outside the image or pressing escape.
    - No project filtering
        Project tags (Film, Hardware, Research, etc.) are currently static labels with no interactive behavior, so visitors can't filter or sort projects by category despite the growing variety.
    - Manual project markup
        Each new project requires manually copying and pasting an entire `project-row` HTML block, making the codebase repetitive and harder to maintain as more projects are added.

    Plans I have for dynamic functionality in the next iteration:
    - A proper JavaScript-based modal (closable via outside click or escape key) to replace the CSS-only lightbox
    - Interactive tag-based filtering for the projects section
    - A data-driven rendering approach for the projects section

## Refleksi Tugas 2
1. Ketika pengguna membuka halaman portofolio baru,misalnya project, alurnya dimulai dari permintaan HTTP yang dikirim browser ke server Django. Permintaan ini pertama kali diterima oleh `urls.py` proyek (`myportofolio/urls.py`), yang bertindak sebagai titik masuk utama dan mendelegasikan permintaan ke aplikasi yang sesuai menggunakan `include()`. Selanjutnya, `urls.py` aplikasi (`main/urls.py`) mencocokkan path URL (misalnya `project/`) dengan salah satu `path()` yang terdaftar, lalu memanggil fungsi view yang dipetakan ke path tersebut, yaitu `show_project`. Di dalam view, Django mengambil data yang dibutuhkan dari model (misalnya `Project.objects.all()`, atau hasil yang sudah difilter jika ada parameter pencarian), memasukkannya ke dalam sebuah `context` berupa dictionary. View kemudian memanggil `render()`, yang menggabungkan data pada `context` tersebut dengan template (`projects.html`) menggunakan Django Template Language. Di sinilah data dari model benar-benar disisipkan ke dalam struktur HTML melalui tag seperti `{{ project.title }}` atau perulangan `{% for project in project_list %}`. Hasil akhir berupa HTML yang sudah lengkap dengan data dikirim kembali sebagai response HTTP ke browser, yang kemudian merender halaman tersebut untuk ditampilkan kepada pengguna.

2. Data untuk bagian portofolio baru sebaiknya disimpan pada model, bukan ditulis langsung di dalam template, karena model merepresentasikan sumber data tunggal yang terstruktur dan dapat diolah secara dinamis, sedangkan template seharusnya hanya bertugas menampilkan data, bukan menyimpannya. Jika data ditulis langsung (hardcoded) di template, setiap perubahan sekecil apa pun, misalnya menambah proyek baru atau memperbaiki deskripsi, mengharuskan saya mengedit file HTML secara manual, yang rentan terhadap kesalahan dan sulit diskalakan seiring bertambahnya jumlah data. Dengan menyimpan data pada model, saya bisa menambah, mengubah, atau menghapus data melalui Django Admin atau shell tanpa perlu menyentuh kode template maupun view sama sekali. Hal ini juga membuka kemungkinan fitur dinamis seperti pencarian dan filter, karena data dapat di-query dan diolah secara terprogram (misalnya menggunakan `Q` objects), sesuatu yang mustahil dilakukan jika data hanya berupa teks statis di HTML. Secara keseluruhan, pemisahan ini membuat aplikasi jauh lebih mudah dipelihara dan dikembangkan, karena perubahan data dan perubahan tampilan bisa dilakukan secara independen satu sama lain.

3. `makemigrations` dan `migrate` adalah dua perintah yang saling melengkapi namun memiliki fungsi berbeda dalam siklus perubahan model Django. `makemigrations` bertugas membaca perubahan yang dibuat pada model (misalnya penambahan field baru, perubahan tipe data, atau penghapusan field) dan menghasilkan file migrasi yang berisi instruksi perubahan tersebut dalam format yang bisa dibaca Django, tetapi perintah ini belum benar-benar mengubah apa pun di database. Sementara itu, `migrate` bertugas menerapkan file migrasi yang sudah dibuat tersebut ke database sesungguhnya, sehingga struktur tabel di database benar-benar berubah sesuai dengan definisi model terbaru.

Contoh nyata dari proyek saya sendiri adalah ketika saya mengubah field `started_at` pada model `Experience` dari `models.DateTimeField(auto_now_add=True)` menjadi `models.DateTimeField()` biasa, agar saya bisa mengisi tanggal mulai secara manual alih-alih otomatis diisi tanggal saat data dibuat. Setelah mengubah baris kode tersebut di `models.py`, saya perlu menjalankan `python manage.py makemigrations` agar Django mendeteksi perubahan pada field tersebut dan membuat file migrasi baru yang mencatat perubahan ini. Setelah itu, saya menjalankan `python manage.py migrate` agar perubahan tersebut benar-benar diterapkan ke database, sehingga kolom `started_at` pada tabel `Experience` tidak lagi otomatis terisi dan siap menerima nilai tanggal yang saya tentukan sendiri melalui shell.

## Refleksi — Tugas 3
1. Saya menggunakan `ModelForm` alih-alih membuat form HTML secara manual karena `ModelForm` secara otomatis membangun struktur form berdasarkan definisi model yang sudah ada, termasuk field, tipe data, serta validasi bawaan (misalnya memastikan `URLField` benar-benar berisi URL yang valid, atau field wajib tidak boleh kosong). Ini membuat kode jauh lebih ringkas dan konsisten, karena saya tidak perlu menulis ulang setiap `<input>` beserta validasinya secara manual di HTML maupun di view — cukup mendefinisikan `fields`, `labels`, dan `widgets` pada satu class, dan Django akan menghasilkan elemen form yang sesuai secara otomatis. Selain itu, jika model berubah (misalnya menambah field baru), form yang menggunakan `ModelForm` dapat langsung menyesuaikan tanpa saya harus mengubah banyak kode HTML secara manual.
Kita diwajibkan menambahkan `{% csrf_token %}` pada form karena Django menerapkan proteksi CSRF (Cross-Site Request Forgery) secara default untuk semua permintaan `POST`. Tanpa token ini, Django akan menolak permintaan form dengan error 403 Forbidden, sebab CSRF token memastikan bahwa permintaan yang dikirim benar-benar berasal dari halaman/form milik aplikasi itu sendiri, bukan dari situs lain yang mencoba menyamar mengirimkan request atas nama pengguna yang sedang login tanpa sepengetahuan mereka. Token ini bersifat unik dan rahasia untuk setiap sesi, sehingga penyerang dari luar tidak dapat memalsukannya.

2. JSON lebih disukai dibandingkan XML dalam pengembangan aplikasi web modern karena beberapa alasan. Pertama, struktur JSON jauh lebih ringkas karena tidak memerlukan tag pembuka dan penutup seperti XML, sehingga ukuran data yang dikirim lebih kecil dan lebih hemat bandwidth, terutama penting untuk aplikasi web modern yang sering melakukan banyak request kecil secara berulang (misalnya lewat AJAX atau API). Kedua, JSON memiliki kemiripan struktur langsung dengan objek pada JavaScript, sehingga browser/frontend dapat langsung mem-parsing dan menggunakan data JSON tanpa proses konversi tambahan yang rumit, sementara XML membutuhkan parser terpisah yang umumnya lebih berat. Ketiga, JSON lebih mudah dibaca oleh manusia dibandingkan XML yang penuh dengan tag berulang, sehingga proses debugging menjadi lebih cepat. Karena alasan-alasan tersebut, hampir seluruh REST API modern (termasuk yang saya buat pada proyek ini) menggunakan JSON sebagai format utama untuk pertukaran data antara server dan client.

3. Alur yang terjadi saat fungsi view mengembalikan data portofolio dalam bentuk JSON dimulai ketika client (misalnya browser, atau fungsi `show_project` saya sendiri) mengirimkan request ke endpoint tertentu, dalam proyek ini `/api/project/`. Request tersebut diarahkan ke fungsi view `get_project_json`, yang kemudian mengambil data dari database melalui model menggunakan query seperti `Project.objects.all()` atau hasil yang sudah difilter berdasarkan parameter pencarian. Data yang diambil ini masih berupa QuerySet berisi objek-objek model Django, yang tidak bisa langsung dikirim sebagai response HTTP, karena format tersebut spesifik untuk Python/Django dan tidak dapat dipahami oleh client lain (browser, aplikasi mobile, atau sistem lain) yang hanya memahami format data universal seperti teks. Di sinilah proses serialization diperlukan — yaitu mengonversi objek model Django menjadi format string/teks terstruktur (dalam kasus ini JSON) menggunakan `serializers.serialize("json", projects)`. Hasil dari serialization tersebut kemudian dikirim kembali ke client sebagai `HttpResponse` dengan `content_type="application/json"`. Jika kita ingin menampilkan kembali data tersebut ke sebuah halaman HTML (seperti yang saya lakukan pada `show_project`), maka data JSON tersebut perlu di-deserialize kembali menjadi objek model Django menggunakan `serializers.deserialize(...)`, sehingga saya dapat memanggil method dan atribut model seperti biasa (misalnya `project.get_tags()`) sebelum dikirim ke template melalui `context`.

## Refleksi — Tugas 4
Tugas ini menambahkan implementasi pembuatan akun dengan implementasi register, login, dan log out. Selain itu, ada perbedaan antara beberapa akun dengan adanya grup Editor dan akun admin dengan kemampuan masing-masing. Menurut saya, tugas 4 ini lumayan sederhana implementasinya karena sebagian besar hanya melanjutkan atau mengulang langkah-langkah dari tutorial 4. Namun, tentunya saya masih belajar banyak mengenai keamanan data, manajemen hak akses, dan interaktivas web. Walau tugas ini membantu saya lebih mengerti dunia web development, saya jujurnya sedikit bingung dengan implementasi registrasi akun pada proyek portofolio. Menurut saya, penambahan akun tidak terlalu diperlukan untuk situs portofolio kecuali untuk akun admin.

## Refleksi — Tugas 5
1. Debouncing adalah teknik untuk menunda eksekusi sebuah fungsi hingga jeda waktu tertentu berlalu tanpa ada event baru yang terjadi. Pada fitur pencarian, setiap karakter yang diketik pengguna memicu event input; jika fungsi pencarian langsung dijalankan pada setiap event tersebut, mencari satu kata yang terdiri dari enam huruf berarti browser mengirim enam permintaan AJAX secara berurutan, padahal pengguna hanya ingin melihat hasil akhir setelah selesai mengetik. Dengan debouncing, setiap kali ada input baru, timer sebelumnya dibatalkan (clearTimeout) dan dimulai ulang (setTimeout). Permintaan pencarian baru benar-benar dikirim hanya jika tidak ada input baru selama durasi jeda yang ditentukan (pada proyek ini 300 milidetik). Teknik ini penting diterapkan pada pencarian berbasis AJAX karena mengurangi jumlah permintaan ke server secara signifikan, menghindari beban server yang tidak perlu, mencegah race condition di mana hasil pencarian lama bisa menimpa hasil yang lebih baru, dan tetap membuat pencarian terasa responsif bagi pengguna tanpa mereka perlu menekan tombol secara eksplisit.

2. fetch() mengembalikan sebuah Promise, yaitu objek yang merepresentasikan hasil dari operasi asinkron yang belum tentu selesai saat baris kode tersebut dieksekusi. Kata kunci await digunakan untuk menjeda eksekusi fungsi async sampai Promise tersebut selesai (resolved) dan mengembalikan hasilnya, sehingga kode berikutnya baru dijalankan setelah data benar-benar diterima dari server. Jika await tidak digunakan, variabel yang menampung hasil fetch() akan berisi objek Promise yang masih tertunda (pending), bukan data respons yang sebenarnya, karena JavaScript akan langsung melanjutkan ke baris kode berikutnya tanpa menunggu permintaan selesai. Akibatnya, kode yang mencoba membaca atau menampilkan data dari hasil fetch() tersebut (misalnya memanggil .json() atau mengakses response.ok) akan gagal atau menghasilkan nilai yang tidak terduga, karena data sebenarnya belum tersedia pada saat kode tersebut dijalankan.

3. XSS (Cross-Site Scripting) adalah jenis serangan di mana penyerang menyisipkan kode skrip berbahaya (biasanya JavaScript) ke dalam halaman web, yang kemudian dieksekusi oleh browser pengguna lain yang membuka halaman tersebut. Pada proyek ini, contohnya adalah menyimpan judul proyek berupa <img src="x" onerror="alert('XSS!')">; jika teks tersebut dirender sebagai HTML alih-alih sebagai teks biasa, browser akan mencoba memuat gambar, gagal, lalu menjalankan skrip pada atribut onerror. Data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini dibandingkan data yang ditampilkan langsung melalui template Django karena Django Template Language melakukan auto-escaping secara otomatis pada setiap variabel yang disisipkan dengan {{ }}, mengubah karakter seperti < dan > menjadi entity HTML sehingga tidak pernah ditafsirkan sebagai tag. Sebaliknya, ketika data JSON dirakit menjadi HTML secara manual di JavaScript (misalnya melalui innerHTML atau template string), tidak ada proses escaping otomatis sama sekali kecuali ditambahkan secara eksplisit. Karena itu, pada proyek ini saya menambahkan dua lapis perlindungan: escaping manual di sisi klien melalui fungsi escapeHtml sebelum setiap nilai teks disisipkan ke HTML, serta pembersihan tag HTML di sisi server menggunakan strip_tags pada method clean_<field> di ModelForm, sehingga data berbahaya sudah ditolak atau dibersihkan sebelum sempat tersimpan ke database.

## Refleksi — Tugas 6
1. REST (Representational State Transfer) adalah gaya arsitektur untuk merancang layanan web, bukan sebuah format data atau library. Prinsip utamanya adalah client–server yang terpisah, komunikasi stateless (setiap request membawa semua informasi yang dibutuhkan), setiap resource punya URL sendiri (misalnya `/api/v1/projects/<id>/`), dan antarmuka yang seragam: aksi ditentukan oleh method HTTP standar (GET untuk membaca, POST untuk membuat, PUT/PATCH untuk mengubah, DELETE untuk menghapus), sedangkan hasilnya dilaporkan lewat status HTTP yang bermakna, seperti 201 Created, 204 No Content, 400 Bad Request, 403 Forbidden, dan 404 Not Found. Hanya mengembalikan JSON belum cukup untuk disebut RESTful, karena JSON hanya format representasi data. Pada Tutorial 05, `get_project_json` memang mengembalikan JSON, tetapi aksi lainnya dilakukan lewat URL yang berbentuk kata kerja seperti `/project/<id>/delete/` dan `/project/<id>/star/` yang semuanya memakai POST dan berakhir dengan redirect atau status 200, sehingga lebih mirip pemanggilan prosedur daripada pengelolaan resource. Pada API yang sekarang, satu URL resource dipakai bersama oleh beberapa method (GET, PUT, PATCH, DELETE pada `/api/v1/projects/<id>/`), dan status HTTP dipakai dengan benar sehingga client (termasuk test saya) dapat memahami hasilnya tanpa menafsirkan isi response. Endpoint star tetap berupa aksi toggle lewat POST, yang menurut saya merupakan kompromi pragmatis dan tidak sepenuhnya murni REST.

    Perbedaan PUT dan PATCH ada pada cakupan perubahannya. PUT mengganti seluruh representasi resource, sehingga semua field wajib dikirim; jika ada field wajib yang hilang, request ditolak. Pada proyek ini, PUT ke proyek dengan hanya `{"title": "Incomplete"}` menghasilkan 400 karena `description` dan `tags` wajib, dan hal ini diuji pada `test_patch_put_and_delete`. PATCH hanya mengubah field yang dikirim, dan field lain tetap memakai nilai sebelumnya karena serializer dipanggil dengan `partial=True`. PATCH sebaiknya dipakai ketika hanya satu atau beberapa field yang berubah, misalnya mengganti judul sebuah proyek dari Console atau menghapus tanggal selesai (`{"ended_at": null}`) pada sebuah pengalaman, sedangkan PUT sebaiknya dipakai ketika client memang mengirim ulang seluruh data resource, misalnya form edit lengkap yang menggantikan semua isi sebelumnya.

2. Serializer pada Django REST Framework berperan sebagai penerjemah dua arah antara objek model dan data yang dapat dikirim lewat HTTP. Pada arah keluar (serialization), serializer mengubah instance model menjadi tipe data sederhana yang kemudian dirender menjadi JSON, termasuk field hitungan seperti `star_count`, `is_starred`, dan `starred_by_names` lewat `SerializerMethodField`. Pada arah masuk (deserialization), serializer memvalidasi data dari request (`is_valid()`), menjalankan metode `validate_<field>` seperti `strip_tags`, lalu menyimpan hasilnya ke model lewat `save()`. Serializer juga menentukan field mana yang tampil melalui daftar `fields` yang ditulis eksplisit, sehingga data sensitif tidak ikut terkirim, dan menandai field tertentu sebagai read-only sehingga tidak dapat dipalsukan dari luar (dibuktikan pada `test_computed_fields_are_read_only`, ketika `star_count: 99` dari request diabaikan).

    Dibandingkan merakit dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05, serializer jauh lebih ringkas dan konsisten. Pada `get_project_json`, saya harus menulis sendiri setiap pasangan kunci–nilai, mengubah UUID menjadi string, dan menghitung star secara manual, sedangkan validasi input dilakukan di tempat lain oleh `ModelForm` dengan format error yang berbeda. Dengan serializer, satu class dipakai untuk daftar, detail, pembuatan, dan pembaruan, dengan aturan validasi yang sama dan format error yang seragam (`{"title": ["..."]}`) sehingga mudah dibaca oleh JavaScript. Serializer juga terikat pada model dan gagal lebih awal bila ada ketidaksesuaian: ketika nama field pada serializer saya (`tech_stack`) tidak ada pada model, DRF langsung menampilkan `ImproperlyConfigured`, sehingga kesalahan itu cepat ketahuan.

3. Autentikasi menjawab pertanyaan "siapa kamu?", yaitu proses mengenali identitas pengguna. Pada proyek ini, `SessionAuthentication` membaca cookie sesi dari request dan mengisi `request.user`. Otorisasi menjawab pertanyaan "apa yang boleh kamu lakukan?", yaitu memutuskan apakah pengguna yang sudah dikenali boleh melakukan aksi tertentu, yang pada DRF dilakukan oleh permission class seperti `IsAuthenticated`, `IsPortfolioOwnerOrReadOnly`, dan `IsPortfolioOwnerOrEditorOrReadOnly`. Seorang pengguna bisa saja berhasil terautentikasi tetapi tidak diotorisasi, misalnya pengguna biasa yang mencoba menghapus pengalaman akan mendapat 403. Pada `SessionAuthentication`, pengunjung yang belum login juga mendapat 403, bukan 401, karena DRF tidak mengirim header `WWW-Authenticate` untuk skema ini.

    Hak akses harus diperiksa dengan permission class di server karena menyembunyikan tombol di template hanya mengatur tampilan, bukan keamanan. Siapa pun dapat mengirim request langsung lewat Console browser, Browsable API, atau alat seperti curl tanpa pernah melihat tombol tersebut, sehingga server tidak boleh mempercayai apa pun yang berasal dari client. Pada halaman Experience, tombol hapus memang hanya dirender untuk pemilik (`EXP_IS_SUPERUSER`), tetapi yang benar-benar mencegah Editor menghapus data adalah permission class di server, yang dibuktikan oleh `test_editor_can_update_but_not_create_or_delete`: Editor mendapat 403 pada create dan delete, dan data pada database tetap ada.

4. `SessionAuthentication` mengenali pengguna dari cookie sesi, dan browser mengirim cookie tersebut secara otomatis pada setiap request ke situs yang sama, termasuk request yang dipicu dari situs lain. Karena itu, penyerang dapat membuat halaman berbahaya yang menyuruh browser korban yang sedang login mengirim POST, PATCH, atau DELETE ke API kita, dan server akan menganggapnya sah. Token CSRF mencegah hal ini: server menyetel cookie `csrftoken`, halaman kita membacanya dengan `getCookie('csrftoken')` lalu mengirimnya pada header `X-CSRFToken`, dan situs lain tidak dapat membaca cookie tersebut karena kebijakan same-origin. Karena itu, `{% csrf_token %}` tetap dipasang pada halaman agar cookie-nya selalu dibuat, dan setiap fungsi `writeProject` serta `writeExperience` menyertakan headernya. DRF hanya menerapkan pemeriksaan CSRF pada pengguna yang terautentikasi lewat sesi, sedangkan permintaan anonim ditolak oleh permission class.

    Test yang memakai `force_authenticate` tidak cukup untuk membuktikan perlindungan CSRF karena metode itu menetapkan pengguna langsung pada request dan melewati class autentikasi sepenuhnya, padahal pemeriksaan CSRF dijalankan di dalam `SessionAuthentication`. Selain itu, `APIClient` secara bawaan tidak menegakkan pemeriksaan CSRF. Artinya, test seperti itu akan tetap lulus walaupun perlindungan CSRF dimatikan. Karena itu, pada proyek ini saya menulis test dengan `APIClient(enforce_csrf_checks=True)` dan `.login()` yang membuat sesi sungguhan: satu test membuktikan bahwa POST, PATCH, dan DELETE tanpa token ditolak dengan 403 dan database tidak berubah, dan satu test lainnya membuktikan bahwa request dengan token yang valid berhasil.

## AI Disclosure
Saya menggunakan AI terutama untuk dua hal: brainstorming dan memperbaiki bug. Saat saya bingung mengenai apa yang harus ditambahkan agar situs web lebih menarik, saya meminta ide dari chatbot AI seperti Gemini milik Google dan Claude. Salah satu contohnya adalah pada fitur tambahan. Saya awalnya ingin menambahkan halaman baru karena tidak memiliki ide lain untuk fitur tambahan. Namun, setelah meminta ide dari chatbot AI, saya menentukkan untuk menambahkan fitur filtering untuk tags project dan kategori experience.
Berikut adalah prompt yang saya gunakan:
"What should the extra feature be? I want to make a new page for maybe education but that might be too much and not really a step forward."
Selain untuk bertukar pikiran, saya menggunakan AI saat mengalami kendala dengan bug, untuk merapikan kode yang berantakan, serta menambahkan komentar agar kode lebih mudah dipahami. Meskipun menggunakan AI, saya selalu memeriksa ulang kodenya dan tidak sekadar copy paste, melainkan juga melakukan penyesuaian dan perubahan sendiri. Hal ini karena AI umumnya tidak memahami cara membuat tampilan visual yang menarik bagi manusia. Jadi, saya menggunakan kode dari AI sebagai kerangka dasar yang kemudian saya modifikasi sendiri, biasanya terkait warna, ukuran, dan tingkat kecerahan.

## Author
**Nuno Mikael Nugroho**
NPM: 2506624865
Class: PBP D
S1 Ilmu Komputer, Fakultas Ilmu Komputer, Universitas Indonesia

## License
This project is created for academic purposes as part of coursework at Universitas Indonesia.