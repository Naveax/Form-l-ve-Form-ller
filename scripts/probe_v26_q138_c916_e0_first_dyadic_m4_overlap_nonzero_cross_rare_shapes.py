#!/usr/bin/env python3
import hashlib, io, json, math, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J

P=O.P
PHYS_N=O.PHYS_N
M4_PATH=Path(os.environ.get("C916_M4_AUTHORITY","authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json"))
EXPECTED_ZC_DIGEST="7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1"

def relation_mask(counts,lvals,rvals):
    z=0; bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts: z|=1<<bit
            bit+=1
    return z

def analyze():
    m4=json.loads(M4_PATH.read_text()); assert m4["zero_cross_pair_digest_sha256"]==EXPECTED_ZC_DIGEST
    zc={tuple(sorted(map(int,e))) for e in m4["zero_cross_pairs"]}
    with redirect_stdout(io.StringIO()): census,groups=O.build_authority()
    gids=tuple(g for g in range(250) if census[g]["multiplicity"]==4); selected=[]
    for i,u in enumerate(gids):
        for v in gids[i+1:]:
            rel,inter=P.support_relation(groups[u]["projection_anchor"],groups[v]["projection_anchor"],PHYS_N)
            if rel!="overlap_incomparable" or (u,v) in zc: continue
            shape=(census[u]["image_size"],census[v]["image_size"])
            if shape!=(7,7): assert inter is not None; selected.append((u,v,len(inter[2]),shape))
    assert len(selected)==29; assert Counter(s for _,_,_,s in selected)==Counter({(9,7):24,(7,9):4,(9,9):1})
    ic={}; mc={}; rows=[]; strict=0; sizehist=Counter(); maskhist=Counter(); dimhist=Counter(); dig=[]
    for idx,(u,v,dim,shape) in enumerate(selected,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc); assert lm==census[u]["counts"] and rm==census[v]["counts"]
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); cart=len(lvals)*len(rvals); size=len(counts); mask=relation_mask(counts,lvals,rvals); isstrict=size<cart; strict+=int(isstrict)
        sizehist[size]+=1; maskhist[f"{len(lvals)}x{len(rvals)}:{mask:x}"]+=1; dimhist[dim]+=1
        rows.append({"left_group_id":u,"right_group_id":v,"intersection_dimension":dim,"left_image_size":len(lvals),"right_image_size":len(rvals),"cartesian_image_size":cart,"joint_image_size":size,"strict_subcartesian":isstrict,"exact_cardinality_gain_log2":math.log2(cart)-math.log2(size),"relation_mask_hex":f"{mask:x}"}); dig.append(f"{u}|{v}|{len(lvals)}x{len(rvals)}|{mask:x}")
        if idx%5==0 or idx==len(selected): print("progress",idx,"/",len(selected),"strict",strict,flush=True)
    out={"position":O.POS,"physical_shared_dimension":PHYS_N,"rare_shape_overlap_nonzero_cross_pairs":len(selected),"shape_histogram":{"7x9":4,"9x7":24,"9x9":1},"intersection_dimension_histogram":dict(sorted(dimhist.items())),"strict_subcartesian_pairs":strict,"full_cartesian_pairs":len(selected)-strict,"joint_image_size_histogram":dict(sorted(sizehist.items())),"relation_mask_histogram":[{"key":k,"count":v} for k,v in sorted(maskhist.items())],"results":rows,"relation_digest_sha256":hashlib.sha256(("\n".join(dig)+"\n").encode()).hexdigest(),"cached_support_intersections":len(ic),"cached_character_moments":len(mc),"decision":"M4_OVERLAP_NONZERO_CROSS_RARE_SHAPES_FULL_CENSUS"}
    outpath=Path(os.environ.get("C916_OVERLAP_RARE_OUT","artifacts/c916_e0_first_dyadic_m4_overlap_nonzero_cross_rare_shapes.json")); outpath.parent.mkdir(parents=True,exist_ok=True); outpath.write_text(json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
    print("result",json.dumps({k:v for k,v in out.items() if k!="results"},sort_keys=True),flush=True); print("authority_artifact_path",outpath,flush=True); print("PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_OVERLAP_NONZERO_CROSS_RARE_SHAPES"); print("ALPHA_PASS=0"); return out

if __name__=="__main__": analyze()
