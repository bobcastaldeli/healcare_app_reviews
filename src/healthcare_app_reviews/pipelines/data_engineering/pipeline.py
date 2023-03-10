"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    download_appstore_reviews, 
    dowload_googleplay_reviews,
    rename_columns,
    append_dataframes,
    clean_review
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=download_appstore_reviews,
                inputs=['parameters'],
                outputs='appstore_reviews_raw',
                name='download_appstore_reviews',
            ),
            node(
                func=dowload_googleplay_reviews,
                inputs=['parameters'],
                outputs='googleplay_reviews_raw',
                name='download_googleplay_reviews',
            ),
            node(
                func=rename_columns,
                inputs=['googleplay_reviews_raw', 'parameters'],
                outputs='googleplay_reviews_intermediate',
                name='rename_googleplay_columns',
            ),
            node(
                func=append_dataframes,
                inputs=['appstore_reviews_raw', 'googleplay_reviews_intermediate', 'parameters'],
                outputs='reviews_primary',
                name='append_dataframes',
            ),
            node(
                func=clean_review,
                inputs=['reviews_primary', 'parameters'],
                outputs='reviews_features',
                name='clean_review',
            )
        ]
    )
