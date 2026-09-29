"""Check exact summary structure and execute the workflow's actual gate command.
Supported subset intentionally matches generated summary blocks; actionlint checks YAML.
"""
import json
import os
from pathlib import Path
import re
import subprocess
import unittest

CASES = {
    'ui-tests.yml': ('ui-promotion', ['rust-quality', 'session-sync-regressions', 'ui-tests', 'macos-frame-recovery', 'ios-tests', 'linux-browser']),
    'preview-tests.yml': ('preview-promotion', ['networking', 'coordinator']),
    'windows.yml': ('windows-promotion', ['tests']),
}

def summary(text, name):
    match = re.search(r'^  ' + re.escape(name) + r':\n(.*?)(?=^  [\w-]+:|\Z)', text, re.M | re.S)
    if not match:
        raise ValueError('missing executable summary: ' + name)
    return match.group(1)

def inspect(text, name, required):
    block = summary(text, name)
    if '    if: always()\n' not in block:
        raise ValueError('summary must run after failure')
    trigger = re.search(r'^  pull_request:\s*\n(.*?)(?=^  [\w-]+:|^permissions:|\Z)', text, re.M | re.S)
    if not trigger or re.search(r'^    (paths|paths-ignore|branches|branches-ignore):', trigger.group(1), re.M):
        raise ValueError('PR trigger is absent or filtered')
    needs = re.search(r'^    needs:([^\n]*)\n((?:      - [^\n]+\n)*)', block, re.M)
    if not needs:
        raise ValueError('missing needs')
    actual = re.findall(r'[\w-]+', needs.group(1)) or re.findall(r'^      - ([\w-]+)$', needs.group(2), re.M)
    if set(actual) != set(required) or len(actual) != len(required):
        raise ValueError('needs differs from required jobs')
    if '        shell: bash\n' not in block:
        raise ValueError('explicit bash required')
    if '          RESULTS: ${{ toJSON(needs) }}\n' not in block:
        raise ValueError('results not bound to native needs')
    configured = re.search(r'^          REQUIRED: (.+)$', block, re.M)
    if not configured or configured.group(1).split(',') != required:
        raise ValueError('required list mismatch')
    if 'continue-on-error' in block:
        raise ValueError('fail-open step')
    command = re.search(r'^        run: \|\n          (python3 -c .+)\n?$', block.rstrip() + '\n', re.M)
    if not command:
        raise ValueError('unsupported summary command shape')
    return command.group(1)

class PromotionGateTests(unittest.TestCase):
    def test_exact_summary_and_actual_predicate(self):
        for filename, (name, required) in CASES.items():
            with self.subTest(workflow=filename):
                text = (Path('.github/workflows') / filename).read_text()
                command = inspect(text, name, required)
                if filename == 'ui-tests.yml':
                    ios = summary(text, 'ios-tests')
                    self.assertNotRegex(ios, r'(?m)^    if:', 'iOS must not be skipped')
                good = {job: {'result': 'success'} for job in required}
                controls = [(good, 0), ({}, 1)]
                for job in required:
                    missing = dict(good); del missing[job]
                    controls.append((missing, 1))
                    for state in ['failure', 'cancelled', 'skipped', 'timed_out', None]:
                        controls.append(({**good, job: {'result': state}}, 1))
                for results, expected in controls:
                    env = dict(os.environ, RESULTS=json.dumps(results), REQUIRED=','.join(required))
                    result = subprocess.run(['bash', '-c', command], env=env, capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, expected, (filename, results, result.stderr))
                # Structural mutants must fail before a command can be accepted.
                mutants = [text.replace('  '+name+':', '  removed-summary:', 1),
                           text.replace('  '+name+':\n    if: always()', '  '+name+':\n    if: success()', 1),
                           text.replace('          RESULTS: ${{ toJSON(needs) }}', '          RESULTS: "{}"', 1)]
                for mutant in mutants:
                    with self.assertRaises(ValueError):
                        inspect(mutant, name, required)

if __name__ == '__main__':
    unittest.main()
