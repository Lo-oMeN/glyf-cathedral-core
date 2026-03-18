#!/usr/bin/env node
/**
 * compare_versions.js - Compare two component versions visually
 * 
 * Usage: node compare_versions.js <v1> <v2> [options]
 * Options:
 *   --output, -o     Output file path for diff image
 *   --format, -f     Output format: side-by-side|overlay|diff (default: side-by-side)
 *   --width, -w      Width in pixels (default: 800)
 *   --height, -h     Height in pixels (default: 600)
 */

const fs = require('fs');
const path = require('path');
const { bundleComponent, bundleFromFile, createHTMLWrapper } = require('./lib/bundler');
const { renderToPNG, getBrowser } = require('./lib/renderer');
const { createCanvas, loadImage } = require('canvas');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    v1: null,
    v2: null,
    output: null,
    format: 'side-by-side', // side-by-side, overlay, diff
    width: 800,
    height: 600,
  };

  // First two non-flag arguments are v1 and v2
  const paths = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    if (!arg.startsWith('--')) {
      if (paths.length < 2) {
        paths.push(arg);
      }
      continue;
    }

    switch (arg) {
      case '--output':
      case '-o':
        options.output = next;
        i++;
        break;
      case '--format':
      case '-f':
        options.format = next;
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
    }
  }

  if (paths.length >= 2) {
    options.v1 = paths[0];
    options.v2 = paths[1];
  }

  return options;
}

async function loadComponentCode(source) {
  // Check if it's a file path
  if (fs.existsSync(path.resolve(source))) {
    return bundleFromFile(source);
  }
  // Otherwise treat as raw JSX code
  return bundleComponent(source);
}

async function renderComponentToBuffer(code, width, height) {
  const html = createHTMLWrapper(code);
  return renderToPNG(html, { width, height });
}

async function createSideBySide(img1Buffer, img2Buffer, width, height) {
  const canvas = createCanvas(width * 2 + 20, height + 60);
  const ctx = canvas.getContext('2d');

  // Background
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Labels
  ctx.fillStyle = '#333';
  ctx.font = 'bold 16px sans-serif';
  ctx.fillText('Version 1', 10, 25);
  ctx.fillText('Version 2', width + 30, 25);

  // Load and draw images
  const img1 = await loadImage(img1Buffer);
  const img2 = await loadImage(img2Buffer);

  // Draw frames
  ctx.strokeStyle = '#ddd';
  ctx.lineWidth = 2;
  ctx.strokeRect(10, 40, width, height);
  ctx.strokeRect(width + 30, 40, width, height);

  // Draw images
  ctx.drawImage(img1, 10, 40, width, height);
  ctx.drawImage(img2, width + 30, 40, width, height);

  return canvas.toBuffer('image/png');
}

async function createOverlay(img1Buffer, img2Buffer, width, height) {
  const canvas = createCanvas(width + 20, height + 60);
  const ctx = canvas.getContext('2d');

  // Background
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Label
  ctx.fillStyle = '#333';
  ctx.font = 'bold 16px sans-serif';
  ctx.fillText('Overlay (50% opacity each)', 10, 25);

  // Load and draw images
  const img1 = await loadImage(img1Buffer);
  const img2 = await loadImage(img2Buffer);

  // Draw frame
  ctx.strokeStyle = '#ddd';
  ctx.lineWidth = 2;
  ctx.strokeRect(10, 40, width, height);

  // Draw first image
  ctx.globalAlpha = 0.5;
  ctx.drawImage(img1, 10, 40, width, height);

  // Draw second image
  ctx.drawImage(img2, 10, 40, width, height);

  // Reset alpha
  ctx.globalAlpha = 1.0;

  return canvas.toBuffer('image/png');
}

