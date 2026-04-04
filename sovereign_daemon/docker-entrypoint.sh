#!/bin/bash
# docker-entrypoint.sh — Container entrypoint for sovereign daemon

set -e

case "$1" in
    daemon)
        echo "╔═══════════════════════════════════════════════╗"
        echo "║   Sovereign Agent Daemon (Container)         ║"
        echo "╚═══════════════════════════════════════════════╝"
        echo ""
        
        # Initialize state if not exists
        if [ ! -f /var/lib/sovereign/state.json ]; then
            echo "Initializing fresh state..."
            python3 /opt/sovereign/sovereign_daemon.py --status || true
        fi
        
        echo "Starting daemon..."
        exec python3 /opt/sovereign/sovereign_daemon.py
        ;;
    
    status)
        exec python3 /opt/sovereign/sovereign_daemon.py --status
        ;;
    
    add-goal)
        shift
        exec python3 /opt/sovereign/sovereign_daemon.py --add-goal "$@"
        ;;
    
    shell)
        exec /bin/bash
        ;;
    
    *)
        exec "$@"
        ;;
esac
