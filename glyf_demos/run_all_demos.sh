#!/bin/bash
# run_all_demos.sh — Execute all GLYF demonstrations

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  GLYF ALGORITHM DEMONSTRATIONS                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "[1] φ-σ-ρ Collapse Cycle"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 demo_phi_sigma_rho.py
echo ""

read -p "Press Enter for next demo..."
echo ""

echo "[2] Quadriline Logic Navigation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 demo_qll_navigation.py
echo ""

read -p "Press Enter for next demo..."
echo ""

echo "[3] 7-Primitive Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 demo_7_primitives.py
echo ""

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  All demonstrations complete                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
