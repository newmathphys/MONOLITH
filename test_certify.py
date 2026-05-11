#!/usr/bin/env python3
import sys; sys.path.insert(0,'src')
from KOKAO_TITAN_v98_ULTRA import MonolithV98, DIM, STABILITY_LIMIT, MU_TARGET
import numpy as np

print("v98 ULTRA CERTIFICATION")
print("-"*45)
m=MonolithV98()
muon=np.zeros(DIM); muon[0]=1.0
for _ in range(52): m.scan(muon)
r,d=m.get_metrics()
print(f"GENESIS:     SRI={r/1e6:.4f} dev={d:.2e} {'OK' if d<STABILITY_LIMIT else 'FAIL'}")
for _ in range(100): m.scan(np.random.randn(DIM)*2.0)
r,d=m.get_metrics()
print(f"NOISE STORM: SRI={r/1e6:.4f} dev={d:.2e} {'OK' if r/1e6>0.99 else 'FAIL'}")
m.nucleus[1:21]=0; m.scan(muon)
r,d=m.get_metrics()
print(f"BIT ROT:     SRI={r/1e6:.4f} dev={d:.2e} {'OK' if d<STABILITY_LIMIT else 'FAIL'}")
print("BARYONIC GOLD")

from KOKAO_TITAN_v99_ATOM import DecaMonolith
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
X,y=load_breast_cancer(return_X_y=True)
X=StandardScaler().fit_transform(X).astype(np.float32)
X_tr,X_te,y_tr,y_te=train_test_split(X,y,test_size=0.3,random_state=42)
m=DecaMonolith(2,X.shape[1]); m.fit(X_tr,y_tr)
p,_=m.predict(X_te)
print(f"\nv99 ATOM: Breast Cancer ACC={accuracy_score(y_te,p):.2%}")
