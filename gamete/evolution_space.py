class Allele(object):
    """
    Init Attributes
    name - A label for the variable. Required.
    locus -
    variable_tuple - The k-Tuple of possible values
    ordered= True - Flag

    Internal Attributes
    index = None - The corresponding index of the generated value
    value = The current value of the variable, defined by the index
    """

    def __init__(self, name, chromo_name, locus, vtype, value, index, ordered):
        self.name = name
        self.chromo_name = chromo_name
        self.locus = locus
        self.vtype = vtype
        self.value = value
        self.index = index
        self.ordered = ordered

        # logging.debug("{}".format(self))

    def __str__(self):
        return self.this_val_str()

    def __repr__(self):
        return self.this_val_str()

    @property
    def val_str(self):
        return str(self.value)

    def this_val_str(self):

        """
        String for current name and current value
        """
        if self.vtype == 'bool':
            if self.value:
                vstr = 1
            else:
                vstr = 0
            return "{}={}".format(self.name, vstr)
            # if self.value:
            #     return "{}={}".format(self.name, '0')
            # else:
            #     return "{}={}".format(self.name, '1')
        else:
            return "{}[{}]={}".format(self.name, self.index, self.val_str)


class Genome(list):
    """An individual is composed of a list of alleles (chromosome).
    Each gene is an instance of the Variable class.
    The individual class inherits list (slicing, assignment, mutability, etc.).

    :param chromosome: list of allele
    .. py:classmethod:: asdf
    .. py:attribute:: name
    """

    def __init__(self, chromosome):

        for val in chromosome:
            assert type(val) == Allele

        list_items = list()
        for gene in chromosome:
            if gene.vtype == 'float':
                list_items.append(float(gene.val_str))
            elif gene.vtype == 'string':
                list_items.append(gene.val_str)
            elif gene.vtype == 'bool':
                list_items.append(gene.val_str)
            elif gene.vtype == 'int':
                list_items.append(gene.val_str)
            else:
                raise Exception("{}".format(gene.vtype))
        super(Genome, self).__init__(list_items)

        self.chromosome = chromosome
        # self.fitness = fitness

        self.start_time = None
        self.finish_time = None
        # self.hash = self.__hash__()

        # logging.debug("individual instantiated; {}".format(self))

    @property
    def hash(self):
        """This is the unique identifier for this individual. """
        return self.__hash__()

    def clone(self):
        new_chromo = list()
        for allele in self.chromosome:
            new_chromo.append(
                Allele(allele.name, allele.locus, allele.vtype, allele.value, allele.index, allele.ordered))

        cloned_Ind = Genome(new_chromo, deepcopy(self.fitness))
        assert (cloned_Ind is not self)
        assert (cloned_Ind.fitness is not self.fitness)
        return cloned_Ind

    def re_init(self):
        list_items = list()
        for gene in self.chromosome:
            if gene.vtype == 'float':
                list_items.append(float(gene.val_str))
            elif gene.vtype == 'string':
                list_items.append(gene.val_str)
            else:
                raise Exception("{}".format(gene.vtype))
        super(individual, self).__init__(list_items)

    def recreate_fitness(self):
        raise
        fit_vals = list()
        for name in self.fitness_names:
            fit_vals.append(getattr(self, name))
        print(self)
        print(self.obj1)
        print(fit_vals)
        raise Exception

    def __hash__(self):
        """This defines the uniqueness of the individual
        An individual can be identified by the combination of its genes, just as in nature.
        For example, the string composed of the individual variable vectors.
        But this would be expensive and complicated to store in a database
        The hash compresses this information to an integer value.
        """
        index_list = [allele.index for allele in self.chromosome]
        return hash(tuple(index_list))

    def __eq__(self, other):
        if self.hash == other.hash:
            return True
        return False

    # def __repr__(self):
    #    return(self.__str__())

    # def __str__(self):
    #     return "{:>12}; {}, fitness:{}".format(self.hash, ", ".join([var.this_val_str() for var in self.chromosome]),
    #                                            self.fitness)

    def __str__(self):
        summary_list = list()
        for allele in self.chromosome:
            if allele.vtype == 'bool':
                if allele.value:
                    summary_list.append('1')
                else:
                    summary_list.append('0')
            else:
                summary_list.append(str(allele.value))

        # return "{:>12}; {}, fitness:{}".format(self.hash, ", ".join([var.this_val_str() for var in self.chromosome]),
        return "{:>12}; {}".format(self.hash, "|".join(summary_list))


    def update(self):
        """Check on the status of the process, update if necessary
        """
        if self.process:
            retcode = self.process.poll()
            # Windows exit code
            if retcode is None:
                # logging.debug("Update {}, Process: {}, RUNNING".format(self.hash,self.process))
                self.status = "Running"
            else:
                # Add more handling for irregular retcodes
                # See i.e. http://www.symantec.com/connect/articles/windows-system-error-codes-exit-codes-description
                # logging.debug("Update {}, Process: {}, DONE".format(self.hash,self.process))
                self.run_status = "Finished"
                self.finish_time = datetime.datetime.now()
        else:
            # This process has not been started]
            raise
            pass



class Generation():
    def __init__(self, gen, individual):
        self.gen = gen
        self.individual = individual

