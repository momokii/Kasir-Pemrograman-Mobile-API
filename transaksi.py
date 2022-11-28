from src import *
from model import *
from carts import carts_get_all


histori = Blueprint('histori', __name__,
                    url_prefix=f'{BASE_URL_API}')


BASE_PATH_DOCS = './docs/transaksi'


# ----------------- ROUTES ----------------- #


@histori.post('/transaksi')
@swag_from(f'{BASE_PATH_DOCS}/transaksi.yaml')
def transaksi():

    request.access_control_request_headers

    try:
        all_carts = Carts.query.all()
        desc_carts = ""
        total_pesanan = 0
        total_jenis_barang = 0
        total_harga = 0
        for data in all_carts:
            desc = f"({data.makanan.nama} | {data.jml_pesanan} | {data.makanan.harga}) "
            desc_carts += desc

            data_carts = data.get_carts_data()
            total_pesanan += data_carts['jumlah_pesanan']
            total_jenis_barang += 1
            total_harga += data_carts['harga_akhir']

            db.session.delete(data)

        new_transaksi = HistoriTransaksi(
            desc_pesanan = desc_carts,
            jml_barang = total_jenis_barang,
            jml_total_pesanan = total_pesanan,
            total_harga = total_harga
        )
        db.session.add(new_transaksi)
        db.session.commit()

        json_return = jsonify({
            'success' : {
                'desc': desc_carts,
                'total_jumlah_pesanan': total_pesanan,
                'total_jenis_barang': total_jenis_barang,
                'total_harga': total_harga }
        }), HTTP_201_CREATED

    except:
        json_return = jsonify(
            error = "Gagal olah transaksi!"
        ), HTTP_400_BAD_REQUEST


    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return




@histori.get('/histori')
@swag_from(f'{BASE_PATH_DOCS}/transaksi_histori_get.yaml')
def histori_transaksi_get():
    request.access_control_request_headers
    all_transaksi = HistoriTransaksi.query.all()
    transaksi_list = []
    for transaki in all_transaksi:
        transaksi_list.append(transaki.get_histori_transaksi_data())

    json_return = jsonify(transaksi_list), HTTP_200_OK


    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return

