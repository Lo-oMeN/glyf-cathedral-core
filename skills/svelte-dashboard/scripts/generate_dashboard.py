#!/usr/bin/env python3
"""
Generate a new Svelte dashboard from the cathedral template.

Usage:
    python generate_dashboard.py --name my-dashboard --output ./my-dashboard
"""

import argparse
import shutil
import os
from pathlib import Path

def generate_dashboard(name: str, output_dir: str):
    """Create a new dashboard from the template."""
    
    template_dir = Path(__file__).parent.parent / 'assets' / 'template'
    output_path = Path(output_dir)
    
    if not template_dir.exists():
        print(f"❌ Template not found: {template_dir}")
        print("Creating minimal template...")
        create_minimal_template(output_path, name)
        return
    
    # Copy template
    shutil.copytree(template_dir, output_path, ignore=shutil.ignore_patterns('node_modules', '.svelte-kit'))
    
    # Update package.json name
    package_json = output_path / 'package.json'
    if package_json.exists():
        content = package_json.read_text()
        content = content.replace('cathedral-dashboard', name)
        package_json.write_text(content)
    
    print(f"✓ Created dashboard: {output_path}")
    print(f"  Name: {name}")
    print("")
    print("Next steps:")
    print(f"  cd {output_dir}")
    print("  npm install")
    print("  npm run dev")

def create_minimal_template(output_path: Path, name: str):
    """Create a minimal dashboard structure."""
    output_path.mkdir(parents=True, exist_ok=True)
    
    # package.json
    (output_path / 'package.json').write_text(f'''{{
  "name": "{name}",
  "version": "0.1.0",
  "type": "module",
  "scripts": {{
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "devDependencies": {{
    "@sveltejs/adapter-static": "^3.0.0",
    "@sveltejs/kit": "^2.0.0",
    "svelte": "^4.0.0",
    "vite": "^5.0.0"
  }}
}}''')
    
    # src/app.html
    src = output_path / 'src'
    src.mkdir(exist_ok=True)
    (src / 'app.html').write_text('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width" />
  %sveltekit.head%
</head>
<body data-sveltekit-preload-data="hover">
  <div style="display: contents">%sveltekit.body%</div>
</body>
</html>''')
    
    # src/routes/+page.svelte
    routes = src / 'routes'
    routes.mkdir(exist_ok=True)
    (routes / '+page.svelte').write_text('''<script>
  let status = { mechanics: 'unknown', gateway: 'unknown' };
  
  async function checkHealth() {
    try {
      const res = await fetch('/api/status');
      status = await res.json();
    } catch (e) {
      status = { mechanics: 'error', gateway: 'error' };
    }
  }
  
  checkHealth();
</script>

<main>
  <h1>Cathedral Dashboard</h1>
  
  <div class="status">
    <p>Mechanics: {status.mechanics}</p>
    <p>Gateway: {status.gateway}</p>
  </div>
  
  <button on:click={checkHealth}>Refresh</button>
</main>

<style>
  :global(body) {
    background: #0a0a0a;
    color: #e0e0e0;
    font-family: system-ui, sans-serif;
  }
  
  main {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  h1 {
    color: #FFD700;
  }
</style>''')
    
    # svelte.config.js
    (output_path / 'svelte.config.js').write_text('''import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    adapter: adapter({
      fallback: 'index.html'
    })
  }
};''')
    
    # vite.config.js
    (output_path / 'vite.config.js').write_text('''import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()]
});''')
    
    print(f"✓ Created minimal dashboard: {output_path}")
    print(f"  Name: {name}")
    print("")
    print("Next steps:")
    print(f"  cd {output_path}")
    print("  npm install")
    print("  npm run dev")

def main():
    parser = argparse.ArgumentParser(description='Generate cathedral dashboard')
    parser.add_argument('--name', default='my-dashboard', help='Dashboard name')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    
    args = parser.parse_args()
    generate_dashboard(args.name, args.output)

if __name__ == '__main__':
    main()
