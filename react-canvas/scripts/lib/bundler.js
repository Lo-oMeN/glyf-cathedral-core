const esbuild = require('esbuild');
const fs = require('fs');
const path = require('path');

/**
 * Bundle React component code with esbuild
 * @param {string} jsxCode - The JSX code to bundle
 * @param {Object} options - Bundling options
 * @returns {Promise<string>} - Bundled JavaScript code
 */
async function bundleComponent(jsxCode, options = {}) {
  const {
    uiLibrary = null, // 'tailwind', 'chakra', 'material-ui'
    externalLibs = [],
    minify = true,
  } = options;

  // Create a temporary entry file
  const tmpDir = path.join(process.env.HOME || '/tmp', '.react-canvas', 'tmp');
  fs.mkdirSync(tmpDir, { recursive: true });
  
  const entryFile = path.join(tmpDir, `entry-${Date.now()}.jsx`);
  
  // Build imports based on UI library
  let imports = '';
  let wrapperStart = '';
  let wrapperEnd = '';
  
  if (uiLibrary === 'tailwind') {
    imports = `import 'tailwindcss/tailwind.css';\n`;
  } else if (uiLibrary === 'chakra') {
    imports = `
import { ChakraProvider } from '@chakra-ui/react';
`;
    wrapperStart = '<ChakraProvider>';
    wrapperEnd = '</ChakraProvider>';
  } else if (uiLibrary === 'material-ui') {
    imports = `
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
const theme = createTheme();
`;
    wrapperStart = '<ThemeProvider theme={theme}><CssBaseline />';
    wrapperEnd = '</ThemeProvider>';
  }

  // Write entry file
  const entryCode = `
import React from 'react';
import ReactDOM from 'react-dom/client';
${imports}

// User component
const UserComponent = () => {
  ${jsxCode.includes('=>') || jsxCode.includes('function') ? '' : 'return ('}
  ${jsxCode}
  ${jsxCode.includes('=>') || jsxCode.includes('function') ? '' : ')'}
};

// Render
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    ${wrapperStart}
    <UserComponent />
    ${wrapperEnd}
  </React.StrictMode>
);
`;

  fs.writeFileSync(entryFile, entryCode);

  try {
    // Bundle with esbuild
    const result = await esbuild.build({
      entryPoints: [entryFile],
      bundle: true,
      write: false,
      minify,
      target: 'es2020',
      jsx: 'automatic',
      platform: 'browser',
      external: externalLibs,
      define: {
        'process.env.NODE_ENV': '"production"',
      },
    });

    const bundledCode = result.outputFiles[0].text;
    
    // Cleanup
    fs.unlinkSync(entryFile);
    
    return bundledCode;
  } catch (error) {
    // Cleanup on error
    try { fs.unlinkSync(entryFile); } catch {}
    throw error;
  }
}

/**
 * Bundle a component from a file path
 * @param {string} filePath - Path to the component file
 * @param {Object} options - Bundling options
 * @returns {Promise<string>} - Bundled JavaScript code
 */
async function bundleFromFile(filePath, options = {}) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Component file not found: ${filePath}`);
  }

  const jsxCode = fs.readFileSync(filePath, 'utf-8');
  return bundleComponent(jsxCode, options);
}

/**
 * Create HTML wrapper for the bundled code
 * @param {string} bundledCode - The bundled JavaScript
 * @param {Object} props - Props to pass to the component
 * @returns {string} - Complete HTML document
 */
function createHTMLWrapper(bundledCode, props = {}) {
  const propsScript = `<script>window.__REACT_CANVAS_PROPS__ = ${JSON.stringify(props)};</script>`;
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React Canvas</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        #root { width: 100%; height: 100%; }
    </style>
    ${propsScript}
</head>
<body>
    <div id="root"></div>
    <script>${bundledCode}</script>
</body>
</html>`;
}

module.exports = {
  bundleComponent,
  bundleFromFile,
  createHTMLWrapper,
};
