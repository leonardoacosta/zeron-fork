#!/usr/bin/env python3
"""Validate planning structure, not product correctness or implementation readiness."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHANGE = Path(__file__).resolve().parent
units = json.loads((CHANGE / 'units.json').read_text())
by_id = {unit['slug']: unit for unit in units}
assert len(by_id) == len(units), 'duplicate change slug'
assert {zf for unit in units for zf in unit['zf']} == {f'{n:02}' for n in range(1, 20)}, 'PRD coverage gap'
visited, active = set(), set()

def visit(slug):
    if slug == 'assignment-record':
        assert (ROOT / 'openspec/changes/assignment-record/tasks.md').is_file()
        return
    assert slug in by_id, f'unknown dependency: {slug}'
    assert slug not in active, f'cycle: {slug}'
    if slug in visited:
        return
    active.add(slug)
    unit = by_id[slug]
    for dependency in unit['deps']:
        if dependency in by_id:
            assert by_id[dependency]['round'] <= unit['round'], f'reverse round dependency: {slug}'
        visit(dependency)
    active.remove(slug)
    visited.add(slug)

for unit in units:
    slug = unit['slug']
    assert unit.get('readiness') in {'refinement_required', 'research_executable', 'implementation_ready'}, f'missing readiness: {slug}'
    assert isinstance(unit.get('readiness_reason'), str) and unit['readiness_reason'].strip(), f'missing readiness evidence: {slug}'
    if unit['readiness'] == 'implementation_ready':
        assert unit.get('handoff_validation'), f'implementation readiness requires exact handoff evidence: {slug}'
    visit(slug)
    base = ROOT / 'openspec/changes' / slug
    texts = {}
    for name in ['proposal.md', 'design.md', 'tasks.md', f'specs/{slug}/spec.md']:
        path = base / name
        assert path.is_file(), f'missing artifact: {path}'
        texts[name] = path.read_text()
        assert not re.search(r'\b(?:TBD|TODO)\b', texts[name]), f'placeholder: {path}'
    assert 'Implementation gate CLOSED' in texts['proposal.md'], slug
    assert f"**Round:** {unit['round']}" in texts['proposal.md'], slug
    for dependency in unit['deps']:
        assert f'`{dependency}`' in texts['proposal.md'], (slug, dependency)
    for source in unit['paths']:
        assert (ROOT / source).is_file(), f'missing source anchor: {source}'
        assert f'`{source}`' in texts['design.md'], (slug, source)
    for n, case in enumerate(unit['cases'], 1):
        assert case in texts[f'specs/{slug}/spec.md'], (slug, n)
        assert case in texts['tasks.md'], (slug, n)
    assert '## Rollback' in texts['tasks.md'], slug
    assert '## CI phase after every implementation iteration' in texts['tasks.md'], slug

index = (CHANGE / 'design.md').read_text()
for n in range(1, 20):
    assert f'| ZF-{n:02} |' in index, f'missing coverage row {n}'
for n in range(10):
    assert f'CI-R{n}' in index, f'missing round barrier {n}'
print(f'PASS: {len(units)} child changes, all 19 PRD references, 10 CI barriers, acyclic dependencies, existing anchors and scenario mappings')
print('Planning validation only. No child product implementation is authorized or proven by this result.')
