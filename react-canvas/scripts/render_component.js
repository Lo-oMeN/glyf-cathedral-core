#!/usr/bin/env node
/**
 * render_component.js - Render JSX code to PNG/SVG
 * 
 * Usage: node render_component.js [options]
 * Options:
 *   --code, -c       JSX code string (required)
 *   --props, -p      JSON string of props (default: {})
 *   --width, -w      Width in pixels (default: 800)
 *   --height, -h     Height in pixels (default: 600)
 *   --format, -f     Output format: png|svg (default: png)
 *   --output, -o     Output file path (default: stdout)
 *   --ui-lib, -u     UI library: tailwind|chakra|material-ui
 *   --canvas, -C     Also save to canvas for viewing
 *   --minify, -m     Minify output (default: true)
 */

const { bundleComponent, createHTMLWrapper } = require('./lib/bundler');
const { renderToPNG, renderToSVG, saveToCanvas } = require('./lib/renderer');
const fs = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    code: '',
    props: {},
    width: 800,
    height: 600,
    format: 'png',
    output: null,
    uiLib: null,
    canvas: false,
    minify: true,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    switch (arg) {
      case '--code':
      case '-c':
        options.code = next;
        i++;
        break;
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
      case '--no-minify':
        options.minify = false;
        break;
    }
  }

  // Check for code from stdin if not provided
  if (!options.code && process.stdin.isTTY === undefined) {
    // Read from stdin
    const chunks = [];
    process.stdin.on('data', chunk => chunks.push(chunk));
    process.stdin.on('end', () => {
      options.code = Buffer.concat(chunks).toString('utf-8');
      run(options);
    });
    return null;
  }

  return options;
}

async function run(options) {
  if (!options) return;

  if (!options.code) {
    console.error('Error: No JSX code provided. Use --code or pipe via stdin.');
    console.error('');
    console.error('Usage: node render_component.js --code "<div>Hello</div>" [--options]');
    console.error('       echo "<div>Hello</div>" | node render_component.js [--options]');
    process.exit(1);
  }

  try {
    console.error('📦 Bundling component...');
    const bundled = await bundleComponent(options.code, {
      uiLibrary: options.uiLib,
      minify: options.minify,
    });

    console.error('🎨 Rendering component...');
    const html = createHTMLWrapper(bundled, options.props);

    // Save to canvas if requested
    if (options.canvas) {
      const canvasPath = await saveToCanvas(html, 'react-canvas-render.html');
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
      console.log(options.output); // For piping
    } else {
      // Write binary to stdout
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

// Main
const options = parseArgs();
if (options) {
  run(options);
}
