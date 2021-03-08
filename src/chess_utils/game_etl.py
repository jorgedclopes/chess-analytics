from builtins import function

import numpy as np
from typing import List


def array_reshape(data: np.ndarray, n_point: int) -> np.ndarray:
    """
    Split an np array into np.ndarray where each row has n_points.

    Parameters
    ----------
    data : np.ndarray
        array with data
    n_point : int
        number of points per row

    Returns
    -------
        np.ndarray with rows of n_point elements
    """
    return np.reshape(
        data[:data.size - (data.size % n_point)],
        (-1, n_point)
    )


def data_transform_array(data_list: list, funcs: List[function], arg_labels=None):
    """
    This function takes a list of data and applies a list of functions.
    The functions are applied to each game and labeled according to arg_labels.
    This function helps to transform the data.
    The initial purpose of this function was to prepare data to plot.
    but we can also use it to prepare for analysis.

    Parameters
    ----------
    data_list : list
        raw data of list of games
    funcs : list
        list of functions to be applied to the games list
    arg_labels : list
        list of labels for the np.array columns

    Returns
    -------
        np.array with columns transformed by funcs
    """
    if arg_labels is None:
        arg_labels = ['X', 'Y', 'Z']
    v_funcs = [np.vectorize(func) for func in funcs]
    temp = [func(data_list) for func in v_funcs]

    d_type = [(arg, arr.dtype) for arr, arg in zip(temp, arg_labels)]
    game_results = np.empty(len(data_list), dtype=d_type)

    for arr, arg in zip(temp, arg_labels):
        game_results[arg] = arr
    return game_results


def get_result_list(game_list: list, player_name: str) -> np.ndarray:
    """

    Parameters
    ----------
    game_list : list
        list of games
    player_name : str
        name of the player for which we what the results

    Returns
    -------
        np.ndarray
            Get number of games per game result
    """
    list_result = [game.get_result(player_name) for game in game_list]
    return np.unique(list_result, return_counts=True)
