# Nuno Mikael Nugroho's Portofolio Website

## Overview
A static personal portfolio website built for "Individual Assignment 1" Pemrograman Berbasis Platform, showcasing my background, skills, and projects as a Computer Science student at Universitas Indonesia.

## Features
- **Responsive layout**
    adapts from desktop to mobile using CSS Grid and media queries
- **Sticky navigation header**
    with smooth scroll to page sections
- **Projects section**
    text/image layout alternates per project for visual rhythm
- **Lightbox image viewer**
    click any project image to view it full-size, built with pure CSS (`:target` selector, no JavaScript)
- **Skills section**
    with icon-labeled pills, grouped visually by category
- **Custom CSS background for header, body, and footer**
    image / texture backgrounds for header and footer, gradient coloring background for body

## Tech Stack
- **HTML5**
    semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- **CSS3** 
    Grid layout, custom properties (CSS variables), media queries, `:target` for interactivity
- **Google Fonts**
    Space Grotesk

No JavaScript was used in this project. All interactivity were achieved through pure HTML / CSS techniques.

## Reflection
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

## AI Disclosure
I used AI for mainly two things, which was brainstorming and bug fixes. Whenever I was confused on what else to add to make the site more interesting, I asked AI chatbots such as Google's Gemini and Claude for ideas. One example was on the skills section when at first I wanted to make a basic list but thought that would be visually unappealing. I asked Gemini for some ideas and the idea I went with was creating small interactive pills.
Here was the prompt used:
"okay so i want to add skills section next. i want to put it above projects but i dont really have an idea on how to make the layout interesting"
Other than brainstorming, I used AI whenever I got stuck on a bug, to tidy up my messy code, and to add comments to make the code more readable. While I used AI, I always check the code twice and not just copy paste it to add my own adjusments and tweaks. This is because AI, mostly, don't understand how to make things look visually inetersting for us humans. So, I use the codes I got from AI as a template that I will alter myself, usually stuff like colors, size, and brightness. Because this assignment is making a website, AI can't directly see what the final product looks like, so they might not understand that some of the codes they make create an awkward or messy look to the site. An example was when I was creating the projects section, I used an AI generated template and the photo was way too big and not aligned with the box, which was also too big. The AI didn't know why, so I fixed it myself by creating boundaries for both not only for laptop layout, but also for mobile layout.

## Author
**Nuno Mikael Nugroho**
NPM: 2506624865
Class: PBP D
S1 Ilmu Komputer, Fakultas Ilmu Komputer, Universitas Indonesia

## License
This project is created for academic purposes as part of coursework at Universitas Indonesia.

# Website Portofolio Nuno Mikael Nugroho

## Gambaran Umum
Website portofolio pribadi yang dibuat untuk mata kuliah Pemrograman Berbasis Platform, menampilkan latar belakang, keahlian, pengalaman, dan proyek saya sebagai mahasiswa Ilmu Komputer di Universitas Indonesia. Awalnya dibangun sebagai situs statis untuk Tugas Individu 1, kemudian dikembangkan menjadi aplikasi Django dinamis menggunakan pola Model-View-Template (MVT) untuk Tugas Individu 2.

## Fitur
- **Tata letak responsif**
    menyesuaikan dari tampilan desktop ke mobile menggunakan CSS Grid dan media queries
- **Header navigasi sticky**
    dengan smooth scroll ke bagian-bagian halaman
- **Halaman Experience dinamis**
    mengambil data dari model `Experience`, menampilkan peran, kategori, dan status masih berlangsung/selesai
- **Halaman Projects dinamis**
    mengambil data dari model `Project`, dengan tata letak teks/gambar yang berselang-seling di setiap proyek untuk ritme visual
- **Kolom pencarian proyek**
    memfilter proyek berdasarkan judul, deskripsi, atau tag menggunakan `Q` objects dari Django dan parameter query `GET` — tanpa JavaScript
- **Lightbox penampil gambar**
    klik gambar proyek mana pun untuk melihatnya secara penuh, dibuat dengan CSS murni (selector `:target`, tanpa JavaScript)
- **Bagian Skills**
    dengan pill berlabel ikon, dikelompokkan secara visual berdasarkan kategori
- **Latar belakang CSS kustom untuk header, body, dan footer**
    latar belakang gambar/tekstur untuk header dan footer, latar belakang gradasi warna untuk body

## Tech Stack
- **Django**
    framework backend yang menangani routing, view, model, dan template (pola MVT)
