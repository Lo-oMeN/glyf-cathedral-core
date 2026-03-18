#!/usr/bin/env python3
"""
CI/CD Pipeline Automation Module
Supports GitHub Actions and GitLab CI
"""

import os
import sys
import yaml
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from urllib.parse import urlparse

# Try to import PyGithub
try:
    from github import Github, GithubException, UnknownObjectException
    from github.WorkflowRun import WorkflowRun
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    print("Warning: PyGithub not installed. GitHub operations will not work.")

class WorkflowValidator:
    """Validates CI/CD workflow files for syntax and best practices"""
    
    GITHUB_ACTIONS_SCHEMA = {
        'required_top_level': ['name', 'on'],
        'valid_event_types': [
            'push', 'pull_request', 'pull_request_target', 'workflow_dispatch',
            'schedule', 'release', 'issues', 'issue_comment', 'discussion',
            'workflow_call', 'workflow_run'
        ],
        'valid_job_keys': ['runs-on', 'steps', 'needs', 'if', 'strategy', 
                          'env', 'outputs', 'defaults', 'concurrency', 'permissions'],
        'valid_step_keys': ['name', 'uses', 'run', 'with', 'env', 'if', 'working-directory', 'shell', 'id']
    }
    
    GITLAB_CI_SCHEMA = {
        'required_global': [],
        'valid_job_keys': ['script', 'image', 'services', 'before_script', 'after_script',
                          'variables', 'cache', 'artifacts', 'dependencies', 'needs',
                          'rules', 'only', 'except', 'when', 'allow_failure', 'timeout',
                          'parallel', 'trigger', 'inherit', 'interruptible', 'retry',
                          'tags', 'coverage', 'environment', 'release', 'pages',
                          'id_tokens', 'secrets'],
        'valid_stage_names': ['build', 'test', 'deploy', 'verify', 'package', 'release']
    }
    
    @staticmethod
    def detect_workflow_type(file_path: str) -> str:
        """Detect if workflow is GitHub Actions or GitLab CI"""
        path = Path(file_path)
        
        # GitHub Actions detection
        if '.github/workflows/' in str(path):
            return 'github_actions'
        if path.name.endswith('.yml') or path.name.endswith('.yaml'):
            content = path.read_text()
            if 'jobs:' in content and 'on:' in content:
                return 'github_actions'
        
        # GitLab CI detection
        if path.name == '.gitlab-ci.yml' or path.name == '.gitlab-ci.yaml':
            return 'gitlab_ci'
        if path.name.endswith('.yml') or path.name.endswith('.yaml'):
            content = path.read_text()
            if 'stages:' in content and 'script:' in content:
                return 'gitlab_ci'
        
        return 'unknown'
    
    @classmethod
    def validate_workflow(cls, file_path: str) -> Dict[str, Any]:
        """Validate a workflow file for syntax and best practices"""
        path = Path(file_path)
        
        if not path.exists():
            return {'valid': False, 'errors': [f'File not found: {file_path}']}
        
        workflow_type = cls.detect_workflow_type(file_path)
        
        if workflow_type == 'github_actions':
            return cls._validate_github_actions(path)
        elif workflow_type == 'gitlab_ci':
            return cls._validate_gitlab_ci(path)
        else:
            return {'valid': False, 'errors': ['Unknown workflow type']}
    
    @classmethod
    def _validate_github_actions(cls, path: Path) -> Dict[str, Any]:
        """Validate GitHub Actions workflow"""
        errors = []
        warnings = []
        suggestions = []
        
        # Parse YAML
        try:
            with open(path, 'r') as f:
                content = f.read()
                workflow = yaml.safe_load(content)
        except yaml.YAMLError as e:
            return {'valid': False, 'errors': [f'YAML syntax error: {str(e)}']}
        
        if not workflow:
            return {'valid': False, 'errors': ['Empty workflow file']}
        
        # Check required fields
        if 'name' not in workflow:
            warnings.append('Missing "name" field - recommended for identification')
        
        if 'on' not in workflow and True not in workflow:
            errors.append('Missing "on" trigger definition')
        
        # Validate triggers
        triggers = workflow.get('on', workflow.get(True, {}))
        if isinstance(triggers, list):
            for trigger in triggers:
                if trigger not in cls.GITHUB_ACTIONS_SCHEMA['valid_event_types']:
                    warnings.append(f'Uncommon event type: {trigger}')
        elif isinstance(triggers, dict):
            for trigger in triggers.keys():
                if trigger not in cls.GITHUB_ACTIONS_SCHEMA['valid_event_types']:
                    warnings.append(f'Uncommon event type: {trigger}')
        
        # Validate jobs
        jobs = workflow.get('jobs', {})
        if not jobs:
            errors.append('No jobs defined')
        
        for job_name, job_config in jobs.items():
            if 'runs-on' not in job_config:
                errors.append(f'Job "{job_name}" missing "runs-on" runner specification')
            
            if 'steps' not in job_config:
                errors.append(f'Job "{job_name}" missing "steps"')
            else:
                steps = job_config['steps']
                for i, step in enumerate(steps):
                    if isinstance(step, dict):
                        if 'uses' not in step and 'run' not in step:
                            errors.append(f'Job "{job_name}", step {i+1}: Must have "uses" or "run"')
                        if 'uses' in step:
                            action_ref = step['uses']
                            # Check for unpinned actions
                            if '@' in action_ref and not re.search(r'@[a-f0-9]{40}$', action_ref):
                                if not re.search(r'@v\d+\.\d+\.\d+$', action_ref):
                                    warnings.append(f'Job "{job_name}", step {i+1}: Action not pinned to SHA or semantic version')
        
        # Security best practices
        if 'pull_request_target' in str(triggers):
            warnings.append('Using "pull_request_target" - ensure proper security checks are in place')
        
        if 'secrets.GITHUB_TOKEN' in content and 'permissions:' not in content:
            suggestions.append('Consider adding explicit permissions for GITHUB_TOKEN')
        
        return {
            'valid': len(errors) == 0,
            'workflow_type': 'github_actions',
            'errors': errors,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    @classmethod
    def _validate_gitlab_ci(cls, path: Path) -> Dict[str, Any]:
        """Validate GitLab CI configuration"""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            with open(path, 'r') as f:
                content = f.read()
                config = yaml.safe_load(content)
        except yaml.YAMLError as e:
            return {'valid': False, 'errors': [f'YAML syntax error: {str(e)}']}
        
        if not config:
            return {'valid': False, 'errors': ['Empty configuration file']}
        
        # Check for stages
        stages = config.get('stages', [])
        if not stages:
            suggestions.append('No stages defined - using default stages')
        
        # Validate jobs
        reserved_keys = ['stages', 'variables', 'workflow', 'include', 'default', 'cache']
        jobs_found = False
        
        for key, value in config.items():
            if key not in reserved_keys and isinstance(value, dict):
                jobs_found = True
                job_config = value
                
                if 'script' not in job_config:
                    errors.append(f'Job "{key}" missing required "script" field')
                
                # Check for deprecated keywords
                if 'only' in job_config or 'except' in job_config:
                    suggestions.append(f'Job "{key}": Consider using "rules" instead of "only/except"')
        
        if not jobs_found:
            errors.append('No jobs defined in configuration')
        
        return {
            'valid': len(errors) == 0,
            'workflow_type': 'gitlab_ci',
            'errors': errors,
            'warnings': warnings,
            'suggestions': suggestions
        }


class WorkflowGenerator:
    """Generate CI/CD workflow files from templates"""
    
    TEMPLATES = {
        'python': {
            'github_actions': {
                'name': 'Python CI',
                'on': {'push': {'branches': ['main']}, 'pull_request': {'branches': ['main']}},
                'jobs': {
                    'test': {
                        'runs-on': 'ubuntu-latest',
                        'strategy': {'matrix': {'python-version': ['3.9', '3.10', '3.11']}},
                        'steps': [
                            {'uses': 'actions/checkout@v4'},
                            {'name': 'Set up Python', 'uses': 'actions/setup-python@v5', 
                             'with': {'python-version': '${{ matrix.python-version }}'}},
                            {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt || pip install .'},
                            {'name': 'Run tests', 'run': 'pytest || python -m pytest'}
                        ]
                    }
                }
            },
            'gitlab_ci': {
                'stages': ['test', 'build', 'deploy'],
                'variables': {'PIP_CACHE_DIR': '$CI_PROJECT_DIR/.cache/pip'},
                'cache': {'paths': ['.cache/pip', 'venv/']},
                'test': {
                    'stage': 'test',
                    'image': 'python:3.11',
                    'script': [
                        'python -m venv venv',
                        'source venv/bin/activate',
                        'pip install -r requirements.txt || pip install .',
                        'pytest || python -m pytest'
                    ]
                }
            }
        },
        'node': {
            'github_actions': {
                'name': 'Node.js CI',
                'on': {'push': {'branches': ['main']}, 'pull_request': {'branches': ['main']}},
                'jobs': {
                    'build': {
                        'runs-on': 'ubuntu-latest',
                        'strategy': {'matrix': {'node-version': ['18.x', '20.x']}},
                        'steps': [
                            {'uses': 'actions/checkout@v4'},
                            {'name': 'Use Node.js', 'uses': 'actions/setup-node@v4',
                             'with': {'node-version': '${{ matrix.node-version }}', 'cache': 'npm'}},
                            {'name': 'Install dependencies', 'run': 'npm ci'},
                            {'name': 'Build', 'run': 'npm run build --if-present'},
                            {'name': 'Test', 'run': 'npm test --if-present'}
                        ]
                    }
                }
            },
            'gitlab_ci': {
                'stages': ['build', 'test'],
                'variables': {'NODE_VERSION': '20'},
                'build': {
                    'stage': 'build',
                    'image': 'node:20',
                    'script': ['npm ci', 'npm run build --if-present'],
                    'cache': {'paths': ['node_modules/']}
                },
                'test': {
                    'stage': 'test',
                    'image': 'node:20',
                    'script': ['npm ci', 'npm test --if-present'],
                    'cache': {'paths': ['node_modules/']}
                }
            }
        },
        'docker': {
            'github_actions': {
                'name': 'Docker Build',
                'on': {'push': {'branches': ['main']}, 'pull_request': {'branches': ['main']}},
                'jobs': {
                    'build': {
                        'runs-on': 'ubuntu-latest',
                        'steps': [
                            {'uses': 'actions/checkout@v4'},
                            {'name': 'Build Docker image', 'run': 'docker build -t myapp:${{ github.sha }} .'},
                            {'name': 'Test Docker image', 'run': 'docker run --rm myapp:${{ github.sha }} echo "Build successful"'}
                        ]
                    }
                }
            },
            'gitlab_ci': {
                'stages': ['build', 'deploy'],
                'variables': {'DOCKER_IMAGE': '$CI_REGISTRY_IMAGE'},
                'build': {
                    'stage': 'build',
                    'image': 'docker:latest',
                    'services': ['docker:dind'],
                    'script': [
                        'docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .',
                        'docker tag $DOCKER_IMAGE:$CI_COMMIT_SHA $DOCKER_IMAGE:latest'
                    ]
                }
            }
        },
        'vercel-deploy': {
            'github_actions': {
                'name': 'Deploy to Vercel',
                'on': {'push': {'branches': ['main']}, 'pull_request': {}},
                'jobs': {
                    'deploy': {
                        'runs-on': 'ubuntu-latest',
                        'steps': [
                            {'uses': 'actions/checkout@v4'},
                            {'name': 'Deploy to Vercel', 
                             'uses': 'vercel/action-deploy@v1',
                             'with': {'vercel-token': '${{ secrets.VERCEL_TOKEN }}',
                                      'vercel-org-id': '${{ secrets.VERCEL_ORG_ID }}',
                                      'vercel-project-id': '${{ secrets.VERCEL_PROJECT_ID }}'}}
                        ]
                    }
                }
            }
        },
        'netlify-deploy': {
            'github_actions': {
                'name': 'Deploy to Netlify',
                'on': {'push': {'branches': ['main']}},
                'jobs': {
                    'deploy': {
                        'runs-on': 'ubuntu-latest',
                        'steps': [
                            {'uses': 'actions/checkout@v4'},
                            {'name': 'Build', 'run': 'npm ci && npm run build'},
                            {'name': 'Deploy to Netlify',
                             'uses': 'nwtgck/actions-netlify@v2.0',
                             'with': {'publish-dir': './dist',
                                      'production-branch': 'main',
                                      'github-token': '${{ secrets.GITHUB_TOKEN }}',
                                      'deploy-message': 'Deploy from GitHub Actions'},
                             'env': {'NETLIFY_AUTH_TOKEN': '${{ secrets.NETLIFY_AUTH_TOKEN }}',
                                     'NETLIFY_SITE_ID': '${{ secrets.NETLIFY_SITE_ID }}'}}
                        ]
                    }
                }
            }
        }
    }
    
    @classmethod
    def generate(cls, template_name: str, project_type: str = 'github_actions', 
                 output_path: Optional[str] = None) -> str:
        """Generate a workflow file from template"""
        
        if template_name not in cls.TEMPLATES:
            available = ', '.join(cls.TEMPLATES.keys())
            raise ValueError(f"Unknown template: {template_name}. Available: {available}")
        
        template = cls.TEMPLATES[template_name].get(project_type)
        if not template:
            raise ValueError(f"Template '{template_name}' not available for {project_type}")
        
        yaml_content = yaml.dump(template, default_flow_style=False, sort_keys=False)
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(yaml_content)
            return output_path
        
        return yaml_content


class GitHubActionsManager:
    """Manage GitHub Actions workflows"""
    
    def __init__(self, token: Optional[str] = None):
        if not GITHUB_AVAILABLE:
            raise ImportError("PyGithub is required. Install with: pip install PyGithub")
        
        self.token = token or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN environment variable.")
        
        self.github = Github(self.token)
    
    def list_workflow_runs(self, repo: str, workflow_name: Optional[str] = None, 
                           limit: int = 10) -> List[Dict]:
        """List recent workflow runs"""
        try:
            repository = self.github.get_repo(repo)
            
            if workflow_name:
                # Find workflow by name
                workflows = repository.get_workflows()
                workflow = None
                for wf in workflows:
                    if wf.name == workflow_name or wf.path.endswith(workflow_name):
                        workflow = wf
                        break
                
                if not workflow:
                    raise ValueError(f"Workflow '{workflow_name}' not found")
                
                runs = workflow.get_runs()
            else:
                runs = repository.get_workflow_runs()
            
            results = []
            for run in runs[:limit]:
                results.append({
                    'id': run.id,
                    'name': run.name,
                    'head_branch': run.head_branch,
                    'head_sha': run.head_sha[:7],
                    'status': run.status,
                    'conclusion': run.conclusion,
                    'created_at': run.created_at.isoformat() if run.created_at else None,
                    'run_number': run.run_number,
                    'html_url': run.html_url
                })
            
            return results
            
        except UnknownObjectException:
            raise ValueError(f"Repository '{repo}' not found")
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e}")
    
    def trigger_workflow_run(self, repo: str, workflow_name: str, 
                             branch: str = 'main', inputs: Optional[Dict] = None) -> Dict:
        """Trigger a workflow run manually"""
        try:
            repository = self.github.get_repo(repo)
            
            # Find workflow
            workflows = repository.get_workflows()
            workflow = None
            for wf in workflows:
                if wf.name == workflow_name or wf.path.endswith(workflow_name):
                    workflow = wf
                    break
            
            if not workflow:
                raise ValueError(f"Workflow '{workflow_name}' not found")
            
            # Trigger workflow
            workflow.create_dispatch(branch, inputs or {})
            
            return {
                'success': True,
                'message': f"Workflow '{workflow_name}' triggered on branch '{branch}'",
                'workflow_id': workflow.id,
                'workflow_path': workflow.path
            }
            
        except UnknownObjectException:
            raise ValueError(f"Repository '{repo}' not found")
        except GithubException as e:
            if e.status == 422:
                raise ValueError(f"Workflow '{workflow_name}' may not be configured for workflow_dispatch")
            raise RuntimeError(f"GitHub API error: {e}")
    
    def get_workflow_logs(self, repo: str, run_id: int, output_dir: Optional[str] = None) -> Dict:
        """Download and parse workflow logs"""
        try:
            repository = self.github.get_repo(repo)
            run = repository.get_workflow_run(run_id)
            
            # Get run info
            run_info = {
                'id': run.id,
                'name': run.name,
                'status': run.status,
                'conclusion': run.conclusion,
                'head_branch': run.head_branch,
                'head_sha': run.head_sha,
                'html_url': run.html_url,
                'created_at': run.created_at.isoformat() if run.created_at else None,
                'updated_at': run.updated_at.isoformat() if run.updated_at else None
            }
            
            # Get jobs
            jobs = run.jobs()
            job_logs = []
            
            for job in jobs:
                job_info = {
                    'name': job.name,
                    'status': job.status,
                    'conclusion': job.conclusion,
                    'started_at': job.started_at.isoformat() if job.started_at else None,
                    'completed_at': job.completed_at.isoformat() if job.completed_at else None,
                    'steps': []
                }
                
                for step in job.steps:
                    job_info['steps'].append({
                        'name': step.name,
                        'status': step.status,
                        'conclusion': step.conclusion,
                        'number': step.number
                    })
                
                job_logs.append(job_info)
            
            result = {
                'run': run_info,
                'jobs': job_logs
            }
            
            # Save to file if output_dir specified
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                output_file = Path(output_dir) / f"run_{run_id}_logs.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                result['output_file'] = str(output_file)
            
            return result
            
        except UnknownObjectException:
            raise ValueError(f"Repository or run not found")
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e}")


