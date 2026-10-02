import json


def T(v):
    r = len(v)
    return [
        v[h] ^ (v[(h - 1) % r] & v[(h + 1) % r])
        for h in range(r)
    ]


def changed(v):
    tv = T(v)
    return [h for h in range(len(v)) if tv[h] != v[h]]


def D(v):
    return len(changed(v))


def wt(v):
    return sum(v)


def path_after(v, h):
    return [v[(h + k) % len(v)] for k in range(1, len(v))]


def main():
    witness = {
        "operation": "forward",
        "x": [0, 1, 0, 0, 1],
        "z": [1, 1, 0, 1, 0, 0, 1],
        "i": 0,
        "j": 0,
        "c": 0,
        "d": 0,
        "u": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        "relation": "T²(u)=u",
        "actual": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
        "claimed": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    }

    def reject(reason):
        print("REFUTATION REJECTED: " + reason)

    x, z = witness["x"], witness["z"]
    i, j, c, d = (witness[k] for k in ("i", "j", "c", "d"))

    if witness["operation"] != "forward":
        reject("Reported operation is not forward.")
        return

    for name, v, h in (("x", x, i), ("z", z, j)):
        if not isinstance(v, list) or any(
            type(bit) is not int or bit not in (0, 1) for bit in v
        ):
            reject(name + " is not a binary word.")
            return
        if len(v) < 5:
            reject(name + " has length less than five.")
            return
        if type(h) is not int or not 0 <= h < len(v):
            reject("Selected position in " + name + " is invalid.")
            return
        tv = T(v)
        if T(tv) != v:
            reject(name + " does not satisfy T²(v)=v.")
            return
        if tv == v:
            reject(name + " does not have exact temporal period two.")
            return
        if tv[h] == v[h]:
            reject("Selected position in " + name + " is not changed.")
            return

    if any(type(bit) is not int or bit not in (0, 1) for bit in (c, d)):
        reject("c and d must be binary entries.")
        return

    a, b = x[i], z[j]
    P, Q = path_after(x, i), path_after(z, j)
    u = P + [c] + Q + [d]
    if u != witness["u"]:
        reject("Reported u is not the stipulated concatenation P c Q d.")
        return

    tx, tz, tu = T(x), T(z), T(u)
    actual = {
        "T²(u)": T(tu),
        "T(u)≠u": tu != u,
        "D(u)": D(u),
        "wt(u)": wt(u),
        "wt(T(u))": wt(tu),
        "temporal_weight_sum": wt(u) + wt(tu),
        "unordered_temporal_weight_pair": sorted([wt(u), wt(tu)]),
    }
    claimed_wt = wt(x) + wt(z) - a - b + c + d
    claimed_twt = wt(tx) + wt(tz) + a + b - c - d
    claimed = {
        "T²(u)": u,
        "T(u)≠u": True,
        "D(u)": D(x) + D(z),
        "wt(u)": claimed_wt,
        "wt(T(u))": claimed_twt,
        "temporal_weight_sum": wt(x) + wt(tx) + wt(z) + wt(tz),
        "unordered_temporal_weight_pair": sorted([claimed_wt, claimed_twt]),
    }

    violated = [key for key in claimed if actual[key] != claimed[key]]
    if not violated:
        reject("All hypotheses hold, but no forward conclusion is violated.")
        return

    print("REFUTATION CONFIRMED: " + json.dumps({
        "witness": witness,
        "computed_actual_side": actual,
        "literal_claimed_side": claimed,
        "violated_conclusions": violated,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()