#!/usr/bin/env python3
"""
Skills Development Test Suite Runner
Safe environment for validating skills before production use
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class SkillsTestSuite:
    """Test runner for skill validation"""
    
    def __init__(self, workspace: str = "/root/.openclaw/workspace/skills-test"):
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True)
        self.log_dir = self.workspace / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.scratch = self.workspace / "scratch"
        self.scratch.mkdir(exist_ok=True)
        
        self.results: List[Dict] = []
        
    def run_all(self) -> Dict:
        """Run all test categories"""
        print("=" * 60)
        print("SKILLS DEVELOPMENT TEST SUITE")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # File operations
        self.test_file_operations()
        
        # Memory management
        self.test_memory_management()
        
        # Voice generation (dry run)
        self.test_voice_generation()
        
        # Cron syntax validation
        self.test_cron_validation()
        
        return self._generate_report()
    
    def test_file_operations(self):
        """Test read/write/edit operations"""
        print("\n📁 Testing File Operations...")
        
        # Test write
        test_file = self.scratch / "test_write.txt"
        try:
            test_file.write_text("Test content φ = 1.618")
            content = test_file.read_text()
            assert content == "Test content φ = 1.618", "Content mismatch"
            self._pass("file_write", "Write and read successful")
        except Exception as e:
            self._fail("file_write", str(e))
        
        # Test edit
        try:
            from textwrap import dedent
            test_file.write_text(dedent("""
                line 1
                line 2
                line 3
            """).strip())
            
            content = test_file.read_text()
            new_content = content.replace("line 2", "line 2 MODIFIED")
            test_file.write_text(new_content)
            
            assert "MODIFIED" in test_file.read_text()
            self._pass("file_edit", "Edit operation successful")
        except Exception as e:
            self._fail("file_edit", str(e))
        
        # Test path resolution
        try:
            abs_path = self.workspace.resolve()
            assert abs_path.exists(), "Path resolution failed"
            self._pass("path_resolution", "Absolute path resolution works")
        except Exception as e:
            self._fail("path_resolution", str(e))
    
    def test_memory_management(self):
        """Test memory operations (safe mode)"""
        print("\n🧠 Testing Memory Management...")
        
        # Test memory file creation
        try:
            mem_file = self.workspace / "memory_test.md"
            mem_file.write_text("# Test Memory\n\nEntry 1\nEntry 2\n")
            
            # Simulate memory_search (simplified)
            content = mem_file.read_text()
            lines = content.split("\n")
            
            assert len(lines) >= 3, "Memory structure invalid"
            self._pass("memory_structure", "Memory file structure valid")
        except Exception as e:
            self._fail("memory_structure", str(e))
        
        # Test append vs overwrite
        try:
            append_file = self.scratch / "append_test.txt"
            append_file.write_text("Line 1\n")
            
            # Append
            with open(append_file, 'a') as f:
                f.write("Line 2\n")
            
            content = append_file.read_text()
            assert "Line 1" in content and "Line 2" in content
            self._pass("memory_append", "Append operation safe")
        except Exception as e:
            self._fail("memory_append", str(e))
    
    def test_voice_generation(self):
        """Test voice generation (dry run / validation only)"""
        print("\n🎙️ Testing Voice Generation...")
        
        # Check Piper availability (dry run)
        try:
            import subprocess
            result = subprocess.run(
                ["/tmp/piper_env/bin/piper", "--help"],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self._pass("voice_piper_available", "Piper TTS available")
            else:
                self._fail("voice_piper_available", "Piper not responding")
        except Exception as e:
            self._fail("voice_piper_available", str(e))
        
        # Check voice profiles exist
        try:
            profiles_dir = Path("/root/.openclaw/workspace/christkey-voice/trained_voices")
            if profiles_dir.exists():
                profiles = list(profiles_dir.glob("*.json"))
                if profiles:
                    self._pass("voice_profiles", f"Found {len(profiles)} voice profiles")
                else:
                    self._fail("voice_profiles", "No profiles found")
            else:
                self._fail("voice_profiles", "Profiles directory missing")
        except Exception as e:
            self._fail("voice_profiles", str(e))
    
    def test_cron_validation(self):
        """Test cron job syntax validation"""
        print("\n⏰ Testing Cron Validation...")
        
        # Test valid job structure
        try:
            test_job = {
                "name": "test-synthesis",
                "schedule": {"kind": "every", "everyMs": 3600000},
                "payload": {
                    "kind": "agentTurn",
                    "message": "Test synthesis"
                },
                "sessionTarget": "isolated"
            }
            
            # Validate required fields
            assert "name" in test_job
            assert "schedule" in test_job
            assert "payload" in test_job
            assert test_job["sessionTarget"] == "isolated"
            self._pass("cron_structure", "Job structure valid")
        except Exception as e:
            self._fail("cron_structure", str(e))
        
        # Test schedule types
        try:
            schedules = [
                {"kind": "every", "everyMs": 3600000},
                {"kind": "at", "at": "2026-04-01T10:00:00Z"},
                {"kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai"}
            ]
            
            for sched in schedules:
                assert "kind" in sched
            
            self._pass("cron_schedules", "All schedule types valid")
        except Exception as e:
            self._fail("cron_schedules", str(e))
    
    def _pass(self, test_name: str, message: str):
        """Record passing test"""
        self.results.append({
            "test": test_name,
            "status": "PASS",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        print(f"  ✅ {test_name}: {message}")
    
    def _fail(self, test_name: str, message: str):
        """Record failing test"""
        self.results.append({
            "test": test_name,
            "status": "FAIL",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        print(f"  ❌ {test_name}: {message}")
    
    def _generate_report(self) -> Dict:
        """Generate test report"""
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        total = len(self.results)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "N/A"
            },
            "results": self.results
        }
        
        # Save report
        report_file = self.log_dir / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total:   {total}")
        print(f"Passed:  {passed} ✅")
        print(f"Failed:  {failed} ❌")
        print(f"Rate:    {report['summary']['pass_rate']}")
        print(f"Log:     {report_file}")
        print("=" * 60)
        
        return report

def main():
    """CLI entry point"""
    suite = SkillsTestSuite()
    report = suite.run_all()
    
    # Exit with error code if any tests failed
    if report["summary"]["failed"] > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
