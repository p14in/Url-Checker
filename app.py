from flask import Flask, request, render_template
import sqlite3
from urllib.parse import urlparse

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                domain TEXT NOT NULL
            )
        ''')
        conn.commit()

# Home route to display and add URLs
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        if url and url.strip():
            # Extract domain from URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or 'Unknown'
            
            # Insert URL into database
            with sqlite3.connect('urls.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO urls (url, domain) VALUES (?, ?)', (url, domain))
                conn.commit()
        else:
            error = "Invalid or empty URL"
    
    # Fetch all URLs from database
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT url, domain FROM urls')
        urls = cursor.fetchall()
    
    return render_template('index.html', urls=urls, error=error)

# Initialize database when app starts
if __name__ == '__main__':
    init_db()
    app.run(debug=True)