from src import *
from model import *


carts = Blueprint('carts', __name__,
                  url_prefix=f"{BASE_URL_API}/carts")


BASE_PATH_DOCS = './docs/carts'

# -------------------- ROUTES -------------------- #


@carts.get('')
@swag_from(f'{BASE_PATH_DOCS}/carts_get_all.yaml')
def carts_get_all():

    carts_all = Carts.query.all()
    carts_list = []
    total_pesanan = 0
    total_jenis_barang = 0
    total_harga = 0
    for data in carts_all:
        carts_data = data.get_carts_data()
        carts_list.append(carts_data)

        total_pesanan += carts_data['jumlah_pesanan']
        total_jenis_barang += 1
        total_harga += carts_data['harga_akhir']

    meta = {
        'total_pesanan' : total_pesanan,
        'total_jenis_barang' : total_jenis_barang,
        'total_harga' : total_harga
    }


    json_return = jsonify({
        "carts" : carts_list,
        "meta" : meta
    }), HTTP_200_OK

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@carts.get('/<id_carts>')
@swag_from(f'{BASE_PATH_DOCS}/carts_get_single.yaml')
def carts_get_single(id_carts):

    carts = Carts.query.get(id_carts)
    if carts:
        json_return = jsonify(carts.get_carts_data()), HTTP_200_OK

    else:
        json_return = jsonify(
            error = f"ID Carts {id_carts} tidak ditemukan"
        ), HTTP_404_NOT_FOUND

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@carts.post('')
@swag_from(f'{BASE_PATH_DOCS}/carts_add.yaml')
def carts_tambah():

    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':

        try:
            data = request.get_json()
            makanan_tambah = Makanan.query.get(data['id'])
            if makanan_tambah:

                if Carts.query.filter_by(id_makanan = data['id']).first():
                    json_return = jsonify(
                        error = f"Barang : {makanan_tambah.nama} sudah ada di carts"
                    ), HTTP_409_CONFLICT

                else:
                    carts_data = Carts(
                        makanan = makanan_tambah,
                        _pesanan = data['jumlah_pesanan']
                    )

                    db.session.add(carts_data)
                    db.session.commit()
                    json_return = jsonify(
                        success = "Berhasil tambah barang ke carts"
                    ), HTTP_201_CREATED

            else:
                json_return = jsonify(
                    error = f'Error, id makanan : {data["id"]} ditambah tidak ditemukan'
                ), HTTP_404_NOT_FOUND

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(req_check)


    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@carts.patch('')
@carts.put('')
@swag_from(f'{BASE_PATH_DOCS}/carts_edit.yaml')
def carts_edit():
    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')

    if req_check == 'application/json':
        try:
            data = request.get_json()
            carts_edited = Carts.query.get(data['id'])
            if carts_edited:

                carts_edited._pesanan = data['pesanan_baru']
                db.session.commit()

                json_return = jsonify(
                    success = f"Berhasil ubah data pesanan carts dengan makanan {carts_edited.makanan.nama} menjadi {data['pesanan_baru']}"
                ), HTTP_200_OK

            else:
                json_return = jsonify(
                    error = f"ID carts ingin diedit : {data['id']} tidak ditemukan"
                ), HTTP_404_NOT_FOUND


        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@carts.delete('')
@swag_from(f'{BASE_PATH_DOCS}/carts_delete.yaml')
def carts_delete():

    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':
        try:
            id = request.get_json()['id']
            delete_data = Carts.query.get(id)
            if delete_data:

                db.session.delete(delete_data)
                db.session.commit()

                json_return = jsonify(
                    success = f"Berhasil hapus carts dengan ID : {id}"
                ), HTTP_200_OK

            else:

                json_return = jsonify(
                    error = f'Gagal hapus carts, id carts: {id} tidak ditemukan'
                ), HTTP_404_NOT_FOUND

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return






@carts.delete('/reset')
@swag_from(f'{BASE_PATH_DOCS}/carts_reset.yaml')
def carts_reset():

    request.access_control_request_headers

    try:
        carts_all = Carts.query.all()
        for data in carts_all:
            db.session.delete(data)

        db.session.commit()
        json_return = jsonify(
            success = 'Berhasil kosongkan carts'
        ), HTTP_200_OK

    except:
        json_return = jsonify(
            error = "Terjadi Kesalahan saat reset carts"
        ), HTTP_400_BAD_REQUEST

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return


