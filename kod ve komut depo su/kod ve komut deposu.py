import sys
import json
import os
import pyperclip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QTextEdit, QPushButton, QLabel, 
                             QLineEdit, QMessageBox, QInputDialog)

class KomutDeposu(QWidget):
    def __init__(self):
        super().__init__()
        self.veri_dosyasi = "kod_verileri.json"
        self.verileri_yukle()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Hızlı Kod & Komut Kütüphanesi')
        self.resize(650, 450)
        
        # Yine o sevdiğimiz karanlık modern tema
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e24;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #ffffff;
            }
            QListWidget {
                background-color: #2a2a35;
                border: 1px solid #3f51b5;
                border-radius: 6px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #3f51b5;
                color: white;
            }
            QTextEdit, QLineEdit {
                background-color: #2a2a35;
                border: 1px solid #5c6bc0;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3f51b5;
                color: white;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #5c6bc0;
            }
        """)
        
        # Ana Düzen (Yatay: Sol taraf liste, Sağ taraf detaylar)
        ana_layout = QHBoxLayout()
        
        # --- SOL TARAF (Liste ve Ekle/Sil Butonları) ---
        sol_layout = QVBoxLayout()
        
        self.liste_label = QLabel("Kayıtlı Kodlar / Komutlar")
        sol_layout.addWidget(self.liste_label)
        
        self.komut_listesi = QListWidget()
        self.komut_listesi.itemClicked.connect(self.komut_secildi)
        sol_layout.addWidget(self.komut_listesi)
        
        # Ekle / Sil Butonları
        buton_layout = QHBoxLayout()
        self.btn_ekle = QPushButton("Yeni Ekle")
        self.btn_ekle.clicked.connect(self.yeni_komut_ekle)
        self.btn_sil = QPushButton("Sil")
        self.btn_sil.clicked.connect(self.komut_sil)
        buton_layout.addWidget(self.btn_ekle)
        buton_layout.addWidget(self.btn_sil)
        sol_layout.addLayout(buton_layout)
        
        ana_layout.addLayout(sol_layout, 2) # Sol tarafın genişlik oranı
        
        # --- SAĞ TARAF (Detay Gösterimi ve Kopyalama) ---
        sag_layout = QVBoxLayout()
        
        self.baslik_label = QLabel("Başlık:")
        sag_layout.addWidget(self.baslik_label)
        
        self.txt_baslik = QLineEdit()
        self.txt_baslik.setPlaceholderText("Komut veya Kod Adı")
        sag_layout.addWidget(self.txt_baslik)
        
        self.Icerik_label = QLabel("Kod / İçerik:")
        sag_layout.addWidget(self.Icerik_label)
        
        self.txt_icerik = QTextEdit()
        self.txt_icerik.setPlaceholderText("Buraya kod bloğunu veya WorldEdit komutunu yapıştır...")
        sag_layout.addWidget(self.txt_icerik)
        
        # Kopyala ve Kaydet Butonları
        sag_buton_layout = QHBoxLayout()
        
        self.btn_kaydet = QPushButton("Değişiklikleri Kaydet 💾")
        self.btn_kaydet.clicked.connect(self.komut_kaydet)
        sag_buton_layout.addWidget(self.btn_kaydet)
        
        self.btn_kopyala = QPushButton("TEK TIKLA KOPYALA 📋")
        self.btn_kopyala.setStyleSheet("background-color: #2e7d32;") # Yeşil buton
        self.btn_kopyala.clicked.connect(self.panoya_kopyala)
        sag_buton_layout.addWidget(self.btn_kopyala)
        
        sag_layout.addLayout(sag_buton_layout)
        
        ana_layout.addLayout(sag_layout, 3) # Sağ tarafın genişlik oranı
        
        self.setLayout(ana_layout)
        self.listeyi_yenile()

    # --- VERİTABANI İŞLEMLERİ (JSON kullanarak) ---
    def verileri_yukle(self):
        if os.path.exists(self.veri_dosyasi):
            with open(self.veri_dosyasi, 'r', encoding='utf-8') as f:
                self.veriler = json.load(f)
        else:
            # İlk açılışta örnek komutlar ekleyelim
            self.veriler = {
                "WorldEdit Büyük Duvar": "//set stone",
                "Python Ekran Temizleme": "import os\nos.system('cls')",
                "Godot Hız Değişkeni": "export var speed = 400"
            }
            self.verileri_kaydet()

    def verileri_kaydet(self):
        with open(self.veri_dosyasi, 'w', encoding='utf-8') as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=4)

    # --- UYGULAMA FONKSİYONLARI ---
    def listeyi_yenile(self):
        self.komut_listesi.clear()
        self.komut_listesi.addItems(self.veriler.keys())

    def komut_secildi(self, item):
        baslik = item.text()
        self.txt_baslik.setText(baslik)
        self.txt_icerik.setText(self.veriler[baslik])

    def yeni_komut_ekle(self):
        isim, ok = QInputDialog.getText(self, 'Yeni Kayıt', 'Kod veya komut için bir başlık girin:')
        if ok and isim:
            if isim in self.veriler:
                QMessageBox.warning(self, 'Hata', 'Bu isimde bir kayıt zaten var!')
            else:
                self.veriler[isim] = ""
                self.verileri_kaydet()
                self.listeyi_yenile()
                # Yeni ekleneni seçelim
                items = self.komut_listesi.findItems(isim, Qt.MatchExactly)
                if items:
                    self.komut_listesi.setCurrentItem(items[0])
                    self.komut_secildi(items[0])

    def komut_kaydet(self):
        eski_baslik = self.komut_listesi.currentItem().text() if self.komut_listesi.currentItem() else None
        yeni_baslik = self.txt_baslik.text().strip()
        icerik = self.txt_icerik.toPlainText()
        
        if not yeni_baslik:
            QMessageBox.warning(self, 'Hata', 'Başlık boş olamaz!')
            return
            
        if eski_baslik and eski_baslik != yeni_baslik:
            # Başlık değiştiyse eskisini silip yenisini ekliyoruz
            del self.veriler[eski_baslik]
            
        self.veriler[yeni_baslik] = icerik
        self.verileri_kaydet()
        self.listeyi_yenile()
        QMessageBox.information(self, 'Başarılı', 'Kod başarıyla depolandı!')

    def komut_sil(self):
        if self.komut_listesi.currentItem():
            baslik = self.komut_listesi.currentItem().text()
            cevap = QMessageBox.question(self, 'Silme Onayı', f"'{baslik}' kaydını silmek istediğinize emin misiniz?", 
                                         QMessageBox.Yes | QMessageBox.No)
            if cevap == QMessageBox.Yes:
                del self.veriler[baslik]
                self.verileri_kaydet()
                self.listeyi_yenile()
                self.txt_baslik.clear()
                self.txt_icerik.clear()

    def panoya_kopyala(self):
        icerik = self.txt_icerik.toPlainText()
        if icerik:
            pyperclip.copy(icerik)
            # Alt barda veya pencere başlığında mini bir bildirim verelim
            self.setWindowTitle('Hızlı Kod & Komut Kütüphanesi (KOPYALANDI! ✅)')
            # 1.5 saniye sonra başlığı eski haline getirmek için timer koyabiliriz ama şimdilik kalsın, basıldığı belli olsun
        else:
            QMessageBox.warning(self, 'Hata', 'Kopyalanacak içerik boş!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KomutDeposu()
    ex.show()
    sys.exit(app.exec_())
