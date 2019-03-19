# --- Evolution
class Mapping(object):
    def __init__(self, design_space, objective_space, individual):
        """
        """

        self.design_space = design_space
        self.objective_space = objective_space
        self.individual = individual
        logging.info(self)

    def __str__(self):
        return "Mapping dimension {} domain to dimension {} range".format(self.design_space.dimension,
                                                                          self.objective_space.dimension)

    def print_summary(self):
        print(self)
        print(self.design_space)
        print(self.objective_space)
        print(self.individual)

    # ---Assignment
    def assign_individual(self, Individual):
        raise Exception("Obselete")

        self.individual = Individual
        logging.info("This mapping will produce individuals of class {}".format(Individual.__name__))

    def assign_evaluator(self, life_cycle):
        self.individual.pre_process = life_cycle['pre_process']
        self.individual.execute = life_cycle['execute']
        self.individual.post_process = life_cycle['post_process']

        logging.info("Bound life cycle {}, {}, {} to {}".format(
            life_cycle['pre_process'],
            life_cycle['execute'],
            life_cycle['post_process'],
            self.individual.__name__)
        )

    def assign_fitness(self, fitness):
        raise Exception("Obselete")
        self.fitness = fitness
        logging.info("This mapping will produce fitness of class {}".format(fitness.__name__))

    # --- Generating points in the space
    def get_random_mapping(self, flg_verbose=False):
        """
        Randomly sample all basis_set vectors, return a random variable vector
        """
        chromosome = list()
        for var in self.design_space.basis_set:
            this_var = var.return_random_allele()
            chromosome.append(this_var)

        this_ind = self.individual(chromosome=chromosome,
                                   )
        # this_ind = this_ind.init_life_cycle()

        if flg_verbose:
            logging.debug("Creating a {} individual with chromosome {}".format(self.individual, chromosome))
            logging.debug("Returned random individual {}".format(this_ind))

        return this_ind

    def get_random_population(self, pop_size, flg_verbose=False):
        """Call get_random_mapping n times to generate a list of individuals
        """
        indiv_list = list()
        for idx in range(pop_size):
            indiv_list.append(self.get_random_mapping(flg_verbose))

        logging.info("Retrieved {} random mappings from a space of {} elements".format(pop_size,
                                                                                       self.design_space.get_cardinality()))

        return indiv_list

    def get_global_search(self):
        raise
        tuple_set = list()
        names = list()
        indices = list()
        for variable in self.design_space.basis_set:
            tuple_set.append(variable.variable_tuple)
            names.append(variable.name)
            indices.append(None)

        run_list = list()
        for vector in itertools.product(*tuple_set):
            # print(vector)
            this_indiv = self.individual(names, vector, indices, self.evaluator)
            # print(this_indiv)
            run_list.append(this_indiv)
        # raise
        log_string = "Retrieved {} individuals over {}-dimension design space".format(len(run_list),
                                                                                      self.design_space.dimension)
        logging.info(log_string)

        return run_list

    def getHyperCorners(self):
        raise
        pass

