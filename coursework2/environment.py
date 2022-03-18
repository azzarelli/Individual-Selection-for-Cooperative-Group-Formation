import copy
import numpy as np
import group as grp
import random
import matplotlib.pyplot as plt

def filter_pop_by_size(pop: list = []):
    """Filter a pool of individuals into two groups by their preference for large and small groups
    """
    popS, popL = [], []
    for p in pop:
        if p.issmall:
            popS.append(p)
        elif not p.issmall:
            popL.append(p)
    return popS, popL


class Environment:
    t = 4

    def __init__(self, pop, N, Gene):
        self.Gene = Gene
        self.N = N
        self.Groups = []
        self.pool = pop
        self.poolSize = len(pop)
        self.hist_ratios = []
        self.hist_sizes = []

    def get_popsize(self):
        return len(self.pool)

    def group_formation(self):
        """Form Groups as explained in documentation
        """
        self.Groups = []
        popS, popL = filter_pop_by_size(self.pool)
        print(f'Population Size: {len(self.pool)}')
        # Initialise first small group
        tempGroup = grp.Group()
        random.shuffle(popS)
        pS = popS.copy()
        c = 0
        while len(pS) > 0 and c < 3:
            groupSize = tempGroup.size()
            if groupSize < tempGroup.maxSize:
                # randomly shuffle the box of individuals
                random.shuffle(pS)
                # go through all remaining invidiuals until one can join (randomly shuffled order)
                for p in range(len(pS)):
                    pos = -(1+p)
                    indv = pS[pos]
                    # see if we can place individual in group
                    if indv.dist.max > tempGroup.minSize and indv.dist.min < tempGroup.maxSize:
                        tempGroup.add_pop(indv)
                        pS.pop(pos)
                        break # break from loop as individual has been groups
                # If you cant add anymore individuals
                if groupSize == tempGroup.size():
                    # check if group meets the minimum number of prefered individuals to exist
                    if groupSize > tempGroup.minSize:
                        tempGroup.maxSize = 0 # Following iteration, appends group to global stack and begins new group
                    # if group isnt enough to live, disperse individuals back into pop
                    else:
                        pS = pS + tempGroup.pop
                        tempGroup.reset()
                        c += 1
            else:
                # Append group and initialise through new group
                c = 0
                tempGroup.calc_resource_intake()
                self.Groups.append(copy.deepcopy(tempGroup))
                tempGroup.reset()
                random.shuffle(pS)
                indv = pS[-1]
                tempGroup.add_pop(indv)
                pS.pop(-1)

       # Initialise first Large group
        tempGroupL = grp.Group(issmall=False)
        random.shuffle(popL)
        pL = popL.copy()
        c = 0
        while len(pL) > 0 and c < 3:
            groupSize = tempGroupL.size()
            if groupSize < tempGroupL.maxSize:
                # randomly shuffle the box of individuals
                random.shuffle(pL)
                # go through all remaining invidiuals until one can join (randomly shuffled order)
                for p in range(len(pL)):
                    pos = -(1+p)
                    indv = pL[pos]

                    # see if we can place individual in group
                    if indv.dist.max > tempGroupL.minSize and indv.dist.min < tempGroupL.maxSize:
                        tempGroupL.add_pop(indv)
                        pL.pop(pos)
                        break # break from loop as individual has been groups

                if groupSize == tempGroupL.size():
                    # check if group meets the minimum number of prefered individuals to exist
                    if groupSize > tempGroupL.minSize:

                        tempGroupL.maxSize = 0 # Following iteration, appends group to global stack and begins new group
                    else:
                        pL = pL + tempGroupL.pop
                        tempGroupL.reset(issmall=False)
                        c +=1
            else:
                tempGroupL.calc_resource_intake()
                self.Groups.append(copy.deepcopy(tempGroupL))
                c = 0
                tempGroupL.reset(issmall=False)
                random.shuffle(pL)
                indv = pL[-1]
                tempGroupL.add_pop(indv)
                pL.pop(-1)

        self.save_group_sizes()

    def reproduce(self):
        """Run each Group object's reproduction through `t` time steps
        """
        Groups_ = []
        for g in self.Groups:
            for i in range(self.t):
                g.get_ri()
                g.reproduce(i)

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
                    pool.append(self.Gene(True, False))
                elif i == 1:
                    pool.append(self.Gene(True, True))
                elif i == 2:
                    pool.append(self.Gene(False, False))
                elif i == 3:
                    pool.append(self.Gene(False, True))
        self.pool = pool

    def save_ratios(self):
        """Save ratios of pool of individuals to plot
        """
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

    def save_group_sizes(self):
        """Save the frequency of group sizes for plotting
        """
        sizes = np.array([[2],[0]]) # 2D array which holds sizes [idx == 0] and count of sizes [idx == 1]
        for g in self.Groups:
            pop_len = len(g.pop)
            idx = np.where(sizes[0] == pop_len)[0].tolist() # find index of found group size (if exists)
            if idx != []:
                sizes[1,idx] += 1

            else: # if not index found, append size to list and count it as one
                size_ = sizes.tolist()
                size_[0].append(pop_len)
                size_[1].append(1)
                sizes = np.array(size_)
        self.hist_sizes.append(sizes)

    def plotting(self, fignum:int=0):
        """Plot all graphs shown in coursework documentation
        """
        f, sub = plt.subplots(nrows=3)
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

        arr_ = self.hist_sizes
        sizes = [[0] for i in range(50)]
        for gen in arr_: # within each generation caluclate the ratio of each group size with proportion to population
            ratio = (gen[0, :] * gen[1, :]) / np.sum(gen[0, :] * gen[1, :])
            for i in range(len(sizes)): # for each history relating to a group size
                idx = np.where(gen[0] == i)[0].tolist() # return the index of the group size in the generation array
                if idx != []:
                    rat_ = ratio[idx].tolist()
                    sizes[i].append(rat_[0])  # append it to a sorted list for group sizes
                else:
                    sizes[i].append(0)

        for s in sizes:
            if any(s): # if there is history for a particular size
                size_idx = sizes.index(s)
                if size_idx < 10:
                    sub[2].plot(s, label=str(size_idx), color='black', alpha=(((size_idx-2)+2)/13))
                    sub[2].text(len(s)-1, s[-1], f'{str(size_idx)}')
                else:
                    sub[2].plot(s, label=str(size_idx), color='darkblue', alpha=((size_idx-30)/20))
                    sub[2].text(len(s)-1, s[-1], f'{str(size_idx)}')

        sub[2].set_xlabel('Generations')
        sub[2].set_ylabel('Population Frequency')
        sub[2].legend(loc='center left', bbox_to_anchor=(1, 0.5),
                        ncol=2, title='Group Sizes')
        plt.show()
