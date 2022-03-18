import copy
import random
import numpy as np

class Group:
    # Growth & Consumption Rates (and product)
    Gs, Gc = 0.02, 0.018
    Cs, Cc = 0.2, 0.1
    GsCs, GcCc = Gs * Cs, Gc * Cc

    # Death rate
    K = 0.1

    def __init__(self, pop: list = [], issmall: bool = True, R: float = 0.0):
        self.reset(pop, issmall, R)


    def reset(self, pop: list = [], issmall: bool = True, R: float = 0.0):
        """Initialise group of individuals

                Attributes
                ----------
                    pop : list of Gene, list of individuals
                    issmall : bool, True for small, False for large
                    R : float, resource influx for group
                """
        self.pop = []
        self.prior_coop, self.prior_self = [],[]
        self.popSize = 0

        self.groupSize = issmall
        self.R = R

        # Contain the maximum and minimum sizes a group can take
        if issmall:
            self.maxSize = 10
            self.minSize = 1
        else:
            self.maxSize = 50
            self.minSize = 30

        self.ns, self.nc = 0, 0
        self.prior_ns, self.prior_nc = 0,0



    def add_pop(self, indv):
        """Add an individual to the group while group is forming in `environment.group_formation`
        """
        imax = indv.dist.max
        imin = indv.dist.min

        # Update new bounds for size constraints
        if self.maxSize > imax:
            self.maxSize = imax
        if self.minSize < imin:
            self.minSize = imin

        self.pop.append(indv)
        self.popSize = len(self.pop)

    def calc_resource_intake(self):
        """Equation defined in coursework documentation
        """
        r0 = 0.9425
        n = len(self.pop)
        self.R = n * (r0) * (1.05)**(np.log2(n))


    def get_ni(self):
        """Count the number of selfish and cooperative individuals $n_i$"""
        for p in self.pop:
            if p.iscoop:
                self.nc += 1
            elif not p.iscoop:
                self.ns += 1

    def get_ri(self):
        """Share of resources for each subset of classes, $r_i$
        """
        self.get_ni()

        nGCs = self.ns * self.GsCs
        nGCc = self.nc * self.GcCc
        SUMj = nGCs + nGCc

        self.rs = self.R * (nGCs / SUMj)
        self.rc = self.R * (nGCc / SUMj)

    def reproduce(self, epoch):
        """Determine n_i(t+1)
        """
        if epoch == 0 :
            self.prior_ns, self.prior_nc = self.ns, self.nc
            prior_pop = copy.deepcopy(self.pop)
            for p in prior_pop:
                if p.iscoop:
                    self.prior_coop.append(copy.deepcopy(p))
                elif not p.iscoop:
                    self.prior_self.append(copy.deepcopy(p))


        ns_, nc_ = self.ns, self.nc
        self.ns = ns_ + (self.rs / self.Cs) - (self.K * ns_)
        self.nc = nc_ + (self.rc / self.Cc) - (self.K * nc_)


    def regenerate_pop(self):
        pop_s = copy.deepcopy(self.prior_self)
        pop_c = copy.deepcopy(self.prior_coop)
        ns_diff = int(self.ns - self.prior_ns)
        nc_diff = int(self.nc - self.prior_nc)
        if ns_diff > 0: # if we need to add to population of selfish individuals
            for n in range(ns_diff):
                p = random.choice(self.prior_self)
                pop_s.append(p)
        elif ns_diff < 0:
            for n in range(abs(ns_diff)):
                if len(pop_s) > 0:
                    p = random.choice(pop_s)
                    pop_s.pop(pop_s.index(p))
                else:
                    break

        if nc_diff > 0: # if we need to add to population of selfish individuals
            for n in range(nc_diff):
                p = copy.deepcopy(random.choice(self.prior_coop))
                pop_c.append(p)
        elif nc_diff < 0:
            for n in range(abs(nc_diff)):
                if len(pop_c) > 0:
                    p = random.choice(pop_c)
                    pop_c.pop(pop_c.index(p))
                else:
                    break
        self.pop = pop_s + pop_c

    def size(self):
        return len(self.pop)



