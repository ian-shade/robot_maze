from node import Node

class PathfindingProblem:
    """
    Represents the pathfinding problem combining robot and environment.
    
    Attributes:
        environment: Environment object
        robot: Robot object
        initial_state: Starting position
        goal_state: Goal position
    """
    
    def __init__(self, environment, robot):
        self.environment = environment
        self.robot = robot
        self.initial_state = environment.initial_state
        self.goal_state = environment.goal_state
    
    def get_initial_node(self):

        return Node(state=self.initial_state, parent=None, action=None, path_cost=0)
    
    def is_goal(self, state):

        return state == self.goal_state
    
    def get_successors(self, node):
        """
        Get successor nodes from a given node.
        
        Args:
            node: Current Node object
            
        Returns:
            List of successor Node objects
        """
        successors = []
        neighbors = self.environment.get_neighbors(
            node.state, 
            self.robot.get_possible_actions()
        )
        
        for next_state, action, step_cost in neighbors:
            successor = Node(
                state=next_state,
                parent=node,
                action=action,
                path_cost=node.path_cost + step_cost
            )
            successors.append(successor)
        
        return successors
    
    def heuristic_manhattan(self, state):
        # Args: state: Current state as tuple (x, y)
        if self.goal_state is None:
            return 0
        return abs(state[0] - self.goal_state[0]) + abs(state[1] - self.goal_state[1])
    
    def heuristic_euclidean(self, state):
        # Args: state: Current state as tuple (x, y)
        if self.goal_state is None:
            return 0
        return ((state[0] - self.goal_state[0])**2 + 
                (state[1] - self.goal_state[1])**2)**0.5
    
    def validate_problem(self):
        # Validate that the problem is properly configured.

        if self.initial_state is None:
            raise ValueError("Initial state not set!")
        if self.goal_state is None:
            raise ValueError("Goal state not set!")
        if not self.environment.is_valid(*self.initial_state):
            raise ValueError("Initial state is not valid!")
        if not self.environment.is_valid(*self.goal_state):
            raise ValueError("Goal state is not valid!")
        return True
    
    def __repr__(self):
        """String representation of the problem."""
        return (f"PathfindingProblem(start={self.initial_state}, "
                f"goal={self.goal_state}, env={self.environment})")
