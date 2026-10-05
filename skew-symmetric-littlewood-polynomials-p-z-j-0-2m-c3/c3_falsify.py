import time
import sys
import numpy as np

START = time.monotonic()
DEADLINE = START + 230.0
rng = np.random.default_rng(20260719)


def sequence(free):
    m = len(free) - 1
    a = np.empty(2 * m + 1, dtype=np.int64)
    a[:m + 1] = free
    for j in range(1, m + 1):
        a[m + j] = (-1 if j % 2 else 1) * a[m - j]
    return a


def brute_energy(a):
    # Direct integer autocorrelations, with no FFT or skew-symmetry shortcut.
    a = np.asarray(a, dtype=np.int64)
    return sum(int(np.dot(a[:-r], a[r:])) ** 2
               for r in range(1, len(a)))


def moves(m):
    out = []
    for d in (1, 2):
        for u in range(m + 1):
            for v in range(u, m + 1, d):
                indices = set(range(u, v + 1, d))
                indices |= {2 * m - i for i in tuple(indices)}
                out.append((u, v, d, sorted(indices)))
    return out


def energies(rows):
    rows = np.asarray(rows, dtype=np.int64)
    n = rows.shape[1]
    size = 1 << (2 * n - 1).bit_length()
    f = np.fft.rfft(rows, n=size, axis=1)
    c = np.rint(np.fft.irfft(f * f.conjugate(), n=size, axis=1)
                [:, 1:n]).astype(np.int64)
    return np.sum(c * c, axis=1, dtype=np.int64)


def neighbor_rows(a, mv):
    b = np.broadcast_to(a, (len(mv), len(a))).copy()
    for k, (_, _, _, indices) in enumerate(mv):
        b[k, indices] *= -1
    return b


def report_if_verified(a):
    m = (len(a) - 1) // 2
    n = len(a)
    # Recompute the literal bound; the multiplied comparison is exact.
    e = brute_energy(a)
    bound_numerator = n * n + 16 * n
    if 8 * e <= bound_numerator:
        return False
    if any(int(x) not in (-1, 1) for x in a):
        return False
    if not all(a[m + j] == (-1) ** j * a[m - j]
               for j in range(m + 1)):
        return False
    # Independently verify every hypothesis by direct correlations.
    for _, _, _, indices in moves(m):
        b = a.copy()
        b[indices] *= -1
        if brute_energy(b) < e:
            return False
    # Second explicit computation of both sides.
    second_e = 0
    aa = list(map(int, a))
    for r in range(1, n):
        c = sum(aa[j] * aa[j + r] for j in range(n - r))
        second_e += c * c
    second_bound = n ** 2 / 8 + 2 * n
    if second_e != e or not second_e > second_bound:
        return False
    print("COUNTEREXAMPLE:",
          {"m": m, "a": aa, "E(a)": second_e,
           "claimed_upper_bound": second_bound}, flush=True)
    sys.exit(0)


def sanity():
    known = sequence([1, 1])
    ok1 = list(known) == [1, 1, -1] and brute_energy(known) == 1
    print("Sanity 1: known N=3 autocorrelations and energy:",
          "PASS" if ok1 else "FAIL", flush=True)

    ok2 = True
    for m in range(1, 6):
        mv = moves(m)
        for bits in range(1 << m):
            a = sequence([1 if (bits >> i) & 1 else -1
                          for i in range(m)] + [1])
            rows = np.vstack((a, neighbor_rows(a, mv)))
            fast = energies(rows)
            direct = np.array([brute_energy(b) for b in rows])
            if not np.array_equal(fast, direct):
                ok2 = False
                break
            for b in rows:
                if not all(b[m + j] == (-1) ** j * b[m - j]
                           for j in range(m + 1)):
                    ok2 = False
                    break
    print("Sanity 2: FFT versus direct integer energies and all moves, "
          "all assignments m=1..5:", "PASS" if ok2 else "FAIL", flush=True)
    if not (ok1 and ok2):
        print("SANITY FAILED", flush=True)
        sys.exit(0)


sanity()
exhaustive = {}
random_completed = {}
random_started = {}
stable_tested = 0

# Exhaustive enumeration uses a complete energy table. Flipping the center
# is normalized back to center +1 by a global sign, which preserves energy.
for m in range(1, 13):
    if time.monotonic() >= DEADLINE:
        break
    count = 1 << m
    rows = np.array([
        sequence([1 if (bits >> i) & 1 else -1 for i in range(m)] + [1])
        for bits in range(count)
    ])
    table = energies(rows)
    mv = moves(m)
    masks = []
    for _, _, _, indices in mv:
        mask = sum(1 << i for i in indices if i < m)
        if m in indices:
            mask ^= count - 1
        masks.append(mask)
    masks = np.unique(masks)
    checked = 0
    for bits in range(count):
        if time.monotonic() >= DEADLINE:
            break
        e = int(table[bits])
        stable = np.all(table[bits ^ masks] >= e)
        checked += 1
        if stable:
            stable_tested += 1
            n = 2 * m + 1
            if 8 * e > n * n + 16 * n:
                if not report_if_verified(rows[bits]):
                    print("SANITY FAILED", flush=True)
                    sys.exit(0)
    exhaustive[m] = checked
    if checked != count:
        break

# Independent random starts, with strictly energy-decreasing moves.
# Stop at the deadline, rather than falsely calling an unfinished descent stable.
for m in (16, 24, 32, 48, 64, 96, 128):
    if time.monotonic() >= DEADLINE:
        break
    mv = moves(m)
    random_completed[m] = 0
    random_started[m] = 0
    for trial in range(100):
        if time.monotonic() >= DEADLINE:
            break
        free = rng.choice(np.array([-1, 1], dtype=np.int64), size=m + 1)
        free[m] = 1
        a = sequence(free)
        e = brute_energy(a)
        random_started[m] += 1
        finished = False
        while time.monotonic() < DEADLINE:
            best_e, best_a = e, None
            complete_scan = True
            for lo in range(0, len(mv), 512):
                if time.monotonic() >= DEADLINE:
                    complete_scan = False
                    break
                candidates = neighbor_rows(a, mv[lo:lo + 512])
                vals = energies(candidates)
                k = int(np.argmin(vals))
                if int(vals[k]) < best_e:
                    best_e = int(vals[k])
                    best_a = candidates[k].copy()
            if not complete_scan:
                break
            if best_a is None:
                finished = True
                stable_tested += 1
                n = len(a)
                if 8 * e > n * n + 16 * n:
                    if not report_if_verified(a):
                        print("SANITY FAILED", flush=True)
                        sys.exit(0)
                break
            a, e = best_a, best_e
        if finished:
            random_completed[m] += 1
        else:
            break

cases = sum(exhaustive.values()) + sum(random_completed.values())
print("NO COUNTEREXAMPLE",
      {"exhaustive_assignment_ids": {
          m: f"0..{k - 1} of 0..{(1 << m) - 1}"
          for m, k in exhaustive.items()
      },
       "random_starts_started": random_started,
       "random_stable_endpoints_checked": random_completed,
       "cases_tested": cases,
       "stable_cases_tested": stable_tested,
       "seed": 20260719}, flush=True)
sys.exit(0)