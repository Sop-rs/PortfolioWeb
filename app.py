from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'temp_development_key')  # Better secret key handling

# Create database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    
    # First, check if the portfolio table exists and drop it to avoid migration issues
    conn.execute('DROP TABLE IF EXISTS portfolio')
    
    # Now create the table with all required columns
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            image_path TEXT,
            project_url TEXT,
            completion_date TEXT
        );
        
        -- Insert some sample data
        INSERT INTO portfolio (title, description, category, image_path, project_url, completion_date)
        VALUES ('E-commerce Website', 'A full-featured online store built with Flask, featuring secure payments, user accounts, and inventory management.', 'web', NULL, 'https://example.com/ecommerce', '2024-12-01');
        
        INSERT INTO portfolio (title, description, category, image_path, project_url, completion_date)
        VALUES ('Brand Identity Design', 'Complete brand identity package including logo design, color palette, typography, and brand guidelines.', 'design', NULL, 'https://example.com/brand', '2024-11-15');
        
        INSERT INTO portfolio (title, description, category, image_path, project_url, completion_date)
        VALUES ('Fitness Tracking App', 'Mobile application for tracking workouts, nutrition, and progress with data visualization and social features.', 'app', NULL, 'https://example.com/fitness', '2024-10-20');
    ''')
    conn.commit()
    conn.close()

# Home page route
@app.route('/')
def home_page():
    # Get featured portfolio items for the homepage
    conn = get_db_connection()
    featured_items = conn.execute('SELECT * FROM portfolio LIMIT 3').fetchall()
    conn.close()
    return render_template('index.html', featured_items=featured_items)

# Portfolio page route
@app.route('/portfolio')
def portfolio():
    conn = get_db_connection()
    portfolio_items = conn.execute('SELECT * FROM portfolio').fetchall()
    conn.close()
    return render_template('portfolio.html', portfolio_items=portfolio_items)

# Portfolio detail page route
@app.route('/portfolio/<int:item_id>')
def portfolio_detail(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM portfolio WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    
    if item is None:
        return redirect(url_for('portfolio'))
        
    return render_template('portfolio_detail.html', item=item)

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
