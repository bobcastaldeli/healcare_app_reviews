"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import download_appstore_reviews


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=download_appstore_reviews,
                inputs=['parameters'],
                outputs='appstore_reviews_raw',
                name='download_appstore_reviews',
            ),
        ]
    )
