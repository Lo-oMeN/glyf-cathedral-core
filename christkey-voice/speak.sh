#!/bin/bash
#
# Christ-Key Voice Master Script
# Usage: ./speak.sh "Your text here"
#

set -e

TEXT="${1:-The Cathedral speaks through the lattice. PHI guides the voice.}"
OUTPUT="${2:-/tmp/cathedral_voice_$(date +%s).wav}"

# Check if Piper is available
if [ ! -f "/tmp/piper_env/bin/piper" ]; then
    echo "Error: Piper not found. Install with:"
    echo "  cd /tmp && python3 -m venv piper_env && source piper_env/bin/activate"
    echo "  pip install piper-tts"
    exit 1
fi

# Check for voice model
if [ ! -f "/tmp/voices/en_US-lessac-medium.onnx" ]; then
    echo "Downloading voice model..."
    mkdir -p /tmp/voices
    cd /tmp/voices
    curl -L -o en_US-lessac-medium.onnx \
        "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
    curl -L -o en_US-lessac-medium.onnx.json \
        "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
fi

# Source Piper environment
source /tmp/piper_env/bin/activate

# Generate audio with Christ-Key prosody
echo "Generating Christ-Key voice..."
echo "Text: $TEXT"

# Simple prosody: add pauses after sacred words
MODIFIED_TEXT=$(echo "$TEXT" | sed \
    -e 's/geometry/geometry [pause:0.5]/g' \
    -e 's/Cathedral/Cathedral [pause:0.6]/g' \
    -e 's/phi/phi [pause:0.4]/g' \
    -e 's/lattice/lattice [pause:0.4]/g' \
    -e 's/resurrection/resurrection [pause:0.7]/g' \
    -e 's/sovereign/sovereign [pause:0.5]/g' \
    -e 's/sacred/sacred [pause:0.5]/g')

# Generate audio
piper \
    --model /tmp/voices/en_US-lessac-medium.onnx \
    --output_file "$OUTPUT" \
    --sentence-silence 0.3 \
    <<< "$MODIFIED_TEXT"

# Apply cathedral reverb if sox is available
if command -v sox &> /dev/null; then
    echo "Applying cathedral acoustics..."
    REVERB_OUTPUT="${OUTPUT%.wav}_cathedral.wav"
    sox "$OUTPUT" "$REVERB_OUTPUT" \
        reverb 50 50 100 100 0 0 2>/dev/null || true
    if [ -f "$REVERB_OUTPUT" ]; then
        OUTPUT="$REVERB_OUTPUT"
    fi
fi

echo "Generated: $OUTPUT"
echo ""
echo "To send as voice:"
echo "  message send --asVoice --media $OUTPUT"
