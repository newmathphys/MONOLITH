# KOKAO PHYSICAL MEMORY v98/v99

**Baryonic Monolith + Multi-Nuclei Classifier**

Две версии: одна для спайк-детекции, вторая для мульти-класс классификации.

## Установка
```bash
pip install numpy scikit-learn
```

## Использование

### v98 ULTRA — Барионный монолит (спайк-детекция)
```python
from src.KOKAO_TITAN_v98_ULTRA import MonolithV98, DIM

spec = MonolithV98()
muon = [0]*DIM; muon[0] = 1.0
for _ in range(52): spec.scan(muon)
r, d = spec.get_metrics()
print(f"SRI={r/1e6:.4f} dev={d:.2e}")
```

### v99 ATOM — Мульти-ядерный классификатор
```python
from src.KOKAO_TITAN_v99_ATOM import DecaMonolith
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X = StandardScaler().fit_transform(X).astype(float)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)
model = DecaMonolith(2, X.shape[1])
model.fit(X_tr, y_tr)
preds, _ = model.predict(X_te)
print(f"ACC={sum(preds==y_te)/len(y_te):.2%}")
```

## Метрики
- **MU_TARGET** = 625/3 − ⁴√6 = 206.7682488
- **SRI** = (L3/L1)³ [0, 1]
- **STABILITY_LIMIT** = 3e-7
- **CFR** = 0 (нет забывания — каждое ядро независимо)

## Author
**Vital Kalinouski**

## Architecture
```
v98 ULTRA (одно ядро)   →  SRI-детектор, baryonic freeze
v99 ATOM  (N ядер)      →  multi-nuclei классификатор
```

## Сертификация v98
```
GENESIS:      SRI=1.0000  dev=6.20e-10  MUON
NOISE STORM:  SRI=1.0000  dev=6.20e-10  SHIELD
BIT ROT:      SRI=1.0000  dev=6.20e-10  HEALED
```

## Результаты v99
```
Breast Cancer: 93.57%
OOD Rejection: 100%
CFR:           -0.26 (рост памяти)
```

## Author
**Vital Kalinouski**

## License
MIT
