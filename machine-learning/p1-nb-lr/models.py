import numpy as np
from typing import Dict
# import wandb

LOG_FREQ = 1


class Model:
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict:
        y_pred = self.predict(X)
        precision = np.mean(y[y_pred == 1] == 1)
        recall = np.mean(y_pred[y == 1] == 1)
        return {
            'accuracy': np.mean(y_pred == y),
            'precision': precision,
            'recall': recall,
            'f1': 2 * precision * recall / (precision + recall)
        }
    
class LogisticRegression(Model):

    def __init__(self, lr: float, n_iter: int, lamb: float, log_id: str, min_delta: float=1e-6, patience: int=20):
        self.lr = lr
        self.n_iter = n_iter
        self.lamb = lamb
        self.w = None # containing the bias
        self.log_id = log_id
        self.min_delta = min_delta
        self.patience = patience
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))
    
    def fit(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray):
        # weight initialization
        _, v = X_train.shape
        self.w = np.zeros(v)

        train_losses, val_losses, train_acc, val_acc = [], [], [], []
        
        for iter in range(self.n_iter):
            # update
            y_pred = self._sigmoid(X_train @ self.w)
            train_error = y_train - y_pred
            grad = X_train.T @ train_error
            self.w += self.lr * (grad - self.lamb * self.w)

            # log errors
            
            if (iter + 1) % LOG_FREQ == 0:
                y_val_pred = self._sigmoid(X_val @ self.w)
                val_error = y_val - y_val_pred
                # wandb.log(
                #     {
                #         f'lr={self.lr}_lambda={self.lamb}/{self.log_id} train_error': np.mean(train_error ** 2),
                #         f'lr={self.lr}_lambda={self.lamb}/{self.log_id} val_error': np.mean(val_error ** 2),
                #     },
                #     # step=iter
                # )
                train_losses.append(np.mean(train_error ** 2))
                val_losses.append(np.mean(val_error ** 2))
                pred = (y_pred > 0.5).astype(int)
                train_acc.append(np.mean(pred == y_train))
                val_pred = (y_val_pred > 0.5).astype(int)
                val_acc.append(np.mean(val_pred == y_val))
            
            if iter > 2 * self.patience and np.mean(val_losses[-self.patience:]) - np.mean(val_losses[-2*self.patience:-self.patience]) > -self.min_delta:
                break
        
        return iter, train_losses, val_losses, train_acc, val_acc
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return (self._sigmoid(X @ self.w) > 0.5).astype(int)

class NaiveBayes(Model):
    """
    https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf
    """
    def __init__(self, variant: str):
        assert variant in ['multinomialNB', 'discreteNB']
        self.prior = None
        self.conprob = None
        self.n_classes = None
        self.variant = variant

    def fit(self, X, y, n_classes):
        n, v = X.shape
        self.prior = np.zeros(n_classes)
        self.conprob = np.zeros((v, n_classes))
        self.n_classes = n_classes

        for c in range(n_classes):
            X_c = X[y == c]
            n_c = len(X_c)
            self.prior[c] = n_c / n

            if self.variant == 'multinomialNB':
                denom = np.sum(X_c) + v
                for t in range(v):
                    self.conprob[t, c] = (np.sum(X_c[:, t]) + 1) / denom
            else:
                self.conprob[:, c] = (np.sum(X_c, axis=0) + 1) / (n_c + v)

    def predict_one(self, x: np.ndarray) -> int:
        score = np.zeros(self.n_classes)
        for c in range(self.n_classes):
            score[c] = np.log(self.prior[c])
            for t in range(x.shape[0]):
                if self.variant == 'multinomialNB':
                    score[c] += x[t] * np.log(self.conprob[t, c])
                else:
                    score[c] += x[t] * np.log(self.conprob[t, c]) + (1 - x[t]) * np.log(1 - self.conprob[t, c])

        return np.argmax(score)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self.predict_one(x) for x in X])
    
class MySGD(Model):
    def __init__(self, model):
        self.model = model
    
    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        return self.model.fit(X_train, y_train)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
