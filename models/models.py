from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

# Configuración de zona horaria para Colombia
CO_TZ = pytz.timezone('America/Bogota')

db = SQLAlchemy()

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
    
    # Relaciones
    services = db.relationship('Service', backref='technician', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

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
    
    # Relaciones
    equipment = db.relationship('Equipment', backref='owner', lazy=True)
    services = db.relationship('Service', backref='customer', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

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
    
    # Relaciones
    services = db.relationship('Service', backref='equipment', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'model': self.model,
            'serial_number': self.serial_number,
            'category': self.category,
            'description': self.description,
            'customer_id': self.customer_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

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
    
    # Relaciones
    evidences = db.relationship('ServiceEvidence', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'equipment_id': self.equipment_id,
            'technician_id': self.technician_id,
            'service_type': self.service_type,
            'description': self.description,
            'status': self.status,
            'estimated_cost': self.estimated_cost,
            'final_cost': self.final_cost,
            'diagnosis': self.diagnosis,
            'work_performed': self.work_performed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None
        }

class ServiceEvidence(db.Model):
    """Modelo para evidencias fotográficas de servicios"""
    __tablename__ = 'service_evidences'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    evidence_type = db.Column(db.String(20), default='before')  # before, during, after
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'filename': self.filename,
            'description': self.description,
            'evidence_type': self.evidence_type,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'brand': self.brand,
            'model': self.model,
            'stock': self.stock,
            'min_stock': self.min_stock,
            'price': self.price,
            'supplier': self.supplier,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class InventoryMovement(db.Model):
    """Modelo para movimientos de inventario"""
    __tablename__ = 'inventory_movements'
    
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    movement_type = db.Column(db.String(20), nullable=False)  # entrada, salida, ajuste
    quantity = db.Column(db.Integer, nullable=False)
    previous_stock = db.Column(db.Integer, nullable=False)
    new_stock = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(CO_TZ))
    
    # Relaciones
    inventory_item = db.relationship('Inventory', backref='movements')
    user = db.relationship('User', backref='inventory_movements')
    
    def to_dict(self):
        return {
            'id': self.id,
            'inventory_id': self.inventory_id,
            'service_id': self.service_id,
            'movement_type': self.movement_type,
            'quantity': self.quantity,
            'previous_stock': self.previous_stock,
            'new_stock': self.new_stock,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }