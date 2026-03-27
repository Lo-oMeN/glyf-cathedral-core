#!/bin/bash
#
# Automated fork and patch of NanoClaw for cathedral deployment
# Usage: ./fork_nanoclaw.sh [options]

set -e

UPSTREAM="https://github.com/qwibitai/nanoclaw"
NAME="cathedral-gateway"
INFERENCE_URL="http://mechanics:8080"
WORKDIR="$(pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --upstream)
      UPSTREAM="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --inference-url)
      INFERENCE_URL="$2"
      shift 2
      ;;
    --output)
      WORKDIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "🔱 Forking NanoClaw"
echo "==================="
echo "Upstream: $UPSTREAM"
echo "Name: $NAME"
echo "Inference URL: $INFERENCE_URL"
echo ""

# Clone
echo "📦 Cloning repository..."
if [ -d "$WORKDIR/$NAME" ]; then
  echo "⚠ Directory exists, pulling latest..."
  cd "$WORKDIR/$NAME"
  git pull
else
  git clone --depth 1 "$UPSTREAM" "$WORKDIR/$NAME"
  cd "$WORKDIR/$NAME"
fi

# Apply patches
echo "🔧 Applying cathedral patches..."

# Create mechanics provider
cat > src/inference/mechanics.ts << 'EOF'
import { OpenAI } from 'openai';
import type { Message, Tool, Response } from '../types';

export class MechanicsProvider {
  private client: OpenAI;
  private baseURL: string;
  
  constructor(baseURL: string = 'http://mechanics:8080') {
    this.baseURL = baseURL;
    this.client = new OpenAI({
      baseURL: `${baseURL}/v1`,
      apiKey: 'local-mechanics'
    });
  }
  
  async generate(messages: Message[], tools?: Tool[]): Promise<Response> {
    const stream = await this.client.chat.completions.create({
      model: 'local-mechanics',
      messages: messages.map(m => ({
        role: m.role,
        content: m.content
      })),
      tools: tools?.map(t => ({
        type: 'function',
        function: {
          name: t.name,
          description: t.description,
          parameters: t.parameters
        }
      })),
      stream: true
    });
    
    let content = '';
    for await (const chunk of stream) {
      content += chunk.choices[0]?.delta?.content || '';
    }
    
    return { content, role: 'assistant' };
  }
  
  async health(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}
EOF

# Patch agent.ts to use mechanics
cat > src/core/agent.ts.patch << 'PATCH'
--- a/src/core/agent.ts
+++ b/src/core/agent.ts
@@ -1,5 +1,5 @@
-import { AnthropicProvider } from '../inference/provider';
+import { MechanicsProvider } from '../inference/mechanics';
 
-const inference = new AnthropicProvider();
+const inference = new MechanicsProvider(
+  process.env.MECHANICS_URL || 'http://mechanics:8080'
+);
PATCH

# Apply patch if patch command available
if command -v patch &> /dev/null; then
  patch -p1 < src/core/agent.ts.patch || echo "⚠ Patch may have already been applied"
else
  echo "⚠ patch command not available, manual update needed"
fi

# Update package.json
echo "📋 Updating dependencies..."
npm install openai --save

# Create .env.example
cat > .env.example << EOF
# Cathedral Gateway Configuration
NODE_ENV=production

# Inference
MECHANICS_URL=${INFERENCE_URL}
INFERENCE_PROVIDER=local-mechanics

# Gateway
GATEWAY_PORT=8080
OPENAI_API_PORT=3000
MEMORY_PATH=./memory

# Channels (enable as needed)
TELEGRAM_TOKEN=
DISCORD_TOKEN=
SLACK_TOKEN=
EOF

echo ""
echo "✓ Fork complete: $WORKDIR/$NAME"
echo ""
echo "Next steps:"
echo "  cd $NAME"
echo "  cp .env.example .env"
echo "  # Edit .env with your tokens"
echo "  npm install"
echo "  npm run build"
echo "  npm start"
