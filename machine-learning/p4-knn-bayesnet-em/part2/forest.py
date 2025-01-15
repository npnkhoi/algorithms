"""
Random Forest of Chow Liu Trees
"""

from CLT_class import CLT
from MIXTURE_CLT import MIXTURE_CLT
from concurrent.futures import ProcessPoolExecutor

class CLTForest(MIXTURE_CLT):
    def __init__(self, n_estimators: int, n_hidden: int):
        """
        n_hidden: the number of mutual information variables to set to 0
        """
        self.clt_list = [
            CLT(n_hidden=n_hidden)
            for _ in range(n_estimators)
        ]
        self.n_components = n_estimators
        self.lambda_ = [1/n_estimators for _ in range(n_estimators)]

    def call_learn(self, clt, dataset):
        return clt.learn(dataset)

    def learn(self, dataset):
        # with ProcessPoolExecutor() as executor:
        #     executor.map(self.call_learn, self.clt_list, [dataset for _ in range(self.n_components)])
        for tree in self.clt_list:
            tree.learn(dataset)

    # computeLL is inherited


