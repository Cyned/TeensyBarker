import numpy as np
import pandas as pd

from app import basic_logger as logger


def pd_to_parquet(df: pd.DataFrame, path: str, **kwargs) -> None:
    """
    Save parquet file
    :param df: data frame to save in parquet
    :param path: path to the parquet file
    :param kwargs: the same parameters as for pandas.read_parquet
    """
    def replace_object_array(array):
        return [replace_object_array(element) if len(element) and isinstance(element[0], np.ndarray) else element
                for element in array]

    new_df = df.apply(
        lambda column: replace_object_array(column) if isinstance(column[0], np.ndarray) else column, raw=True,
    )
    new_df.to_parquet(path, **kwargs)
    logger.info(f'Save parquet: {path}')


def read_parquet(path: str) -> pd.DataFrame:
    """
    Read parquet file
    :param path: path to the parquet file
    :return: data frame
    """
    data = pd.read_parquet(path)
    logger.info(f'Read parquet: {path}')
    return data


def flatten_paragraphs(column: pd.Series) -> pd.Series:
    """
    Flattens paragraphs from lists of lists to lists
    :param column: series with tokenized texts like sent_x, sent_y or kinds from full_df dataset
    :return: modified series
    """
    return column.apply(lambda text: [sentence for paragraph in text for sentence in paragraph])
