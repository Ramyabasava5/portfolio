from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "portfolio.db"


# -----------------------------
# Database Setup
# -----------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Contact Form Submit
# -----------------------------
@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contacts
        (name,email,subject,message,created_at)
        VALUES (?,?,?,?,?)
    """, (
        name,
        email,
        subject,
        message,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("success"))


# -----------------------------
# Success Page
# -----------------------------
@app.route("/success")
def success():
    return """
    <html>
    <head>
        <title>Success</title>
        <style>
            body{
                font-family:Arial;
                background:#f4f4f4;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }
            .box{
                background:black;
                padding:40px;
                border-radius:10px;
                text-align:center;
                box-shadow:0px 0px 15px rgba(0,0,0,0.1);
            }
            a{
                text-decoration:none;
                color:white;
                background:#6C63FF;
                padding:10px 20px;
                border-radius:5px;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Message Sent Successfully ✅</h1>
            <p>Thank you for contacting Basava Naga Ramya.</p>
            <br>
            <a href="/">Go Back</a>
        </div>
    </body>
    </html>
    """


# -----------------------------
# Admin Dashboard
# -----------------------------
@app.route("/admin")
def admin():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM contacts
        ORDER BY id DESC
    """)

    contacts = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        contacts=contacts
    )


# -----------------------------
# Delete Message
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)