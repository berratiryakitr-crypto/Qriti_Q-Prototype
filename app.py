from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cok_gizli_anahtar'

# --- 1. KULLANICILAR (RESİMLER VE BİLGİLER BURADA) ---
ornek_kullanicilar = [
    {
        "id": 1, 
        "isim": "Belinay Ciğerci",  # İsmi buradan değiştirebilirsin
        "rol": "Sinefi", 
        "bio": "Turuncu benim rengim! Enerjik filmler.", 
        "resim": "/static/bekinay.jpg",  # Senin yüklediğin resim
        "bg_gradient": "linear-gradient(135deg, #ff9a44 0%, #fc6076 100%)", 
        "spotlight_gradient": "radial-gradient(circle, rgba(255, 220, 150, 0.5) 0%, rgba(255, 160, 80, 0.2) 50%, transparent 70%)",
        "vurgu_renk": "#ff9a44", "avatar_sekil": "50%", 
        "takipci": "421", "izlenen": 2
    },
    {
        "id": 2, 
        "isim": "Furkan Gençoğlu ", 
        "rol": "Hatay Dürüm", 
        "bio": "Siyah beyaz filmler ve noir atmosferi.", 
        "resim": "/static/furkan.jpg", # Senin yüklediğin resim
        "bg_gradient": "linear-gradient(135deg, #000000 0%, #1a1a1a 100%)",
        "spotlight_gradient": "radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, rgba(150, 150, 150, 0.05) 40%, transparent 70%)",
        "vurgu_renk": "#ffffff", "avatar_sekil": "10px", 
        "takipci": "1", "izlenen": 1
    },
    {
        "id": 3, 
        "isim": "Sudenaz Gevrek", 
        "rol": "Sudish", 
        "bio": "Derin sular, klasik müzikler.", 
        "resim": "/static/sude.jpg", # Senin yüklediğin resim
        "bg_gradient": "linear-gradient(135deg, #020024 0%, #090979 100%)",
        "spotlight_gradient": "radial-gradient(circle, rgba(0, 212, 255, 0.3) 0%, rgba(0, 100, 200, 0.1) 40%, transparent 70%)",
        "vurgu_renk": "#00d4ff", "avatar_sekil": "0px", "ozel_sekil_class": "diamond", 
        "takipci": "132", "izlenen": 17
    }
]


