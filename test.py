def isAhead(speed, pos1, pos2):
    l1 = speed[1] / speed[0] * (pos2[0] - pos1[0] + speed[1]) + pos1[1] + speed[0]
    l2 = speed[1] / speed[0] * (pos2[0] - pos1[0] - speed[1]) + pos1[1] - speed[0]

    l3 = speed[0] / speed[1] * (- pos2[0] + pos1[0]) + pos1[1]
    l4 = speed[0] / speed[1] * (- pos2[0] + pos1[0]  + 4 * speed[0]) + pos1[1] + 4 * speed[1]

    # print(f"{speed[1]} / {speed[0]} * ({pos2[0]} - {pos1[0]} + {speed[1]}) + {pos1[1]} + {speed[0]}")
    # print(f"{speed[1]} / {speed[0]} * ({pos2[0]} - {pos1[0]} - {speed[1]}) + {pos1[1]} - {speed[0]}")

    # print(f"{speed[0]} / {speed[1]} * ({-pos2[0]} + {pos1[0]}) + {pos1[1]}")
    # print(f"{speed[0]} / {speed[1]} * ({-pos2[0]} + {pos1[0]} + 4 * {speed[0]}) + {pos1[1]} + 4 *{speed[1]}")


    sign1 = 1 if speed[0] > 0 else -1
    sign2 = 1 if speed[1] > 0 else -1
    # print(pos2[1], '\t', sign1, sign2, '\t', l1, l2, l3, l4)

    # print(
    #     l1 * sign1 > pos2[1] * sign1,
    #     l2 * sign1 < pos2[1] * sign1,
    #     l3 * sign2 < pos2[1] * sign2,
    #     l4 * sign2 > pos2[1] * sign2
    # )

    return (
        l1 * sign1 > pos2[1] * sign1
        and l2 * sign1 < pos2[1] * sign1
        and l3 * sign2 < pos2[1] * sign2
        and l4 * sign2 > pos2[1] * sign2
    )



values = [
    {
        "speed": (2.5, -3.8),
        "pos1": (-5,8.3),
        "pos2": (-4,4),
    },
    {
        "speed": (3.2, 1.2),
        "pos1": (-2,8),
        "pos2": (4,10),
    },
    {
        "speed": (-3.5, 1.3),
        "pos1": (20,20),
        "pos2": (10,25),
    },
    {
        "speed": (-3.6, -2),
        "pos1": (20,20),
        "pos2": (12,16),
    },
    {
        "speed": (2.5, -2),
        "pos1": (20,20),
        "pos2": (25,15),
    }
]


for val in values:
    assert isAhead(**val)