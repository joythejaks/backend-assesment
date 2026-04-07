from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load data dari JSON
with open('data/customers.json') as f:
    customers = json.load(f)


# GET /api/customers (pagination)
@app.route('/api/customers', methods=['GET'])
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "data": customers[start:end],
        "total": len(customers),
        "page": page,
        "limit": limit
    })


# GET /api/customers/{id}
@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    for c in customers:
        if c["customer_id"] == customer_id:
            return jsonify(c)

    return jsonify({"error": "Customer not found"}), 404


# GET /api/health
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)