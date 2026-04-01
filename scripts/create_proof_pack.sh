#!/usr/bin/env bash
set -euo pipefail

MILESTONE="${1:-milestone-1-foundation}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PACK_DIR="artifacts/proof/${TIMESTAMP}-${MILESTONE}"

mkdir -p "$PACK_DIR/playwright-report" "$PACK_DIR/test-results" "$PACK_DIR/screenshots"

if [[ -d "playwright-report" ]]; then
  cp -R playwright-report/. "$PACK_DIR/playwright-report/"
fi

if [[ -d "test-results" ]]; then
  cp -R test-results/. "$PACK_DIR/test-results/"
fi

if [[ -f "test-results/smoke-screener-to-detail-and-methodology/test-finished-1.png" ]]; then
  cp "test-results/smoke-screener-to-detail-and-methodology/test-finished-1.png" "$PACK_DIR/screenshots/home-detail-methodology.png"
fi

if [[ -f "test-results/smoke-screener-to-detail-and-methodology/video.webm" ]]; then
  cp "test-results/smoke-screener-to-detail-and-methodology/video.webm" "$PACK_DIR/TOUR.webm"
fi

cat > "$PACK_DIR/README.md" <<EOF
# Proof Pack

Milestone: ${MILESTONE}
Generated at: ${TIMESTAMP}
EOF

echo "Created $PACK_DIR"
