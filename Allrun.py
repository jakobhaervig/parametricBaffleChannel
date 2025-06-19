from pathlib import Path
import subprocess as sp
import numpy as np
import platypus as pp
import csv
import matplotlib.pyplot as plt

CASECOUNT = 1

def replace_variables(casePath, vars):
    for file in list(casePath.glob('**/*')):
        if file.is_file():
            content = file.read_text()
            for key, value in vars.items():
                content = content.replace("{"+str(key)+"}", str(value))
            file.write_text(content)

def run_fcn(X):
    global CASECOUNT
    print('############## CASE %05d ##############' % (CASECOUNT))
    print('Variables:', X)

    cwd = Path(__file__).parent
    case_path = cwd / f'case{CASECOUNT:04d}'
    template_path = cwd / 'template'
    resultsfile_path = cwd / 'results.csv'

    # Make a copy of the template case
    sp.run(['cp', '-r', template_path, case_path], check=True, capture_output=True)

    # Replace variables in the case files
    vars = {
        'alpha': X[0],
        's': X[1]
    }
    replace_variables(case_path, vars)

    # Run the simulation
    sp.run(['./Allrun'], cwd=case_path, check=True, capture_output=True)

    # Extract and write results
    avgP = np.mean(np.loadtxt(case_path / 'postProcessing/pDrop/0/surfaceFieldValue.dat', comments='#', usecols=(1,), unpack=True)[-10:])
    meanT = np.mean(np.loadtxt(case_path / 'postProcessing/outletFluxWeightedTemp/0/surfaceFieldValue.dat', comments='#', usecols=(1,), unpack=True)[-10:])

    if not resultsfile_path.exists():
        with open(resultsfile_path, 'w') as csvfile:
            csvf = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvf.writerow(['case'] + list(vars.keys()) + ['avgP', 'meanT'])

    with open(resultsfile_path, 'a') as results:
            csvf = csv.writer(results, delimiter=',', lineterminator='\n')
            csvf.writerow([CASECOUNT] + list(vars.values()) + [avgP, meanT])

    CASECOUNT += 1
    print('Result:', avgP, meanT)
    return [avgP, -meanT]  # Return objectives: minimize avgP, maximize meanT

if __name__ == "__main__":
    problem = pp.Problem(2, 2)
    problem.directions[0] = pp.Direction.MINIMIZE
    problem.directions[1] = pp.Direction.MINIMIZE
    problem.types[0] = pp.Real(0, 90)
    problem.types[1] = pp.Real(0.008, 0.040)
    
    problem.function = run_fcn

    algorithm = pp.NSGAIII(problem, divisions_outer=12, population_size=50)
    algorithm.run(500)

    for solution in algorithm.result:
        print(solution.variables, solution.objectives)

    plt.scatter([s.objectives[0] for s in algorithm.result],
                [s.objectives[1] for s in algorithm.result])
    
    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")
    plt.show()