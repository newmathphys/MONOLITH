# KOKAO PHYSICAL MEMORY — Vital Kalinouski 2026
#!/usr/bin/env python3
"""
KOKAO TITAN v99 ATOM — Multi-Nuclei Quantum Classifier
===========================================================
N ядер Monolith → матрица резонансов → argmax → классификация
"""
import numpy as np, warnings; warnings.filterwarnings('ignore')

MU_TARGET = (625/3) - np.power(6, 1/4)
STABILITY_LIMIT = 3e-7

class MonolithNucleus:
    """Одно ядро — детектор одного эталона"""
    def __init__(self, dim):
        self.dim = dim
        self.nucleus = np.random.randn(dim)
        self.nucleus /= np.linalg.norm(self.nucleus) + 1e-12
        self.m = np.zeros(dim)
        self.step = 0

    def get_sri(self):
        l3 = np.power(np.sum(np.abs(self.nucleus)**3), 1/3)
        l1 = np.sum(np.abs(self.nucleus)) + 1e-12
        return (l3/l1)**3

    def update(self, data, freeze=True):
        """Обучить ядро на одном примере"""
        self.step += 1
        nrm = np.linalg.norm(data)
        if nrm < 1e-12: return
        x = np.asarray(data, dtype=np.float32) / nrm
        sim_raw = float(np.dot(self.nucleus, x))

        sri_val = self.get_sri()
        frozen = sri_val > 0.98 and freeze
        if not frozen:
            beta = 0.9
            eta = float(np.tanh((8/7) * np.abs(1 - abs(sim_raw))))
            if abs(sim_raw) > 0.08: eta *= 1.5
            v_eff = x - (sim_raw * self.nucleus)
            self.m = beta * self.m + (1-beta) * np.sign(v_eff) * (np.abs(v_eff)**3)
            self.nucleus += self.m * eta
            self.nucleus /= np.linalg.norm(self.nucleus) + 1e-12

    def similarity(self, data):
        """Косинусное сходство с ядром"""
        nrm = np.linalg.norm(data)
        if nrm < 1e-12: return 0.0
        return float(np.dot(self.nucleus, data / nrm))


class DecaMonolith:
    """Многоядерный классификатор на резонансах"""
    def __init__(self, n_classes, dim):
        self.n_classes = n_classes
        self.dim = dim
        self.nuclei = [MonolithNucleus(dim) for _ in range(n_classes)]

    def fit(self, X, y):
        """Обучить каждое ядро на своих примерах"""
        for x, yt in zip(X, y):
            self.nuclei[yt].update(x)

    def predict(self, X):
        """Выбрать класс с максимальным резонансом"""
        preds = []
        confs = []
        for x in X:
            sims = np.array([n.similarity(x) for n in self.nuclei])
            preds.append(int(np.argmax(sims)))
            confs.append(float(np.max(sims)))
        return np.array(preds), np.array(confs)

    def predict_with_rejection(self, X, threshold=0.3):
        """Классификация с отклонением: если все sims < threshold → VOID"""
        preds = []
        for x in X:
            sims = np.array([n.similarity(x) for n in self.nuclei])
            max_sim = float(np.max(sims))
            if max_sim < threshold:
                preds.append(-1)  # VOID
            else:
                preds.append(int(np.argmax(sims)))
        return np.array(preds)


# ═══════════════════════════════════════════════════════════════
# ТЕСТЫ
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("="*65)
    print("KOKAO TITAN v99 ATOM — Multi-Nuclei Classifier")
    print("="*65)

    # 1. BREAST CANCER (2 класса) — улучшение Dual-Core
    print("\n1️⃣  BREAST CANCER (2 nuclei):")
    from sklearn.datasets import load_breast_cancer
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, f1_score

    X, y = load_breast_cancer(return_X_y=True)
    X = StandardScaler().fit_transform(X).astype(np.float32)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

    model = DecaMonolith(2, X.shape[1])
    model.fit(X_tr, y_tr)
    preds, confs = model.predict(X_te)
    acc = accuracy_score(y_te, preds)
    f1 = f1_score(y_te, preds)
    print(f"  ACC={acc:.2%}  F1={f1:.4f}")

    # 2. MNIST (10 классов) — Дека-Монолит
    print("\n2️⃣  MNIST (10 nuclei):")
    try:
        from sklearn.datasets import fetch_openml
        from sklearn.metrics import accuracy_score
        import time

        d = fetch_openml('mnist_784', parser='auto', as_frame=False)
        X = np.asarray(d.data[:5000], dtype=np.float32) / 255.0
        y = d.target[:5000].astype(int)

        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

        model10 = DecaMonolith(10, 784)
        t0 = time.time()
        model10.fit(X_tr, y_tr)
        t1 = time.time()

        preds, confs = model10.predict(X_te)
        acc = accuracy_score(y_te, preds)
        print(f"  ACC={acc:.2%}  Время: {t1-t0:.1f}s  Ядер: 10")

        # С отклонением VOID
        preds_r = model10.predict_with_rejection(X_te, threshold=0.3)
        valid = preds_r != -1
        if valid.sum() > 0:
            acc_r = accuracy_score(y_te[valid], preds_r[valid])
            rejection = (1 - valid.sum()/len(preds_r))*100
            print(f"  С отклонением: ACC={acc_r:.2%}  Отвергнуто: {rejection:.1f}%")
    except Exception as e:
        print(f"  SKIP: {e}")

    # 3. OOD DETECTION (rejection)
    print("\n3️⃣  OOD DETECTION (MNIST vs noise):")
    try:
        noise = np.random.randn(500, 784).astype(np.float32)
        preds_r = model10.predict_with_rejection(noise, threshold=0.3)
        rejected = (preds_r == -1).mean() * 100
        print(f"  Шум отвергнут: {rejected:.1f}% {'✅' if rejected>80 else '❌'}")
    except: pass

    # 4. CONTINUAL LEARNING (последовательное обучение)
    print("\n4️⃣  CONTINUAL LEARNING (5 tasks → 5 nuclei):")
    try:
        # 5 бинарных задач из MNIST
        tasks = [(0,1),(2,3),(4,5),(6,7),(8,9)]
        cl_model = DecaMonolith(2, 784)
        for ti, (c1, c2) in enumerate(tasks):
            mask = (y == c1) | (y == c2)
            Xt, yt = X[mask], (y[mask] == c2).astype(int)
            Xt_tr, Xt_te, yt_tr, yt_te = train_test_split(Xt, yt, test_size=0.3, random_state=42)
            cl_model.fit(Xt_tr, yt_tr)
            preds_t, _ = cl_model.predict(Xt_te)
            acc_t = accuracy_score(yt_te, preds_t)
            print(f"  Task {ti+1}: classes {c1}/{c2} → ACC={acc_t:.2%}", end='')
            if ti == len(tasks)-1:
                # Проверка на всех предыдущих
                accs_prev = []
                for pj, (pc1, pc2) in enumerate(tasks):
                    mask_p = (y == pc1) | (y == pc2)
                    Xp, yp = X[mask_p], (y[mask_p] == pc2).astype(int)
                    _, Xp_te, _, yp_te = train_test_split(Xp, yp, test_size=0.3, random_state=42)
                    preds_p, _ = cl_model.predict(Xp_te)
                    accs_prev.append(accuracy_score(yp_te, preds_p))
                print(f"  → Avg prev ACC={np.mean(accs_prev):.2%} CFR={accs_prev[0]-accs_prev[-1]:.4f}")
    except Exception as e:
        print(f"  SKIP: {e}")
