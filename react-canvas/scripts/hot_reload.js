#!/usr/bin/env node
/**
 * hot_reload.js - Watch and auto-reload a component file
 * 
 * Usage: node hot_reload.js <file-path> [options]
 * Options:
 *   --props, -p      JSON string of props (default: {})
 *   --width, -w      Width in pixels (default: 800)
 *   --height, -h     Height in pixels (default: 600)
 *   --output, -o     Output file path for screenshots
 *   --ui-lib, -u     UI library: tailwind|chakra|material-ui
 *   --debounce, -d   Debounce time in ms (default: 500)
 */

const fs = require('fs');
const path = require('path');
const { bundleFromFile, createHTMLWrapper } = require('./lib/bundler');
const { renderToPNG, saveToCanvas } = require('./lib/renderer');

// Simple debounce implementation
function debounce(fn, ms) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    filePath: null,
    props: {},
    width: 800,
    height: 600,
    output: null,
    uiLib: null,
    debounce: 500,
  };

  let filePathFound = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    if (!arg.startsWith('--') && !filePathFound) {
      options.filePath = arg;
      filePathFound = true;
      continue;
    }

    switch (arg) {
      case '--props':
      case '-p':
        try {
          options.props = JSON.parse(next);
        } catch (e) {
          console.error('Invalid props JSON:', e.message);
          process.exit(1);
        }
        i++;
        break;
      case '--width':
      case '-w':
        options.width = parseInt(next, 10);
        i++;
        break;
      case '--height':
      case '-h':
        options.height = parseInt(next, 10);
        i++;
        break;
      case '--output':
      case '-o':
        options.output = next;
        i++;
        break;
      case '--ui-lib':
      case '-u':
        options.uiLib = next;
        i++;
        break;
      case '--debounce':
      case '-d':
        options.debounce = parseInt(next, 10);
        i++;
        break;
    }
  }

  return options;
}

async function renderFile(filePath, options, isReload = false) {
  try {
    if (!isReload) {
      console.error(`📦 Bundling component from ${filePath}...`);
    } else {
      console.error(`🔄 Reloading ${path.basename(filePath)}...`);
    }

    const bundled = await bundleFromFile(filePath, {
      uiLibrary: options.uiLib,
    });

    const html = createHTMLWrapper(bundled, options.props);

    // Save to canvas
    const canvasPath = await saveToCanvas(html, 'react-canvas-hot-reload.html');

    // Render to PNG
    const pngBuffer = await renderToPNG(html, {
      width: options.width,
      height: options.height,
    });

    // Save if output specified
    if (options.output) {
      fs.writeFileSync(options.output, pngBuffer);
      if (!isReload) {
        console.error(`✅ Initial render saved to: ${options.output}`);
      }
    }

    console.error(`📺 Canvas updated: ${canvasPath}`);
    console.error(`📐 ${options.width}x${options.height}px`);

    return true;
  } catch (error) {
    console.error('❌ Render error:', error.message);
    return false;
  }
}

async function run() {
  const options = parseArgs();

  if (!options.filePath) {
    console.error('Error: No file path provided.');
    console.error('');
    console.error('Usage: node hot_reload.js <file-path> [--options]');
    console.error('Example: node hot_reload.js ./components/Button.jsx -w 400 -h 300');
    process.exit(1);
  }

  const fullPath = path.resolve(options.filePath);

  if (!fs.existsSync(fullPath)) {
    console.error(`Error: File not found: ${fullPath}`);
    process.exit(1);
  }

  // Initial render
  await renderFile(fullPath, options, false);

  console.error('');
  console.error('👀 Watching for changes... (Press Ctrl+C to stop)');
  console.error('─────────────────────────────────────────────');

  // Create debounced render function
  const debouncedRender = debounce(async () => {
    await renderFile(fullPath, options, true);
    console.error('─────────────────────────────────────────────');
  }, options.debounce);

  // Watch file
  fs.watchFile(fullPath, { interval: 100 }, async (curr, prev) => {
    if (curr.mtime !== prev.mtime) {
      debouncedRender();
    }
  });

  // Keep process alive
  process.on('SIGINT', () => {
    console.error('\n👋 Stopping watcher...');
    const { closeBrowser } = require('./lib/renderer');
    closeBrowser().then(() => {
      process.exit(0);
    });
  });
}

run();
