#!/usr/bin/env python3
"""Exact profile-251 fan-in after splitting the 32 timed-out fifth-level cells one level deeper."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_profile_251_adaptive_fifth_level_fanin_exact as F5
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_profile_251_mixed_depth_fanin_exact as M

HEAVY_FOURTH_PATHS=((1,1,1,1),(1,1,1,3),(1,1,3,1),(1,1,3,3),(1,3,1,1),(1,3,1,3),(1,3,3,1),(1,3,3,3),(3,1,1,1),(3,1,1,3),(3,1,3,1),(3,1,3,3),(3,3,1,1),(3,3,1,3),(3,3,3,1),(3,3,3,3))
FIFTH_DIRECT=(0,1,4)
FIFTH_REPLACED=(2,3)
SIXTH_STATES=(0,1,2,3)

def parse_path(text:str):
    return tuple(int(x) for x in text.split(",") if x!="")

def aggregate_sixth(path_indices,directory:Path,output:Path):
    path_indices=tuple(map(int,path_indices))
    assert len(path_indices)==5 and path_indices[:4] in HEAVY_FOURTH_PATHS
    assert path_indices[4] in FIFTH_REPLACED
    prefix="-".join(map(str,path_indices))
    paths=sorted(directory.glob(f"profile-251-path-{prefix}-child-*.json"))
    assert len(paths)==4,[p.name for p in paths]
    rows=[json.loads(p.read_text()) for p in paths]
    by={int(r["shard"]["next_split"]["state_index"]):r for r in rows}
    assert tuple(sorted(by))==SIXTH_STATES
    first=by[0]["shard"]
    assert tuple(map(int,first["path_indices"]))==path_indices
    assert int(first["next_split"]["state_count"])==4
    for i in SIXTH_STATES:
        row=by[i]
        assert tuple(map(int,row["shard"]["path_indices"]))==path_indices
        assert int(row["shard"]["next_split"]["state_index"])==i
        assert int(row["shard"]["next_split"]["state_count"])==4
        assert int(row["all_current"]["base_mass"])==M.BASE_MASS
    raw=sum(int(by[i]["all_current"]["exact_profile_count"]) for i in SIXTH_STATES)
    weighted=sum(int(by[i]["all_current"]["exact_weighted_summand"]) for i in SIXTH_STATES)
    assert weighted==M.BASE_MASS*raw
    out={"position":"C","physical_shared_dimension":149,"domain_state_sum":M.TARGET,
         "path_indices":list(path_indices),"exact_parent_profile_count":raw,
         "exact_parent_weighted_summand":weighted,
         "next_split_variable_index":int(first["next_split"]["variable_index"]),
         "next_split_variable_members":first["next_split"]["variable_members"],
         "next_split_domain_mask":int(first["next_split"]["domain_mask"]),
         "next_split_state_count":4,
         "decision":"C916_PROFILE_251_ADAPTIVE_SIXTH_LEVEL_PARENT_AGGREGATED_EXACT"}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(out,sort_keys=True)+"\n")
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_ADAPTIVE_SIXTH_LEVEL_PARENT_AGGREGATE_EXACT")
    print("ALPHA_PASS=0")
    return out

def load_fifth_success(directory:Path):
    rows={}
    for path in sorted(directory.glob("profile-251-path-*-child-*.json")):
        row=json.loads(path.read_text()); s=row["shard"]
        p=tuple(map(int,s["path_indices"])); idx=int(s["next_split"]["state_index"])
        if len(p)!=4 or p not in HEAVY_FOURTH_PATHS or idx not in FIFTH_DIRECT: continue
        key=p+(idx,); assert key not in rows,key
        assert int(s["next_split"]["state_count"])==4
        assert int(row["all_current"]["base_mass"])==M.BASE_MASS
        rows[key]=row
    assert len(rows)==len(HEAVY_FOURTH_PATHS)*len(FIFTH_DIRECT),len(rows)
    return rows

def load_sixth(directory:Path):
    rows={}
    for path in sorted(directory.glob("profile-251-path-*-aggregate.json")):
        row=json.loads(path.read_text()); key=tuple(map(int,row["path_indices"]))
        if len(key)!=5 or key[:4] not in HEAVY_FOURTH_PATHS or key[4] not in FIFTH_REPLACED: continue
        assert key not in rows,key
        assert int(row["exact_parent_weighted_summand"])==M.BASE_MASS*int(row["exact_parent_profile_count"])
        rows[key]=row
    assert len(rows)==len(HEAVY_FOURTH_PATHS)*len(FIFTH_REPLACED),len(rows)
    return rows

def build_fifth_replacements(fifth_directory:Path,sixth_directory:Path,output_directory:Path):
    fifth=load_fifth_success(fifth_directory); sixth=load_sixth(sixth_directory)
    output_directory.mkdir(parents=True,exist_ok=True)
    source_rows=[]
    for p4 in HEAVY_FOURTH_PATHS:
        raw=0; local=[]
        for s in range(5):
            key=p4+(s,)
            if s in FIFTH_DIRECT:
                row=fifth[key]; count=int(row["all_current"]["exact_profile_count"]); weighted=int(row["all_current"]["exact_weighted_summand"]); source="direct_fifth_level"
            else:
                row=sixth[key]; count=int(row["exact_parent_profile_count"]); weighted=int(row["exact_parent_weighted_summand"]); source="adaptive_sixth_level_aggregate"
            assert weighted==M.BASE_MASS*count
            raw+=count
            rec={"path":list(key),"source":source,"exact_profile_count":count,"exact_weighted_summand":weighted}
            local.append(rec); source_rows.append(rec)
        out={"position":"C","physical_shared_dimension":149,"domain_state_sum":M.TARGET,
             "path_indices":list(p4),"exact_parent_profile_count":raw,
             "exact_parent_weighted_summand":M.BASE_MASS*raw,
             "fifth_cell_sources":local,
             "decision":"C916_PROFILE_251_MIXED_FIFTH_SIXTH_LEVEL_FOURTH_CELL_AGGREGATE_EXACT"}
        dest=output_directory/f"profile-251-path-{'-'.join(map(str,p4))}-aggregate.json"
        dest.write_text(json.dumps(out,sort_keys=True)+"\n")
    assert len(source_rows)==len(HEAVY_FOURTH_PATHS)*5
    return source_rows

def analyze(first_level_directory:Path,nested_directory:Path,direct_third_directory:Path,direct_fourth_directory:Path,
            fifth_directory:Path,sixth_directory:Path,fifth_replacement_directory:Path,
            grandchild_replacement_directory:Path,output:Path):
    source_rows=build_fifth_replacements(fifth_directory,sixth_directory,fifth_replacement_directory)
    out=F5.analyze(first_level_directory,nested_directory,direct_third_directory,direct_fourth_directory,
                   fifth_replacement_directory,grandchild_replacement_directory,output)
    out["sixth_level_replacement_cells"]=len(HEAVY_FOURTH_PATHS)*len(FIFTH_REPLACED)
    out["mixed_fifth_sixth_cell_sources"]=source_rows
    out["decision"]="C916_ALL_CURRENT_WEIGHTED_PROFILE_251_FINAL_WITH_ADAPTIVE_SIXTH_LEVEL_REPLACEMENTS_EXACT"
    output.write_text(json.dumps(out,sort_keys=True)+"\n")
    print("sixth_final_result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_ADAPTIVE_SIXTH_LEVEL_FINAL_EXACT")
    print("boundary=successful fifth-level cells are reused exactly once; only timed-out fifth-state 2/3 cells are replaced by exact sixth-level aggregates")
    print("ALPHA_PASS=0")
    return out

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="mode",required=True)
    a=sub.add_parser("aggregate-sixth"); a.add_argument("--path",required=True); a.add_argument("--directory",type=Path,required=True); a.add_argument("--output",type=Path,required=True)
    f=sub.add_parser("final")
    for name in ("first-level-directory","nested-directory","direct-third-directory","direct-fourth-directory","fifth-directory","sixth-directory","fifth-replacement-directory","grandchild-replacement-directory","output"):
        f.add_argument("--"+name,type=Path,required=True)
    args=p.parse_args()
    if args.mode=="aggregate-sixth":
        aggregate_sixth(parse_path(args.path),args.directory,args.output)
    else:
        analyze(args.first_level_directory,args.nested_directory,args.direct_third_directory,args.direct_fourth_directory,
                args.fifth_directory,args.sixth_directory,args.fifth_replacement_directory,args.grandchild_replacement_directory,args.output)

if __name__=="__main__": main()
