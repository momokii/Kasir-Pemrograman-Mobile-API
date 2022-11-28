from src import *
from model import *


user = Blueprint('user', __name__,
                 url_prefix=f'{BASE_URL_API}/user')


BASE_PATH_DOCS = "./docs/user"


# -------------------- ROUTES -------------------- #

@user.post('/login')
@swag_from(f'{BASE_PATH_DOCS}/login.yaml')
def login():
    request.access_control_request_headers

    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':
        try:
            data = request.get_json()
            username = data['username']
            user = User.query.filter_by(username = username).first()
            if user:
                if user.check_login_pass(data['password']):
                    json_return = jsonify({
                        "success" : {
                            'username' : user.username,
                            'nama' : user.nama,
                            'token' : user.password_hash
                        }
                    }), HTTP_202_ACCEPTED

                else:
                    json_return = jsonify(
                        error = "Login Gagal, Password Salah!"
                    ), HTTP_401_UNAUTHORIZED

            else:
                json_return = jsonify(
                    error = "Login gagal, username tidak ada"
                ), HTTP_404_NOT_FOUND


        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@user.post('')
@swag_from(f'{BASE_PATH_DOCS}/user_add.yaml')
def user_add():

    request.access_control_request_headers

    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':

        try:
            data = request.get_json()
            username = data['username']
            if User.query.filter_by(username = username).first():
                json_return = jsonify(
                    error = "Gagal, Username sudah digunakan!"
                ), HTTP_409_CONFLICT

            else:
                password = data['password']
                password_konfir = data['password_konfir']
                if password == password_konfir:
                    new_user = User(
                        username = username,
                        password = password,
                        nama = data['nama']
                    )
                    db.session.add(new_user)
                    db.session.commit()

                    json_return = jsonify(
                        success = f"Berhasil buat akun, username : {username}"
                    ), HTTP_201_CREATED

                else:
                    json_return = jsonify(
                        error = "Gagal, password konfirmasi tidak sesuai"
                    ), HTTP_409_CONFLICT

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@user.delete('')
@swag_from(f'{BASE_PATH_DOCS}/delete.yaml')
def user_delete():

    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':
        try:
            data = request.get_json()
            username = data['username']
            user = User.query.filter_by(username=username).first()
            if user:
                if user.check_login_pass(data['password']):

                    db.session.delete(user)
                    db.session.commit()

                    json_return = jsonify(
                        success = f"Berhasil hapus user dengan username : {username}"
                    ), HTTP_200_OK

                else:
                    json_return = jsonify(
                        error="Hapus Gagal, Password Salah!"
                    ), HTTP_401_UNAUTHORIZED

            else:
                json_return = jsonify(
                    error="Hapus gagal, username tidak ada"
                ), HTTP_404_NOT_FOUND


        except KeyError:
            json_return = wrong_parameter_input()


    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return




@user.put('')
@user.patch('')
@swag_from(f'{BASE_PATH_DOCS}/edit.yaml')
def user_edit():
    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':

        try:
            data = request.get_json()
            username = data['username']
            user = User.query.filter_by(username=username).first()
            if user:

                nama_lama = user.nama
                user.nama = data['nama_baru']
                db.session.commit()
                json_return = jsonify(
                    success = f"Berhasil edit nama username : {username}, dari ({nama_lama}) menjadi ({data['nama_baru']})"
                ), HTTP_202_ACCEPTED

            else:
                json_return = jsonify(
                    error="Edit gagal, username tidak ada"
                ), HTTP_404_NOT_FOUND

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@user.patch('/pass_change')
@swag_from(f'{BASE_PATH_DOCS}/change_pass.yaml')
def user_change_pass():
    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':
        try:
            data = request.get_json()
            username = data['username']

            password = data['password_baru']
            user = User.query.filter_by(username=username).first()
            if user:
                if user.check_login_pass(data['password']):
                    if password == data['konfir_password']:

                        user.password = password
                        db.session.commit()

                        json_return = jsonify(
                            success=f"Berhasil edit password user dengan username : {username}"
                        ), HTTP_200_OK

                    else:
                        json_return = jsonify(
                            error = "Konfirmasi password baru tidak sesuai, ganti password gagal"
                        ), HTTP_406_NOT_ACCEPTABLE

                else:
                    json_return = jsonify(
                        error="Password tidak sesuai, ganti password gagal"
                    ), HTTP_401_UNAUTHORIZED

            else:
                json_return = jsonify(
                    error="Ganti password gagal, username tidak ada"
                ), HTTP_404_NOT_FOUND


        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(req_check)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





















