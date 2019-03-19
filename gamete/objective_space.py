# --- Objective space
class Objective():
    def __init__(self, name, goal):
        self.name = name
        self.goal = goal


class ObjectiveSpace(object):
    def __init__(self, objectives):
        objective_names = [obj.name for obj in objectives]
        objective_goals = [obj.goal for obj in objectives]

        assert not isinstance(objective_names, str)
        assert not isinstance(objective_goals, str)
        assert (type(objective_names) == list or type(objective_names) == tuple)
        assert (type(objective_goals) == list or type(objective_names) == tuple)
        assert (len(objective_names) == len(objective_goals))
        for obj in objective_names:
            assert obj not in ["hash", "start", "finish"]

        # for goal in objective_goals:
        #    assert(goal == "Min" or goal == "Max")

        self.objective_names = objective_names
        self.objective_goals = objective_goals
        logging.debug("Created {}".format(self))

    # Information about the space -------------
    def __str__(self):
        return "ObjectiveSpace: {} Dimensions : {}".format(self.dimension,
                                                           zip(self.objective_names, self.objective_goals))

    @property
    def dimension(self):
        return len(self.objective_names)
