from flask import Flask, render_template, redirect, url_for, jsonify
import subprocess

app = Flask(__name__)

# Define your containers and their ports
containers = {
    "audiobookshelf": 13378,
    "podgrab": 8080,
    "photoprism": 2342,
    "myjellyfin": 8096,

    # Add more containers if needed
}

def check_health(port):
    try:
        subprocess.run(
            ["curl", "--max-time", "2", "-s", f"http://localhost:{port}"],
            check=True,
            stderr=subprocess.DEVNULL
        )
        return "🟢 Running"
    except subprocess.CalledProcessError:
        return "🔴 Down"

@app.route('/status')
def status():
    statuses = {name: check_health(port) for name, port in containers.items()}
    return jsonify(statuses)


@app.route('/')
def index():
    statuses = {name: check_health(port) for name, port in containers.items()}
    return render_template('index.html', containers=containers, statuses=statuses)

@app.route('/restart/<container>')
def restart(container):
    if container in containers:
        subprocess.run(["podman", "restart", container])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
