import numpy as np


def array_reshape(data, n_point):
    return np.reshape(
        data[:data.size - (data.size % n_point)],
        (-1, n_point)
    )


def data_transform_array(game_list, funcs, arg_labels=('X', 'Y', 'Z')):
    v_funcs = [np.vectorize(func) for func in funcs]
    temp = [func(game_list) for func in v_funcs]

    d_type = [(arg, arr.dtype) for arr, arg in zip(temp, arg_labels)]
    game_results = np.empty(len(game_list), dtype=d_type)

    for arr, arg in zip(temp, arg_labels):
        game_results[arg] = arr
    return game_results
