import sys
from PyQt5.QtWidgets import *
import sqlite3
 
class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        self.baglanti_olustur()
        self.init_ui()
    def init_ui(self):
        kul=QLabel("Mail: ")
        self.user_name=QLineEdit()
        par = QLabel("Par: ")
        self.password=QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.sign_up=QPushButton("Kayıt ol")
        self.sign_in=QPushButton("Giriş Yap")
        self.yazi=QLabel("")
        to=QLabel("Kime: ")
        self.send_to=QLineEdit()
        sub=QLabel("Konu: ")
        self.subject=QLineEdit()
        text=QLabel("Metin: ")
        self.yazi_alani=QTextEdit()
        self.send=QPushButton("GÖNDER")
 
        h_kul=QHBoxLayout()
        h_kul.addWidget(kul)
        h_kul.addWidget(self.user_name)
        h_kul.addStretch()
        h_par=QHBoxLayout()
        h_par.addWidget(par)
        h_par.addWidget(self.password)
        h_par.addStretch()
        h_sign=QHBoxLayout()
        h_sign.addStretch()
        h_sign.addWidget(self.sign_up)
        h_sign.addWidget(self.sign_in)
        h_sign.addStretch()
        h_sign.addStretch()
        h_to=QHBoxLayout()
        h_to.addWidget(to)
        h_to.addWidget(self.send_to)
        h_to.addStretch()
        h_sub=QHBoxLayout()
        h_sub.addWidget(sub)
        h_sub.addWidget(self.subject)
        h_text=QHBoxLayout()
        h_text.addWidget(text)
        h_text.addWidget(self.yazi_alani)
        h_send=QHBoxLayout()
        h_send.addStretch()
        h_send.addWidget(self.send)
        h_send.addStretch()
        v_box=QVBoxLayout()
        v_box.addLayout(h_kul)
        v_box.addLayout(h_par)
        v_box.addLayout(h_sign)
        v_box.addWidget(self.yazi)
        v_box.addLayout(h_to)
        v_box.addLayout(h_sub)
        v_box.addLayout(h_text)
        v_box.addLayout(h_send)
        self.setLayout(v_box)
 
        self.sign_up.clicked.connect(self.kayit_ol)
        self.sign_in.clicked.connect(self.giris)
 
        self.send.clicked.connect(self.mail_yollama)
 
        self.show()
 
    def baglanti_olustur(self):
        self.baglanti=sqlite3.connect("Mailler.db")
        self.cursor=self.baglanti.cursor()
        sorgu="Create Table if not exists bilgiler (e_posta TEXT,parola TEXT)"
        self.cursor.execute(sorgu)
 
    def kayit_ol(self):
        user=self.user_name.text()
        par=self.password.text()
        if user.endswith(".com"):
            sorgu = "insert into bilgiler Values(?,?)"
            self.cursor.execute(sorgu,(user,par))
            self.baglanti.commit()
            print("Yeni kullanıcı\nMail: {}".format(user))
            self.yazi.setText("Kaydınız yapıldı.Hoşgeldiniz!")
        else:
            print("Yanlış bir mail adresi girdiniz!")
            self.yazi.setText("Mail adresiniz hatalı.")
 
    def giris(self): #GELİŞTİRİLEBİLİR(eğer birden fazla kullanıcı varsa login işlemi çalışmıyor)
        sorgu="Select * from bilgiler"
        self.cursor.execute(sorgu)
        mailler=self.cursor.fetchall()
        user = self.user_name.text()
        par = self.password.text()
        for i,j in mailler:
            if i==user and j==par:
                print("Giriş yapıldı..")
                self.yazi.setText("Giriş yapıldı.")
 
            else:
                print("Hatalı giriş yaptınız..")
                self.yazi.setText("Hatalı giriş!!")
 
 
    def mail_yollama(self):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
 
 
        user_name=self.user_name.text()
        password=self.password.text()
        send=self.send_to.text()
        subject=self.subject.text()
        yazi_alani=self.yazi_alani.toPlainText() #BU FONKSİYONLA QTextEditi texte çeviriyosun!!
        #yazi_alani="Tebrikler"
 
        message=MIMEMultipart()
        message["From"]=user_name
        message["To"]=send
        message["Subject"]=subject
 
        message_body=MIMEText(yazi_alani,"plain") #yazacağım mail(burdaki plain normal karakter olsun diye var)
        message.attach(message_body)
 
        try:
            mail=smtplib.SMTP("smtp.gmail.com",587) #587. porta bağlanıyoruz(gmailin izin verdiği port)
            mail.ehlo() #smtp serverına kendimizi tanıtıyoruz
            mail.starttls() #kullanıcı adımızın ve şifremizin şifrelenmesi için
            mail.login(user_name,password)
            mail.sendmail(message["From"],message["To"],message.as_string())
            print("Mail başarıyla gönderildi!!")
            mail.close()
 
        except:
            self.yazi.setText("Mail gönderilemedi.")
            sys.stderr.write("Bir hata oluştu..")
            sys.stderr.flush()
 
 
app=QApplication(sys.argv)
pencere=Pencere()
sys.exit(app.exec_())
