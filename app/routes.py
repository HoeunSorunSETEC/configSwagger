from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields, abort

# Define a Blueprint
main_routes = Blueprint('main_routes', __name__)

# Define a Namespace for the API
api_ns = Namespace('items', description='CRUD operations for items')

# Mock database (in-memory list)
items = []

# Define a model for Swagger UI
item_model = api_ns.model('Item', {
    'id': fields.Integer(description='Item ID', required=True),
    'name': fields.String(description='Item Name', required=True),
    'description': fields.String(description='Item Description', required=False),
})


@api_ns.route('/')
class ItemList(Resource):
    @api_ns.doc('list_items', description="Retrieve a list of all items.")
    def get(self):
        """List all items"""
        return items, 200

    @api_ns.expect(item_model, validate=True)
    @api_ns.doc('create_item', description="Create a new item with ID, name, and optional description.")
    def post(self):
        """Create a new item"""
        new_item = api_ns.payload
        # Check for duplicate ID
        if any(item['id'] == new_item['id'] for item in items):
            abort(400, "An item with this ID already exists.")
        items.append(new_item)
        return new_item, 201


@api_ns.route('/<int:id>')
@api_ns.param('id', 'The unique identifier of the item')
class Item(Resource):
    @api_ns.doc('get_item', description="Retrieve an item by its ID.")
    def get(self, id):
        """Fetch an item by ID"""
        item = next((item for item in items if item['id'] == id), None)
        if not item:
            abort(404, "Item not found.")
        return item, 200

    @api_ns.doc('delete_item', description="Delete an item by its ID.")
    def delete(self, id):
        """Delete an item by ID"""
        global items
        item = next((item for item in items if item['id'] == id), None)
        if not item:
            abort(404, "Item not found.")
        items = [item for item in items if item['id'] != id]
        return {'message': 'Item deleted successfully.'}, 200

    @api_ns.expect(item_model, validate=True)
    @api_ns.doc('update_item', description="Update an existing item by its ID.")
    def put(self, id):
        """Update an item by ID"""
        updated_data = api_ns.payload
        item = next((item for item in items if item['id'] == id), None)
        if not item:
            abort(404, "Item not found.")
        item.update(updated_data)
        return item, 200


# Register the Namespace
from flask_restx import Api

def register_api(app):
    api = Api(
        app,
        title='Item Management API',
        version='1.0',
        description='A simple CRUD API for managing items.'
    )
    api.add_namespace(api_ns)
