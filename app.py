from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
import pytz
import os
import uuid
from datetime import datetime
import pytz
import os

# Configuración de zona horaria para Colombia
CO_TZ = pytz.timezone('America/Bogota')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundlab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración para subida de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Crear directorio instance si no existe
if not os.path.exists('instance'):
    os.makedirs('instance')

# Crear directorio uploads si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Función auxiliar para verificar extensiones de archivos permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función auxiliar para guardar archivos de evidencia
def save_evidence_file(file, service_id):
    if file and allowed_file(file.filename):
        # Generar nombre único para el archivo
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"service_{service_id}_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

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

class ServiceEvidence(db.Model):
    """Modelo para evidencias fotográficas de servicios"""
    __tablename__ = 'service_evidences'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    evidence_type = db.Column(db.String(50), nullable=False)  # recepcion, proceso, entrega
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))

class Service(db.Model):
    """Modelo de servicios de mantenimiento y reparación"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)  # Optional, can be manual entry
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # mantenimiento, reparacion, revision
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Recibido')  # Recibido, En proceso, Completado, Entregado
    
    # Equipment fields for manual entry (when equipment_id is null)
    equipment_type = db.Column(db.String(100), nullable=True)
    equipment_name = db.Column(db.String(200), nullable=True)
    equipment_brand = db.Column(db.String(100), nullable=True)
    equipment_model = db.Column(db.String(100), nullable=True)
    equipment_serial = db.Column(db.String(100), nullable=True)
    equipment_color = db.Column(db.String(50), nullable=True)
    equipment_accessories = db.Column(db.Text, nullable=True)
    equipment_condition = db.Column(db.Text, nullable=True)
    estimated_cost = db.Column(db.Float, default=0.0)
    estimated_days = db.Column(db.Integer, default=3)
    final_cost = db.Column(db.Float, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    work_performed = db.Column(db.Text, nullable=True)
    parts_used = db.Column(db.Text, nullable=True)  # JSON string con partes utilizadas
    start_date = db.Column(db.DateTime, nullable=True)
    completion_date = db.Column(db.DateTime, nullable=True)
    delivery_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ), onupdate=lambda: datetime.now(CO_TZ))
    
    # Relationships
    evidences = db.relationship('ServiceEvidence', backref='service', lazy=True, cascade='all, delete-orphan')

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

@app.route('/customers/create', methods=['GET', 'POST'])
@login_required
def customer_create():
    """Crear nuevo cliente"""
    if request.method == 'GET':
        # Redirect GET requests to the form
        return redirect(url_for('customer_new'))
    
    # Handle POST request
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

@app.route('/inventory/create', methods=['GET', 'POST'])
@login_required
def inventory_create():
    """Crear nuevo item de inventario"""
    if request.method == 'GET':
        # Redirect GET requests to the form
        return redirect(url_for('inventory_new'))
    
    # Handle POST request
    try:
        item = Inventory(
            name=request.form['name'],
            description=request.form.get('description'),
            category=request.form['category'],
            brand=request.form.get('brand'),
            model=request.form.get('model'),
            stock=int(request.form['stock']),
            min_stock=int(request.form.get('min_stock', 5)),
            price=float(request.form.get('price', 0)) if request.form.get('price') else None,
            supplier=request.form.get('supplier'),
            location=request.form.get('location'),
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

@app.route('/inventory/<int:id>/edit')
@login_required
def inventory_edit(id):
    """Formulario para editar item de inventario"""
    item = Inventory.query.get_or_404(id)
    return render_template('inventory/form.html', item=item)

@app.route('/inventory/<int:id>/update', methods=['POST'])
@login_required
def inventory_update(id):
    """Actualizar item de inventario"""
    try:
        item = Inventory.query.get_or_404(id)
        item.name = request.form['name']
        item.description = request.form.get('description')
        item.category = request.form['category']
        item.brand = request.form.get('brand')
        item.model = request.form.get('model')
        item.stock = int(request.form['stock'])
        item.min_stock = int(request.form.get('min_stock', 5))
        item.price = float(request.form.get('price', 0)) if request.form.get('price') else None
        item.supplier = request.form.get('supplier')
        item.location = request.form.get('location')
        item.updated_at = datetime.now(CO_TZ)
        
        db.session.commit()
        flash('Item actualizado exitosamente', 'success')
        return redirect(url_for('inventory'))
    except Exception as e:
        db.session.rollback()
        flash('Error al actualizar item', 'danger')
        return redirect(url_for('inventory_edit', id=id))

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

@app.route('/services/create', methods=['GET', 'POST'])
@login_required
def service_create():
    """Crear nuevo servicio"""
    if request.method == 'GET':
        # Redirect GET requests to the form
        return redirect(url_for('service_new'))
    
    # Handle POST request
    try:
        # Get equipment_id if selecting from existing equipment, otherwise None for manual entry
        equipment_id = request.form.get('equipment_id')
        if equipment_id == '':
            equipment_id = None
        
        service = Service(
            customer_id=request.form['customer_id'],
            equipment_id=equipment_id,
            service_type=request.form['service_type'],
            description=request.form['description'],
            status='Recibido',
            estimated_cost=float(request.form.get('estimated_cost', 0)),
            estimated_days=int(request.form.get('estimated_days', 3)),
            technician_id=current_user.id,
            created_at=datetime.now(CO_TZ),
            # Manual equipment fields
            equipment_type=request.form.get('equipment_type'),
            equipment_name=request.form.get('equipment_name'),
            equipment_brand=request.form.get('equipment_brand'),
            equipment_model=request.form.get('equipment_model'),
            equipment_serial=request.form.get('equipment_serial'),
            equipment_color=request.form.get('equipment_color'),
            equipment_accessories=request.form.get('equipment_accessories'),
            equipment_condition=request.form.get('equipment_condition')
        )
        
        db.session.add(service)
        db.session.flush()  # Flush to get the service.id
        
        # Handle photo uploads
        uploaded_files = request.files.getlist('photos[]')
        for file in uploaded_files:
            if file and file.filename != '':
                filename = save_evidence_file(file, service.id)
                if filename:
                    evidence = ServiceEvidence(
                        service_id=service.id,
                        filename=filename,
                        evidence_type='recepcion',
                        description='Foto de recepción del equipo'
                    )
                    db.session.add(evidence)
        
        db.session.commit()
        flash('Servicio creado exitosamente', 'success')
        return redirect(url_for('services'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear servicio: {str(e)}', 'danger')
        return redirect(url_for('service_new'))

@app.route('/services/<int:id>')
@login_required
def service_detail(id):
    """Ver detalles de un servicio"""
    service = Service.query.get_or_404(id)
    return render_template('services/detail.html', service=service)

@app.route('/services/<int:id>/edit')
@login_required
def service_edit(id):
    """Formulario para editar servicio"""
    service = Service.query.get_or_404(id)
    customers = Customer.query.all()
    equipment = Equipment.query.all()
    return render_template('services/form.html', service=service, customers=customers, equipment=equipment)

@app.route('/services/<int:id>/update', methods=['POST'])
@login_required
def service_update(id):
    """Actualizar servicio"""
    try:
        service = Service.query.get_or_404(id)
        service.customer_id = request.form['customer_id']
        service.equipment_id = request.form['equipment_id']
        service.service_type = request.form['service_type']
        service.description = request.form['description']
        service.status = request.form.get('status', service.status)
        service.estimated_cost = float(request.form.get('estimated_cost', 0))
        service.final_cost = float(request.form['final_cost']) if request.form.get('final_cost') else None
        service.diagnosis = request.form.get('diagnosis')
        service.work_performed = request.form.get('solution')
        service.updated_at = datetime.now(CO_TZ)
        
        db.session.commit()
        flash('Servicio actualizado exitosamente', 'success')
        return redirect(url_for('services'))
    except Exception as e:
        db.session.rollback()
        flash('Error al actualizar servicio', 'danger')
        return redirect(url_for('service_edit', id=id))

@app.route('/services/<int:id>/details')
@login_required
def service_details_modal(id):
    """Detalles de servicio para modal"""
    service = Service.query.get_or_404(id)
    return render_template('services/details_modal.html', service=service)

@app.route('/services/<int:id>/print')
@login_required
def service_print(id):
    """Imprimir orden de servicio"""
    service = Service.query.get_or_404(id)
    return render_template('services/print.html', service=service)

# ========== GESTIÓN DE ARCHIVOS ==========

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Servir archivos subidos"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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