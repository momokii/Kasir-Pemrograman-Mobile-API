from src import *
from makanan import *
from carts import *
from model import *
from transaksi import *
from user import *



# --------------- GLOBAL ERROR HANDLER --------------- #

@app.errorhandler(HTTP_400_BAD_REQUEST)
def handler_400(e):
    return jsonify(
        error = "BAD REQUEST 400"
    ), HTTP_400_BAD_REQUEST


@app.errorhandler(HTTP_404_NOT_FOUND)
def handler_404(e):
    return jsonify(
        error = "Halaman/route tidak ditemukan!"
    ), HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
def handler_406(e):
    return jsonify(
        error = "Fungsi HTTP Tidak sesuai!"
    ), HTTP_405_METHOD_NOT_ALLOWED


@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handler_500(e):
    return jsonify(
        error = "Error pada server"
    ), HTTP_500_INTERNAL_SERVER_ERROR






# --------------- BLUEPRINT ADD --------------- #

app.register_blueprint(makanan)
app.register_blueprint(carts)
app.register_blueprint(histori)
app.register_blueprint(user)


if __name__ == "__main__":
    app.run(debug= True)