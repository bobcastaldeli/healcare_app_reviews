"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.6
"""

import time
import logging
from typing import Any, Callable, Dict, Tuple
import numpy as np
import pandas as pd
from app_store_scraper import AppStore


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
    for app in parameters['appstoreapps']:
        logger.info(f"Downloading reviews for {app}")
        rvws = AppStore(
            app_name=app,
            country=parameters['country'],
        )
        rvws.review(sleep=1)
        rvws_app = pd.DataFrame(np.array(rvws.reviews), columns=["review"])
        rvws_app["appstore_id"] = app
        reviews_df = pd.concat(
            [
            reviews_df, 
            rvws_app.join(pd.DataFrame(rvws_app.pop("review").to_list()))
            ]
        )
    return reviews_df

        
