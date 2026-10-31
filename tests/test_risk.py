import unittest
from risk import assess
class RiskTests(unittest.TestCase):
 def setUp(self): self.d=dict(hr=72,spo2=98,temp=36.7,rr=16,sys=118)
 def test_stable(self): self.assertEqual(assess(self.d)['level'],'Low')
 def test_hypoxia(self): self.assertEqual(assess(dict(self.d,spo2=88))['level'],'High')
 def test_fever_and_note(self): self.assertEqual(assess(dict(self.d,temp=38.5),'Feels dizzy')['level'],'High')
 def test_negation(self): self.assertEqual(assess(self.d,'No chest pain')['level'],'Low')
 def test_invalid(self):
  for v in [None,True,float('nan'),101]:
   with self.assertRaises((ValueError,TypeError)): assess(dict(self.d,spo2=v))