async function createDiff(img1Buffer, img2Buffer, width, height) {
  const canvas = createCanvas(width + 20, height + 60);
  const ctx = canvas.getContext('2d');

  // Background
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Label
  ctx.fillStyle = '#333';
  ctx.font = 'bold 16px sans-serif';
  ctx.fillText('Difference (red = changed)', 10, 25);

  // Create temporary canvas for pixel manipulation
  const tempCanvas = createCanvas(width, height);
  const tempCtx = tempCanvas.getContext('2d');

  // Load images
  const img1 = await loadImage(img1Buffer);
  const img2 = await loadImage(img2Buffer);

  // Draw first image and get data
  tempCtx.drawImage(img1, 0, 0, width, height);
  const data1 = tempCtx.getImageData(0, 0, width, height);

  // Draw second image and get data
  tempCtx.clearRect(0, 0, width, height);
  tempCtx.drawImage(img2, 0, 0, width, height);
  const data2 = tempCtx.getImageData(0, 0, width, height);

  // Create diff image
  const diffData = tempCtx.createImageData(width, height);
  let diffCount = 0;

  for (let i = 0; i < data1.data.length; i += 4) {
    const r1 = data1.data[i];
    const g1 = data1.data[i + 1];
    const b1 = data1.data[i + 2];
    const a1 = data1.data[i + 3];

    const r2 = data2.data[i];
    const g2 = data2.data[i + 1];
    const b2 = data2.data[i + 2];
    const a2 = data2.data[i + 3];

    // Check if pixels differ
    const threshold = 10;
    if (Math.abs(r1 - r2) > threshold ||
        Math.abs(g1 - g2) > threshold ||
        Math.abs(b1 - b2) > threshold ||
        Math.abs(a1 - a2) > threshold) {
      // Mark as changed (red)
      diffData.data[i] = 255;     // R
      diffData.data[i + 1] = 0;   // G
      diffData.data[i + 2] = 0;   // B
      diffData.data[i + 3] = 200; // A
      diffCount++;
    } else {
      // Semi-transparent original
      diffData.data[i] = r1;
      diffData.data[i + 1] = g1;
      diffData.data[i + 2] = b1;
      diffData.data[i + 3] = 30;
    }
  }

  // Draw diff
  tempCtx.putImageData(diffData, 0, 0);

  // Draw frame
  ctx.strokeStyle = '#ddd';
  ctx.lineWidth = 2;
  ctx.strokeRect(10, 40, width, height);

  // Draw diff image
  ctx.drawImage(tempCanvas, 10, 40);

  // Add stats
  const totalPixels = width * height;
  const diffPercent = ((diffCount / totalPixels) * 100).toFixed(2);
  ctx.fillStyle = '#666';
  ctx.font = '12px sans-serif';
  ctx.fillText(`Changed pixels: ${diffPercent}%`, 10, height + 55);

  return canvas.toBuffer('image/png');
}

async function run() {
  const options = parseArgs();

  if (!options.v1 || !options.v2) {
    console.error('Error: Two component sources required.');
    console.error('');
    console.error('Usage: node compare_versions.js <v1> <v2> [--options]');
    console.error('');
    console.error('Examples:');
    console.error('  # Compare two files');
    console.error('  node compare_versions.js ./Button-v1.jsx ./Button-v2.jsx');
    console.error('');
    console.error('  # Compare file with inline code');
    console.error('  node compare_versions.js ./Button.jsx "<div>New Button</div>"');
    console.error('');
    console.error('  # Output diff image');
    console.error('  node compare_versions.js v1.jsx v2.jsx -o diff.png --format diff');
    process.exit(1);
  }

  try {
    console.error('📦 Bundling version 1...');
    const code1 = await loadComponentCode(options.v1);

    console.error('📦 Bundling version 2...');
    const code2 = await loadComponentCode(options.v2);

    console.error('🎨 Rendering version 1...');
    const img1Buffer = await renderComponentToBuffer(code1, options.width, options.height);

    console.error('🎨 Rendering version 2...');
    const img2Buffer = await renderComponentToBuffer(code2, options.width, options.height);

    console.error(`🔍 Creating ${options.format} comparison...`);

    let resultBuffer;
    switch (options.format) {
      case 'overlay':
        resultBuffer = await createOverlay(img1Buffer, img2Buffer, options.width, options.height);
        break;
      case 'diff':
        resultBuffer = await createDiff(img1Buffer, img2Buffer, options.width, options.height);
        break;
      case 'side-by-side':
      default:
        resultBuffer = await createSideBySide(img1Buffer, img2Buffer, options.width, options.height);
        break;
    }

    // Output
    if (options.output) {
      fs.writeFileSync(options.output, resultBuffer);
      console.error(`✅ Comparison saved to: ${options.output}`);
      console.log(options.output);
    } else {
      const tmpPath = path.join('/tmp', `compare-${Date.now()}.png`);
      fs.writeFileSync(tmpPath, resultBuffer);
      console.error(`✅ Comparison saved to: ${tmpPath}`);
      console.log(tmpPath);
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
