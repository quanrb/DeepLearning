from typing import Any

import numpy as np
from tqdm import tqdm

def _calc_number_of_files_to_take(
    data_sources: list[dict[str, Any]], number_of_files: int
) -> list[int]:
    files_to_take = [0 for _ in data_sources]
    while number_of_files > 0:
        total_weight = sum([s["weight"] for s in data_sources])
        number_of_files_per_source = [
            int(number_of_files * s["weight"] / total_weight) for s in data_sources
        ]
        number_of_files_per_source[-1] = number_of_files - sum(number_of_files_per_source[:-1])

        max_available_ratios = []
        for i, source in enumerate(data_sources):
            max_available_ratios.append(min(source["len"] / number_of_files_per_source[i], 1))

        limiting_ratio = min(max_available_ratios)
        number_of_files_per_source = [int(limiting_ratio * n) for n in number_of_files_per_source]

        for i, n in enumerate(number_of_files_per_source):
            number_of_files -= n
            ds_id = data_sources[i]["id"]
            files_to_take[ds_id] += n
            data_sources[i]["len"] -= n

        data_sources = [s for s in data_sources if s["len"] > 0]
    return files_to_take


def _take_all_training_sets(indexes: list[list[str]]) -> list[str]:
    train_index = []
    for index in indexes:
        train_index += index
    np.random.shuffle(train_index)
    return train_index

"""
Add verbose
"""

def mix_training_sets(
    data_sources: list[list[str]], weights: list[float], number_of_files: int
) -> list[str]:
    # We want the training and validation sets to be the same for each run
    # if the input hasn't changed and therefore set the seed here.
    np.random.seed(1720697007)
    
    print("Shuffling data sources...")
    for data_source in tqdm(data_sources, desc="Shuffling data sources"):
        np.random.shuffle(data_source)
    
    if number_of_files < 0:
        print("Taking all training sets...")
        return _take_all_training_sets(data_sources)
    
    print(f"Calculating number of files to take from each data source for a total of {number_of_files} files...")
    number_of_files_per_index = _calc_number_of_files_to_take(
        [
            {"len": len(index), "weight": weights[i], "id": i}
            for i, index in enumerate(data_sources)
        ],
        number_of_files,
    )
    
    print(f"Number of files per index: {number_of_files_per_index}")
    
    mixed_source = []
    for i, data_source in enumerate(tqdm(data_sources, desc="Mixing data sources")):
        mixed_source += data_source[: number_of_files_per_index[i]]
    
    print("Shuffling mixed source...")
    np.random.shuffle(mixed_source)
    
    print("Mixing complete.")
    return mixed_source
