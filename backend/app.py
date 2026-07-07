from flask import Flask, render_template, request, redirect, session
import sqlite3
import uuid

app = Flask(__name__)

# Secret Key for Session
app.secret_key = "todo_management_secret"


# ---------------- DATABASE ---------------- #

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo_lists(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        is_public INTEGER DEFAULT 0,
        share_token TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        list_id INTEGER,
        title TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        tag TEXT DEFAULT 'No Tag'
    )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return redirect("/login")


# ---------------- SIGNUP ---------------- #

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        if cursor.fetchone():

            conn.close()

            return "Username already exists!"

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, password)
        )

        conn.commit()

        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")
# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM todo_lists
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    todo_lists = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        todo_lists=todo_lists,
        username=session["username"]
    )


# ---------------- CREATE TODO LIST ---------------- #

@app.route("/create_list", methods=["POST"])
def create_list():

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO todo_lists(user_id, title, is_public, share_token)
        VALUES (?, ?, ?, ?)
        """,
        (
            session["user_id"],
            title,
            0,
            str(uuid.uuid4())[:8]
        )
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- RENAME TODO LIST ---------------- #

@app.route("/rename_list/<int:list_id>", methods=["POST"])
def rename_list(list_id):

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE todo_lists
        SET title=?
        WHERE id=? AND user_id=?
        """,
        (
            title,
            list_id,
            session["user_id"]
        )
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- DELETE TODO LIST ---------------- #

@app.route("/delete_list/<int:list_id>")
def delete_list(list_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM todo_lists
        WHERE id=? AND user_id=?
        """,
        (
            list_id,
            session["user_id"]
        )
    )

    todo = cursor.fetchone()

    if not todo:
        conn.close()
        return "Access Denied"

    cursor.execute(
        "DELETE FROM todo_items WHERE list_id=?",
        (list_id,)
    )

    cursor.execute(
        "DELETE FROM todo_lists WHERE id=?",
        (list_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
# ---------------- OPEN TODO LIST ---------------- #

@app.route("/todo/<int:list_id>")
def todo(list_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    # Check ownership
    cursor.execute(
        """
        SELECT * FROM todo_lists
        WHERE id=? AND user_id=?
        """,
        (
            list_id,
            session["user_id"]
        )
    )

    todo_list = cursor.fetchone()

    if not todo_list:
        conn.close()
        return "Access Denied"

    cursor.execute(
        """
        SELECT * FROM todo_items
        WHERE list_id=?
        ORDER BY id DESC
        """,
        (list_id,)
    )

    todo_items = cursor.fetchall()

    conn.close()

    return render_template(
        "todo.html",
        todo_list=todo_list,
        todo_items=todo_items
    )


# ---------------- ADD TODO ITEM ---------------- #

@app.route("/add_item/<int:list_id>", methods=["POST"])
def add_item(list_id):

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    tag = request.form.get("tag", "No Tag")

    conn = get_db()
    cursor = conn.cursor()

    # Verify ownership
    cursor.execute(
        """
        SELECT * FROM todo_lists
        WHERE id=? AND user_id=?
        """,
        (
            list_id,
            session["user_id"]
        )
    )

    if not cursor.fetchone():
        conn.close()
        return "Access Denied"

    cursor.execute(
        """
        INSERT INTO todo_items(list_id,title,completed,tag)
        VALUES(?,?,?,?)
        """,
        (
            list_id,
            title,
            0,
            tag
        )
    )

    conn.commit()
    conn.close()

    return redirect(f"/todo/{list_id}")


# ---------------- TOGGLE COMPLETE ---------------- #

@app.route("/toggle_item/<int:item_id>/<int:list_id>")
def toggle_item(item_id, list_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT completed
        FROM todo_items
        WHERE id=?
        """,
        (item_id,)
    )

    item = cursor.fetchone()

    if not item:
        conn.close()
        return redirect(f"/todo/{list_id}")

    status = 0 if item["completed"] else 1

    cursor.execute(
        """
        UPDATE todo_items
        SET completed=?
        WHERE id=?
        """,
        (
            status,
            item_id
        )
    )

    conn.commit()
    conn.close()

    return redirect(f"/todo/{list_id}")


# ---------------- DELETE TODO ITEM ---------------- #

@app.route("/delete_item/<int:item_id>/<int:list_id>")
def delete_item(item_id, list_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM todo_items WHERE id=?",
        (item_id,)
    )

    conn.commit()
    conn.close()

    return redirect(f"/todo/{list_id}")


# ---------------- EDIT TODO ITEM ---------------- #

@app.route("/edit_item/<int:item_id>/<int:list_id>", methods=["POST"])
def edit_item(item_id, list_id):

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    tag = request.form["tag"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE todo_items
        SET title=?, tag=?
        WHERE id=?
        """,
        (
            title,
            tag,
            item_id
        )
    )

    conn.commit()
    conn.close()

    return redirect(f"/todo/{list_id}")


# ---------------- FILTER BY TAG ---------------- #

@app.route("/todo/<int:list_id>/tag/<tag>")
def filter_tag(list_id, tag):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM todo_lists
        WHERE id=? AND user_id=?
        """,
        (
            list_id,
            session["user_id"]
        )
    )

    todo_list = cursor.fetchone()

    if not todo_list:
        conn.close()
        return "Access Denied"

    cursor.execute(
        """
        SELECT * FROM todo_items
        WHERE list_id=? AND tag=?
        ORDER BY id DESC
        """,
        (
            list_id,
            tag
        )
    )

    todo_items = cursor.fetchall()

    conn.close()

    return render_template(
        "todo.html",
        todo_list=todo_list,
        todo_items=todo_items
    )
    # ---------------- PUBLIC SHARE ---------------- #

@app.route("/share/<token>")
def share(token):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM todo_lists
        WHERE share_token=?
        """,
        (token,)
    )

    todo_list = cursor.fetchone()

    if not todo_list:
        conn.close()
        return "Invalid Share Link"

    cursor.execute(
        """
        SELECT * FROM todo_items
        WHERE list_id=?
        ORDER BY id DESC
        """,
        (todo_list["id"],)
    )

    todo_items = cursor.fetchall()

    conn.close()

    return render_template(
        "todo.html",
        todo_list=todo_list,
        todo_items=todo_items
    )


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    init_db()

    app.run(debug=True)