from flask import Flask, render_template, request, redirect, url_for,flash , session
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user , login_required
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static')

# ✅ PostgreSQL SQLAlchemy connection string
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://maaz_sidd:26bgYVIRdA2P5mPUuE0L6BduGEs9ek3R@dpg-d28l1q7diees73f299kg-a:5432/go_todo_task_db_j0d4'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATA_BASES.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres+psycopg2://postgres.odadsmvjsofuvjpiigxj:maaz1234567890MAAZ@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:maaz1234567890MAAZ@db.txscflsdnrtmtpzqueyy.supabase.co:5432/postgres"
# DATABASE_URL = f"postgresql+psycopg2://postgres:maaz1234567890MAAZ@db.txscflsdnrtmtpzqueyy.supabase.co:5432/postgres"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-very-very-ultra-secret-top-confidential-highly-predicted-secret-key'

db = SQLAlchemy(app)

class USER_DATABASE(db.Model,UserMixin):
    __tablename__ = 'User_Database'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500), nullable=False)
    og_password = db.Column(db.String(500), nullable=False)
    
    
class Todo(db.Model):
    __tablename__ = 'Todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False) #
    content = db.Column(db.String(500), nullable=False) #
    user_email = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String, default=str(datetime.utcnow()).split(' ')[0])
    priority = db.Column(db.String(10), default='Low', nullable=False) 
    table_name = db.Column(db.String(200), nullable=False) #

class DeletedTodo(db.Model):
    __tablename__ = 'Deleted_Todo'
    
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String, default=str(datetime.utcnow()).split(' ')[0])
    user_email = db.Column(db.String(200), nullable=False)
    table_name = db.Column(db.String(200), nullable=False)
    
class ALL_TABLE_LIST(db.Model):
    __tablename__ = 'All_Table_List'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(200), nullable=False)
    table_name = db.Column(db.String(200), nullable=False)
    
    
@app.errorhandler(Exception)
def handle_exception(e):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            text-align: center;
        }}
        h1 {{
            font-size: 3.5rem;
            color: #000;
            margin-bottom: 1rem;
            border-bottom: #000 solid 3px;
        }}
        p {{
            font-size: 1.2rem;
            color: #333;
            max-width: 600px;
        }}
    </style>
</head>
<body>
    <h1>Error</h1>
    
    <p>{str(e)}</p>
    <p><a href="/">Go To Home</a></p>
