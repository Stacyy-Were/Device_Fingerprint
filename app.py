from flask import Flask, render_template, request, jsonify
import hashlib
import json
import sqlite3
from datetime import datetime, timezone

app = Flask(__name__)

DATABASE = "fingerprints.db"

SIGNAL_WEIGHTS = {
    "platform": 10,
    "screenWidth": 8,
    "screenHeight": 7,
    "colorDepth": 5,
    "pixelRatio": 5,
    "timezone": 15,
    "cpuCores": 10,
    "touchPoints": 5,
    "language": 10,
    "userAgent": 20,
    "doNotTrack": 5
}

NETWORK_WEIGHTS = {
    "ipAddress": 15,
    "forwardedFor": 5,
    "scheme": 2
}


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS fingerprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            fingerprint TEXT NOT NULL,
            signals TEXT NOT NULL,
            network TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_fingerprint(data):
    normalized = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def get_client_ip():
    forwarded = request.headers.get("X-Forwarded-For")

    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.remote_addr


def collect_network_metadata():
    return {
        "ipAddress": get_client_ip(),
        "forwardedFor": request.headers.get("X-Forwarded-For"),
        "scheme": request.scheme
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "service": "Device Fingerprint Lab"
    })


@app.route("/fingerprint", methods=["POST"])
def fingerprint():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "No fingerprint data received"
        }), 400

    label = data.get(
        "label",
        "Unnamed capture"
    )

    signals = {
        key: value
        for key, value in data.items()
        if key != "label"
    }

    fingerprint_value = create_fingerprint(
        signals
    )

    network = collect_network_metadata()

    connection = get_db()

    connection.execute(
        """
        INSERT INTO fingerprints
        (label, fingerprint, signals, network, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            label,
            fingerprint_value,
            json.dumps(signals),
            json.dumps(network),
            datetime.now(timezone.utc).isoformat()
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "label": label,
        "fingerprint": fingerprint_value,
        "signals": signals,
        "network": network
    })


@app.route("/captures", methods=["GET"])
def captures():
    connection = get_db()

    rows = connection.execute(
        """
        SELECT id, label, fingerprint, signals, network, created_at
        FROM fingerprints
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    results = []

    for row in rows:
        results.append({
            "id": row["id"],
            "label": row["label"],
            "fingerprint": row["fingerprint"],
            "signals": json.loads(row["signals"]),
            "network": json.loads(row["network"]),
            "created_at": row["created_at"]
        })

    return jsonify(results)


@app.route("/capture/<int:capture_id>", methods=["GET"])
def get_capture(capture_id):
    connection = get_db()

    row = connection.execute(
        """
        SELECT *
        FROM fingerprints
        WHERE id = ?
        """,
        (capture_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return jsonify({
            "error": "Capture not found"
        }), 404

    return jsonify({
        "id": row["id"],
        "label": row["label"],
        "fingerprint": row["fingerprint"],
        "signals": json.loads(row["signals"]),
        "network": json.loads(row["network"]),
        "created_at": row["created_at"]
    })


@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "No comparison data received"
        }), 400

    fingerprint_a = data.get(
        "fingerprint_a",
        {}
    )

    fingerprint_b = data.get(
        "fingerprint_b",
        {}
    )

    signals_a = fingerprint_a.get(
        "signals",
        {}
    )

    signals_b = fingerprint_b.get(
        "signals",
        {}
    )

    network_a = fingerprint_a.get(
        "network",
        {}
    )

    network_b = fingerprint_b.get(
        "network",
        {}
    )

    browser_score = 0

    browser_comparison = {}

    for signal, weight in SIGNAL_WEIGHTS.items():

        value_a = signals_a.get(signal)
        value_b = signals_b.get(signal)

        matched = value_a == value_b

        if matched:
            browser_score += weight

        browser_comparison[signal] = {
            "match": matched,
            "value_a": value_a,
            "value_b": value_b,
            "weight": weight
        }

    network_score = 0

    network_comparison = {}

    for signal, weight in NETWORK_WEIGHTS.items():

        value_a = network_a.get(signal)
        value_b = network_b.get(signal)

        matched = (
            value_a is not None
            and value_b is not None
            and value_a == value_b
        )

        if matched:
            network_score += weight

        network_comparison[signal] = {
            "match": matched,
            "value_a": value_a,
            "value_b": value_b,
            "weight": weight
        }

    browser_percentage = browser_score

    network_percentage = round(
        (
            network_score
            / sum(NETWORK_WEIGHTS.values())
        ) * 100
    )

    total_possible = (
        sum(SIGNAL_WEIGHTS.values())
        + sum(NETWORK_WEIGHTS.values())
    )

    total_score = (
        browser_score
        + network_score
    )

    overall_percentage = round(
        (total_score / total_possible) * 100
    )

    if overall_percentage >= 85:

        assessment = "HIGH SIMILARITY"
        confidence = "HIGH"

    elif overall_percentage >= 60:

        assessment = "POSSIBLY RELATED"
        confidence = "MEDIUM"

    else:

        assessment = "LOW SIMILARITY"
        confidence = "LOW"

    return jsonify({
        "browser_score": browser_score,
        "browser_percentage": browser_percentage,
        "network_score": network_score,
        "network_percentage": network_percentage,
        "overall_score": total_score,
        "overall_percentage": overall_percentage,
        "assessment": assessment,
        "confidence": confidence,
        "browser_comparison": browser_comparison,
        "network_comparison": network_comparison
    })


if __name__ == "__main__":

    init_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )