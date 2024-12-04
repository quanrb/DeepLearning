from training.segmentation.dense_dataset_definitions import (
    DENSE_DATASET_DEFINITIONS as DEF,
)

CLASS_CHANNEL_LIST = [
    DEF.STEM + DEF.ALL_RESTS_EXCEPT_LARGE + DEF.BARLINE_BETWEEN + DEF.BARLINE_END,
    DEF.NOTEHEADS_ALL,
    DEF.ALL_CLEFS + DEF.ALL_KEYS + DEF.ALL_ACCIDENTALS,
]

CLASS_CHANNEL_MAP = {
    color: idx + 1 for idx, colors in enumerate(CLASS_CHANNEL_LIST) for color in colors
}

CHANNEL_NUM = len(CLASS_CHANNEL_LIST) + 1  # Plus 'background' and 'others' channel.
