#!/usr/bin/env python3
"""
DOCX Engine - Unified CLI wrapper
Usage: python3 docx_engine_cli.py <command> [options]

Commands:
  template    Create document from template
  create      Create document from content blocks
  merge       Mail merge - bulk generation
  style       Apply styling to document
  pdf         Convert to PDF
  extract     Extract text from document
  test        Run test suite
"""

import sys
import os
import subprocess

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')


def show_help():
    print(__doc__)
    print("\nExamples:")
    print("  python3 docx_engine_cli.py template template.docx data.json output.docx")
    print("  python3 docx_engine_cli.py create config.json output.docx")
    print("  python3 docx_engine_cli.py merge template.docx data.csv output_dir/")
    print("  python3 docx_engine_cli.py style input.docx styles.json output.docx")
    print("  python3 docx_engine_cli.py pdf input.docx output.pdf")
    print("  python3 docx_engine_cli.py extract input.docx --output text.txt")


def run_script(script_name, args):
    """Run a script with arguments."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    cmd = [sys.executable, script_path] + args
    result = subprocess.run(cmd)
    return result.returncode


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'template':
        sys.exit(run_script('create_from_template.py', args))
    
    elif command == 'create':
        sys.exit(run_script('create_document.py', args))
    
    elif command == 'merge':
        sys.exit(run_script('mail_merge.py', args))
    
    elif command == 'style':
        sys.exit(run_script('add_styling.py', args))
    
    elif command == 'pdf':
        sys.exit(run_script('convert_to_pdf.py', args))
    
    elif command == 'extract':
        sys.exit(run_script('extract_text.py', args))
    
    elif command == 'test':
        result = subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, 'test_docx_engine.py')])
        sys.exit(result.returncode)
    
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
