class Gene:
    def __init__(self, issmall:bool, iscoop:bool):
        """Individuals Genotype

        Attributes
        ----------
            joinSize : bool, 0 for small and 1 for large group which the gene should join
            decrease_Gr : bool, True when gene is cooperative (decrease growth rate)
        """
        self.issmall = issmall
        self.iscoop = iscoop