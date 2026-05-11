# KOKAO PHYSICAL MEMORY

**Author:** Vital Kalinouski  
**License:** GNU GPL v3.0  
**Tag:** v100-PRO-GOLDEN  
**Bitcoin OTS:** `11c6eaaaa0288344f627d335c3c991757223007f71a679048fbf4c770d48b6bb`

---

## О проекте

Физическая память на основе SRI (Sparsity Resonance Index).
Две версии — для спайк-детекции и мульти-класс классификации.

```
v98 ULTRA — барионный монолит (одно ядро, SRI-детектор)
v99 ATOM  — мульти-ядерный классификатор (N ядер, argmax)
```

Весь код принадлежит Vital Kalinouski и может быть свободно
использован в других проектах согласно GNU GPL v3.0.

## Установка

```bash
pip install numpy scikit-learn
```

## Использование

### v98 ULTRA — Спайк-детекция

```python
from src.KOKAO_TITAN_v98_ULTRA import MonolithV98, DIM

spec = MonolithV98()
muon = [0]*DIM; muon[0] = 1.0
for _ in range(52): spec.scan(muon)
r, d = spec.get_metrics()
print(f"SRI={r/1e6:.4f} dev={d:.2e}")
```

### v99 ATOM — Классификация

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

| Метрика | Значение |
|---------|----------|
| MU_TARGET | 625/3 − ⁴√6 = 206.7682488 |
| SRI | (L3/L1)³ [0, 1] |
| STABILITY_LIMIT | 3e-7 |
| GENESIS dev | 6.20e-10 |
| NOISE STORM | ✅ SRI > 0.99 |
| BIT ROT (20 бит) | ✅ Восстановление за 1 шаг |
| Breast Cancer ACC | 93.57% |
| OOD Rejection | 100% |
| CFR | −0.26 (рост памяти) |

## Сертификация

```bash
python3 test_certify.py
```

```
GENESIS:      SRI=1.0000 dev=6.20e-10  💎
NOISE STORM:  SRI=1.0000 dev=6.20e-10  ✅
BIT ROT:      SRI=1.0000 dev=6.20e-10  ⚕️
BARYONIC GOLD
v99 ATOM: Breast Cancer ACC=93.57%
```

## Структура

```
MONOLITH/
├── src/
│   ├── KOKAO_TITAN_v98_ULTRA.py   — барионный монолит (170 строк)
│   └── KOKAO_TITAN_v99_ATOM.py    — мульти-ядерный классификатор (179 строк)
└── test_certify.py                  — сертификация
```

## Хэш доказательства

```
Файл: kokao_titan_final_release.tar.gz
SHA256: 11c6eaaaa0288344f627d335c3c991757223007f71a679048fbf4c770d48b6bb
OTS:    kokao_titan_final_release.tar.gz.ots
Дата:   2026-05-11 (заверено Bitcoin)
```

## Лицензия

```
Copyright (c) 2026 Vital Kalinouski

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License.

You may use this code in your own projects.
Credit appreciated but not required.
```
