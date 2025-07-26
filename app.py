from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user , login_required
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static')

# ✅ PostgreSQL SQLAlchemy connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://go_todo_task_db_user:z3YSJb1og6V5aDVXuJqv9Kgsn7VgBpTO@dpg-d20liqndiees739m4op0-a.oregon-postgres.render.com/go_todo_task_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATA_BASE.db'
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

class Todo(db.Model,UserMixin):
    __tablename__ = 'Todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    user_email = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String, default=str(datetime.utcnow()).split(' ')[0])
    priority = db.Column(db.String(10), default='Low', nullable=False)

class DeletedTodo(db.Model,UserMixin):
    __tablename__ = ' Deleted_Todo'
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String, default=str(datetime.utcnow()).split(' ')[0])
    user_email = db.Column(db.String(200), nullable=False)
    
@app.errorhandler(Exception)
def handle_exception(e):
    return f"Error: {str(e)}", 500
    
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

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        if title and desc:
            to_do = Todo(title=title, content=desc, user_email=current_user.email)
            db.session.add(to_do)
            db.session.commit()

    if current_user.is_authenticated:
        all_todo = Todo.query.filter_by(user_email=current_user.email).all()
        all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
        del_all_todo = DeletedTodo.query.filter_by(user_email=current_user.email).all()
        return render_template(
            'index.html',
            all_todo=all_todo,
            deltodo=del_all_todo,
            current_user=current_user.email,
            logged_in=current_user.is_authenticated
        )

    return render_template(
        'index.html',
        all_todo=[],
        deltodo=[],
        logged_in=current_user.is_authenticated
    )


@app.route('/done/<int:id>', methods=['POST', 'GET'])
def done(id):
    user_to_delete = db.session.query(Todo).filter_by(sno=id).first()
    if user_to_delete:
        deleted_entry = DeletedTodo(
            sno=user_to_delete.sno,
            title=user_to_delete.title,
            content=user_to_delete.content,
            user_email = user_to_delete.user_email
        )
        db.session.add(deleted_entry)
        db.session.delete(user_to_delete)
        db.session.commit()
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    all_todo = Todo.query.all()
    all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
    del_all_todo = DeletedTodo.query.all()
        
    return render_template('index.html', all_todo=all_todo, deltodo=del_all_todo,current_user=current_user.email,logged_in = current_user.is_authenticated)

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
        all_todo = Todo.query.all()
        all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
        del_all_todo = DeletedTodo.query.all()
        
        return render_template('index.html', all_todo=all_todo, deltodo=del_all_todo,current_user=current_user.email,logged_in = current_user.is_authenticated)
        
    user_to_update = Todo.query.filter_by(sno=id).first()
    return render_template('update.html', todo=user_to_update,logged_in = current_user.is_authenticated)

@app.route('/deldone/<int:id>', methods=['POST', 'GET'])
def deldone(id):
    user_to_delete = db.session.query(DeletedTodo).filter_by(sno=id).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        all_todo = Todo.query.all()
        all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
        del_all_todo = DeletedTodo.query.all()
        
        return render_template('index.html', all_todo=all_todo, deltodo=del_all_todo,current_user=current_user.email,logged_in = current_user.is_authenticated)


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
                priority_order = {"High": 1, "Medium": 2, "Low": 3}
                all_todo = Todo.query.all()
                all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
                del_all_todo = DeletedTodo.query.all()
        
                return render_template('index.html', all_todo=all_todo, deltodo=del_all_todo,current_user=current_user.email,logged_in = current_user.is_authenticated)
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
                
                priority_order = {"High": 1, "Medium": 2, "Low": 3}
                all_todo = Todo.query.all()
                all_todo = sorted(all_todo, key=lambda x: priority_order.get(x.priority, 4))
            
                del_all_todo = DeletedTodo.query.all()
        
                return render_template('index.html', all_todo=all_todo, deltodo=del_all_todo,current_user=current_user.email,logged_in = current_user.is_authenticated)
            except:
                db.session.rollback()
                flash('An unexpected error occurred during registration. Please try again later.', 'danger')
        
    return render_template('register.html',logged_in = current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home',logged_in = current_user.is_authenticated))

@app.route('/profile')
def profile():
    return render_template('profile.html',logged_in = current_user.is_authenticated,
                           username = current_user.username,
                           email=current_user.email,
                           password=current_user.og_password)
    
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
        
    return render_template('index.html', all_todo=all_todo, deltodo=del_all_todo,current_user=current_user.email,logged_in = current_user.is_authenticated)


# Create database tables if they don't exist (runs once)
with app.app_context():
    db.create_all()               # runs once per cold‑start

# Local development only
if __name__ == '__main__':
    app.run(debug=True)
