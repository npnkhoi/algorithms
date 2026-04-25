import numpy as np
from classifier import Classifier
from layers import fc_forward, fc_backward, relu_forward, relu_backward


class TwoLayerNet(Classifier):
    """
    A neural network with two layers, using a ReLU nonlinearity on its one
    hidden layer. That is, the architecture should be:

    input -> FC layer -> ReLU layer -> FC layer -> scores
    """
    def __init__(self, input_dim=3072, num_classes=10, hidden_dim=512,
                 weight_scale=1e-3):
        """
        Initialize a new two layer network.

        Inputs:
        - input_dim: The number of dimensions in the input.
        - num_classes: The number of classes over which to classify
        - hidden_dim: The size of the hidden layer
        - weight_scale: The weight matrices of the model will be initialized
          from a Gaussian distribution with standard deviation equal to
          weight_scale. The bias vectors of the model will always be
          initialized to zero.
        """
        #######################################################################
        # TODO: Initialize the weights and biases of a two-layer network.     #
        #######################################################################
        
        self.fc1_w = np.random.normal(0, weight_scale, (input_dim, hidden_dim))
        self.fc1_b = np.zeros(hidden_dim)
        self.fc2_w = np.random.normal(0, weight_scale, (hidden_dim, num_classes))
        self.fc2_b = np.zeros(num_classes)
        
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################

    def parameters(self):
        params = None
        #######################################################################
        # TODO: Build a dict of all learnable parameters of this model.       #
        #######################################################################
        params = {
            'fc1_w': self.fc1_w,
            'fc1_b': self.fc1_b,
            'fc2_w': self.fc2_w,
            'fc2_b': self.fc2_b
        }
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
        return params

    def forward(self, X):
        scores, cache = None, None
        #######################################################################
        # TODO: Implement the forward pass to compute classification scores   #
        # for the input data X. Store into cache any data that will be needed #
        # during the backward pass.                                           #
        #######################################################################
        X, fc1_cache = fc_forward(X, self.fc1_w, self.fc1_b)
        X, relu_cache = relu_forward(X)
        X, fc2_cache = fc_forward(X, self.fc2_w, self.fc2_b)
        scores = X
        cache = {
            'fc1': fc1_cache,
            'relu': relu_cache,
            'fc2': fc2_cache
        }
        
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
        return scores, cache

    def backward(self, grad_scores, cache):
        grads = None
        #######################################################################
        # TODO: Implement the backward pass to compute gradients for all      #
        # learnable parameters of the model, storing them in the grads dict   #
        # above. The grads dict should give gradients for all parameters in   #
        # the dict returned by model.parameters().                            #
        #######################################################################
        
        grad_fc2_x, grad_fc2_w, grad_fc2_b = fc_backward(grad_scores, cache['fc2'])
        grad_relu_x = relu_backward(grad_fc2_x, cache['relu'])
        _, grad_fc1_w, grad_fc1_b = fc_backward(grad_relu_x, cache['fc1'])
        
        grads = {
            'fc1_w': grad_fc1_w,
            'fc1_b': grad_fc1_b,
            'fc2_w': grad_fc2_w,
            'fc2_b': grad_fc2_b
        }
        
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
        return grads