class PreviewDeployer:
    """Deploy preview environments for Vercel/Netlify"""
    
    @staticmethod
    def deploy_vercel_preview(repo: str, branch: str, cwd: Optional[str] = None) -> Dict:
        """Deploy a branch to Vercel preview"""
        results = {
            'platform': 'vercel',
            'repo': repo,
            'branch': branch,
            'success': False,
            'url': None,
            'commands': []
        }
        
        # Check for Vercel CLI
        try:
            subprocess.run(['vercel', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            results['error'] = 'Vercel CLI not found. Install with: npm i -g vercel'
            return results
        
        # Check for token
        if not os.environ.get('VERCEL_TOKEN'):
            results['error'] = 'VERCEL_TOKEN environment variable required'
            return results
        
        work_dir = cwd or os.getcwd()
        
        try:
            # Deploy with Vercel CLI
            cmd = ['vercel', '--token', os.environ['VERCEL_TOKEN'], 
                   '--yes', '--confirm', '--cwd', work_dir]
            
            if branch != 'main' and branch != 'master':
                cmd.extend(['--target', 'preview'])
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
            results['commands'].append(' '.join(cmd))
            
            if result.returncode == 0:
                # Extract URL from output
                output = result.stdout + result.stderr
                url_match = re.search(r'(https?://[^\s]+\.vercel\.app)', output)
                if url_match:
                    results['url'] = url_match.group(1)
                results['success'] = True
                results['output'] = output
            else:
                results['error'] = result.stderr
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    @staticmethod
    def deploy_netlify_preview(repo: str, branch: str, cwd: Optional[str] = None,
                                build_dir: str = 'dist') -> Dict:
        """Deploy a branch to Netlify preview"""
        results = {
            'platform': 'netlify',
            'repo': repo,
            'branch': branch,
            'success': False,
            'url': None,
            'commands': []
        }
        
        # Check for Netlify CLI
        try:
            subprocess.run(['netlify', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            results['error'] = 'Netlify CLI not found. Install with: npm i -g netlify-cli'
            return results
        
        # Check for auth
        if not os.environ.get('NETLIFY_AUTH_TOKEN'):
            results['error'] = 'NETLIFY_AUTH_TOKEN environment variable required'
            return results
        
        work_dir = cwd or os.getcwd()
        
        try:
            # Deploy with Netlify CLI
            cmd = ['netlify', 'deploy', 
                   '--auth', os.environ['NETLIFY_AUTH_TOKEN'],
                   '--site', os.environ.get('NETLIFY_SITE_ID', ''),
                   '--dir', build_dir,
                   '--json']
            
            if branch != 'main' and branch != 'master':
                cmd.append('--alias=' + branch.replace('/', '-'))
            else:
                cmd.append('--prod')
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
            results['commands'].append(' '.join(cmd))
            
            if result.returncode == 0:
                try:
                    deploy_info = json.loads(result.stdout)
                    results['url'] = deploy_info.get('deploy_url') or deploy_info.get('url')
                    results['success'] = True
                    results['deploy_info'] = deploy_info
                except json.JSONDecodeError:
                    results['output'] = result.stdout
                    results['success'] = True
            else:
                results['error'] = result.stderr
                
        except Exception as e:
            results['error'] = str(e)
        
        return results


# CLI Interface
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='CI/CD Pipeline Automation')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate workflow file')
    validate_parser.add_argument('file_path', help='Path to workflow file')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate workflow from template')
    generate_parser.add_argument('template', help='Template name (python, node, docker, etc.)')
    generate_parser.add_argument('--type', choices=['github_actions', 'gitlab_ci'], 
                                 default='github_actions', help='CI/CD platform type')
    generate_parser.add_argument('--output', '-o', help='Output file path')
    
    # List runs command
    list_parser = subparsers.add_parser('list-runs', help='List workflow runs')
    list_parser.add_argument('repo', help='Repository (owner/repo)')
    list_parser.add_argument('--workflow', help='Workflow name or file')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of runs to show')
    
    # Trigger command
    trigger_parser = subparsers.add_parser('trigger', help='Trigger workflow run')
    trigger_parser.add_argument('repo', help='Repository (owner/repo)')
    trigger_parser.add_argument('workflow', help='Workflow name')
    trigger_parser.add_argument('--branch', default='main', help='Branch to run on')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Get workflow logs')
    logs_parser.add_argument('repo', help='Repository (owner/repo)')
    logs_parser.add_argument('run_id', type=int, help='Run ID')
    logs_parser.add_argument('--output', '-o', help='Output directory for logs')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy-preview', help='Deploy preview environment')
    deploy_parser.add_argument('repo', help='Repository (owner/repo)')
    deploy_parser.add_argument('branch', help='Branch to deploy')
    deploy_parser.add_argument('--platform', choices=['vercel', 'netlify'], 
                               default='vercel', help='Deployment platform')
    deploy_parser.add_argument('--build-dir', default='dist', help='Build directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'validate':
            result = WorkflowValidator.validate_workflow(args.file_path)
            print(json.dumps(result, indent=2))
            sys.exit(0 if result['valid'] else 1)
        
        elif args.command == 'generate':
            output = WorkflowGenerator.generate(args.template, args.type, args.output)
            if args.output:
                print(f"Generated: {output}")
            else:
                print(output)
        
        elif args.command == 'list-runs':
            manager = GitHubActionsManager()
            runs = manager.list_workflow_runs(args.repo, args.workflow, args.limit)
            print(json.dumps(runs, indent=2))
        
        elif args.command == 'trigger':
            manager = GitHubActionsManager()
            result = manager.trigger_workflow_run(args.repo, args.workflow, args.branch)
            print(json.dumps(result, indent=2))
        
        elif args.command == 'logs':
            manager = GitHubActionsManager()
            result = manager.get_workflow_logs(args.repo, args.run_id, args.output)
            print(json.dumps(result, indent=2))
        
        elif args.command == 'deploy-preview':
            if args.platform == 'vercel':
                result = PreviewDeployer.deploy_vercel_preview(args.repo, args.branch)
            else:
                result = PreviewDeployer.deploy_netlify_preview(
                    args.repo, args.branch, build_dir=args.build_dir
                )
            print(json.dumps(result, indent=2))
            sys.exit(0 if result['success'] else 1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()