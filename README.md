# Hedef Tespit ve Takip
Tübitak 2020 İHA yarışması için hazırladığımız İHA' nın hedef tespit ve takip amacıyla hazırladığım servo kontrollü takip sistemi.

# Sistemin Çalışması
Sistemin çalışmasını şu şekilde özetleyebilirim:
Program çalıştığında ekranda hedef yoksa sistem tarama yaparak hedefi aramaya başlar. (Servo kamerayı sağa ve sola döndürür.)
Kamera 4 bölgeye bölünmüş ve hangi bölgede hedef görülürse o bölgenin kodları çalışmaya başlar ve hedefi kameranın merkezindeki alana almaya çalışır.
Hedefin kamera merkezine alınması durumunda servolar kamera pozisyonunu korur.
Hedef konum değiştirirse tekrar hedefi kamera merkezine alır.
Hedef kameranın merkezine alınamayacak durumda ise (servolar belli seviyeye kadar dönebilir) bu durumda Hata73 ekranda dönecektir. Hedef konum değiştirdiğinde ve servo hareket kısıtlaması olmadığında takip devam eder.
Hedef kaybedilirse tekrar tarama ile hedef aranır.

# Çalışma Videoları
https://youtu.be/l6eMpreRYwo

----------------------------

https://youtu.be/MoxhSnn2OQM

# Çalışma Amacı
Bu çalışmanın amacı otonom uçuşta hedef ve yön belirlenmesinde daha sağlıklı sonuçlar elde etmek amacıyla tasarlanmıştır.

# Geliştirme
Proje geliştirme aşamasındadır. Otonom uçuş için döndürülecek değerler kodda bulunmamaktadır ve 3d çizimlerde düzeltmeler yapılacaktır.
