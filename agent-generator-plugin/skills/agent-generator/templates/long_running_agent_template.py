"""
Long-Running Agent Template

Based on Anthropic's long-running agent research.
Implements the session protocol for multi-window work.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List

class LongRunningAgent:
    """
    Agent for working on a single feature in a multi-session project.
    
    Protocol:
    1. Get bearings (read history, verify environment)
    2. Select work (find next incomplete feature)
    3. Implement (work on ONE feature)
    4. Verify (test, commit, update tracking)
    5. Handoff (document for next session)
    """
    
    def __init__(self, project_id: str, session_num: int):
        self.project_id = project_id
        self.session_num = session_num
        self.project_dir = Path(project_id)
        self.features_file = self.project_dir / "features.json"
        self.progress_file = self.project_dir / "claude-progress.txt"
        self.init_script = self.project_dir / "init.sh"
        
    def run_session(self):
        """Execute complete session protocol"""
        print(f"\n{'='*60}")
        print(f"SESSION {self.session_num}: {self.project_id}")
        print(f"{'='*60}\n")
        
        # Phase 1: Get Bearings
        print("[1/5] Getting bearings...\n")
        self.get_bearings()
        
        # Phase 2: Select Work
        print("[2/5] Selecting work...\n")
        features = self.select_work()
        
        # Phase 3: Implement
        print("[3/5] Implementing features...\n")
        self.implement_features(features)
        
        # Phase 4: Verify & Commit
        print("[4/5] Verifying and committing...\n")
        self.verify_and_commit(features)
        
        # Phase 5: Handoff
        print("[5/5] Preparing handoff...\n")
        self.prepare_handoff(features)
        
        print(f"\n{'='*60}")
        print(f"SESSION {self.session_num} COMPLETE")
        print(f"{'='*60}\n")
    
    def get_bearings(self):
        """
        Phase 1: Understand project state
        - Run init.sh
        - Read progress file
        - Check git log
        - Run baseline tests
        """
        
        # Step 1: Current directory
        print("  $ pwd")
        result = subprocess.run(['pwd'], capture_output=True, text=True)
        print(f"  {result.stdout.strip()}")
        
        # Step 2: Read progress file
        print("\n  $ cat claude-progress.txt (last 30 lines)")
        if self.progress_file.exists():
            with open(self.progress_file) as f:
                lines = f.readlines()
                for line in lines[-30:]:
                    print(f"  {line.rstrip()}")
        else:
            print("  [Progress file not found - this is first session]")
        
        # Step 3: Git log
        print("\n  $ git log --oneline -10")
        result = subprocess.run(['git', 'log', '--oneline', '-10'],
                              cwd=self.project_dir,
                              capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                print(f"  {line}")
        else:
            print("  [Git repo not initialized yet]")
        
        # Step 4: Run init script
        print("\n  $ bash init.sh")
        if self.init_script.exists():
            result = subprocess.run(['bash', str(self.init_script)],
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✓ Environment ready")
            else:
                print(f"  ✗ Environment setup failed:\n{result.stderr}")
                raise RuntimeError("Environment setup failed")
        else:
            print("  [init.sh not found]")
        
        # Step 5: Run baseline tests
        print("\n  $ pytest tests/baseline_test.py")
        result = subprocess.run(['pytest', 'tests/baseline_test.py', '-v'],
                              cwd=self.project_dir,
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ Baseline tests PASS")
            self.baseline_passed = True
        else:
            print(f"  ✗ Baseline tests FAIL")
            print(result.stdout)
            self.baseline_passed = False
    
    def select_work(self) -> List[dict]:
        """
        Phase 2: Select features to work on
        - Read features.json
        - Find incomplete features
        - Check dependencies
        - Select up to N features
        """
        
        with open(self.features_file) as f:
            all_features = json.load(f)
        
        # Find incomplete features
        incomplete = [f for f in all_features if not f.get('passes', False)]
        
        print(f"  Total features: {len(all_features)}")
        print(f"  Incomplete: {len(incomplete)}")
        print(f"  Complete: {len(all_features) - len(incomplete)}")
        
        # Select features to work on (respect priorities and dependencies)
        features_to_work = self._select_prioritized_features(incomplete, max_count=3)
        
        print(f"\n  Selected for this session:")
        for f in features_to_work:
            deps_str = f"(depends on: {', '.join(f['blockers'])})" if f.get('blockers') else ""
            print(f"    - Feature {f['id']}: {f['description'][:50]}... {deps_str}")
        
        return features_to_work
    
    def implement_features(self, features: List[dict]):
        """
        Phase 3: Implement selected features
        - Work on features one at a time
        - Test as you go
        - Commit intermediate progress
        """
        
        for feature in features:
            print(f"\n  Implementing Feature {feature['id']}: {feature['description']}")
            print(f"  Steps:")
            for step in feature.get('steps', []):
                print(f"    - {step}")
            
            # This is where the actual AI agent would write code
            # For this template, we just mark it as "implemented"
            print(f"\n  [Implementation would happen here]")
            print(f"  [Code testing would happen here]")
            print(f"  [Committing progress...]")
            
            # In real implementation:
            # - Write code
            # - Test thoroughly
            # - Commit with git
    
    def verify_and_commit(self, features: List[dict]):
        """
        Phase 4: Verify features work and commit
        - Run tests
        - Verify baseline still passes
        - Update features.json
        - Create git commit
        """
        
        print("  Running baseline tests...")
        result = subprocess.run(['pytest', 'tests/baseline_test.py', '-q'],
                              cwd=self.project_dir,
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✓ Baseline tests PASS")
            self.baseline_passed = True
        else:
            print(f"  ✗ Baseline tests FAIL")
            print(result.stdout)
            raise RuntimeError("Baseline tests must pass before committing")
        
        # Update features.json
        with open(self.features_file) as f:
            all_features = json.load(f)
        
        for feature in features:
            for f in all_features:
                if f['id'] == feature['id']:
                    f['passes'] = True
                    f['verified_in_session'] = self.session_num
                    break
        
        with open(self.features_file, 'w') as f:
            json.dump(all_features, f, indent=2)
        
        print(f"\n  Updated features.json")
        
        # Create git commit
        commit_msg = f"Complete features {', '.join([f['id'] for f in features])}\n\n"
        for f in features:
            commit_msg += f"- Feature {f['id']}: {f['description']}\n"
        commit_msg += f"\nAll baseline tests passing"
        
        subprocess.run(['git', 'add', '-A'],
                      cwd=self.project_dir, capture_output=True)
        subprocess.run(['git', 'commit', '-m', commit_msg],
                      cwd=self.project_dir, capture_output=True)
        
        print(f"  Created git commit")
    
    def prepare_handoff(self, features: List[dict]):
        """
        Phase 5: Document handoff for next session
        - Update progress file
        - Provide guidance
        - Clear state verification
        """
        
        # Append to progress file
        handoff_text = f"\n{'='*70}\n"
        handoff_text += f"SESSION {self.session_num} [{datetime.now().isoformat()}]\n"
        handoff_text += f"{'='*70}\n\n"
        handoff_text += f"Features Completed: {len(features)}\n"
        for f in features:
            handoff_text += f"- Feature {f['id']}: PASS\n"
        
        handoff_text += f"\nBaseline Status: {'PASS ✓' if self.baseline_passed else 'FAIL ✗'}\n"
        handoff_text += f"Status: CLEAN STATE ✓\n\n"
        handoff_text += f"Next Session Guidance:\n"
        handoff_text += f"1. Run bash init.sh to start environment\n"
        handoff_text += f"2. Run pytest tests/baseline_test.py to verify nothing broke\n"
        handoff_text += f"3. Work on next priority features\n"
        handoff_text += f"4. Test thoroughly before marking complete\n"
        
        with open(self.progress_file, 'a') as f:
            f.write(handoff_text)
        
        print(f"  Updated claude-progress.txt")
        print(f"  Handoff documentation complete")
    
    def _select_prioritized_features(self, incomplete: List[dict],
                                    max_count: int = 3) -> List[dict]:
        """
        Select features based on priority and dependencies.
        Don't select features with unmet dependencies.
        """
        
        selected = []
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'normal': 2, 'low': 3}
        incomplete_sorted = sorted(
            incomplete,
            key=lambda f: priority_order.get(f.get('priority', 'normal'), 99)
        )
        
        # Get completed feature IDs
        with open(self.features_file) as f:
            all_features = json.load(f)
        completed = {f['id'] for f in all_features if f.get('passes')}
        
        # Select features with met dependencies
        for feature in incomplete_sorted:
            if len(selected) >= max_count:
                break
            
            # Check if dependencies are met
            blockers = set(feature.get('blockers', []))
            if blockers and not blockers.issubset(completed):
                continue  # Skip if dependencies not met
            
            selected.append(feature)
        
        return selected


def main():
    """Run a session of the long-running agent"""
    
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python long_running_agent_template.py <project_id> <session_num>")
        sys.exit(1)
    
    project_id = sys.argv[1]
    session_num = int(sys.argv[2])
    
    agent = LongRunningAgent(project_id, session_num)
    agent.run_session()


if __name__ == "__main__":
    main()
