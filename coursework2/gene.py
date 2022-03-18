import random
random.seed(7)

class Distribution:
    """Represents the gene for distribution, i.e contains the true preference `mu` and the margin of error `sig`
    """
    # Classify the range which an individual preference is randomly chosen
    LRANGE = [30,50]
    SRANGE = [1,5]
    # Define the std (error rate) of an individual's size preference
    LSIG = 3
    SSIG = 1

    def __init__(self, pref:bool, mu:float=0.0):
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
            self.mu = random.randint(self.SRANGE[0], self.SRANGE[1])
            self.sig = self.SSIG
        # Lagre group
        else:
            self.mu = random.randint(self.LRANGE[0], self.LRANGE[1])
            self.sig = self.LSIG

        self.min = self.mu - self.sig
        self.max = self.mu + self.sig


class Gene:
    def __init__(self, issmall:bool, iscoop:bool, mu:float=0.0):
        """Individuals Genotype

        Attributes
        ----------
            joinSize : bool, 0 for small and 1 for large group which the gene should join
            dist : Distribution, holds ranges and statistical propoerties of individual distribution for preference
            decrease_Gr : bool, True when gene is cooperative (decrease growth rate)
        """
        self.issmall = issmall
        self.dist = Distribution(issmall, mu)
        self.iscoop = iscoop