from flask import (
    Blueprint, flash, render_template, request
)


from majapp.db import get_db


bp = Blueprint('search', __name__)


@bp.route('/search', methods=('GET', 'POST'))
def search():

    result = ""
    result2 = ""
    archiname = ""
    address1 = ""

    if request.method == 'POST':
        archiname = request.form['architect_name']
        address1 = request.form['address1']
        error = None

        if not archiname and not address1:
            error = 'archiname is required.'

        if error is not None:
            flash(error)

        else:

            connect = get_db()
            with connect.cursor() as cursor:

                print('!!!!!!!!'+archiname+'!!!!!!!!!!!!')

                if (archiname != '' and address1 == ""):
                    # 建築家名から建築家IDを取得する
                    search_word = "%" + archiname + "%"
                    sql = "SELECT * FROM architect WHERE architect_name LIKE \
                    %s;"
                    cursor.execute(sql, (search_word,))
                    result = cursor.fetchall()

                    result_dict = result[0]
                    archiname_id = result_dict['architect_id']

                    # 建築家IDから建築物を取得する
                    search_word = archiname_id
                    sql = "SELECT \
                        a.architecture_id, \
                        a.architecture_name, \
                        b.architect_name, \
                        a.postalcode, \
                        a.address1, \
                        a.address2, \
                        a.address3, \
                        a.address4, \
                        a.latitude, \
                        a.longitude, \
                        a.architect_id, \
                        a.createdate, \
                        a.updatedate \
                        FROM architecture as a \
                        JOIN architect as b \
                        ON a.architect_id = b.architect_id \
                        WHERE a.architect_id = %s;"

                    cursor.execute(sql, (search_word,))
                    result2 = cursor.fetchall()

                elif (archiname == "" and address1 != ""):
                    
                    print('!!!!!!!!!!!!!!!!!!!!はいった!!!!!!!!!!!!')
                    # 住所1から建築物を取得する
                    search_word = "%" + address1 + "%"
                    sql = "SELECT \
                        a.architecture_id, \
                        a.architecture_name, \
                        b.architect_name, \
                        a.postalcode, \
                        a.address1, \
                        a.address2, \
                        a.address3, \
                        a.address4, \
                        a.latitude, \
                        a.longitude, \
                        a.architect_id, \
                        a.createdate, \
                        a.updatedate \
                        FROM architecture as a \
                        JOIN architect as b \
                        ON a.architect_id = b.architect_id \
                        WHERE a.address1 like %s;"

                    cursor.execute(sql, (search_word,))
                    result2 = cursor.fetchall()
                    print(result2)

                else:
                    result2 = ""

                print(type(result))
                # print(result_dict)

            connect.close()

    return render_template('search.html', archs=result2)
