from src import *
from model import *



makanan = Blueprint('makanan', __name__,
                       url_prefix=f"{BASE_URL_API}/makanan")

BASE_PATH_DOCS = "./docs/makanan"


# -------------------- ROUTES -------------------- #



@makanan.get('')
@swag_from(f'{BASE_PATH_DOCS}/makanan_get.yaml')
def makanan_get():
    page = request.args.get('page')
    per_page = request.args.get('per_page')

    if page or per_page:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=5, type=int)
        makanan_paginate = Makanan.query.paginate(page = page, per_page = per_page)

        makanan_list = []
        for data in makanan_paginate.items:
            data_makanan = data.data_makanan()
            makanan_list.append(data_makanan)
            json_return = jsonify({
                'data_makanan' : makanan_list,
                'meta' : {
                    'page' : makanan_paginate.page,
                    'total_page' : makanan_paginate.pages,
                    'total_data' : makanan_paginate.total,
                    'prev_page' : makanan_paginate.prev_num,
                    'next_page' : makanan_paginate.next_num,
                    'has_prev' : makanan_paginate.has_prev,
                    'has_next' : makanan_paginate.has_next
                }
            }), HTTP_200_OK

    else:
        makanan_all = Makanan.query.all()
        makanan_list = []
        for data in makanan_all:
            data_makanan = data.data_makanan()

            makanan_list.append(data_makanan)

        json_return = jsonify(makanan_list), HTTP_200_OK

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@makanan.get('/<id>')
@swag_from(f'{BASE_PATH_DOCS}/makanan_get_single.yaml')
def makanan_get_single(id):
    makanan = Makanan.query.get(id)
    if makanan:
        data_makanan = makanan.data_makanan()
        json_return = jsonify(data_makanan), HTTP_200_OK

    else:
        json_return = jsonify(
            error=f'Data makanan dengan id : {id}, tidak ada'
        ), HTTP_404_NOT_FOUND

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return






@makanan.post('')
@swag_from(f"{BASE_PATH_DOCS}/makanan_add.yaml")
def makanan_add():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        try:
            data = request.get_json()
            makanan = Makanan(
                nama = data['nama'],
                harga = data['harga'],
                kategori = data['kategori']
            )
            db.session.add(makanan)
            db.session.commit()
            json_return = jsonify(
                success = "Berhasil Tambah Data Makanan"
            ), HTTP_201_CREATED

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@makanan.patch('')
@makanan.put('')
@swag_from(f'{BASE_PATH_DOCS}/makanan_edit.yaml')
def makanan_edit():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        try:
            data = request.get_json()
            makanan_edited = Makanan.query.get(data['id'])
            if makanan_edited:
                try:
                    makanan_edited.nama = data['nama_edit']
                    makanan_edited.harga = data['harga_edit']
                    makanan_edited.kategori = data['kategori_edit']
                    db.session.commit()

                    json_return = jsonify(
                        success = f"sukses edit makanan dengan id : {data['id']}"
                    ), HTTP_200_OK

                except KeyError:
                    json_return = wrong_parameter_input()

            else:
                json_return = jsonify(
                    error = "ID makanan tidak ditemukan"
                ), HTTP_404_NOT_FOUND

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@makanan.delete('')
@swag_from(f'{BASE_PATH_DOCS}/makanan_delete.yaml')
def makanan_delete():
    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':

        try:
            id = request.get_json()['id']
            makanan_deleted = Makanan.query.get(id)

        except KeyError:
            json_return = wrong_parameter_input()

        else:
            if makanan_deleted:
                db.session.delete(makanan_deleted)
                db.session.commit()
                json_return = jsonify(
                    success = f'berhasil hapus makanan dengan id : {id}'
                ), HTTP_200_OK

            else:
                json_return = jsonify(
                    error = f"hapus gagal, id makanan {id} tidak ditemukan"
                ), HTTP_404_NOT_FOUND

    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return







































