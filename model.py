from src import *


class Order:
    @staticmethod
    def get_now_time():
        return datetime.datetime.today()


### ----------------------- DATABASE ----------------------- ###
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    password_hash = db.Column(db.String(300), nullable = False)
    nama = db.Column(db.String(50))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=8)

    def check_login_pass(self, pass_login):
        return check_password_hash(self.password_hash, pass_login)



class Makanan(db.Model):
    __tablename__ = 'makanan'
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String(100), nullable = False)
    harga = db.Column(db.Integer, default = 0)
    kategori = db.Column(db.String(30), nullable = False)


    def data_makanan(self):
        return {
            'id' : self.id,
            'nama' : self.nama,
            'harga' : self.harga,
            'kategori' : self.kategori
        }



class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key = True)
    id_makanan = db.Column(db.Integer, ForeignKey('makanan.id'))
    jml_pesanan = db.Column(db.Integer, default = 1)
    harga_akhir = db.Column(db.Integer)
    makanan = relationship('Makanan', backref = 'carts')

    @property
    def _pesanan(self):
        self._pesanan

    @_pesanan.setter
    def _pesanan(self, pesanan):
        self.jml_pesanan = pesanan
        self.harga_akhir = self.makanan.harga * self.jml_pesanan


    def get_carts_data(self):
        return {
            'id_carts': self.id,
            'id_makanan' : self.id_makanan,
            'nama_makanan' : self.makanan.nama,
            'kategori_makanan' : self.makanan.kategori,
            'harga_satuan' : self.makanan.harga,
            'jumlah_pesanan' : self.jml_pesanan,
            'harga_akhir' : self.harga_akhir
        }



class HistoriTransaksi(db.Model):
    __tablename__ = 'histori_transaksi'
    id = db.Column(db.Integer, primary_key = True)
    desc_pesanan = db.Column(db.String(2000))
    waktu_order = db.Column(db.DateTime, default = Order.get_now_time())
    jml_barang = db.Column(db.Integer)
    jml_total_pesanan = db.Column(db.Integer)
    total_harga = db.Column(db.Integer)


    def get_histori_transaksi_data(self):
        return {
            'id_histori' : self.id,
            'desc_pesanan' : self.desc_pesanan,
            'waktu_order' : self.waktu_order,
            'jml_jenis_barang' : self.jml_barang,
            'jml_total_barang' : self.jml_total_pesanan,
            'total_harga_order' : self.total_harga
        }


#db.create_all()


