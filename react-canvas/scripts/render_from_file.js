#!/usr/bin/env node
/**
 * render_from_file.js - Render a React component from file
 * 
 * Usage: node render_from_file.js <component-path> [options]
 * Options:
 *   --props, -p      JSON string of props (default: {})
 *   --width, -w      Width in pixels (default: 800)
 *   --height, -h     Height in pixels (default: 600)
 *   --format, -f     Output format: png|svg (default: png)
 *   --output, -o     Output file path (default: stdout)
 *   --ui-lib, -u     UI library: tailwind|chakra|material-ui
 *   --canvas, -C     Also save to canvas for viewing
 */

const { bundleFromFile, createHTMLWrapper } = require('./lib/bundler');
const { renderToPNG, renderToSVG, saveToCanvas } = require('./lib/renderer');
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    filePath: null,
    props: {},
    width: 800,
    height: 600,
    format: 'png',
    output: null,
    uiLib: null,
    canvas: false,
  };

  // First non-flag argument is the file path
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
      case '--format':
      case '-f':
        options.format = next.toLowerCase();
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
      case '--canvas':
      case '-C':
        options.canvas = true;
        break;
    }
  }

  return options;
}

async function run() {
  const options = parseArgs();

  if (!options.filePath) {
    console.error('Error: No component file path provided.');
    console.error('');
    console.error('Usage: node render_from_file.js <component-path> [--options]');
    console.error('Example: node render_from_file.js ./components/Button.jsx --props \'{"text":"Click me"}\'');
    process.exit(1);
  }

  const fullPath = path.resolve(options.filePath);

  if (!fs.existsSync(fullPath)) {
    console.error(`Error: File not found: ${fullPath}`);
    process.exit(1);
  }

  try {
    console.error(`📦 Bundling component from ${options.filePath}...`);
    const bundled = await bundleFromFile(fullPath, {
      uiLibrary: options.uiLib,
    });

    console.error('🎨 Rendering component...');
    const html = createHTMLWrapper(bundled, options.props);

    // Save to canvas if requested
    if (options.canvas) {
      const canvasPath = await saveToCanvas(html, 'react-canvas-file.html');
      console.error(`📺 Canvas file saved: ${canvasPath}`);
    }

    // Render to image
    let buffer;
    if (options.format === 'svg') {
      buffer = await renderToSVG(html, {
        width: options.width,
        height: options.height,
      });
    } else {
      buffer = await renderToPNG(html, {
        width: options.width,
        height: options.height,
      });
    }

    // Output
    if (options.output) {
      fs.writeFileSync(options.output, buffer);
      console.error(`✅ Saved to: ${options.output}`);
      console.log(options.output);
    } else {
      process.stdout.write(buffer);
    }

    // Cleanup
    const { closeBrowser } = require('./lib/renderer');
    await closeBrowser();

  } catch (error) {
    console.error('❌ Error:', error.message);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

run();
