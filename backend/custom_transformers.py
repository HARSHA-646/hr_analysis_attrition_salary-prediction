import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class SelectiveTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, transformer=None, columns=None, all_columns=None):
        self.transformer = transformer
        self.columns = columns
        self.all_columns = all_columns

    def _to_dataframe(self, X):
        if isinstance(X, pd.DataFrame):
            return X.copy()

        if self.all_columns is not None:
            return pd.DataFrame(X, columns=self.all_columns)

        n = X.shape[1]
        cols = [f"col_{i}" for i in range(n)]
        return pd.DataFrame(X, columns=cols)

    def fit(self, X, y=None):
        X_df = self._to_dataframe(X)
        if self.columns:
            arr = X_df[self.columns].values
            self.transformer.fit(arr)
        return self

    def transform(self, X):
        X_df = self._to_dataframe(X)
        if not self.columns:
            return X_df

        arr = X_df[self.columns].values
        trans = self.transformer.transform(arr)

        X_df.loc[:, self.columns] = pd.DataFrame(
            trans, columns=self.columns, index=X_df.index
        )
        return X_df

    def inverse_transform(self, X):
        X_df = self._to_dataframe(X)
        if not self.columns:
            return X_df

        arr = X_df[self.columns].values
        inv = self.transformer.inverse_transform(arr)

        X_df.loc[:, self.columns] = pd.DataFrame(
            inv, columns=self.columns, index=X_df.index
        )
        return X_df
