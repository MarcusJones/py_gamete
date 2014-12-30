
class FitnessMJ(Fitness):
    def __init__(self, values=()):
        #self.names = names
        super(FitnessMJ, self).__init__(values)

    def __str__(self):
        """Return the values of the fitness object."""
        return str(self.names) + str(self.values if self.valid else tuple())  
