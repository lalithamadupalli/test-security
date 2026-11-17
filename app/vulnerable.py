import ipaddress
import re
import sqlite3
import subprocess

from flask import request, abort

from app.main import app

HOSTNAME_RE = re.compile(r"^[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?$")


@app.get("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    # Fixed: parameterized query, input is passed as data, not SQL
    cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return str(cur.fetchall())


def _is_valid_host(host):
    if not host:
        return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return bool(HOSTNAME_RE.match(host))


@app.get("/ping")
def ping():
    host = request.args.get("host")
    if not _is_valid_host(host):
        abort(400, "invalid host")
    # Fixed: no shell, arguments passed as a list
    return subprocess.check_output(["ping", "-c", "1", host])
