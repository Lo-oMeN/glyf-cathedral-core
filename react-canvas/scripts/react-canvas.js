#!/usr/bin/env node
/**
 * react-canvas-wrapper.js - Main OpenClaw skill wrapper
 * 
 * This script provides a unified interface for all react-canvas operations.
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const SCRIPTS_DIR = __dirname;

function showHelp() {
  console.log(`
React Canvas - Render React components to images

Usage: react-canvas <command> [options]

Commands:
  render <code>              Render JSX code to PNG/SVG
  render-file <path>        Render component from file
  template <name>           Create a new component template
  hot-reload <path>         Watch and auto-reload a component
  compare <v1> <v2>          Compare two component versions

Global Options:
  --width, -w     Output width in pixels (default: 800)
  --height, -h    Output height in pixels (default: 600)
  --output, -o    Output file path
  --format, -f    Output format: png|svg (default: png)
  --ui-lib, -u    UI library: tailwind|chakra|material-ui
  --help          Show this help message

Examples:
  # Render simple JSX
  react-canvas render "<div>Hello World</div>" -o hello.png

  # Render with props and custom size
  react-canvas render "<Button text={text} />" \\
    -p '{"text":"Click me"}' -w 400 -h 200

  # Render from file
  react-canvas render-file ./components/Button.jsx -o button.png

  # Create a new component template
  react-canvas template MyComponent -t functional -p title,description

  # Hot reload a component
  react-canvas hot-reload ./components/Chart.jsx -w 1200 -h 800

  # Compare two versions
  react-canvas compare ./Button-v1.jsx ./Button-v2.jsx -o diff.png
`);
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }

  const command = args[0];
  const remainingArgs = args.slice(1);

  let scriptPath;
  
  switch (command) {
    case 'render':
      scriptPath = path.join(SCRIPTS_DIR, 'render_component.js');
      // If code is provided directly, pass it with --code flag
      if (remainingArgs.length > 0 && !remainingArgs[0].startsWith('-')) {
        remainingArgs.unshift('--code');
      }
      break;
    case 'render-file':
      scriptPath = path.join(SCRIPTS_DIR, 'render_from_file.js');
      break;
    case 'template':
      scriptPath = path.join(SCRIPTS_DIR, 'create_template.js');
      break;
    case 'hot-reload':
      scriptPath = path.join(SCRIPTS_DIR, 'hot_reload.js');
      break;
    case 'compare':
      scriptPath = path.join(SCRIPTS_DIR, 'compare_versions.js');
      break;
    default:
      console.error(`Unknown command: ${command}`);
      showHelp();
      process.exit(1);
  }

  if (!fs.existsSync(scriptPath)) {
    console.error(`Script not found: ${scriptPath}`);
    process.exit(1);
  }

  // Execute the script with remaining args
  const nodePath = process.execPath;
  const cmd = `${nodePath} ${scriptPath} ${remainingArgs.map(a => `"${a}"`).join(' ')}`;
  
  try {
    execSync(cmd, { stdio: 'inherit' });
  } catch (error) {
    // Script exit error, already handled by child process
    process.exit(error.status || 1);
  }
}

main();
