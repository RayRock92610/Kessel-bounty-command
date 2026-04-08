#!/bin/bash
# Kessel Flow: Retention recalibration

echo "[1/2] Locating active pruning processes..."
# Find the PID of the prune_blood_moon script or the specific sqlite3 loop
PRUNE_PID=$(pgrep -f "prune_blood_moon.sh")

if [ -n "$PRUNE_PID" ]; then
    kill $PRUNE_PID
    echo "[SUCCESS] Overwrite process $PRUNE_PID terminated."
else
    echo "[NOTICE] No active overwrite process found."
fi

echo "[2/2] Updating master_logs for 30-day retention..."
sqlite3 blood_moon.db "INSERT INTO master_logs (event_type, status_summary) VALUES ('RETENTION_UPDATE', 'Overwrite disabled; 30-day persistence active');"

# Rename the script to prevent accidental execution
if [ -f "prune_blood_moon.sh" ]; then
    mv prune_blood_moon.sh prune_blood_moon.sh.disabled
fi

echo "Log retention policy synchronized."
