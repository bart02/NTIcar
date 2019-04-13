M = {1: {2: 'r', 4: 'l', 5: 'n'},
     2: {1: 'l'},
     3: {5: 'l', 6: 'l'},
     4: {5: 'r', 7: 'n', 1: 'v'},
     5: {1: 'v', 3: 'r', 4: 'l', 7: 'n'},
     6: {3: 'r', 7: 'l', 8: 'n'},
     7: {5: 'v', 4: 'l', 6: 'r'},
     8: {6: 'v'}}

naprs = {'l': {'n': 'tl', 'v': 'tr', 'l': 'tv'},
         'r': {'n': 'tr', 'v': 'tl', 'r': 'tv'},
         'v': {'l': 'tl', 'r': 'tr', 'v': 'tv'},
         'n': {'r': 'tl', 'l': 'tr', 'n': 'tv'}}

changedots = {(1, 4): 'n',
              (4, 7): 'r',
              (6, 3): 'l',
              (5, 3): 'l'}


def solve(route):
    turns = []
    print('set car on', M[ route[0] ][ route[1] ])
    napr = M[ route[0] ][ route[1] ]
    for i in range(len(route) - 1):
        needn = M[ route[i] ][ route[i+1] ]

        print(route[i], route[i+1] , naprs[napr][needn])
        turns.append(naprs[napr][needn])

        napr = needn
        if (route[i], route[i+1] ) in changedots:
            napr = changedots[(route[i], route[i+1] )]
    print('car will turned on', napr)
    return turns


# print(solve(r))