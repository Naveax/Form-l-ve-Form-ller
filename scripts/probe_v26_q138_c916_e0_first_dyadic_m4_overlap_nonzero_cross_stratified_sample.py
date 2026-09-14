#!/usr/bin/env python3
import hashlib, io, json, math, os, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J

P=O.P
PHYS_N=O.PHYS_N
SAMPLE_N=64
M4_PATH=Path(os.environ.get("C916_M4_AUTHORITY","authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json"))
EXPECTED_ZC_DIGEST="7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1"
HUBS=(19,20,23,61,83,129,134,139,140,157,232)
ISOLATES=(158,180,236,238)

def relation_mask(counts,lvals,rvals):
    mask=0; bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts: mask|=1<<bit
            bit+=1
    return mask

def endpoint_class(u,v,H,I):
    cu="h" if u in H else "i" if u in I else "l"; cv="h" if v in H else "i" if v in I else "l"; return "".join(sorted((cu,cv)))

def analyze():
    m4=json.loads(M4_PATH.read_text()); assert m4["zero_cross_pair_digest_sha256"]==EXPECTED_ZC_DIGEST
    zc={tuple(sorted(map(int,e))) for e in m4["zero_cross_pairs"]}
    with redirect_stdout(io.StringIO()): census,groups=O.build_authority()
    gids=tuple(g for g in range(250) if census[g]["multiplicity"]==4); H=set(HUBS); I=set(ISOLATES)
    bysig=defaultdict(list); overlap=0; overlap_zc=0
    for i,u in enumerate(gids):
        for v in gids[i+1:]:
            rel,inter=P.support_relation(groups[u]["projection_anchor"],groups[v]["projection_anchor"],PHYS_N)
            if rel!="overlap_incomparable": continue
            overlap+=1
            if (u,v) in zc: overlap_zc+=1; continue
            assert inter is not None
            sig=(endpoint_class(u,v,H,I),len(inter[2]),census[u]["image_size"],census[v]["image_size"]); bysig[sig].append((u,v))
    assert overlap==2766 and overlap_zc==766 and sum(map(len,bysig.values()))==2000
    selected=[]; pos={k:0 for k in bysig}; keys=tuple(sorted(bysig))
    while len(selected)<SAMPLE_N:
        advanced=False
        for k in keys:
            j=pos[k]
            if j<len(bysig[k]):
                selected.append((k,bysig[k][j])); pos[k]=j+1; advanced=True
                if len(selected)==SAMPLE_N: break
        assert advanced
    assert len({p for _,p in selected})==SAMPLE_N
    ic={}; mc={}; rows=[]; strict=0; sizehist=Counter(); gainhist=Counter(); maskhist=Counter(); sighist=Counter(); dig=[]
    for idx,(sig,(u,v)) in enumerate(selected,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc); assert lm==census[u]["counts"] and rm==census[v]["counts"]
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); cart=len(lvals)*len(rvals); size=len(counts); mask=relation_mask(counts,lvals,rvals); gain=math.log2(cart)-math.log2(size); isstrict=size<cart
        strict+=int(isstrict); sizehist[size]+=1; gainhist[round(gain,12)]+=1; maskhist[f"{len(lvals)}x{len(rvals)}:{mask:x}"]+=1; sighist[(sig,isstrict)]+=1
        rows.append({"left_group_id":u,"right_group_id":v,"endpoint_class":sig[0],"intersection_dimension":sig[1],"left_image_size":len(lvals),"right_image_size":len(rvals),"cartesian_image_size":cart,"joint_image_size":size,"strict_subcartesian":isstrict,"exact_cardinality_gain_log2":gain,"relation_mask_hex":f"{mask:x}"})
        dig.append(f"{u}|{v}|{len(lvals)}x{len(rvals)}|{mask:x}")
        if idx%8==0 or idx==SAMPLE_N: print("progress",idx,"/",SAMPLE_N,"strict",strict,flush=True)
    out={"position":O.POS,"physical_shared_dimension":PHYS_N,"overlap_incomparable_pairs":overlap,"overlap_zero_cross_pairs":overlap_zc,"overlap_nonzero_cross_pairs":2000,"sample_size":SAMPLE_N,"sample_strict_subcartesian_pairs":strict,"sample_full_cartesian_pairs":SAMPLE_N-strict,"joint_image_size_histogram":dict(sorted(sizehist.items())),"gain_histogram_rounded_12":[{"gain_log2":k,"count":v} for k,v in sorted(gainhist.items())],"relation_mask_histogram":[{"key":k,"count":v} for k,v in sorted(maskhist.items())],"signature_strict_histogram":[{"endpoint_class":k[0][0],"intersection_dimension":k[0][1],"left_image_size":k[0][2],"right_image_size":k[0][3],"strict":k[1],"count":v} for k,v in sorted(sighist.items())],"results":rows,"sample_relation_digest_sha256":hashlib.sha256(("\n".join(dig)+"\n").encode()).hexdigest(),"cached_support_intersections":len(ic),"cached_character_moments":len(mc),"decision":"M4_OVERLAP_NONZERO_CROSS_STRATIFIED_VALUE_SAMPLE"}
    outpath=Path(os.environ.get("C916_OVERLAP_SAMPLE_OUT","artifacts/c916_e0_first_dyadic_m4_overlap_nonzero_cross_stratified_sample.json")); outpath.parent.mkdir(parents=True,exist_ok=True); outpath.write_text(json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
    print("result",json.dumps({k:v for k,v in out.items() if k!="results"},sort_keys=True),flush=True); print("sample_artifact_path",outpath,flush=True); print("PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_OVERLAP_NONZERO_CROSS_STRATIFIED_SAMPLE"); print("ALPHA_PASS=0"); return out

if __name__=="__main__": analyze()
