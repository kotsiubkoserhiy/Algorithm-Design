from queue import Queue
from queue import PriorityQueue


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    def __lt__(self, other):
        return len(self.state) < len(other.state)

class EightQueensSolver:
    def __init__(self, size=8):
        self.size = size

    def conflict(self, state):
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i][0] == state[j][0] or state[i][1] == state[j][1] or abs(state[i][0] - state[j][0]) == abs(state[i][1] - state[j][1]):
                    return True
        return False

    def solve_bfs(self):
        if self.size < 1:
            return []
        solutions = []
        queue = Queue()
        queue.put([])
        try:
            while not queue.empty():
                solution = queue.get()
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
                    queue.put(queens)
        except Exception as e:
            print(f"An error occurred: {e}")
        return solutions

    def heuristic(self, state):
        conflicts = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i][0] == state[j][0] or state[i][1] == state[j][1] or abs(state[i][0] - state[j][0]) ==\
                        abs(state[i][1] - state[j][1]):
                    visible = True
                    for k in range(len(state)):
                        if k != i and k != j:
                            if state[k][0] == state[i][0] and min(state[k][1], state[i][1]) < state[j][1] <\
                                    max(state[k][1], state[i][1]):
                                visible = False
                                break
                    if visible:
                        conflicts += 1
        return conflicts

    def solve_a_star(self):
        start_node = Node([])
        open_list = PriorityQueue()
        open_list.put((0, start_node))
        closed_list = set()

        while not open_list.empty():
            _, current_node = open_list.get()
            closed_list.add(current_node)

            if len(current_node.state) == self.size and not self.conflict(current_node.state):
                return current_node.state

            for col in range(self.size):
                if not any(abs(col - current_node.state[j][1]) == len(current_node.state) - j for j in
                           range(len(current_node.state))):
                    child_state = current_node.state + [(len(current_node.state), col)]
                    child_node = Node(child_state, current_node)

                    if not self.conflict(child_state) and child_node not in closed_list:
                        priority = len(child_node.state) + self.heuristic(child_state)
                        open_list.put((priority, child_node))

        return None


def main():
    while True:
        user_input = input("Введіть 'exit', щоб вийти, або виберіть алгоритм (bfs або a*): ").lower()
        if user_input == 'exit':
            print("Вихід з програми.")
            return
        elif user_input == 'bfs' or user_input == 'a*':
            break
        else:
            print("Невірний ввід. Спробуйте ще раз.")

    solver = EightQueensSolver()

    if user_input == 'bfs':
        solutions = solver.solve_bfs()
    elif user_input == 'a*':
        solutions = [solver.solve_a_star()]

    if solutions:
        print(f"Знайдено {len(solutions)} рішень:")
        for solution in solutions:
            print(solution)

        while True:
            choice = input("Бажаєте спробувати інший алгоритм? ('yes' або 'no'): ").lower()
            if choice == 'yes':
                main()
                break
            elif choice == 'no':
                print("Вихід з програми.")
                return
            else:
                print("Невірний ввід. Спробуйте ще раз.")
    else:
        print("Рішень не знайдено.")


if __name__ == "__main__":
    main()

