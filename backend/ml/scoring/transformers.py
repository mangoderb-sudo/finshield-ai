import numpy as np

from sklearn.base import (
    BaseEstimator,
    TransformerMixin
)


class FeatureEngineeringTransformer(
    BaseEstimator,
    TransformerMixin
):

    # =================================================
    # FIT
    # =================================================

    def fit(self, X, y=None):

        return self

    # =================================================
    # TRANSFORM
    # =================================================

    def transform(self, X):

        X = X.copy()

        # =============================================
        # EXT SOURCE FEATURES
        # =============================================

        ext_sources = [
            "EXT_SOURCE_1",
            "EXT_SOURCE_2",
            "EXT_SOURCE_3"
        ]

        X["EXT_SOURCE_MEAN"] = (
            X[ext_sources]
            .mean(axis=1)
        )

        X["EXT_SOURCE_MAX"] = (
            X[ext_sources]
            .max(axis=1)
        )

        X["EXT_SOURCE_MIN"] = (
            X[ext_sources]
            .min(axis=1)
        )

        X["EXT_SOURCE_PRODUCT"] = (
            X["EXT_SOURCE_1"]
            *
            X["EXT_SOURCE_2"]
            *
            X["EXT_SOURCE_3"]
        )

        # =============================================
        # RATIOS
        # =============================================

        X["GOODS_CREDIT_RATIO"] = (
            X["AMT_GOODS_PRICE"]
            /
            X["AMT_CREDIT"]
        )

        X["DOWN_PAYMENT_RATIO"] = (
            (
                X["AMT_CREDIT"]
                -
                X["AMT_GOODS_PRICE"]
            )
            /
            X["AMT_CREDIT"]
        )

        X["ANNUITY_CREDIT_RATIO"] = (
            X["AMT_ANNUITY"]
            /
            X["AMT_CREDIT"]
        )

        # =============================================
        # EMPLOYMENT FEATURES
        # =============================================

        X["EMPLOYMENT_YEARS"] = (
            np.abs(X["DAYS_EMPLOYED"])
            / 365
        )

        X["EMPLOYMENT_AGE_RATIO"] = (
            np.abs(X["DAYS_EMPLOYED"])
            /
            np.abs(X["DAYS_BIRTH"])
        )

        # =============================================
        # EDUCATION
        # =============================================

        low_education = [
            "Lower secondary",
            "Secondary / secondary special"
        ]

        X["LOW_EDUCATION"] = (
            X["NAME_EDUCATION_TYPE"]
            .isin(low_education)
            .astype(int)
        )

        return X