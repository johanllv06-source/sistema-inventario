import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

DATABASE = "inventario.db"

# Crear base de datos si no existe
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )
        """)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/productos")
def productos():
    with sqlite3.connect(DATABASE) as conn:
        productos = conn.execute("SELECT * FROM productos").fetchall()
    return render_template("productos.html", productos=productos)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
            (nombre, precio, cantidad)
        )

    return redirect(url_for("productos"))

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)