from TravellingSalesmanProblem import BeeAlgorithm

if __name__ == "__main__":
    num_vertices = 250
    n_bees = 45
    n_sites = 5
    elite_sites = 2
    ngh_size = 1
    report_interval = 20
    print("TravellingSalesmanProblem (bee algorithm)")
    print("Num vertices = 250 ; N_bees = 45 ; N_sites = 5 ; Elite_sites = 2 ; Ngh_size = 1")

    bee_algorithm = BeeAlgorithm(num_vertices, n_bees, n_sites, elite_sites, ngh_size, 0, report_interval)
    bee_algorithm.run()