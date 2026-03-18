const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

let browser = null;

/**
 * Get or create shared browser instance
 * @returns {Promise<Browser>}
 */
async function getBrowser() {
  if (!browser) {
    browser = await puppeteer.launch({
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
      ],
    });
  }
  return browser;
}

/**
 * Close the shared browser instance
 */
async function closeBrowser() {
  if (browser) {
    await browser.close();
    browser = null;
  }
}

/**
 * Render HTML to PNG screenshot
 * @param {string} html - HTML content
 * @param {Object} options - Rendering options
 * @returns {Promise<Buffer>} - PNG image buffer
 */
async function renderToPNG(html, options = {}) {
  const {
    width = 800,
    height = 600,
    waitFor = 1000, // ms to wait for React to render
    fullPage = false,
  } = options;

  const browser = await getBrowser();
  const page = await browser.newPage();
  
  try {
    await page.setViewport({ width, height });
    await page.setContent(html, { waitUntil: 'networkidle0' });
    
    // Wait for React to render
    await page.waitForTimeout(waitFor);
    
    // Additional wait for any animations
    await page.evaluate(() => {
      return new Promise(resolve => {
        if (document.readyState === 'complete') {
          setTimeout(resolve, 100);
        } else {
          window.addEventListener('load', () => setTimeout(resolve, 100));
        }
      });
    });

    const screenshot = await page.screenshot({
      type: 'png',
      fullPage,
    });

    return screenshot;
  } finally {
    await page.close();
  }
}

/**
 * Render HTML to SVG (via PNG conversion for now)
 * @param {string} html - HTML content
 * @param {Object} options - Rendering options
 * @returns {Promise<Buffer>} - SVG buffer
 */
async function renderToSVG(html, options = {}) {
  // For now, we'll create an SVG that embeds the screenshot as data URI
  // In a more advanced implementation, we could use something like
  // dom-to-svg or similar to get true vector output
  const pngBuffer = await renderToPNG(html, options);
  const dataUri = `data:image/png;base64,${pngBuffer.toString('base64')}`;
  
  const { width = 800, height = 600 } = options;
  
  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <image href="${dataUri}" width="${width}" height="${height}"/>
</svg>`;

  return Buffer.from(svg, 'utf-8');
}

/**
 * Save HTML to file for canvas viewing
 * @param {string} html - HTML content
 * @param {string} filename - Output filename
 * @returns {string} - Path to saved file
 */
async function saveToCanvas(html, filename = null) {
  const canvasRoot = process.env.REACT_CANVAS_ROOT || 
                     path.join(process.env.HOME || '/tmp', 'clawd', 'canvas');
  
  fs.mkdirSync(canvasRoot, { recursive: true });
  
  const outputFile = filename || `react-canvas-${Date.now()}.html`;
  const outputPath = path.join(canvasRoot, outputFile);
  
  fs.writeFileSync(outputPath, html);
  
  return outputPath;
}

module.exports = {
  renderToPNG,
  renderToSVG,
  saveToCanvas,
  closeBrowser,
  getBrowser,
};
