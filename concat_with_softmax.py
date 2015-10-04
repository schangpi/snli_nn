import theano.tensor as T
import util
from updates import vanilla, rmsprop

class ConcatWithSoftmax(object):
    def __init__(self, states, n_labels, n_hidden):
        self.states = states
        self.Wy = util.sharedMatrix(n_labels, len(states) * n_hidden, 'Wy', False)
        self.by = util.shared(util.zeros((1, n_labels)), 'by')

    def params(self):
        return [self.Wy, self.by] 

    def updates_wrt_cost(self, cost, learning_rate):
        gradients = T.grad(cost=cost, wrt=self.params())
        return vanilla(self.params(), gradients, learning_rate)

    def prob_pred(self):
        concatted_state = T.concatenate(self.states)
        prob_y = T.nnet.softmax(T.dot(self.Wy, concatted_state) + self.by)
        pred_y = T.argmax(prob_y, axis=1)
        return (prob_y, pred_y)

