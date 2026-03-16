from flask import Flask, render_template, request
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into user (username,email,phone,country_id,web3_id,projets) values (:username,:email,:phone,:country_id,:web3_id,:projets)",request.form)
        user = query_db('select * from user')
        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user")
    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user")

@app.route("/add_one_projet", methods=["GET","POST"])
def add_one_projet():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into projet (title,description,programminglanguage_id,frontend_id,user_id) values (:title,:description,:programminglanguage_id,:frontend_id,:user_id)",request.form)
        user = query_db('select * from projet')
        return render_template("projetform.html", projets=user, one_user=one_user, the_title="add new projet")
    user = query_db('select * from projet')
    one_user = query_db("select * from projet limit 1", one=True)
    return render_template("projetform.html", projets=user, one_user=one_user, the_title="add new projet")

