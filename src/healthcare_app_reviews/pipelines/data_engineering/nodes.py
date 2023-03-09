"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.6
"""

import time
import logging
from typing import Any, Callable, Dict, Tuple, List
import numpy as np
import pandas as pd
from app_store_scraper import AppStore
from google_play_scraper import app, Sort, reviews_all 


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def download_appstore_reviews(parameters: Dict[str, Any]) -> pd.DataFrame:
    """Node for downloading appstore reviews
    Args:
        parameters: A dictionary of parameters.
    Returns:
        pd.DataFrame: The data from the node.
    """
    reviews_df = pd.DataFrame()
    for app, company in zip(parameters['appstoreapps'], parameters['companies']):
        logger.info(f"Downloading reviews for {company}")
        rvws = AppStore(
            app_name=app,
            country=parameters['country'],
        )
        rvws.review(sleep=1)
        rvws_app = pd.DataFrame(np.array(rvws.reviews), columns=["review"])
        rvws_app["company"] = company
        rvws_app["store_id"] = "appstore"
        reviews_df = pd.concat(
            [
            reviews_df, 
            rvws_app.join(pd.DataFrame(rvws_app.pop("review").to_list()))
            ]
        )
    return reviews_df

        
def dowload_googleplay_reviews(parameters: Dict[str, Any]) -> pd.DataFrame:
    """Node for downloading googleplay reviews
    Args:
        parameters: A dictionary of parameters.
    Returns:
        pd.DataFrame: The data from the node.
    """
    reviews_df = pd.DataFrame()
    for app, company in zip(parameters['googleplayapps'], parameters['companies']):
        logger.info(f"Downloading reviews for {company}")
        rvws = reviews_all(
            app_id=app,
            sleep_milliseconds=1,
            country="br",
            lang="pt",
            sort=Sort.NEWEST,
        )

        rvws_df = pd.DataFrame(rvws)
        rvws_df['company'] = company
        rvws_df['store_id'] = 'googleplay'
        reviews_df = pd.concat([reviews_df, rvws_df])
        time.sleep(120)
    return reviews_df


def rename_columns(dataframe: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
    """Node for renaming columns
    Args:
        dataframe: A pandas dataframe.
        parameters: A dictionary of parameters.
    Returns:
        pd.DataFrame: The data from the node.
    """
    reviews_renamed = dataframe.rename(columns=parameters["renamedcolumns"])
    return reviews_renamed


def append_dataframes(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
    """Node for appending dataframes
    Args:
        dataframe1: A pandas dataframe.
        dataframe2: A pandas dataframe.
        parameters: A dictionary of parameters.
    Returns:
        pd.DataFrame: The data from the node.
    """
    # select columns for dataframe1 and dataframe2 at the same time
    dataframe1 = dataframe1[parameters["selectedcolumns"]]
    dataframe2 = dataframe2[parameters["selectedcolumns"]]
    reviews = pd.concat([dataframe1, dataframe2])
    return reviews
