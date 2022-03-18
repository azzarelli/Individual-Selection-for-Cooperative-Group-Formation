from gene_noext import Gene


class Group:
    # Growth & Consumption Rates (and product)
    Gs, Gc = 0.02, 0.018
    Cs, Cc = 0.2, 0.1
    GsCs, GcCc = Gs * Cs, Gc * Cc

    # Death rate
    K = 0.1

    def __init__(self, pop: list = [], size: bool = False, R: float = 0.0):
        """Initialise group of individuals

        Attributes
        ----------
            pop : list of Gene, list of individuals
            size : bool, True for small, False for large
            R : float, resource influ for group
        """
        self.pop = pop
        self.groupSize = size
        self.R = R

        self.ns, self.nc = 0, 0

    def get_ni(self):
        for p in self.pop:
            if p.iscoop:
                self.nc += 1
            elif not p.iscoop:
                self.ns += 1

    def get_ri(self):
        """Share of resources for each subset of classes, $r_i$

        Notes
        -----
        Determine r_s and r_c using the provided equation
        """
        self.get_ni()

        nGCs = self.ns * self.GsCs
        nGCc = self.nc * self.GcCc
        SUMj = nGCs + nGCc

        self.rs = self.R * (nGCs / SUMj)
        self.rc = self.R * (nGCc / SUMj)

    def reproduce(self):
        """Determine n_i(t+1) (no individuals added untill whole reproductive cycle determines final number of individuals, computationally more efficient)
        """
        ns_, nc_ = self.ns, self.nc
        self.ns = ns_ + (self.rs / self.Cs) - (self.K * ns_)
        self.nc = nc_ + (self.rc / self.Cc) - (self.K * nc_)

    def regenerate_pop(self):
        """Regenerate population once reproduction has been accomplished
        """
        pop = []
        for n in range(int(self.ns)):
            pop.append(Gene(self.groupSize, False))
        for n in range(int(self.nc)):
            pop.append(Gene(self.groupSize, True))
        self.pop = pop

    def size(self):
        return len(self.pop)