- **HTML5**
    elemen semantik (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- **CSS3** 
    Grid layout, custom properties (CSS variables), media queries, `:target` untuk interaktivitas
- **Google Fonts**
    Space Grotesk

Tidak ada JavaScript yang digunakan dalam proyek ini. Seluruh interaktivitas dicapai melalui logika sisi server Django yang dikombinasikan dengan teknik HTML/CSS murni.

## Refleksi
1. Ketika pengguna membuka halaman portofolio baru,misalnya project, alurnya dimulai dari permintaan HTTP yang dikirim browser ke server Django. Permintaan ini pertama kali diterima oleh `urls.py` proyek (`myportofolio/urls.py`), yang bertindak sebagai titik masuk utama dan mendelegasikan permintaan ke aplikasi yang sesuai menggunakan `include()`. Selanjutnya, `urls.py` aplikasi (`main/urls.py`) mencocokkan path URL (misalnya `project/`) dengan salah satu `path()` yang terdaftar, lalu memanggil fungsi view yang dipetakan ke path tersebut, yaitu `show_project`. Di dalam view, Django mengambil data yang dibutuhkan dari model (misalnya `Project.objects.all()`, atau hasil yang sudah difilter jika ada parameter pencarian), memasukkannya ke dalam sebuah `context` berupa dictionary. View kemudian memanggil `render()`, yang menggabungkan data pada `context` tersebut dengan template (`projects.html`) menggunakan Django Template Language. Di sinilah data dari model benar-benar disisipkan ke dalam struktur HTML melalui tag seperti `{{ project.title }}` atau perulangan `{% for project in project_list %}`. Hasil akhir berupa HTML yang sudah lengkap dengan data dikirim kembali sebagai response HTTP ke browser, yang kemudian merender halaman tersebut untuk ditampilkan kepada pengguna.

2. Data untuk bagian portofolio baru sebaiknya disimpan pada model, bukan ditulis langsung di dalam template, karena model merepresentasikan sumber data tunggal yang terstruktur dan dapat diolah secara dinamis, sedangkan template seharusnya hanya bertugas menampilkan data, bukan menyimpannya. Jika data ditulis langsung (hardcoded) di template, setiap perubahan sekecil apa pun, misalnya menambah proyek baru atau memperbaiki deskripsi, mengharuskan saya mengedit file HTML secara manual, yang rentan terhadap kesalahan dan sulit diskalakan seiring bertambahnya jumlah data. Dengan menyimpan data pada model, saya bisa menambah, mengubah, atau menghapus data melalui Django Admin atau shell tanpa perlu menyentuh kode template maupun view sama sekali. Hal ini juga membuka kemungkinan fitur dinamis seperti pencarian dan filter, karena data dapat di-query dan diolah secara terprogram (misalnya menggunakan `Q` objects), sesuatu yang mustahil dilakukan jika data hanya berupa teks statis di HTML. Secara keseluruhan, pemisahan ini membuat aplikasi jauh lebih mudah dipelihara dan dikembangkan, karena perubahan data dan perubahan tampilan bisa dilakukan secara independen satu sama lain.

3. `makemigrations` dan `migrate` adalah dua perintah yang saling melengkapi namun memiliki fungsi berbeda dalam siklus perubahan model Django. `makemigrations` bertugas membaca perubahan yang dibuat pada model (misalnya penambahan field baru, perubahan tipe data, atau penghapusan field) dan menghasilkan file migrasi yang berisi instruksi perubahan tersebut dalam format yang bisa dibaca Django, tetapi perintah ini belum benar-benar mengubah apa pun di database. Sementara itu, `migrate` bertugas menerapkan file migrasi yang sudah dibuat tersebut ke database sesungguhnya, sehingga struktur tabel di database benar-benar berubah sesuai dengan definisi model terbaru.

Contoh nyata dari proyek saya sendiri adalah ketika saya mengubah field `started_at` pada model `Experience` dari `models.DateTimeField(auto_now_add=True)` menjadi `models.DateTimeField()` biasa, agar saya bisa mengisi tanggal mulai secara manual alih-alih otomatis diisi tanggal saat data dibuat. Setelah mengubah baris kode tersebut di `models.py`, saya perlu menjalankan `python manage.py makemigrations` agar Django mendeteksi perubahan pada field tersebut dan membuat file migrasi baru yang mencatat perubahan ini. Setelah itu, saya menjalankan `python manage.py migrate` agar perubahan tersebut benar-benar diterapkan ke database, sehingga kolom `started_at` pada tabel `Experience` tidak lagi otomatis terisi dan siap menerima nilai tanggal yang saya tentukan sendiri melalui shell.

## AI Disclosure
Saya menggunakan AI terutama untuk dua hal: brainstorming dan memperbaiki bug. Saat saya bingung mengenai apa yang harus ditambahkan agar situs web lebih menarik, saya meminta ide dari chatbot AI seperti Gemini milik Google dan Claude. Salah satu contohnya adalah pada bagian projects di mana saya ingin menambahkan ftur filtering untuk filter proyek-proyeknya berdasarkan tags yang disediakan. Tapi, fitur itu tidak terlalu berguna menurut saya karena jumlah proyeknya tidak terlalu banyak dan tags yang digunakan biasanya digunakan oleh banyak proyek sehingga tidak terlalu beragam antar proyek. Saya meminta ide kepada Claude dan akhirnya saya memilih untuk membuat sebuah search bar karena lebih praktikal dan mudah dipakai.
Berikut adalah prompt yang saya gunakan:
"Okay, so I want to add a tag filter for the projects but I don't think that would be very practical or interesting. What else can I add to projects to make it more dynamic and add more interactivity. Maybe something along the lines of filtering?"
Selain untuk bertukar pikiran, saya menggunakan AI saat mengalami kendala dengan bug, untuk merapikan kode yang berantakan, serta menambahkan komentar agar kode lebih mudah dipahami. Meskipun menggunakan AI, saya selalu memeriksa ulang kodenya dan tidak sekadar copy paste, melainkan juga melakukan penyesuaian dan perubahan sendiri. Hal ini karena AI umumnya tidak memahami cara membuat tampilan visual yang menarik bagi manusia. Jadi, saya menggunakan kode dari AI sebagai kerangka dasar yang kemudian saya modifikasi sendiri, biasanya terkait warna, ukuran, dan tingkat kecerahan. Karena tugas ini melibatkan pembuatan situs web, AI tidak bisa melihat langsung seperti apa hasil akhirnya, sehingga AI mungkin tidak menyadari bahwa kode yang dihasilkannya bisa membuat tampilan situs menjadi berantakan atau kurang menarik.

## Penulis
**Nuno Mikael Nugroho**
NPM: 2506624865
Kelas: PBP D
S1 Ilmu Komputer, Fakultas Ilmu Komputer, Universitas Indonesia

## Lisensi
Proyek ini dibuat untuk keperluan akademik sebagai bagian dari perkuliahan di Universitas Indonesia.