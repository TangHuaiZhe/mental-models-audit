#!/usr/bin/env python3
from pathlib import Path
import sys, yaml
ROOT=Path(__file__).resolve().parents[1]
reg=yaml.safe_load((ROOT/"config/model-registry.yaml").read_text())
mig=yaml.safe_load((ROOT/"config/migration-map.yaml").read_text())
models=reg["models"]; errors=[]
if len(models)!=100: errors.append(f"active model count={len(models)} != 100")
ids=[m["id"] for m in models]; slugs=[m["slug"] for m in models]; paths=[m["path"] for m in models]
if len(set(ids))!=100: errors.append("duplicate active ids")
if len(set(slugs))!=100: errors.append("duplicate active slugs")
if len(set(paths))!=100: errors.append("duplicate active paths")
mods={}
for m in models:
    mods.setdefault(int(m["module"]),[]).append(m["id"])
    if not (ROOT/m["path"]).exists(): errors.append(f"missing skill: {m['path']}")
for n in range(1,11):
    if len(mods.get(n,[]))!=10: errors.append(f"module {n:02d} has {len(mods.get(n,[]))} active models")
required={"015":"goodharts-law","019":"explore-exploit-tradeoff","021":"wrights-law-experience-curve","053":"s-curve-diffusion","057":"capital-cycle","058":"power-law-pareto","070":"antifragility-convexity","091":"maturity-transformation-duration-gap"}
lookup={m["id"]:m for m in models}
for mid,slug in required.items():
    if lookup.get(mid,{}).get("slug")!=slug: errors.append(f"{mid} expected {slug}")
mig_old={e["old_id"] for e in mig["entries"]}
for mid in required:
    if mid not in mig_old: errors.append(f"migration missing old id {mid}")
if errors:
    print("MODEL SET VALIDATION FAILED")
    for e in errors: print("-",e)
    sys.exit(1)
print("MODEL SET VALIDATION PASSED")
print("active_models=100")
for n in range(1,11): print(f"module_{n:02d}=10")
