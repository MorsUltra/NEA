from initialising.table_init import Tables

t = Tables()
print(t.UDslice_Ocorner_pruning_table)

# @classmethod
# def make_edge4_edge8_prune(cls):
#     edge4_edge8_prune = [-1] * (cls.EDGE4 * cls.EDGE8)
#     edge4_edge8_prune[0] = 0
#     count, depth = 1, 0
#     while count < cls.EDGE4 * cls.EDGE8:
#         for i in range(cls.EDGE4 * cls.EDGE8):
#             if edge4_edge8_prune[i] == depth:
#                 m = [
#                     cls.edge4_move[i // cls.EDGE8][j] * cls.EDGE8
#                     + cls.edge8_move[i % cls.EDGE8][j]
#                     for j in range(18)
#                 ]
#                 for x in m:
#                     if edge4_edge8_prune[x] == -1:
#                         count += 1
#                         edge4_edge8_prune[x] = depth + 1
#         depth += 1
#     return PruningTable(edge4_edge8_prune, cls.EDGE8)