</body>
</html>
""", 500

    
# set up flask login 
login_manager = LoginManager()
login_manager.init_app(app=app)
# login_manager.login_view('login')

# load  user for flask login
@login_manager.user_loader
def load_user(user_id):
    return USER_DATABASE.query.get(int(user_id))


@app.route('/', methods=['POST', 'GET'])
def home():
    priority_order = {"High": 1, "Medium": 2, "Low": 3}

    # Initialize with default values to avoid unbound local variable errors
    all_todo = []
    del_all_todo = []
    all_table = []
    # testing purpose
    # print(session)
    
    # POST: Add a new todo
    if request.method == 'POST':
        # if session['TABLE_NAME'] is None or " ":
        #     flash('SELECT A TABLE FIRST', 'warning')
            
        if current_user.is_authenticated and 'TABLE_NAME' in session and session['TABLE_NAME'] is not None:
            table = session['TABLE_NAME']
            title = request.form.get('title')
            desc = request.form.get('desc')
            table_name=session['TABLE_NAME']
            if not table_name:
                flash("Session expired. Please select a table.",'warning')
                return redirect(url_for('home'))
            if title and desc:
                to_do = Todo(
                    title=title,
                    content=desc,
                    user_email=current_user.email,
                    table_name=table_name
                )
                try:
                    db.session.add(to_do)
                    db.session.commit()
                except IntegrityError as e:
                    flash(f'ERROR Integrity Error: {e}','danger')
                    
                finally:
                    all_todo = Todo.query.filter_by(user_email=current_user.email).all()
                    all_table = ALL_TABLE_LIST.query.filter_by(user_email=current_user.email).all()
                    all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
                    del_all_todo = DeletedTodo.query.filter_by(user_email=current_user.email).all()
                    return render_template('index.html',
                                           all_todo=all_todo,
                                            deltodo=del_all_todo,
                                           current_user=current_user.email,
                                           logged_in=True,
                                           table=session['TABLE_NAME'],
                                           all_table=all_table)
                    
        else:
            flash('SELECT A TABLE FIRST', 'warning')

    # GET: Load todos and deleted todos for current user
    if current_user.is_authenticated:
        all_todo = Todo.query.filter_by(user_email=current_user.email).all()
        all_table = ALL_TABLE_LIST.query.filter_by(user_email=current_user.email).all()
        all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
        del_all_todo = DeletedTodo.query.filter_by(user_email=current_user.email).all()
        if session.get("TABLE_NAME") in (None, "None", "", " "):
            try:
                if all_table:
                    xt = all_table[0]
                    x=vars(xt)['table_name']
                    session['TABLE_NAME'] = x
                else:
                    session['TABLE_NAME'] = None
            except Exception as e :
                pass
            
    if current_user.is_authenticated and 'TABLE_NAME' in session:
        return render_template(
            'index.html',
            all_todo=all_todo,
            deltodo=del_all_todo,
            current_user=current_user.email,
            logged_in=True,
            table=session['TABLE_NAME'],
            all_table=all_table
        )
    elif current_user.is_authenticated:
        return render_template(
            'index.html',
            all_todo=all_todo,
            deltodo=del_all_todo,
            current_user=current_user.email,
            logged_in=True,
            all_table=all_table[0]
        )
    else:
        return render_template(
            'index.html',
            all_todo=[],
            deltodo=[],
            logged_in=False,
            
        )


@app.route('/done/<int:id>', methods=['POST', 'GET'])
def done(id):
    user_to_delete = db.session.query(Todo).filter_by(sno=id).first()
    if user_to_delete:
        deleted_entry = DeletedTodo(
            sno=user_to_delete.sno,
            title=user_to_delete.title,
            content=user_to_delete.content,
            user_email = user_to_delete.user_email,
            table_name=session.get('TABLE_NAME') if current_user.is_authenticated else ''
        )
        db.session.add(deleted_entry)
        db.session.delete(user_to_delete)
        db.session.commit()
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    # all_todo = Todo.query.all()
    # all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
    # del_all_todo = DeletedTodo.query.all()
        
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        user_to_update = Todo.query.filter_by(sno=id).first()
        user_to_update.title = title
        user_to_update.content = desc
        db.session.commit()
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        # all_todo = Todo.query.all()
        # all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
        # del_all_todo = DeletedTodo.query.all()
        
        return redirect(url_for('home'))
        
    user_to_update = Todo.query.filter_by(sno=id).first()
    return render_template('update.html', todo=user_to_update,logged_in = current_user.is_authenticated)

@app.route('/deldone/<int:id>', methods=['POST', 'GET'])
def deldone(id):
    user_to_delete = db.session.query(DeletedTodo).filter_by(sno=id).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        # all_todo = Todo.query.all()
        # all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
        # del_all_todo = DeletedTodo.query.all()
        
        return redirect(url_for('home'))



@app.route('/forget-password', methods=['POST', 'GET'])
def forget_password():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        user = USER_DATABASE.query.filter_by(email=email,username=username).first()
        print('+---------------------------------------------+')
        print(password,re_password)
        print('+---------------------------------------------+')
        if password == re_password:
            if user:
                hashed_password = generate_password_hash(password=password,method='pbkdf2:sha256',salt_length=8)
                # password = db.Column(db.String(500), nullable=False)
                # # og_password = db.Column(db.String(500), nullable=False)
                user.password = hashed_password
                user.og_password = re_password
                db.session.commit()
                return redirect(url_for('home'))
            else:
                flash("User Doesn't Exists Register your self",'danger')
        else:
            flash("Password Did not match",'danger')
        
    return render_template('forget_password.html')


@app.route('/about')
def about():
    return render_template('connect.html',logged_in = current_user.is_authenticated)

@app.route('/docs')
def docs():
    return render_template('docs.html',logged_in = current_user.is_authenticated)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        check_user_exist = USER_DATABASE.query.filter_by(email=email).first()
        if check_user_exist:
            if check_password_hash(check_user_exist.password,password):
                login_user(user=check_user_exist)    
                # priority_order = {"High": 1, "Medium": 2, "Low": 3}
                # all_todo = Todo.query.all()
                # all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
                # del_all_todo = DeletedTodo.query.all()
        
                return redirect(url_for('home'))
            else:
                 flash('Incorrect password. Please try again.', 'warning')
        else:
            flash('No account found with that email. Please register first.', 'danger')
        
    return render_template('login.html',logged_in = current_user.is_authenticated)



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u_name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        hashed_password = generate_password_hash(password=password,method='pbkdf2:sha256',salt_length=8)
        
        exist_user =USER_DATABASE.query.filter_by(email=email).first()
        
        if exist_user:
            flash('A user with this email already exists. Please log in instead.', 'danger')
        else:
            new_user = USER_DATABASE(username=u_name,email=email,password=hashed_password,og_password=password)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                new_table = ALL_TABLE_LIST(user_email=current_user.email,table_name=current_user.username)
                db.session.add(new_table)
                db.session.commit()
        
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                flash('An unexpected error occurred during registration. Please try again later.', 'danger')
        
    return render_template('register.html',logged_in = current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    session['TABLE_NAME'] = ' '
    logout_user()
    return redirect(url_for('home',logged_in = current_user.is_authenticated))

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        
        return render_template('profile.html',logged_in = True,
                            username = current_user.username,
                            email=current_user.email,
                            password=current_user.og_password)
    else:
        return render_template('profile.html',logged_in = False,)
    

    
@app.route('/priority/<prior>/<int:id>')
def priority(prior,id):
    print('+-----------------------------+')
    print(prior,id)
    user = Todo.query.filter_by(sno=id).first()
    if user:
        if prior == 'High':
            user.priority = 'High'
            db.session.commit()
            print('priority updated to high')
            
        elif prior == 'Medium':
            user.priority = 'Medium'
            db.session.commit()
            print('priority updated to Medium')
            
        elif prior == 'Low':
            user.priority = 'Low'
            db.session.commit()
            print('priority updated to Low')
            
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        all_todo = Todo.query.all()
        all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
        del_all_todo = DeletedTodo.query.all()
        
    return redirect(url_for('home'))




    
@app.route('/table/<table_name_selected>')
@login_required
def table(table_name_selected):
    
    if current_user.is_authenticated:
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        all_todo = Todo.query.filter_by(user_email=current_user.email).all()
        all_table = ALL_TABLE_LIST.query.filter_by(user_email=current_user.email).all()
        all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
        del_all_todo = DeletedTodo.query.filter_by(user_email=current_user.email).all()
        session['TABLE_NAME'] = table_name_selected
    return render_template(
                'index.html',
                all_todo=all_todo,
                deltodo=del_all_todo,
                current_user=current_user.email,
                logged_in=True,
                table=session['TABLE_NAME'],
                all_table=all_table
            )


@app.route('/add-table')
@login_required
def add_table():
    t = random.choices('qwertyuiopasdfghjklzxcvbnm',k=5)
    x= ''.join(t)
    new_table = ALL_TABLE_LIST(user_email=current_user.email,table_name=x)
    db.session.add(new_table)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete-table/<int:id>')
@login_required
def delete_table(id):
    new_table = ALL_TABLE_LIST.query.filter_by(id=id).first()
    todos = Todo.query.filter_by(table_name=new_table.table_name).all()
    delltodos = DeletedTodo.query.filter_by(table_name=new_table.table_name).all()
    for i in delltodos:
        db.session.delete(i)
    db.session.commit()
    
    for i in todos:
        db.session.delete(i)
    db.session.commit()
    db.session.delete(new_table)
    db.session.commit()
    
    session['TABLE_NAME'] = None
    return redirect(url_for('home'))


@app.route('/edit-table/<int:id>',methods=["GET","POST"])
@login_required
def edit_table(id):
    new_table = ALL_TABLE_LIST.query.filter_by(id=id).first()
    if request.method == 'POST':
        old_table_name = new_table.table_name
        print(old_table_name)
        name = request.form.get('title')    
        new_table.table_name = name
        db.session.commit()  
        try:
            todoo = Todo.query.filter_by(table_name=old_table_name).update({"table_name":name})
            deltodoo = DeletedTodo.query.filter_by(table_name=old_table_name).update({"table_name": name})
            db.session.commit()  
        except :
            pass
        return redirect(f'/table/{name}')
          
    
    return render_template('edit_table.html',t=new_table)





# Create database tables if they don't exist (runs once)
with app.app_context():
    db.create_all()               # runs once per cold‑start

# Local development only
if __name__ == '__main__':
    app.run(debug=True)
