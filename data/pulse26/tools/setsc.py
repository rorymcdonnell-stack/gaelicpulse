import json, re, os, sys

CACHE='/tmp/held_scorer_cache.json'
def loadcache():
    if os.path.exists(CACHE): return json.load(open(CACHE))
    return {}
def savecache(c): json.dump(c, open(CACHE,'w'), indent=2, ensure_ascii=False)

def pts(s):
    m=re.match(r'^(\d+)-(\d+)$',s.strip()); return (int(m.group(1)),int(m.group(2))) if m else None
def summ(scorers):
    g=p=0
    for s in scorers:
        m=re.match(r'^(\d+)-(\d+)$',s['tally'].strip()); g+=int(m.group(1)); p+=int(m.group(2))
    return g,p

def file(c): return f'{c}-football-2026_verified.json'
def find(d,opp,rnd_sub,comp_sub):
    for g in d['results']:
        if g['opponent']==opp and rnd_sub.lower() in g['round'].lower() and comp_sub.lower() in g['competition'].lower():
            return g
    return None

def set_scorers(county, opp, rnd_sub, comp_sub, scorers, tp_for, tp_against, built=True, expect=None):
    """If built: write to county file, validating sum vs score_for. If not built (held): stash in cache."""
    g_sum=summ(scorers)
    if built:
        d=json.load(open(file(county)))
        g=find(d,opp,rnd_sub,comp_sub)
        if not g: 
            print(f"  !! {county} v {opp} {rnd_sub}/{comp_sub} NOT FOUND"); return
        want=pts(g['score_for'])
        if g_sum!=want:
            print(f"  !! {county} v {opp}: scorers sum {g_sum[0]}-{g_sum[1]} != recorded {g['score_for']}  -- NOT WRITTEN"); return
        g['scorers']=scorers
        g['two_pointers']={"for":tp_for,"against":tp_against}
        json.dump(d, open(file(county),'w'), indent=2, ensure_ascii=False)
        print(f"  ok {county:10} v {opp:11} {comp_sub[:9]:9} {rnd_sub:8} -> {len(scorers)} scorers sum {g_sum[0]}-{g_sum[1]} == {g['score_for']} [2pt {tp_for}/{tp_against}]")
    else:
        if expect and g_sum!=pts(expect):
            print(f"  !! HELD {county} v {opp}: sum {g_sum[0]}-{g_sum[1]} != expected {expect} -- NOT CACHED"); return
        c=loadcache()
        key=f"{county}|{opp}|{comp_sub}|{rnd_sub}"
        c[key]={"county":county,"opp":opp,"comp":comp_sub,"round":rnd_sub,"scorers":scorers,"two_pointers":{"for":tp_for,"against":tp_against},"score":expect}
        savecache(c)
        print(f"  cached(held) {county:9} v {opp:11} -> {len(scorers)} scorers sum {g_sum[0]}-{g_sum[1]} (held county, will write when built)")
