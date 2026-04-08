#!/bin/bash
# Kessel Flow Master Startup - Port 36132

echo "[1/4] Starting Blood Moon API..."
nohup uvicorn blood_moon_api:app --host 0.0.0.0 --port 36132 > blood_moon.log 2>&1 &

echo "[2/4] Starting Witch Hunter FS..."
nohup python witch_hunter.py > fs.log 2>&1 &

echo "[3/4] Starting Witch Hunter NET..."
nohup python witch_hunter_net.py > net.log 2>&1 &

echo "[4/4] Starting Clive Orchestrator..."
nohup python clive_orchestrator.py > clive.log 2>&1 &

echo "KESSEL FLOW STACK DEPLOYED. Monitoring logs..."
