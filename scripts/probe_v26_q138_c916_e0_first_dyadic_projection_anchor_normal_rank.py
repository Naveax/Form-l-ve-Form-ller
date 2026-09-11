#!/usr/bin/env python3
import io, json, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

PHYS_N=O.PHYS_N
POS=O.POS
R=O.P.R
assert PHYS_N==149

def rank(rows):
    return R.gf2_rank(tuple(int(x) for x in rows))

def analyze():
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    assert len(groups)==250
    fam={'s':[],'m2':[],'m4':[]}
    for g in range(250):
        mult=census[g]['multiplicity']
        fam['s' if mult==1 else 'm2' if mult==2 else 'm4'].append(g)

    per_group=[]; all_normals=[]; all_aug=[]
    for g in range(250):
        a=groups[g]['projection_anchor']; cons=tuple(a['physical_support_constraints'])
        normals=tuple(int(m) for m,_ in cons)
        assert rank(normals)==len(normals)
        assert len(cons)==PHYS_N-groups[g]['projection_rank']
        all_normals.extend(normals)
        all_aug.extend(int(m) | (int(rhs)<<PHYS_N) for m,rhs in cons)
        per_group.append({'group_id':g,'multiplicity':census[g]['multiplicity'],
                          'projection_rank':groups[g]['projection_rank'],'constraint_rank':len(cons)})

    family_rows={}
    for name,gids in fam.items():
        normals=[]; augmented=[]; unique_pairs=set(); unique_normals=set()
        for g in gids:
            cons=groups[g]['projection_anchor']['physical_support_constraints']
            for m,rhs in cons:
                normals.append(int(m)); augmented.append(int(m)|(int(rhs)<<PHYS_N))
                unique_normals.add(int(m)); unique_pairs.add((int(m),int(rhs)))
        family_rows[name]={
            'groups':len(gids),'constraint_occurrences':len(normals),
            'unique_constraint_normals':len(unique_normals),'unique_affine_constraints':len(unique_pairs),
            'normal_span_rank':rank(normals),'augmented_affine_row_rank':rank(augmented),
            'codimension_histogram':dict(sorted(Counter(PHYS_N-groups[g]['projection_rank'] for g in gids).items())),
        }

    m4_progress=[]; rows=[]; prev=0
    for g in fam['m4']:
        rows.extend(int(m) for m,_ in groups[g]['projection_anchor']['physical_support_constraints'])
        r=rank(rows)
        if r>prev:
            m4_progress.append({'group_id':g,'rank_before':prev,'rank_after':r,'rank_gain':r-prev})
            prev=r
    m4_rank=family_rows['m4']['normal_span_rank']
    assert prev==m4_rank

    combos={}
    for names in (('s','m2'),('s','m4'),('m2','m4'),('s','m2','m4')):
        rows=[]
        for name in names:
            for g in fam[name]: rows.extend(int(m) for m,_ in groups[g]['projection_anchor']['physical_support_constraints'])
        combos['+'.join(names)]=rank(rows)

    decision=('M4_PROJECTION_MEMBERSHIP_DEPENDS_ON_LOWER_RANK_SYNDROME' if m4_rank<PHYS_N
              else 'M4_PROJECTION_MEMBERSHIP_NORMALS_SPAN_FULL_PHYSICAL_DUAL')
    out={'position':POS,'physical_shared_dimension':PHYS_N,'outputs':250,
         'family_normal_geometry':family_rows,
         'combined_normal_span_ranks':combos,
         'all_constraint_occurrences':len(all_normals),'all_unique_constraint_normals':len(set(all_normals)),
         'all_unique_affine_constraints':len(set((x & ((1<<PHYS_N)-1),x>>PHYS_N) for x in all_aug)),
         'all_normal_span_rank':rank(all_normals),'all_augmented_affine_row_rank':rank(all_aug),
         'm4_rank_growth_events':m4_progress,
         'm4_membership_syndrome_upper_bound_bits':m4_rank,
         'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PROJECTION_ANCHOR_NORMAL_RANK')
    print('theorem=every projection-anchor membership predicate is determined by the syndrome of the union of its affine constraint normals; the reported GF(2) span rank is therefore an exact upper bound on membership-syndrome bits')
    print('important=this concerns anchor membership only, not output values inside anchors and not the complete output joint image')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
