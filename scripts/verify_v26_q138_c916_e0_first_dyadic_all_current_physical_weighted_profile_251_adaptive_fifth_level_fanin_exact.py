#!/usr/bin/env python3
"""Exact profile-251 fan-in after adaptive replacement of heavy fourth-level shards."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_profile_251_mixed_depth_fanin_exact as M

HEAVY_PAIRS=M.HEAVY_PAIRS
HEAVY_GRANDCHILDREN=(1,3)
FOURTH_STATES=range(5)
DIRECT_FOURTH={0,2,4}
ADAPTIVE_FOURTH={1,3}

def direct_rows(directory:Path):
    rows={}
    for path in sorted(directory.glob("profile-251-parent-*-child-*-grandchild-*-fourth-*.json")):
        row=json.loads(path.read_text()); s=row["shard"]
        key=(int(s["parent_shard_index"]),int(s["child_shard_index"]),int(s["grandchild_shard_index"]),int(s["fourth_shard_index"]))
        if key[:2] not in HEAVY_PAIRS or key[2] not in HEAVY_GRANDCHILDREN: continue
        assert key not in rows,key
        assert int(row["all_current"]["base_mass"])==M.BASE_MASS
        rows[key]=row
    return rows

def adaptive_rows(directory:Path):
    rows={}
    for path in sorted(directory.glob("profile-251-path-*-aggregate.json")):
        row=json.loads(path.read_text()); key=tuple(map(int,row["path_indices"]))
        if len(key)!=4 or key[:2] not in HEAVY_PAIRS or key[2] not in HEAVY_GRANDCHILDREN: continue
        assert key not in rows,key
        raw=int(row["exact_parent_profile_count"]); weighted=int(row["exact_parent_weighted_summand"])
        assert weighted==M.BASE_MASS*raw
        rows[key]=row
    return rows

def build_grandchild_replacements(direct_directory:Path,adaptive_directory:Path,output_directory:Path):
    direct=direct_rows(direct_directory); adaptive=adaptive_rows(adaptive_directory)
    output_directory.mkdir(parents=True,exist_ok=True)
    replacements={}; source_rows=[]
    for p,c in HEAVY_PAIRS:
        for g in HEAVY_GRANDCHILDREN:
            total=0; local=[]
            for f in FOURTH_STATES:
                key=(p,c,g,f); have_direct=key in direct; have_adaptive=key in adaptive
                assert have_direct ^ have_adaptive,("fourth-level cell must have exactly one source",key,have_direct,have_adaptive)
                if f in DIRECT_FOURTH:
                    assert have_direct and not have_adaptive,key
                    row=direct[key]; raw=int(row["all_current"]["exact_profile_count"]); weighted=int(row["all_current"]["exact_weighted_summand"])
                    source="direct_fourth_level"
                else:
                    assert f in ADAPTIVE_FOURTH and have_adaptive and not have_direct,key
                    row=adaptive[key]; raw=int(row["exact_parent_profile_count"]); weighted=int(row["exact_parent_weighted_summand"])
                    source="adaptive_fifth_level_aggregate"
                assert weighted==M.BASE_MASS*raw
                total+=raw
                rec={"path":list(key),"source":source,"exact_profile_count":raw,"exact_weighted_summand":weighted}
                source_rows.append(rec); local.append(rec)
            out={"position":"C","physical_shared_dimension":149,"domain_state_sum":M.TARGET,
                 "path_indices":[p,c,g],"exact_parent_profile_count":total,
                 "exact_parent_weighted_summand":M.BASE_MASS*total,"fourth_cell_sources":local,
                 "decision":"C916_PROFILE_251_MIXED_FOURTH_ADAPTIVE_GRANDCHILD_AGGREGATE_EXACT"}
            path=output_directory/f"profile-251-path-{p}-{c}-{g}-aggregate.json"
            path.write_text(json.dumps(out,sort_keys=True)+"\n"); replacements[(p,c,g)]=out
    assert len(replacements)==8
    return replacements,source_rows

def analyze(first_level_directory:Path,nested_directory:Path,direct_third_directory:Path,direct_fourth_directory:Path,adaptive_directory:Path,replacement_directory:Path,output:Path):
    replacements,source_rows=build_grandchild_replacements(direct_fourth_directory,adaptive_directory,replacement_directory)
    out=M.analyze(first_level_directory,nested_directory,direct_third_directory,replacement_directory,output)
    out["adaptive_fourth_replacement_cells"]=len(source_rows)
    out["adaptive_fourth_replacement_grandchildren"]=len(replacements)
    out["adaptive_fourth_cell_sources"]=source_rows
    out["decision"]="C916_ALL_CURRENT_WEIGHTED_PROFILE_251_FINAL_WITH_ADAPTIVE_FIFTH_LEVEL_REPLACEMENTS_EXACT"
    output.write_text(json.dumps(out,sort_keys=True)+"\n")
    print("adaptive_final_result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_ADAPTIVE_FIFTH_LEVEL_FINAL_EXACT")
    print("boundary=each heavy fourth-level cell is covered exactly once by either its successful direct artifact or one adaptive exact replacement aggregate")
    print("ALPHA_PASS=0")
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--first-level-directory",type=Path,required=True)
    p.add_argument("--nested-directory",type=Path,required=True)
    p.add_argument("--direct-third-directory",type=Path,required=True)
    p.add_argument("--direct-fourth-directory",type=Path,required=True)
    p.add_argument("--adaptive-directory",type=Path,required=True)
    p.add_argument("--replacement-directory",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    analyze(a.first_level_directory,a.nested_directory,a.direct_third_directory,a.direct_fourth_directory,a.adaptive_directory,a.replacement_directory,a.output)

if __name__=="__main__": main()