# --- 2. FİLMLER ---
ornek_filmler = [
    {"id": 101, "baslik": "Inception", "kullanici_puan": 9, "yorum": "Rüya içinde rüya...", "kullanici_id": 1, "durum": "izlendi", "poster_url": "/static/inception.jpg"},
    {"id": 102, "baslik": "Barbie", "kullanici_puan": "-", "yorum": "Merakla bekliyorum!", "kullanici_id": 1, "durum": "izlenecek", "poster_url": "https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg"},
    {"id": 103, "baslik": "Interstellar", "kullanici_puan": 10, "yorum": "Müzikleri efsane.", "kullanici_id": 2, "durum": "izlendi", "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniL6E8ahDaX06e8q288HL.jpg"},
    {"id": 105, "baslik": "Portrait of a Lady on Fire", "kullanici_puan": 9.5, "yorum": "Tablo gibi.", "kullanici_id": 3, "durum": "izlendi", "poster_url": "https://image.tmdb.org/t/p/w500/3A1k7U9696d16f028f01830551063709.jpg"},
    {"id": 106, "baslik": "The Godfather", "kullanici_puan": 10, "yorum": "Reddemeyeceği bir teklif...", "kullanici_id": 99, "durum": "izlendi", "poster_url": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"},
    {"id": 107, "baslik": "Dune: Part Two", "kullanici_puan": "-", "yorum": "", "kullanici_id": 99, "durum": "izlenecek", "poster_url": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg"}
]

# --- 3. SOHBETLER (Düzeltilmiş Gen Z Muhabbeti) ---
# --- 3. SOHBETLER (İSİMLER EŞLEŞTİRİLDİ) ---
sohbetler = {
    # GRUP SOHBETİ (Burası Aynı Kalabilir)
    "Sinema Kulübü": [
        {"kimden": "Furkan Gençoğlu", "mesaj": "Gençler bu akşam toplanıp 'Bir Zamanlar Anadolu'da' izliyoruz değil mi? Sanat kotamı doldurmam lazım.", "saat": "19:00"},
        {"kimden": "Belinay Ciğerci", "mesaj": "Ya bi dur Allah aşkına... Geçen seferki 3 saatlik bakışma sahnesinden sonra ruhum çekildi. Benim acil Barbie izlemem lazım.", "saat": "19:02"},
        {"kimden": "Sudenaz Gevrek", "mesaj": "HAHAHA +1. Furkan sal bizi kanka, beynim yandı geçen hafta. Bize kaos lazım, dedikodu lazım. Mean Girls açalım?", "saat": "19:05"},
        {"kimden": "Furkan Gençoğlu", "mesaj": "Sizdeki bu vizyonsuzluk beni gerçekten yaralıyor... Sanat diyorum, estetik diyorum, sinematografi diyorum?", "saat": "19:07"},
        {"kimden": "Belinay Ciğerci", "mesaj": "Kardeşim benim vizyonum bol soslu dürüm yerken Shrek izlemek. Var mı ötesi? :d", "saat": "19:10"},
        {"kimden": "Sudenaz Gevrek", "mesaj": "Belinay haklı. Shrek > Nuri Bilge. Konu kilit. Mısırlar benden. 🍿", "saat": "19:12"},
        {"kimden": "Furkan Gençoğlu", "mesaj": "Tamam lanet olsun gelin. Ama Shrek 2 izleriz, en iyisi o. Sen ne dersin Berra?", "saat": "19:15"},
        {"kimden": "Belinay Ciğerci", "mesaj": "Alooo Berrraaa. Müsait değil şuan sanırım", "saat": "19:16"}
    ],
    
 
 
    "Belinay Ciğerci": [
        {"kimden": "Belinay Ciğerci", "mesaj": "Kanka akşama aç gel, efsane soslu bir yer buldum.", "saat": "14:30"}
    ],
    "Furkan Gençoğlu": [
        {"kimden": "Furkan Gençoğlu", "mesaj": "Dün attığım listeyi izledin mi?", "saat": "09:00"}
    ],
    "Sudenaz Gevrek": [
        {"kimden": "Sudenaz Gevrek", "mesaj": "Alacakaranlık serisine baştan başlıyorum, yargılama sakın.", "saat": "23:00"}
    ]
}
# --- ROTALAR ---

@app.route('/')
def home():
    if 'kullanici_adi' not in session: return redirect(url_for('login'))
    return render_template('index.html', filmler=ornek_filmler)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['kullanici_adi'] = request.form.get('username')
        session['user_id'] = 99 
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/film-ekle', methods=['POST'])
def film_ekle():
    baslik = request.form.get('film_adi')
    if baslik:
        yeni_id = len(ornek_filmler) + 100
        yeni_film = {
            "id": yeni_id, "baslik": baslik, "kullanici_puan": "-", "yorum": "", "kullanici_id": 99, "durum": "izlenecek",
            "poster_url": "https://via.placeholder.com/300x450?text=" + baslik.replace(" ", "+")
        }
        ornek_filmler.append(yeni_film)
    return redirect(url_for('profil'))

@app.route('/film-degerlendir/<int:film_id>', methods=['GET', 'POST'])
def film_degerlendir(film_id):
    if 'kullanici_adi' not in session: return redirect(url_for('login'))
    film = next((f for f in ornek_filmler if f['id'] == film_id), None)
    if not film: return "Film bulunamadı", 404
    if request.method == 'POST':
        film['kullanici_puan'] = request.form.get('puan')
        film['yorum'] = request.form.get('yorum')
        film['durum'] = 'izlendi'
        return redirect(url_for('profil'))
    return render_template('film_degerlendir.html', film=film)

@app.route('/profil')
def profil():
    if 'kullanici_adi' not in session: return redirect(url_for('login'))
    return render_template('profil.html', filmler=ornek_filmler)

@app.route('/users')
def users():
    if 'kullanici_adi' not in session: return redirect(url_for('login'))
    return render_template('users.html', users=ornek_kullanicilar)

@app.route('/user/<int:id>')
def user_profile(id):
    if 'kullanici_adi' not in session: return redirect(url_for('login'))
    secilen = next((u for u in ornek_kullanicilar if u['id'] == id), None)
    if not secilen: return "Kullanıcı bulunamadı!", 404
    return render_template('user_profile.html', user=secilen, filmler=ornek_filmler)

@app.route('/mesaj-yaz')
def mesaj_yaz():
    if 'kullanici_adi' not in session: return redirect(url_for('login'))
    alici = request.args.get('alici', 'Genel Sohbet')
    if alici not in sohbetler: sohbetler[alici] = []
    return render_template('mesaj_yaz.html', alici=alici, mesajlar=sohbetler[alici])

@app.route('/mesaj-gonder', methods=['POST'])
def mesaj_gonder():
    alici = request.form.get('alici')
    icerik = request.form.get('mesaj')
    if icerik:
        su_an = datetime.now().strftime("%H:%M")
        if alici not in sohbetler: sohbetler[alici] = []
        sohbetler[alici].append({"kimden": "ben", "mesaj": icerik, "saat": su_an})
    return redirect(url_for('mesaj_yaz', alici=alici))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)