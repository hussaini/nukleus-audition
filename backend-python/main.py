from dataclasses import dataclass

from faker import Faker
from faker.generator import random
from flask import Flask, jsonify, request, Response, make_response, abort
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import click
import faker_commerce
from sqlalchemy.orm import Mapped

db = SQLAlchemy()


@dataclass
class Supplier(db.Model):
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


@dataclass
class Product(db.Model):
    id: int
    name: str
    description: str
    image_path: str
    supplier_id: int
    supplier: Mapped[Supplier]
    created_at: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    supplier = db.relationship('Supplier', backref='supplier')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


role_permission = db.Table('role_permission',
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                           )


@dataclass
class Permission(db.Model):
    id: int
    action: str
    subject: str

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)


@dataclass
class Role(db.Model):
    id: int
    name: str
    permissions: Mapped[list[Permission]]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    permissions = db.relationship('Permission', secondary=role_permission, backref='role')


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.before_request
    def before_request():
        user_role = request.cookies.get('user_role', 'Guest')
        role_query = Role.query.filter(Role.name == user_role)\
            .filter(Role.permissions.any(subject='Product'))

        if '/api/inventory' in request.path and request.method == 'GET':
            role_query = role_query.filter(Role.permissions.any(action='view'))
        elif '/api/add-inventory' in request.path and request.method == 'POST':
            role_query = role_query.filter(Role.permissions.any(action='create'))
        elif '/api/delete-inventory' in request.path and request.method == 'POST':
            role_query = role_query.filter(Role.permissions.any(action='delete'))
        elif '/api/update-inventory' in request.path and request.method == 'POST':
            role_query = role_query.filter(Role.permissions.any(action='update'))

        if role_query.first() is None:
            response = jsonify(message='You are unauthorized to perform this action')
            response.status_code = 403
            return response

    @app.after_request
    def after_request(response):
        user_role = request.cookies.get('user_role')
        if user_role is None:
            response.set_cookie('user_role', 'Guest')

        return response

    @app.route('/api/roles', methods=['GET'])
    def get_roles():
        roles = Role.query.all()

        return jsonify(roles)

    @app.route('/api/roles/create', methods=['POST'])
    def create_role():
        input_data = request.get_json()

        role = Role(name=input_data['name'])
        role.permissions = Permission.query.filter(Permission.id.in_(input_data['permissions'])).all()

        db.session.add(role)
        db.session.commit()

        response = Response(status=204)
        response.set_cookie('user_role', role.name)

        return response

    @app.route('/api/switch-role', methods=['POST'])
    def switch_role():
        input_data = request.get_json()

        response = make_response('')
        response.set_cookie('user_role', input_data['role'])

        return response

    @app.route('/api/roles/subjects', methods=['GET'])
    def get_subjects():
        subjects = [{'name': 'Product'}]

        return jsonify(subjects)

    @app.route('/api/roles/permissions', methods=['GET'])
    def get_permissions():
        permissions = Permission.query.all()

        return jsonify(permissions)

    @app.route('/api/inventory', methods=['GET'])
    def get_inventory():
        products = Product.query

        search_name = request.args.get('search_name')
        search_description = request.args.get('search_description')
        search_supplier_id = request.args.get('search_supplier_id')
        sort_by = request.args.get('sort_by')
        sort_order = request.args.get('sort_order')
        per_page = int(request.args.get('per_page', 10))
        current_page = int(request.args.get('current_page', 1))

        if search_name is not None:
            products = products.filter(Product.name.like(f'%{search_name}%'))

        if search_description is not None:
            products = products.filter(Product.description.like(f'%{search_description}%'))

        if search_supplier_id is not None:
            products = products.filter(Product.supplier_id == search_supplier_id)

        if sort_by is not None:
            if sort_by == 'Name':
                if sort_order == 'desc':
                    products = products.order_by(Product.name.desc())
                else:
                    products = products.order_by(Product.name.asc())

            elif sort_by == 'Description':
                if sort_order == 'desc':
                    products = products.order_by(Product.description.desc())
                else:
                    products = products.order_by(Product.description.asc())
        else:
            products = products.order_by(Product.id.desc())

        products = products.paginate(page=current_page, per_page=per_page)

        response = {
            'data': products.items,
            'currentPage': products.page,
            'perPage': products.per_page,
            'totalPage': products.pages,
            'totalItem': products.total,
        }

        return jsonify(response)

    @app.route('/api/inventory/<int:product_id>', methods=['GET'])
    def get_inventory_by_id(product_id):
        product = Product.query.get_or_404(product_id)
        return jsonify(product)

    @app.route('/api/add-inventory', methods=['POST'])
    def add_inventory():
        input_data = request.get_json()

        product = Product(name=input_data['name'], description=input_data['description'], supplier_id=input_data['supplier_id'])

        db.session.add(product)
        db.session.commit()

        return jsonify(product)

    @app.route('/api/delete-inventory', methods=['POST'])
    def delete_inventory():
        input_data = request.get_json()

        product = Product.query.get(input_data['product_id'])
        db.session.delete(product)
        db.session.commit()

        return Response(status=204)

    @app.route('/api/update-inventory', methods=['POST'])
    def update_inventory():
        input_data = request.get_json()

        product = Product.query.get(input_data['product_id'])
        product.name = input_data['name']
        product.description = input_data['description']
        product.supplier_id = input_data['supplier_id']

        db.session.commit()

        return jsonify(product)

    @app.route('/api/inventory/suppliers', methods=['GET'])
    def get_suppliers():
        suppliers = Supplier.query.all()

        return jsonify(suppliers)

    @click.command('db:seed')
    @with_appcontext
    def database_seed(total=1000):
        db.create_all()

        fake = Faker()
        fake.add_provider(faker_commerce.Provider)

        # populate permission table
        permission_create = Permission(id=1, action='create', subject='Product')
        permission_view = Permission(id=2, action='view', subject='Product')
        permission_update = Permission(id=3, action='update', subject='Product')
        permission_delete = Permission(id=4, action='delete', subject='Product')

        db.session.add(permission_create)
        db.session.add(permission_view)
        db.session.add(permission_update)
        db.session.add(permission_delete)

        # populate role table
        role_guest = Role(id=1, name='Guest')
        role_admin = Role(id=2, name='Admin')

        role_guest.permissions.append(permission_view)

        role_admin.permissions.append(permission_create)
        role_admin.permissions.append(permission_view)
        role_admin.permissions.append(permission_update)
        role_admin.permissions.append(permission_delete)

        db.session.add(role_guest)
        db.session.add(role_admin)

        # populate product table

        suppliers = [
            {
                'id': 1,
                'name': 'Supplier One',
            },
            {
                'id': 2,
                'name': 'Supplier Two',
            },
            {
                'id': 3,
                'name': 'Supplier Three',
            },
        ]

        for supplier in suppliers:
            db.session.add(Supplier(id=supplier['id'], name=supplier['name']))

        for i in range(0, total):
            product_name = fake.ecommerce_name()
            product_description = fake.text()
            supplier_id = random.randint(1, 3)
            product = Product(name=product_name, description=product_description, supplier_id=supplier_id)

            db.session.add(product)

        db.session.commit()

    app.cli.add_command(database_seed)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
