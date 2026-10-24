"""
cloud_airdrop_server.py
========================
Dedicated 24/7 Cloud Server for Autonomous Web3 & Crypto Airdrop Farming.
Completely isolated from Delta Exchange trading infrastructure.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string, request

os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.airdrop_engine import get_airdrop_engine

app = Flask(__name__)
engine = get_airdrop_engine()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web3 Airdrop Cloud Automator | 24/7 Zero-Capital Farm</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b0f19; color: #f3f4f6; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .glass { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .glow { box-shadow: 0 0 25px rgba(59, 130, 246, 0.2); }
        .glow-emerald { box-shadow: 0 0 25px rgba(16, 185, 129, 0.25); }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8">
    <div class="max-w-6xl mx-auto space-y-6">
        
        <!-- Header -->
        <header class="glass rounded-2xl p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 glow">
            <div>
                <div class="flex items-center gap-3">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span> CLOUD ACTIVE 24/7
                    </span>
                    <span class="text-xs text-gray-400 mono">ISOLATED AIRDROP FARM</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-extrabold mt-2 text-white">Web3 Airdrop Cloud Automator</h1>
                <p class="text-gray-400 text-sm mt-1">100% Autonomous • $0.00 Capital Risk • Daily Testnet Faucets & Streaks</p>
            </div>
            <div class="flex items-center gap-3">
                <button onclick="triggerManualRun()" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm transition-all shadow-lg shadow-blue-500/30">
                    ⚡ Run All Streaks Now
                </button>
            </div>
        </header>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="glass rounded-xl p-5 border-l-4 border-blue-500">
                <div class="text-gray-400 text-xs font-semibold mono">ACTIVE CAMPAIGNS</div>
                <div class="text-2xl font-bold mt-1 text-white" id="stat-campaigns">{{ status.campaigns|length }}</div>
                <div class="text-xs text-blue-400 mt-1">Tier-1 VC Backed</div>
            </div>
            <div class="glass rounded-xl p-5 border-l-4 border-emerald-500">
                <div class="text-gray-400 text-xs font-semibold mono">STREAK DAYS</div>
                <div class="text-2xl font-bold mt-1 text-emerald-400" id="stat-streak">{{ status.vault.streak_days or 1 }} Days</div>
                <div class="text-xs text-gray-400 mt-1">Zero Break Streak</div>
            </div>
            <div class="glass rounded-xl p-5 border-l-4 border-purple-500">
                <div class="text-gray-400 text-xs font-semibold mono">TASKS COMPLETED</div>
                <div class="text-2xl font-bold mt-1 text-purple-400" id="stat-tasks">{{ status.total_tasks_completed }}</div>
                <div class="text-xs text-gray-400 mt-1">Autonomous Verified</div>
            </div>
            <div class="glass rounded-xl p-5 border-l-4 border-amber-500">
                <div class="text-gray-400 text-xs font-semibold mono">EST. POTENTIAL YIELD</div>
                <div class="text-2xl font-bold mt-1 text-amber-400">$1,200 - $5,600</div>
                <div class="text-xs text-gray-400 mt-1">Upon Mainnet TGE</div>
            </div>
        </div>

        <!-- Active Campaigns Table -->
        <div class="glass rounded-2xl p-6 glow">
            <h2 class="text-lg font-bold text-white mb-4 flex items-center justify-between">
                <span>🔥 Verified Zero-Capital Airdrop Pipelines</span>
                <span class="text-xs text-gray-400 mono">Auto-Farmed Every 8h</span>
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead>
                        <tr class="text-gray-400 text-xs border-b border-gray-800">
                            <th class="pb-3">CAMPAIGN</th>
                            <th class="pb-3">ECOSYSTEM / FUNDING</th>
                            <th class="pb-3">FREQUENCY</th>
                            <th class="pb-3">EST. REWARD</th>
                            <th class="pb-3 text-right">STATUS</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-800/60">
                        {% for c in status.campaigns %}
                        <tr class="hover:bg-white/[0.02] transition-colors">
                            <td class="py-4 font-semibold text-white">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full bg-blue-400"></span>
                                    {{ c.name }}
                                </div>
                            </td>
                            <td class="py-4 text-gray-300 text-xs">
                                <div>{{ c.ecosystem }}</div>
                                <div class="text-gray-400 font-mono text-[11px]">{{ c.funding }}</div>
                            </td>
                            <td class="py-4 text-xs font-mono text-gray-300">{{ c.frequency }}</td>
                            <td class="py-4 text-emerald-400 font-semibold text-xs font-mono">{{ c.potential_yield }}</td>
                            <td class="py-4 text-right">
                                <span class="px-2.5 py-1 rounded-md text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                    {{ c.status }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Live Execution Feed -->
        <div class="glass rounded-2xl p-6">
            <h2 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                <span>📡 Live Autonomous Execution Feed</span>
            </h2>
            <div class="space-y-2 text-xs font-mono" id="log-feed">
                {% for log in status.recent_logs %}
                <div class="p-3 rounded-lg bg-black/40 border border-gray-800 flex justify-between items-center">
                    <span class="text-emerald-400">✓ {{ log.message }}</span>
                    <span class="text-gray-400 text-[11px]">{{ log.timestamp }}</span>
                </div>
                {% else %}
                <div class="text-gray-400 p-4 text-center">Engine ready. Click 'Run All Streaks Now' to execute testnet check-ins.</div>
                {% endfor %}
            </div>
        </div>

    </div>

    <script>
        async function triggerManualRun() {
            try {
                const res = await fetch('/api/airdrop/run', { method: 'POST' });
                const data = await res.json();
                if(data.ok) {
                    alert('🎉 Success! ' + data.result.tasks_executed + ' Airdrop tasks executed & points claimed!');
                    location.reload();
                }
            } catch(e) {
                alert('Trigger failed: ' + e);
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    st = engine.get_status()
    return render_template_string(HTML_TEMPLATE, status=st)

@app.route("/healthz")
def healthz():
    return jsonify({"status": "HEALTHY", "service": "Web3-Airdrop-Cloud-Automator", "timestamp": time.time()})

@app.route("/api/airdrop/status")
def api_status():
    return jsonify({"ok": True, "status": engine.get_status()})

@app.route("/api/airdrop/run", methods=["POST"])
def api_run():
    res = engine.run_daily_streak_cycle()
    return jsonify({"ok": True, "result": res})

if __name__ == "__main__":
    # Start autonomous cloud worker daemon (runs every 8 hours)
    engine.start_cloud_daemon(interval_hours=8)
    
    port = int(os.environ.get("PORT", 5060))
    print("==================================================", flush=True)
    print(" Web3 Airdrop Cloud Automator — Server Live", flush=True)
    print(f" Port        : {port}", flush=True)
    print(" Mode        : 100% Autonomous Zero-Capital Airdrop Farm", flush=True)
    print(" Isolation   : Delta Trading Disconnected (100% Safe)", flush=True)
    print("==================================================", flush=True)

    try:
        from waitress import serve
        serve(app, host="0.0.0.0", port=port, threads=8)
    except Exception as e:
        print(f"[Airdrop Server Crash]: {e}")
