#!/bin/bash
# install_sovereign_daemon.sh — Install sovereign agent as system daemon

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Sovereign Daemon Installation                          ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: Please run as root (sudo)${NC}"
    exit 1
fi

# Configuration
INSTALL_DIR="/opt/sovereign"
DATA_DIR="/var/lib/sovereign"
LOG_DIR="/var/log"
SERVICE_USER="sovereign"
DAEMON_FILE="$(dirname "$0")/sovereign_daemon.py"
SERVICE_FILE="$(dirname "$0")/sovereign.service"

echo "[1/7] Checking prerequisites..."
python3 --version || { echo -e "${RED}Python 3 not found${NC}"; exit 1; }

# Check systemd
if ! command -v systemctl &> /dev/null; then
    echo -e "${YELLOW}Warning: systemd not found. Daemon will run in foreground mode only.${NC}"
    USE_SYSTEMD=false
else
    USE_SYSTEMD=true
fi

echo "[2/7] Creating directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$DATA_DIR"
mkdir -p "$DATA_DIR/inbox"
mkdir -p "$DATA_DIR/archive"
mkdir -p "$LOG_DIR"

echo "[3/7] Creating service user..."
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --home-dir "$DATA_DIR" --shell /bin/false \
            --user-group "$SERVICE_USER"
    echo "  Created user: $SERVICE_USER"
else
    echo "  User exists: $SERVICE_USER"
fi

echo "[4/7] Installing Python dependencies..."
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install python-daemon

echo "[5/7] Installing daemon files..."
if [ -f "$DAEMON_FILE" ]; then
    cp "$DAEMON_FILE" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/sovereign_daemon.py"
    echo "  Installed: sovereign_daemon.py"
else
    echo -e "${RED}Error: sovereign_daemon.py not found at $DAEMON_FILE${NC}"
    exit 1
fi

# Copy service file
if [ "$USE_SYSTEMD" = true ] && [ -f "$SERVICE_FILE" ]; then
    cp "$SERVICE_FILE" /etc/systemd/system/
    echo "  Installed: sovereign.service"
fi

echo "[6/7] Setting permissions..."
chown -R "$SERVICE_USER:$SERVICE_USER" "$DATA_DIR"
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
touch "$LOG_DIR/sovereign.log"
chown "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR/sovereign.log"

echo "[7/7] Initializing state..."
source "$INSTALL_DIR/venv/bin/activate"
python3 "$INSTALL_DIR/sovereign_daemon.py" --status 2>/dev/null || true

if [ "$USE_SYSTEMD" = true ]; then
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Installation Complete!                                  ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Commands:"
    echo "  Start:   sudo systemctl start sovereign"
    echo "  Stop:    sudo systemctl stop sovereign"
    echo "  Status:  sudo systemctl status sovereign"
    echo "  Logs:    sudo journalctl -u sovereign -f"
    echo "  Enable:  sudo systemctl enable sovereign  # Start on boot"
    echo ""
    echo "Add a goal:"
    echo "  sudo /opt/sovereign/venv/bin/python /opt/sovereign/sovereign_daemon.py --add-goal 'Research GLYF cathedral architecture' --priority HIGH"
    echo ""
    echo "Check status:"
    echo "  sudo /opt/sovereign/venv/bin/python /opt/sovereign/sovereign_daemon.py --status"
    echo ""
    echo -e "${YELLOW}Start the daemon now?${NC}"
    read -p "[Y/n] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        systemctl daemon-reload
        systemctl start sovereign
        echo -e "${GREEN}Daemon started!${NC}"
        sleep 2
        systemctl status sovereign --no-pager
    fi
else
    echo ""
    echo -e "${YELLOW}Systemd not available. Run in foreground mode:${NC}"
    echo "  cd $INSTALL_DIR && source venv/bin/activate"
    echo "  python3 sovereign_daemon.py"
fi

echo ""
echo "Directories:"
echo "  Install:  $INSTALL_DIR"
echo "  Data:     $DATA_DIR"
echo "  Logs:     $LOG_DIR/sovereign.log"
echo "  Inbox:    $DATA_DIR/inbox/  (drop .json files for processing)"
