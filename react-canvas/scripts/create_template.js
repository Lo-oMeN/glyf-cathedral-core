#!/usr/bin/env node
/**
 * create_template.js - Scaffold a new React component
 * 
 * Usage: node create_template.js <name> [options]
 * Options:
 *   --template, -t   Template type: functional|class|arrow (default: functional)
 *   --output, -o     Output directory (default: ./components)
 *   --ui-lib, -u     UI library: tailwind|chakra|material-ui|none (default: none)
 *   --props, -p      Comma-separated prop names
 *   --overwrite, -f  Overwrite existing file
 */

const fs = require('fs');
const path = require('path');

const TEMPLATES = {
  functional: (name, props, uiLib) => {
    const propList = props.map(p => `${p}`).join(', ');
    const propDestructure = props.length > 0 ? `{ ${propList} }` : '';
    
    let uiImports = '';
    let uiUsage = '';
    
    if (uiLib === 'tailwind') {
      uiUsage = `className="p-4 bg-white rounded shadow"`;
    } else if (uiLib === 'chakra') {
      uiImports = `import { Box } from '@chakra-ui/react';\n`;
      uiUsage = `as={Box} p={4} bg="white" boxShadow="md" borderRadius="md"`;
    } else if (uiLib === 'material-ui') {
      uiImports = `import { Paper } from '@mui/material';\n`;
      uiUsage = `component={Paper} elevation={2} sx={{ p: 2 }}`;
    }

    return `import React from 'react';
${uiImports}
/**
 * ${name} Component
 * 
 * @description Add your component description here
 * @param {Object} props - Component props
 * @returns {JSX.Element}
 */
const ${name} = ${propDestructure ? `(${propDestructure})` : '()'} => {
  return (
    <div ${uiUsage}>
      <h2>${name} Component</h2>
      ${props.map(p => `<p>${p}: {${p}}</p>`).join('\n      ') || '<p>Edit this component to add your content.</p>'}
    </div>
  );
};

export default ${name};
`;
  },

  class: (name, props, uiLib) => {
    const propList = props.map(p => `${p}`).join(', ');
    
    let uiImports = '';
    let uiUsage = '';
    
    if (uiLib === 'tailwind') {
      uiUsage = `className="p-4 bg-white rounded shadow"`;
    } else if (uiLib === 'chakra') {
      uiImports = `import { Box } from '@chakra-ui/react';\n`;
      uiUsage = `as={Box} p={4} bg="white" boxShadow="md" borderRadius="md"`;
    } else if (uiLib === 'material-ui') {
      uiImports = `import { Paper } from '@mui/material';\n`;
      uiUsage = `component={Paper} elevation={2} sx={{ p: 2 }}`;
    }

    return `import React, { Component } from 'react';
${uiImports}
/**
 * ${name} Component
 * 
 * @description Add your component description here
 */
class ${name} extends Component {
  constructor(props) {
    super(props);
    ${props.length > 0 ? '' : '// '}this.state = {
    ${props.map(p => `  ${p}: props.${p} || '',`).join('\n    ')}
    ${props.length > 0 ? '' : '// '}};
  }

  render() {
    ${props.length > 0 ? `const { ${propList} } = this.props;` : ''}
    return (
      <div ${uiUsage}>
        <h2>${name} Component</h2>
        ${props.map(p => `<p>${p}: {${p}}</p>`).join('\n        ') || '<p>Edit this component to add your content.</p>'}
      </div>
    );
  }
}

export default ${name};
`;
  },

  arrow: (name, props, uiLib) => {
    const propList = props.map(p => `${p}`).join(', ');
    const propDestructure = props.length > 0 ? `{ ${propList} }` : '';
    
    let uiImports = '';
    let uiUsage = '';
    
    if (uiLib === 'tailwind') {
      uiUsage = `className="p-4 bg-white rounded shadow"`;
    } else if (uiLib === 'chakra') {
      uiImports = `import { Box } from '@chakra-ui/react';\n`;
      uiUsage = `as={Box} p={4} bg="white" boxShadow="md" borderRadius="md"`;
    } else if (uiLib === 'material-ui') {
      uiImports = `import { Paper } from '@mui/material';\n`;
      uiUsage = `component={Paper} elevation={2} sx={{ p: 2 }}`;
    }

    return `import React from 'react';
${uiImports}
/**
 * ${name} Component
 * 
 * @description Add your component description here
 * @param {Object} props - Component props
 * @returns {JSX.Element}
 */
const ${name} = ${propDestructure ? `(${propDestructure})` : '()'} => (
  <div ${uiUsage}>
    <h2>${name} Component</h2>
    ${props.map(p => `<p>${p}: {${p}}</p>`).join('\n    ') || '<p>Edit this component to add your content.</p>'}
  </div>
);

export default ${name};
`;
  },
};

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    name: null,
    template: 'functional',
    output: './components',
    uiLib: 'none',
    props: [],
    overwrite: false,
  };

  let nameFound = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    if (!arg.startsWith('--') && !nameFound) {
      options.name = arg;
      nameFound = true;
      continue;
    }

    switch (arg) {
      case '--template':
      case '-t':
        options.template = next;
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
      case '--props':
      case '-p':
        options.props = next.split(',').map(s => s.trim()).filter(Boolean);
        i++;
        break;
      case '--overwrite':
      case '-f':
        options.overwrite = true;
        break;
    }
  }

  return options;
}

function toPascalCase(str) {
  return str
    .replace(/[-_](.)/g, (_, char) => char.toUpperCase())
    .replace(/^(.)/, (_, char) => char.toUpperCase());
}

async function run() {
  const options = parseArgs();

  if (!options.name) {
    console.error('Error: No component name provided.');
    console.error('');
    console.error('Usage: node create_template.js <name> [--options]');
    console.error('Example: node create_template.js Button --props text,onClick --ui-lib tailwind');
    process.exit(1);
  }

  const componentName = toPascalCase(options.name);
  const templateFn = TEMPLATES[options.template];

  if (!templateFn) {
    console.error(`Error: Unknown template "${options.template}".`);
    console.error(`Available templates: ${Object.keys(TEMPLATES).join(', ')}`);
    process.exit(1);
  }

  // Create output directory
  const outputDir = path.resolve(options.output);
  fs.mkdirSync(outputDir, { recursive: true });

  // Generate component
  const componentCode = templateFn(componentName, options.props, options.uiLib);
  const fileName = `${componentName}.jsx`;
  const filePath = path.join(outputDir, fileName);

  // Check if file exists
  if (fs.existsSync(filePath) && !options.overwrite) {
    console.error(`Error: File already exists: ${filePath}`);
    console.error('Use --overwrite to replace it.');
    process.exit(1);
  }

  // Write file
  fs.writeFileSync(filePath, componentCode);

  console.log(`✅ Created component: ${filePath}`);
  console.log(`   Template: ${options.template}`);
  console.log(`   UI Library: ${options.uiLib}`);
  if (options.props.length > 0) {
    console.log(`   Props: ${options.props.join(', ')}`);
  }
}

run();
