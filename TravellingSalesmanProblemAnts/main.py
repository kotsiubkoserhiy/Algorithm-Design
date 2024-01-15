from TravellingSalesmanProblem import TravellingSalesmanProblem

if __name__ == "__main__":
    num_vertices = 250
    alpha = 2
    beta = 4
    rho = 0.6
    ants = 45
    print("TravellingSalesmanProblem (ant algorithm)")
    print("Num vertices = 250 ; Alpha = 2 ; Beta = 4 ; Rho = 0,6 ; Ants = 45")

    tsp = TravellingSalesmanProblem(num_vertices, alpha, beta, rho, ants, 0, 20)
    iterations = tsp.get_iterations()

    main = TravellingSalesmanProblem(num_vertices, alpha, beta, rho, ants, iterations, 20)
    main.run()
