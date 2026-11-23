#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(msg):
    print(f"[FAIL] {msg}")
    return False

def ok(msg):
    print(f"[OK] {msg}")

registry = (ROOT / "config/model-registry.yaml").read_text(encoding="utf-8")
model_re = re.compile(
    r'  - id: "(\d{3})"\n'
    r'    name: "([^"]+)"\n'
    r'    slug: "([^"]+)"\n'
    r'    module: (\d+)\n'
    r'    source: "([^"]+)"\n'
    r'    path: "([^"]+)"'
)
models = [
    dict(id=m[0], name=m[1], slug=m[2], module=int(m[3]), source=m[4], path=m[5])
    for m in model_re.findall(registry)
]

good = True
if len(models) != 100:
    good &= fail(f"active model count = {len(models)}, expected 100")
else:
    ok("active model count = 100")

ids = [m["id"] for m in models]
expected = [f"{i:03d}" for i in range(1, 101)]
if sorted(ids) != expected:
    good &= fail("active IDs are not exactly 001..100")
else:
    ok("active IDs are exactly 001..100")

for field in ("id", "slug", "path"):
    vals = [m[field] for m in models]
    if len(vals) != len(set(vals)):
        good &= fail(f"duplicate {field}")
    else:
        ok(f"{field} values are unique")

# Every active skill exists and declares the matching model_id.
for m in models:
    p = ROOT / m["path"]
    if not p.exists():
        good &= fail(f"missing active skill: {m['path']}")
        continue
    text = p.read_text(encoding="utf-8")
    if f'model_id: "{m["id"]}"' not in text:
        good &= fail(f"skill model_id mismatch: {m['path']}")
    if "legacy: true" in text:
        good &= fail(f"active registry points to legacy skill: {m['path']}")
if good:
    ok("active skill paths exist and are non-legacy")

# Routing metadata must cover the same 100 IDs.
metadata = (ROOT / "config/model-routing-metadata.yaml").read_text(encoding="utf-8")
meta_ids = re.findall(r'^  "(\d{3})":$', metadata, flags=re.M)
if sorted(meta_ids) != expected:
    good &= fail(f"routing metadata IDs mismatch: found {len(meta_ids)}")
else:
    ok("routing metadata covers 001..100")

# Module routers must reference every active skill exactly in its declared module.
for m in models:
    mod = ROOT / f"modules/{m['module']:02d}/SKILL.md"
    if not mod.exists():
        good &= fail(f"missing module router {mod.relative_to(ROOT)}")
        continue
    text = mod.read_text(encoding="utf-8")
    rel = "../../" + m["path"]
    if rel not in text:
        good &= fail(f"module {m['module']:02d} does not reference {m['path']}")
if good:
    ok("module routers reference all active skills")

# New GitHub-authored course sources must exist.
for m in models:
    if m["source"].startswith("docs/"):
        if not (ROOT / m["source"]).exists():
            good &= fail(f"missing course source: {m['source']}")
if good:
    ok("GitHub-authored course sources exist")

# Migration map must cover every intentionally changed legacy ID.
migration = (ROOT / "config/migration-map.yaml").read_text(encoding="utf-8")
required_changed = {"015","021","034","042","053","057","067","070","075","091"}
mapped = set(re.findall(r'old_id: "(\d{3})"', migration))
missing = required_changed - mapped
if missing:
    good &= fail(f"migration map missing IDs: {sorted(missing)}")
else:
    ok("migration map covers all changed IDs")

for legacy_path in re.findall(r'legacy_skill: "([^"]+)"', migration):
    if not (ROOT / legacy_path).exists():
        good &= fail(f"missing legacy skill: {legacy_path}")
if good:
    ok("legacy skill paths remain available")

# MkDocs navigation must expose 100 active course entries.
mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
course_refs = re.findall(r'course/(\d{3}-[^\s]+\.md)', mkdocs)
if len(course_refs) != 100 or len(set(course_refs)) != 100:
    good &= fail(f"MkDocs active course nav count = {len(set(course_refs))}, expected 100")
else:
    ok("MkDocs navigation contains 100 unique course pages")

# Basic model-set version checks.
for path in ["SKILL.md", "config/model-registry.yaml", "config/model-routing-metadata.yaml",
             "config/mechanism-clusters.yaml", "config/router.yaml", "schema/audit-output.yaml"]:
    text = (ROOT / path).read_text(encoding="utf-8")
    if "1.0.0" not in text:
        good &= fail(f"{path} does not declare Model Set v1.0")
if good:
    ok("core configs declare v1.0")

if not good:
    sys.exit(1)
print("\nModel Set v1.0 validation passed.")
