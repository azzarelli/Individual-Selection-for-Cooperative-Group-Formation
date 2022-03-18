import random
import numpy as np

random.seed(7)


class Distribution:
    LRANGE = [[37,43], [37,43], [30,50], [30,50]]
    SRANGE = [[4,5], [2,5], [4,5], [2,5]]
    LSIG = 3
    SSIG = 1

    def __init__(self, pref:bool, mu:float=0.0, ep:int=0):
        self.pref = pref

        # First check if mu's have been given (should be >2 for anny assignment to exist)
        if mu > 0.0 and mu < 10:
            self.mu = mu
            self.sig = self.SSIG
        elif mu > 10:
            self.mu = mu
            self.sig = self.LSIG
        # Small group - set the mu and std of distribution for choice of groups
        elif self.pref:
            self.mu = random.randint(self.SRANGE[ep][0], self.SRANGE[ep][1])
            self.sig = self.SSIG
        # Lagre group
        else:
            self.mu = random.randint(self.LRANGE[ep][0], self.LRANGE[ep][1])
            self.sig = self.LSIG

        self.min = self.mu - self.sig
        self.max = self.mu + self.sig


class Gene0:
    def __init__(self, issmall:bool, iscoop:bool, mu:float=0.0):
        """Individuals Genotype

        Attributes
        ----------
            joinSize : bool, 0 for small and 1 for large group which the gene should join
            dist : Distribution, holds ranges and statistical propoerties of individual distribution for preference
            decrease_Gr : bool, True when gene is cooperative (decrease growth rate)
        """
        self.issmall = issmall
        self.dist = Distribution(issmall, mu, ep=0)
        self.iscoop = iscoop

class Gene1:
    def __init__(self, issmall:bool, iscoop:bool, mu:float=0.0):
        """Individuals Genotype

        Attributes
        ----------
            joinSize : bool, 0 for small and 1 for large group which the gene should join
            dist : Distribution, holds ranges and statistical propoerties of individual distribution for preference
            decrease_Gr : bool, True when gene is cooperative (decrease growth rate)
        """
        self.issmall = issmall
        self.dist = Distribution(issmall, mu, ep=1)
        self.iscoop = iscoop
class Gene2:
    def __init__(self, issmall:bool, iscoop:bool, mu:float=0.0):
        """Individuals Genotype

        Attributes
        ----------
            joinSize : bool, 0 for small and 1 for large group which the gene should join
            dist : Distribution, holds ranges and statistical propoerties of individual distribution for preference
            decrease_Gr : bool, True when gene is cooperative (decrease growth rate)
        """
        self.issmall = issmall
        self.dist = Distribution(issmall, mu, ep=2)
        self.iscoop = iscoop
class Gene3:
    def __init__(self, issmall:bool, iscoop:bool, mu:float=0.0):
        """Individuals Genotype

        Attributes
        ----------
            joinSize : bool, 0 for small and 1 for large group which the gene should join
            dist : Distribution, holds ranges and statistical propoerties of individual distribution for preference
            decrease_Gr : bool, True when gene is cooperative (decrease growth rate)
        """
        self.issmall = issmall
        self.dist = Distribution(issmall, mu, ep=3)
        self.iscoop = iscoop
