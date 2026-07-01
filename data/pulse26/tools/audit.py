import json, glob, re, os
from collections import defaultdict

files = sorted(glob.glob('*-football-2026_verified.json'))

def pts(score):
    """ 'X-YY' -> total points (goal=3). Returns (goals, points_component, total_pts) """
    if not score or not isinstance(score,str): return None
    m = re.match(r'^(\d+)-(\d+)$', score.strip())
    if not m: return None
    g,p = int(m.group(1)), int(m.group(2))
    return g, p, g*3+p

def parse_tally(t):
    if not t or not isinstance(t,str): return None
    m = re.match(r'^(\d+)-(\d+)$', t.strip())
    if not m: return None
    return int(m.group(1)), int(m.group(2))

margin_errors=[]
scorer_sum_full=[]   # full lists that DON'T reconcile
scorer_partial=[]    # partial/empty lists (data gap)
provisional=[]       # notes flag provisional/unverified/discrepancy
game_index=defaultdict(list)  # (frozenset(counties)) -> list of (county, round, score_for, score_against, opp)
county_summary={}

for f in files:
    d=json.load(open(f))
    county=d['entity']['county']
    games=d.get('results',[])
    full=part=empty=0
    for gi,g in enumerate(games):
        rnd=f"{g.get('competition','?')} {g.get('round','?')}"
        opp=g.get('opponent')
        sf,sa=g.get('score_for'),g.get('score_against')
        pf,pa=pts(sf),pts(sa)
        # margin check
        if pf and pa and g.get('margin') is not None:
            calc=pf[2]-pa[2]
            if calc!=g['margin']:
                margin_errors.append(f"{county} v {opp} ({rnd}): recorded margin {g['margin']} but {sf} vs {sa} = {calc}")
        # cross-file index
        if opp:
            game_index[frozenset([county,opp])].append({'county':county,'opp':opp,'round':rnd,'sf':sf,'sa':sa,'date':g.get('date')})
        # scorer completeness + sum
        scs=g.get('scorers',[])
        if not scs:
            empty+=1; scorer_partial.append(f"{county} v {opp} ({rnd}): NO scorers")
        else:
            tallies=[parse_tally(s.get('tally')) for s in scs]
            if all(t is not None for t in tallies) and len(tallies)>0:
                # purported full-ish list: check sum vs team total
                tg=sum(t[0] for t in tallies); tp=sum(t[1] for t in tallies)
                if pf:
                    if (tg,tp)==(pf[0],pf[1]):
                        full+=1
                    else:
                        # could be legitimately partial even if all have tallies
                        scorer_sum_full.append(f"{county} v {opp} ({rnd}): scorers sum {tg}-{tp} but team scored {sf}  -> {'PARTIAL list' if (tg<pf[0] or tp<pf[1]) else 'MISMATCH/OVER'}")
                        part+=1
                else:
                    part+=1
            else:
                part+=1
                nnull=sum(1 for t in tallies if t is None)
                scorer_partial.append(f"{county} v {opp} ({rnd}): PARTIAL ({nnull}/{len(tallies)} scorers have no tally)")
        # provisional flags in notes
        note=(g.get('note') or '')+ (g.get('scoreline_unverified') and ' [scoreline_unverified=True]' or '')
        if re.search(r'provisional|not re-sourced|DISCREPANCY|to be re-verified|cross-referenced', note, re.I) or g.get('scoreline_unverified'):
            provisional.append(f"{county} v {opp} ({rnd})")
    county_summary[county]={'games':len(games),'full':full,'partial':part,'empty':empty}

print("="*70); print("1. MARGIN ARITHMETIC ERRORS"); print("="*70)
print("\n".join(margin_errors) if margin_errors else "  none - every recorded margin matches its scoreline.")

print("\n"+"="*70); print("2. CROSS-FILE SCORE RECONCILIATION (same game, two files)"); print("="*70)
mismatch=0; matched=0; onlyone=0
for cset,recs in sorted(game_index.items(), key=lambda x: sorted(x[0])):
    counties=sorted(cset)
    if len(recs)==1:
        onlyone+=1; continue
    # group records by which county authored them
    # a game between A and B: A's file says sf(A)-sa(A); B's file should say sf(B)=sa(A), sa(B)=sf(A)
    by=defaultdict(list)
    for r in recs: by[r['county']].append(r)
    # try to match each pair
    reported=False
    for r in recs:
        mirror_c=r['opp']
        # find mirror record authored by opp about this county
        cand=[x for x in recs if x['county']==mirror_c and x['opp']==r['county']]
        for c in cand:
            if r['sf']!=c['sa'] or r['sa']!=c['sf']:
                if not reported:
                    print(f"  MISMATCH {counties[0]} <-> {counties[1]}:")
                    print(f"     {r['county']} file: {r['sf']}-{r['sa']} ({r['round']})")
                    print(f"     {c['county']} file: {c['sf']}-{c['sa']} ({c['round']})")
                    mismatch+=1; reported=True
            else:
                matched+=1
print(f"\n  reconciled game-pairs OK: ~{matched//2 if matched else 0}; mismatches: {mismatch}; games present in only one file (other county held/not built): {onlyone}")

print("\n"+"="*70); print("3. PROVISIONAL / UNVERIFIED / DISCREPANCY FLAGS"); print("="*70)
print("\n".join("  "+p for p in provisional) if provisional else "  none")

print("\n"+"="*70); print("4. SCORER COMPLETENESS BY COUNTY"); print("="*70)
print(f"  {'county':<12}{'games':>6}{'full':>6}{'partial':>9}{'empty':>7}")
tg=tf=tp=te=0
for c in sorted(county_summary):
    s=county_summary[c]; tg+=s['games']; tf+=s['full']; tp+=s['partial']; te+=s['empty']
    flag = '  <-- needs work' if (s['empty']>0 or s['partial']>0) else ''
    print(f"  {c:<12}{s['games']:>6}{s['full']:>6}{s['partial']:>9}{s['empty']:>7}{flag}")
print(f"  {'TOTAL':<12}{tg:>6}{tf:>6}{tp:>9}{te:>7}")

print("\n"+"="*70); print("5. SCORER-SUM INTEGRITY (lists that don't sum to team total)"); print("="*70)
print("\n".join("  "+s for s in scorer_sum_full) if scorer_sum_full else "  none of the full lists mis-sum (good)")
