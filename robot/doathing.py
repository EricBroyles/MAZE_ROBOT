# import nashpy as nash
# import numpy as np

# list_prices = [150, 200, 250, 300]
# matrix = []

# for r, p_a in enumerate(list_prices):
#     row = []
#     for c, p_b in enumerate(list_prices):
#         prof_a = (p_a - 50) * (550 - (p_a + p_b))
#         prof_b = (p_b - 50) * (550 - (p_a + p_b))
#         row.append([prof_a, prof_b])
#     matrix.append(row)

# for item in matrix:
#     print(item)

# game = nash.game(matrix)
# equilibria = game.support_enumeration()
# list(equilibria)