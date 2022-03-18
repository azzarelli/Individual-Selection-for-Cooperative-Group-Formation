from environment_noext import Environment
from gene_noext import Gene
# define popsize, generations and fixed group sizes
global POPSIZE
POPSIZE = 4000
global small_size
global large_size
small_size, large_size = 4, 40
# t = 4 (reproduce 4x in group before migrant reformation)
epochs = 4

def Initialise(popsize):
    """Initialise population of selfish and cooperative individuals, and small and large preferences
    """
    pop = []
    for i in range(popsize):
        # Split pop size into 4 genotypes
        if i % 8 in [0,1]:
            # isSmall and iscoop
            ind = Gene(True, True)
        elif i % 8 in [2,3]:
            # SC
            ind = Gene(True, False)
        elif i % 8 in [4,5]:
            # LC
            ind = Gene(False, True)
        elif i % 8 in [6,7]:
            # LS
            ind = Gene(False, False)
        pop.append(ind)
    return pop

if __name__ == '__main__':
    ratios = []

# 1 Initialisation
    pop = Initialise(POPSIZE)
    env = Environment(pop, POPSIZE)

    # Set first ratios for plotting
    env.save_ratios()

    for i in range(120):
        print('Iteration ', i)


    # 2 Group Formation
        env.group_formation()


    # 3 Reproduction
        env.reproduce()


    # 4 Migrant Pool Formation
        env.migrant_pool_formation()

    # 5 Maintain Global Capacity
        psize = env.get_popsize()
        print(f'Final Pop Size {psize}')
        if psize > POPSIZE:
            env.rescale()

    # Plot results
    env.plotting()