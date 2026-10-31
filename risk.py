"""Transparent demonstration rules; not a validated clinical model."""
import math, re
def assess(d, note=''):
    ranges={'hr':(25,240),'spo2':(50,100),'temp':(30,44),'rr':(4,65),'sys':(50,240)}
    for key,(lo,hi) in ranges.items():
        v=d[key]
        if isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or not lo<=v<=hi: raise ValueError('Invalid '+key)
    reasons=[]; score=0
    for condition, points, reason in [
        (d['spo2']<92,4,'Oxygen saturation below demo threshold (92%)'),
        (d['hr']>110 or d['hr']<50,2,'Heart rate outside demo range (50–110)'),
        (d['rr']>24 or d['rr']<10,2,'Respiratory rate outside demo range (10–24)'),
        (d['temp']>=38,2,'Temperature at or above 38°C'),
        (d['sys']<90,3,'Systolic pressure below 90 mmHg')]:
        if condition: score+=points; reasons.append(reason)
    # Only explicit, non-negated phrases. This is deliberately limited keyword NLP.
    terms=['breathless','confused','chest pain','dizzy']
    flagged=[t for t in terms if re.search(r'\b'+t+r'\b',note.lower()) and not re.search(r'\b(no|not|without)\s+(?:\w+\s+){0,2}'+t+r'\b',note.lower())]
    if flagged: score+=2; reasons.append('Caregiver reported: '+', '.join(flagged))
    level='High' if score>=4 else 'Medium' if score>=2 else 'Low'
    return {'level':level,'score':score,'reasons':reasons or ['No demonstration thresholds exceeded'], 'model':'Transparent rules v1 • unvalidated'}
