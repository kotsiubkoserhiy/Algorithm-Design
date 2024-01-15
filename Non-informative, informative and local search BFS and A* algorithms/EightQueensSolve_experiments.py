from queue import Queue
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

class EightQueensSolver:
    def __init__(self, size=8, initial_state=None):
        self.size = size
        self.generated_states = 0
        self.memorized_states = 0
        self.queue = Queue()
        if initial_state is None:
            self.initial_state = self.generate_random_state()
        else:
            self.initial_state = initial_state


    def conflict(self, state):
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i][0] == state[j][0] or state[i][1] == state[j][1] or abs(state[i][0] - state[j][0]) == abs(
                        state[i][1] - state[j][1]):
                    return True
        return False

    def generate_random_state(self):
        state = [(i, random.randint(0, self.size - 1)) for i in range(self.size)]
        return state

    def solve_bfs(self):
        if self.size < 1:
            return []
        solutions = []
        self.queue.put([])
        self.generated_states += 1
        while not self.queue.empty():
            solution = self.queue.get()
            if self.conflict(solution):
                continue
            row = len(solution)
            if row == self.size:
                solutions.append(solution)
                continue
            for col in range(self.size):
                queen = (row, col)
                queens = solution.copy()
                queens.append(queen)
                self.queue.put(queens)
                self.generated_states += 1
            self.memorized_states = self.queue.qsize()
        return solutions

    def solve_a_star(self):
        start_node = Node([])
        open_list = [start_node]
        closed_list = []

        while open_list:
            open_list.sort(key=lambda x: len(x.state), reverse=True)
            current_node = open_list.pop()
            closed_list.append(current_node)

            if len(current_node.state) == self.size and not self.conflict(current_node.state):
                self.generated_states += 1
                return current_node.state

            for col in range(self.size):
                if not any(abs(col - current_node.state[j][1]) == len(current_node.state) - j for j in
                           range(len(current_node.state))):
                    child_state = current_node.state + [(len(current_node.state), col)]
                    child_node = Node(child_state, current_node)

                    if not self.conflict(child_state) and all(child_node.state != node.state for node in closed_list):
                        open_list.append(child_node)
                        self.generated_states += 1
            self.memorized_states = len(open_list) + len(closed_list)
        return None

    def get_bfs_iterations(self, solutions):
        return len(solutions) if solutions else 0

    def get_bfs_dead_ends(self, solutions):
        dead_ends = 0
        for solution in solutions:
            if self.conflict(solution):
                dead_ends += 1
        return dead_ends

    def get_bfs_generated_states(self):
        return self.generated_states

    def get_bfs_memory_states(self):
        return self.memorized_states

    def get_a_star_iterations(self, solution):
        return 1 if solution is not None else 0

    def get_a_star_dead_ends(self, solution):
        return 0 if solution is not None and not self.conflict(solution) else 1

    def get_a_star_generated_states(self):
        return self.generated_states

    def get_a_star_memory_states(self):
        return self.memorized_states

class ExperimentResult:
    def __init__(self, bfs_iterations, bfs_dead_ends, bfs_generated_states, bfs_memory_states, a_star_iterations,
                 a_star_dead_ends, a_star_generated_states, a_star_memory_states):
        self.bfs_iterations = bfs_iterations
        self.bfs_dead_ends = bfs_dead_ends
        self.bfs_generated_states = bfs_generated_states
        self.bfs_memory_states = bfs_memory_states
        self.a_star_iterations = a_star_iterations
        self.a_star_dead_ends = a_star_dead_ends
        self.a_star_generated_states = a_star_generated_states
        self.a_star_memory_states = a_star_memory_states

    def __str__(self):
        return f"BFS: Iterations={self.bfs_iterations}, Dead Ends={self.bfs_dead_ends}, " \
               f"Generated States={self.bfs_generated_states}, Memory States={self.bfs_memory_states}\n" \
               f"A*: Iterations={self.a_star_iterations}, Dead Ends={self.a_star_dead_ends}, " \
               f"Generated States={self.a_star_generated_states}, Memory States={self.a_star_memory_states}"


def main():
    experiment_results = []

    for i in range(20):
        solver = EightQueensSolver()
        initial_state = solver.generate_random_state()
        solver_bfs = EightQueensSolver(initial_state=initial_state)
        solver_a_star = EightQueensSolver(initial_state=initial_state)

        solutions_bfs = solver_bfs.solve_bfs()
        bfs_iterations = solver_bfs.get_bfs_iterations(solutions_bfs)
        bfs_dead_ends = solver_bfs.get_bfs_dead_ends(solutions_bfs)
        bfs_generated_states = solver_bfs.get_bfs_generated_states()
        bfs_memory_states = solver_bfs.get_bfs_memory_states()

        a_star_solution = solver_a_star.solve_a_star()
        a_star_iterations = solver_a_star.get_a_star_iterations(a_star_solution)
        a_star_dead_ends = solver_a_star.get_a_star_dead_ends(a_star_solution)
        a_star_generated_states = solver_a_star.get_a_star_generated_states()
        a_star_memory_states = solver_a_star.get_a_star_memory_states()

        experiment_result = ExperimentResult(bfs_iterations, bfs_dead_ends, bfs_generated_states, bfs_memory_states,
                            a_star_iterations, a_star_dead_ends, a_star_generated_states, a_star_memory_states)
        experiment_results.append(experiment_result)

        del solver_bfs
        del solver_a_star

    for i, result in enumerate(experiment_results):
        print(f"Експеримент {i + 1}:")
        print(result)
        print()

if __name__ == '__main__':
    main()