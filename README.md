cat << 'EOF' > README.md
# WitchHunter_NET Agent
### Kessel Flow | Security & State Telemetry

`WitchHunter_NET` is a lightweight Python-based network audit agent. It monitors local TCP listeners, identifies unauthorized ports, and synchronizes the state with the `BLOOD_MOON` coordinator.

---

## 🛠 Installation & Deployment

### 1. Quick Start (One-Shot)
```bash
pip install requests
termux-wake-lock
nohup python3 witchhunter.py > witchhunter.log 2>&1 &
