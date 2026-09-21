from flask import Flask, render_template_string
import time
import os

app = Flask(__name__)
START_TIME = time.time()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Server Dashboard</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    min-height: 100vh;
    font-family: Inter, Arial, sans-serif;
    background:
        radial-gradient(circle at top left, #18243d 0%, transparent 35%),
        radial-gradient(circle at bottom right, #102d2a 0%, transparent 35%),
        #080b12;
    color: #fff;
    padding: 24px;
}

.container {
    width: 100%;
    max-width: 1100px;
    margin: auto;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo {
    width: 44px;
    height: 44px;
    border-radius: 13px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #6c63ff, #00d4ff);
    font-size: 22px;
    box-shadow: 0 8px 30px #0006;
}

h1 {
    font-size: 22px;
}

.subtitle {
    color: #8992a5;
    font-size: 13px;
    margin-top: 3px;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 14px;
    border-radius: 30px;
    background: #0d251d;
    border: 1px solid #1d684d;
    color: #62e6a4;
    font-size: 13px;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #36e58b;
    box-shadow: 0 0 12px #36e58b;
}

.hero {
    padding: 32px;
    border: 1px solid #ffffff12;
    border-radius: 22px;
    background: #ffffff07;
    backdrop-filter: blur(18px);
    margin-bottom: 20px;
}

.hero h2 {
    font-size: 32px;
    margin-bottom: 10px;
}

.hero p {
    color: #9aa3b5;
}

.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 20px;
}

.card {
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #ffffff10;
    background: #ffffff06;
    backdrop-filter: blur(15px);
}

.card-title {
    color: #8d96a9;
    font-size: 13px;
    margin-bottom: 12px;
}

.value {
    font-size: 25px;
    font-weight: 700;
}

.green {
    color: #55e49b;
}

.blue {
    color: #63c7ff;
}

.purple {
    color: #a894ff;
}

.section {
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #ffffff10;
    background: #ffffff06;
}

.section h3 {
    margin-bottom: 18px;
}

.endpoint {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid #ffffff09;
}

.endpoint:last-child {
    border-bottom: 0;
}

.path {
    font-family: monospace;
    color: #cbd2df;
}

.badge {
    color: #55e49b;
    background: #55e49b12;
    border: 1px solid #55e49b30;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
}

.footer {
    text-align: center;
    color: #596274;
    font-size: 12px;
    margin-top: 24px;
}

@media (max-width: 700px) {
    body {
        padding: 15px;
    }

    .header {
        align-items: flex-start;
        gap: 15px;
    }

    .status {
        font-size: 11px;
    }

    .hero {
        padding: 24px;
    }

    .hero h2 {
        font-size: 26px;
    }

    .grid {
        grid-template-columns: 1fr;
    }
}
</style>
</head>

<body>

<div class="container">

    <div class="header">
        <div class="brand">
            <div class="logo">⚡</div>
            <div>
                <h1>Server Dashboard</h1>
                <div class="subtitle">Powered by Python</div>
            </div>
        </div>

        <div class="status">
            <span class="dot"></span>
            ONLINE
        </div>
    </div>

    <div class="hero">
        <h2>Server is running 🚀</h2>
        <p>Your Render server is online and responding normally.</p>
    </div>

    <div class="grid">

        <div class="card">
            <div class="card-title">STATUS</div>
            <div class="value green">Operational</div>
        </div>

        <div class="card">
            <div class="card-title">RUNTIME</div>
            <div class="value blue">Python 3</div>
        </div>

        <div class="card">
            <div class="card-title">UPTIME</div>
            <div class="value purple" id="uptime">Calculating...</div>
        </div>

    </div>

    <div class="section">
        <h3>API Endpoints</h3>

        <div class="endpoint">
            <span class="path">GET /</span>
            <span class="badge">ONLINE</span>
        </div>

        <div class="endpoint">
            <span class="path">GET /health</span>
            <span class="badge">ONLINE</span>
        </div>

    </div>

    <div class="footer">
        Server Dashboard • Render Deployment
    </div>

</div>

<script>
const started = {{ started }};

function updateUptime() {
    let seconds = Math.floor(Date.now() / 1000 - started);

    let days = Math.floor(seconds / 86400);
    seconds %= 86400;

    let hours = Math.floor(seconds / 3600);
    seconds %= 3600;

    let minutes = Math.floor(seconds / 60);
    seconds %= 60;

    document.getElementById("uptime").textContent =
        `${days}d ${hours}h ${minutes}m ${seconds}s`;
}

updateUptime();
setInterval(updateUptime, 1000);
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        started=START_TIME
    )


@app.route("/health")
def health():
    return {
        "status": "online",
        "service": "server",
        "runtime": "python"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)