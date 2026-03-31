#!/bin/bash
#
# Christ-Key Voice Speak with Trained Profile
# Usage: ./speak_with_voice.sh voice_profile.json "Your text"
#

set -e

VOICE_PROFILE="${1:-trained_voices/alan_watts_doja_cat_0.60_speak.json}"
TEXT="${2:-The Cathedral speaks through the lattice. PHI guides the voice. Every byte modulates the timbre.}"
OUTPUT="${3:-/tmp/christkey_output_$(date +%s).wav}"

# Check profile exists
if [ ! -f "$VOICE_PROFILE" ]; then
    echo "Error: Voice profile not found: $VOICE_PROFILE"
    echo "Available profiles:"
    ls -1 trained_voices/*_speak.json 2>/dev/null || echo "  (none)"
    exit 1
fi

# Source Piper
source /tmp/piper_env/bin/activate

# Extract prosody parameters from JSON
LENGTH_SCALE=$(python3 -c "import json; print(json.load(open('$VOICE_PROFILE'))['piper_params']['length_scale'])")
NOISE_SCALE=$(python3 -c "import json; print(json.load(open('$VOICE_PROFILE'))['piper_params']['noise_scale'])")
NOISE_W=$(python3 -c "import json; print(json.load(open('$VOICE_PROFILE'))['piper_params']['noise_w'])")

echo "Using voice: $(python3 -c "import json; print(json.load(open('$VOICE_PROFILE'))['voice_name'])")"
echo "Speech rate: $(python3 -c "import json; d=json.load(open('$VOICE_PROFILE')); print(f\"{1.0/d['piper_params']['length_scale']*150:.0f}\")") WPM"

# Apply prosody modifications based on profile
# Sacred words get longer pauses
MODIFIED_TEXT=$(echo "$TEXT" | sed \
    -e 's/\bCathedral\b/Cathedral [break time="0.44s"]/g' \
    -e 's/\bgeometry\b/geometry [break time="0.44s"]/g' \
    -e 's/\blattice\b/lattice [break time="0.44s"]/g' \
    -e 's/\bresurrection\b/resurrection [break time="0.50s"]/g' \
    -e 's/\bsovereign\b/sovereign [break time="0.44s"]/g' \
    -e 's/\bphi\b/phi [break time="0.40s"]/g')

# Generate with trained parameters
piper \
    --model /tmp/voices/en_US-lessac-medium.onnx \
    --output_file "$OUTPUT" \
    --length-scale "$LENGTH_SCALE" \
    --noise-scale "$NOISE_SCALE" \
    --noise-w "$NOISE_W" \
    <<< "$MODIFIED_TEXT"

echo ""
echo "Generated: $OUTPUT"
echo ""
echo "To send as voice:"
echo "  message send --asVoice --media $OUTPUT --target 7429450163"
