from mealpy.EHO import *

def elephant(dim, max_iterations, alpha, beta, n_clans, obj_func, pop_size):
    lb = [0] * dim
    ub = [1] * dim

    eho = BaseEHO(obj_func, lb, ub, False, max_iterations, pop_size, alpha, beta, n_clans)
    best_pos1, best_fit1, list_loss1 = eho.train()

    return best_pos1