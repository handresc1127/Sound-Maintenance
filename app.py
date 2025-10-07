from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz
import os

# Configuración de zona horaria para Colombia
CO_TZ = pytz.timezone('America/Bogota')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundlab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear directorio instance si no existe
if not os.path.exists('instance'):
    os.makedirs('instance')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ========== MODELOS ==========

class User(UserMixin, db.Model):
    """Modelo de usuarios del sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='technician')  # admin, technician
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ), onupdate=lambda: datetime.now(CO_TZ))

class Customer(db.Model):
    """Modelo de clientes"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ), onupdate=lambda: datetime.now(CO_TZ))

class Equipment(db.Model):
    """Modelo de equipos de DJ"""
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    serial_number = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # consola, controlador, luces, sonido, humo, otros
    description = db.Column(db.Text, nullable=True)
    purchase_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ), onupdate=lambda: datetime.now(CO_TZ))

class Service(db.Model):
    """Modelo de servicios de mantenimiento y reparación"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # mantenimiento, reparacion, revision
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Recibido')  # Recibido, En proceso, Completado, Entregado
    estimated_cost = db.Column(db.Float, default=0.0)
    final_cost = db.Column(db.Float, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    work_performed = db.Column(db.Text, nullable=True)
    parts_used = db.Column(db.Text, nullable=True)  # JSON string con partes utilizadas
    start_date = db.Column(db.DateTime, nullable=True)
    completion_date = db.Column(db.DateTime, nullable=True)
    delivery_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ), onupdate=lambda: datetime.now(CO_TZ))

class Inventory(db.Model):
    """Modelo de inventario de repuestos y accesorios"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # repuestos, cables, conectores, accesorios, herramientas
    brand = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=5)
    price = db.Column(db.Float, default=0.0)
    supplier = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)  # ubicación en el taller
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ), onupdate=lambda: datetime.now(CO_TZ))

# Helper para fechas en templates
@app.template_global()
def moment():
    class MomentHelper:
        def year(self):
            return datetime.now(CO_TZ).year
        
        def format(self, format_str):
            return datetime.now(CO_TZ).strftime('%A, %B %d, %Y')
    
    return MomentHelper()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========== RUTAS PRINCIPALES ==========

@app.route('/')
@login_required
def dashboard():
    """Dashboard principal con estadísticas"""
    # Estadísticas básicas
    total_customers = Customer.query.count()
    total_equipment = Equipment.query.count()
    active_services = Service.query.filter_by(status='En proceso').count()
    low_stock_items = Inventory.query.filter(Inventory.stock <= Inventory.min_stock).count()
    
    return render_template('dashboard.html', 
                         total_customers=total_customers,
                         total_equipment=total_equipment,
                         active_services=active_services,
                         low_stock_items=low_stock_items)

# ========== AUTENTICACIÓN ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuarios"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout de usuarios"""
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('login'))

# ========== GESTIÓN DE CLIENTES ==========

@app.route('/customers')
@login_required
def customers():
    """Lista de clientes"""
    customers = Customer.query.all()
    return render_template('customers/list.html', customers=customers)

@app.route('/customers/new')
@login_required
def customer_new():
    """Formulario para nuevo cliente"""
    return render_template('customers/form.html', customer=None)

@app.route('/customers/create', methods=['POST'])
@login_required
def customer_create():
    """Crear nuevo cliente"""
    try:
        customer = Customer(
            name=request.form['name'],
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            created_at=datetime.now(CO_TZ)
        )
        db.session.add(customer)
        db.session.commit()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('customers'))
    except Exception as e:
        db.session.rollback()
        flash('Error al crear cliente', 'danger')
        return redirect(url_for('customer_new'))

# ========== GESTIÓN DE INVENTARIO ==========

@app.route('/inventory')
@login_required
def inventory():
    """Lista de inventario"""
    items = Inventory.query.all()
    return render_template('inventory/list.html', items=items)

@app.route('/inventory/new')
@login_required
def inventory_new():
    """Formulario para nuevo item de inventario"""
    return render_template('inventory/form.html', item=None)

@app.route('/inventory/create', methods=['POST'])
@login_required
def inventory_create():
    """Crear nuevo item de inventario"""
    try:
        item = Inventory(
            name=request.form['name'],
            description=request.form.get('description'),
            category=request.form['category'],
            stock=int(request.form['stock']),
            min_stock=int(request.form.get('min_stock', 5)),
            price=float(request.form.get('price', 0)),
            created_at=datetime.now(CO_TZ)
        )
        db.session.add(item)
        db.session.commit()
        flash('Item agregado al inventario exitosamente', 'success')
        return redirect(url_for('inventory'))
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar item al inventario', 'danger')
        return redirect(url_for('inventory_new'))

# ========== GESTIÓN DE SERVICIOS ==========

@app.route('/services')
@login_required
def services():
    """Lista de servicios"""
    services = Service.query.all()
    return render_template('services/list.html', services=services)

@app.route('/services/new')
@login_required
def service_new():
    """Formulario para nuevo servicio"""
    customers = Customer.query.all()
    equipment = Equipment.query.all()
    return render_template('services/form.html', service=None, customers=customers, equipment=equipment)

@app.route('/services/create', methods=['POST'])
@login_required
def service_create():
    """Crear nuevo servicio"""
    try:
        service = Service(
            customer_id=request.form['customer_id'],
            equipment_id=request.form['equipment_id'],
            service_type=request.form['service_type'],
            description=request.form['description'],
            status='Recibido',
            estimated_cost=float(request.form.get('estimated_cost', 0)),
            technician_id=current_user.id,
            created_at=datetime.now(CO_TZ)
        )
        db.session.add(service)
        db.session.commit()
        flash('Servicio creado exitosamente', 'success')
        return redirect(url_for('services'))
    except Exception as e:
        db.session.rollback()
        flash('Error al crear servicio', 'danger')
        return redirect(url_for('service_new'))

# ========== INICIALIZACIÓN ==========

def init_db():
    """Inicializar base de datos con datos por defecto"""
    db.create_all()
    
    # Crear usuario administrador por defecto
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@soundlab.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True,
            created_at=datetime.now(CO_TZ)
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado: admin / admin123")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)