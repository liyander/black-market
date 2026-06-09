from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os

app = Flask(__name__)

def init_db():
    db_path = os.environ.get('DB_PATH', '/tmp/market.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS secrets (
        id INTEGER PRIMARY KEY,
        flag TEXT NOT NULL
    )''')
    c.execute("INSERT OR IGNORE INTO products VALUES (1, 'Black Pearl Necklace', 4999.99)")
    c.execute("INSERT OR IGNORE INTO products VALUES (2, 'Obsidian Ring', 1299.99)")
    c.execute("INSERT OR IGNORE INTO products VALUES (3, 'Dark Sapphire Pendant', 7499.99)")
    c.execute("INSERT OR IGNORE INTO secrets VALUES (1, 'blackperl{un10n_s3l3ct_1s_y0ur_w34p0n}')")
    conn.commit()
    conn.close()

PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Black Market</title>
    <style>
        body { background: #0a0a0a; color: #c0c0c0; font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #8b0000; text-align: center; }
        .search-box { text-align: center; margin: 30px; }
        input[type="text"] { padding: 10px; width: 300px; }
        button { padding: 10px 20px; background: #8b0000; color: white; border: none; cursor: pointer; }
        .results { max-width: 600px; margin: 0 auto; }
        .product { background: #1a1a1a; padding: 15px; margin: 10px 0; }
        .error { color: #ff4444; text-align: center; background: #2a0000; padding: 10px; }
        .hint { color: #666; text-align: center; font-size: 14px; margin-top: 50px; }
    </style>
</head>
<body>
    <h1>Black Market</h1>
    <div class="search-box">
        <form method="GET" action="/">
            <input type="text" name="search" placeholder="Search products..." value="{{ search }}">
            <button type="submit">Search</button>
        </form>
    </div>
    <div class="results">
        {% if error %}
        <div class="error">Error: {{ error }}</div>
        {% endif %}
        {% for product in products %}
        <div class="product">
            <h3>ID: {{ product[0] }} | {{ product[1] }} | ${{ product[2] }}</h3>
        </div>
        {% endfor %}
    </div>
    <p class="hint">HINT: The search is vulnerable to SQL injection. Try: ' OR '1'='1<br>
    Then figure out how many columns the products table has, and use UNION SELECT to read from the secrets table.</p>
</body>
</html>
'''

@app.route('/')
def index():
    search = request.args.get('search', '')
    products = []
    error = None

    if search:
        db_path = os.environ.get('DB_PATH', '/tmp/market.db')
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            query = "SELECT id, name, price FROM products WHERE name LIKE '%" + search + "%'"
            c.execute(query)
            products = c.fetchall()
            conn.close()
        except Exception as e:
            error = str(e)

    return render_template_string(PAGE, products=products, search=search, error=error)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
