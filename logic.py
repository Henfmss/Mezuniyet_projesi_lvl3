import sqlite3

def db_meslekler():
    conn = sqlite3.connect("meslekler.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meslekler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meslek TEXT,
    aciklama TEXT
    )
""")
    meslekler_bilgiler = [
    ("Yapay Zeka Eğitmeni", "Robotlara ve bilgisayarlara yeni şeyler öğretirsin."),
    ("Oyun Tasarımcısı", "İnsanların keyifle oynadığı eğlenceli bilgisayar ve mobil oyunları kurgularsın."),
    ("Siber Güvenlik Uzmanı", "Bilgisayar sistemlerini ve dijital bilgileri kötü niyetli korsanlardan korursun."),
    ("Robotik Mühendisi", "Fabrikalarda veya günlük hayatta insanlara yardım eden robotlar tasarlayıp yaparsın."),
    ("Genetik Mühendisi", "Canlıların DNA'sını inceleyerek hastalıkları önlemeye ve yeni tedaviler bulmaya çalışırsın."),
    ("Veri Bilimci", "Karmaşık veri yığınlarındaki gizli kalıpları çözerek geleceğe dair tahminler yaparsın."),
    ("Etik Hacker", "Sistemlerin açıklarını bulmak için güvenlik testleri yapar, sistemlerin daha güvenli olmasını sağlarsın."),
    ("Çevre Mühendisi", "Doğayı korumak, kirliliği önlemek ve geri dönüşümü yaygınlaştırmak için projeler geliştirirsin."),
    ("Uzay Mimarı", "Ay'da veya Mars'ta insanların yaşayabileceği geleceğin uzay istasyonlarını ve evlerini tasarlarsın."),
    ("Deniz Biyoloğu", "Okyanus altındaki gizemli canlıları ve deniz ekosistemini araştırırsın."),
    ("Drone Pilotu", "İnsansız hava araçlarını yönlendirerek haritalama, arama-kurtarma veya çekim işlerini yürütürsün."),
    ("UX/UI Tasarımcısı", "Uygulama ve web sitelerinin kullanıcılar için kullanımı kolay ve şık görünmesini sağlarsın."),
    ("Yenilenebilir Enerji Uzmanı", "Güneş ve rüzgar gibi doğa dostu kaynaklardan temiz elektrik üretmek için sistemler kurarsın."),
    ("Biyomedikal Mühendisi", "Hastalıkların tedavisinde kullanılan tıbbi cihazları ve yapay organları geliştirirsin."),
    ("Astrofizikçi", "Yıldızların, gezegenlerin ve kara deliklerin evrendeki hareketlerini ve yapısını incelersin."),
    ("3D Modelleme Uzmanı", "Çizgi filmler, filmler veya oyunlar için üç boyutlu karakterler ve dünyalar yaratırsın."),
    ("Akıllı Tarım Uzmanı", "Sensörler ve yapay zeka kullanarak tarım ürünlerinin daha verimli yetişmesini sağlarsın."),
    ("Ses Mühendisi", "Müzik, film ve oyunlardaki ses efektlerini düzenleyip en kaliteli hale getirirsin."),
    ("Dijital İçerik Üreticisi", "İnternet dünyasında insanlara ilham veren, eğlendiren ve bilgilendiren içerikler hazırlarsın.")
    ]
    cursor.executemany("INSERT INTO meslekler (meslek, aciklama)VALUES(?,?)",meslekler_bilgiler)

    conn.commit()
    conn.close()


def select_data():
    conn = sqlite3.connect("meslekler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT meslek, aciklama, video  FROM meslekler ORDER BY RANDOM() LIMIT 5")
    meslekler = cursor.fetchall()


    conn.close()
    return meslekler
        
if __name__ == "__main__":
    db_meslekler()


