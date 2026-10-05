from collections import deque
from math import gcd


def main():
    witness = (3, 3, 1, 1)
    p, q, r, s = witness

    if not all(type(x) is int for x in witness):
        print("REFUTATION REJECTED: witness entries must be integers")
        return
    if not (p >= 2 and q >= 2 and 1 <= r < q and 1 <= s < p):
        print("REFUTATION REJECTED: witness violates the parameter hypotheses")
        return

    # C_i is represented by i; D_j is represented by p + j.
    states = tuple(range(p + q))
    a = tuple(
        (x + 1) % p if x < p else p + ((x - p + 1) % q)
        for x in states
    )
    b = tuple(
        p + r if x == 0 else s if x == p else x
        for x in states
    )

    if any(y not in states for mapping in (a, b) for y in mapping):
        print("REFUTATION REJECTED: constructed maps are not total state maps")
        return
    if any(b[b[x]] != b[x] for x in states):
        print("REFUTATION REJECTED: constructed b is not idempotent")
        return
    if len(set(b)) != p + q - 2:
        print("REFUTATION REJECTED: constructed b has the wrong image size")
        return

    # Exhaustive BFS on images of the full state set under words.
    # Applying each next letter to the current image implements left-to-right
    # word action. Every reachable image is visited; a singleton is a reset.
    start = frozenset(states)
    queue = deque([(start, 0)])
    seen = {start}
    minimum_length = None

    while queue:
        image, length = queue.popleft()
        if len(image) == 1:
            minimum_length = length
            break
        for mapping in (a, b):
            next_image = frozenset(mapping[x] for x in image)
            if next_image not in seen:
                seen.add(next_image)
                queue.append((next_image, length + 1))

    actual_exists = minimum_length is not None
    claimed_exists = gcd(p, q, r + s) == 1
    claimed_bound = (p + q - 1) ** 2

    equivalence_fails = actual_exists != claimed_exists
    bound_fails = claimed_exists and (
        minimum_length is None or minimum_length > claimed_bound
    )

    if equivalence_fails or bound_fails:
        print(
            f"REFUTATION CONFIRMED: {witness}; "
            f"actual: reset_exists={actual_exists}, "
            f"minimum_length={minimum_length}; "
            f"claimed: reset_exists={claimed_exists}, "
            f"length_at_most={claimed_bound if claimed_exists else 'not required'}"
        )
    else:
        print("REFUTATION REJECTED: witness satisfies the claim's conclusion")


if __name__ == "__main__":
    main()