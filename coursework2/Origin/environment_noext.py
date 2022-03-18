from gene_noext import Gene
import group_noext as grp
import random
import matplotlib.pyplot as plt

def filter_pop_by_size(pop: list = []):
    popS, popL = [], []
    for p in pop:
        if p.issmall:
            popS.append(p)
        elif not p.issmall:
            popL.append(p)
    return popS, popL


class Environment:
    small_size = 4
    large_size = 40

    t = 4

    def __init__(self, pop, N):
        self.N = N
        self.Groups = []
        self.pool = pop
        self.poolSize = len(pop)
        self.hist_ratios = []

    def get_popsize(self):
        return len(self.pool)

    def group_formation(self):
        """Form small and large groups by randomly shuffling the subset population (small and large gene split) and
        extracting final index. Groups are sized by `self.large_size` and `self.small_size`

        Outcome
        -------
        Generate a list of all group objects `self.Groups`
        """
        self.Groups = []
        popS, popL = filter_pop_by_size(self.pool)
        print(f'Population Size: {len(self.pool)}')
        Rs, Rl = 4, 50

        num_small = int(len(popS) / self.small_size)
        num_large = int(len(popL) / self.large_size)

        # Group small individuals
        for i in range(num_small):
            tpop = []
            for j in range(self.small_size):
                random.shuffle(popS)
                tpop.append(popS[-1])
                popS.pop(-1)
            self.Groups.append(grp.Group(tpop, True, R=Rs))


        # Group Large individuals
        for i in range(num_large):
            tpop = []
            for j in range(self.large_size):
                random.shuffle(popL)
                tpop.append(popL[-1])
                popL.pop(-1)
            self.Groups.append(grp.Group(tpop, False, R=Rl))

        del popS, popL

    def reproduce(self):
        """Run each Group object's reproduction through `t` time steps
        """
        Groups_ = []
        for g in self.Groups:

            for i in range(self.t):
                g.get_ri()
                g.reproduce()

            g.regenerate_pop()
            Groups_.append(g)

        self.Groups = Groups_
        self.save_ratios()

    def migrant_pool_formation(self):
        """Return all individuals to the migrant pool, `self.pool`
        """
        pool = []
        popSize = 0
        for g in self.Groups:
            for p in g.pop:
                pool.append(p)
                popSize += 1
        self.pool = pool

    def rescale(self):
        """Determine the genotype population split (ratio, `fi` for i in ss,sc, ls, lc).
        """
        # Init. number of genotypes index: (0) ss, (1) sc, (2) ls, (3) lc
        ni = [0. for i in range(4)]
        self.poolSize = len(self.pool)
        for p in self.pool:
            i = 0
            if p.iscoop:
                i += 1  # index (1) or (3)
            if not p.issmall:
                i += 2  # index (0) or (2)
            ni[i] += 1.
        # Determine the ratio of each genotype
        fi = [ni[i] / self.poolSize for i in range(4)]
        ni_ = [int(fi[i] * self.N) for i in range(4)]
        pool = []
        for i in range(4):
            for j in range(ni_[i]):
                # issmal, iscoop
                if i == 0:
                    pool.append(Gene(True, False))
                elif i == 1:
                    pool.append(Gene(True, True))
                elif i == 2:
                    pool.append(Gene(False, False))
                elif i == 3:
                    pool.append(Gene(False, True))
        self.pool = pool

    def save_ratios(self):
        # Init. number of genotypes index: (0) ss, (1) sc, (2) ls, (3) lc
        ni = [0 for i in range(4)]
        self.poolSize = len(self.pool)
        for p in self.pool:
            i = 0
            if p.iscoop:
                i += 1  # index (1) or (3)
            if not p.issmall:
                i += 2  # index (0) or (2)
            ni[i] += 1
        fi = [ni[i] / self.poolSize for i in range(4)]


        self.hist_ratios.append(fi)
        print(f'Pop Ratios: \n    SS {fi[0]}\n    SC {fi[1]}\n    LS {fi[2]}\n    LC {fi[3]}')


    def plotting(self, fignum:int=0):
        f, sub = plt.subplots(1,2)
        ss, sc, ls, lc = [], [], [], []
        selfish, large = [], []

        for r in self.hist_ratios:
            ss.append(r[0])
            sc.append(r[1])
            ls.append(r[2])
            lc.append(r[3])
            selfish.append(r[0]+r[2])
            large.append(r[2]+r[3])

        sub[1].plot(ss, label='Small+Selfish', color='orange')
        sub[1].plot(sc, label='Small+Cooperative', color='lightblue')
        sub[1].plot(ls, label='Large+Selfish', color='orange', linestyle='-.')
        sub[1].plot(lc, label='Large+Cooperative', color='lightblue', linestyle='-.')
        sub[1].axhline(1, color='green', alpha=0.2, linestyle='--')
        sub[1].axhline(0, color='green', alpha=0.2, linestyle='--')
        sub[1].set_xlabel('Generation')
        sub[1].set_ylabel('Population Frequency')
        sub[1].legend()

        sub[0].plot(selfish, label='Selfish', color='lightgrey')
        sub[0].plot(large, label='Large', color='lightgrey', linestyle='-.')
        sub[0].set_xlabel('Generation')
        sub[0].set_ylabel('Population Frequency')
        sub[0].legend()

        plt.show()

