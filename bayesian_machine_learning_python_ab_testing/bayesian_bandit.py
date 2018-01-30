import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

NUM_TRIALS = 2000
BANDIT_PROBABILITIES = [0.2, 0.5, 0.75]

class Bandit:
    def __init__(self, p):
        self.p = p
        self.a = 1
        self.b = 1

    def pull(self):
        return np.random.random() < self.p

    def sample(self):
        return np.random.beta(self.a, self.b)

    def update(self, x):
        self.a += x
        self.b += 1 - x

def plot(bandits, trials):
    x = np.linspace(0, 1, 200)
    for bandit in bandits:
        y = beta.pdf(x, bandit.a, bandit.b)
        plt.plot(x, y, label="real p: %.4f" % bandit.p)
    plt.title("Bandit distribution after %s trials" % trials)
    plt.legend()
    plt.show()

def experiment():
    bandits = [Bandit(p) for p in BANDIT_PROBABILITIES]

    sample_points = [5, 10, 100, 500, 1500]

    for i in range(NUM_TRIALS):

        # take a sample from each bandit
        bestb = None
        maxsample = -1
        allsamples = []
        for bandit in bandits:
            sample = bandit.sample()
            print(sample)
            allsamples.append("%.4f" % sample)
            if sample > maxsample:
                maxsample = sample
                bestb = bandit
        if i in sample_points:
            print("current samples: %s" % allsamples)
            plot(bandits, i)

        # pull the arm for the bandit with the largest sample
        x = bestb.pull()

        # update the distribution for the bandit whose arm we just pulled
        bestb.update(x)

if __name__ == '__main__':
    experiment()


