from pathlib import Path
import subprocess as sp
import numpy as np
import platypus as pp
import csv

CASECOUNT = 0

def replace_variables(casePath, vars):
    for file in list(casePath.glob('**/*')):
        if file.is_file():
            content = file.read_text()
            for key, value in vars.items():
                content = content.replace("{"+str(key)+"}", str(value))
            file.write_text(content)

def run_fcn(X):
    global CASECOUNT
    CASECOUNT += 1

    print('############## CASE %05d ##############' % (CASECOUNT))
    cwd = Path(__file__).parent
    case_path = cwd / f'case{CASECOUNT:04d}'
    template_path = cwd / 'template'
    resultsfile_path = cwd / 'results.csv'

    # Make a copy of the template case
    sp.run(['cp', '-r', template_path, case_path], check=True, capture_output=True)

    # Replace variables in the case files
    vars = {
        'alpha': X[0],
        'L': X[1],
        's': X[2]
    }
    replace_variables(case_path, vars)

    # Run the simulation
    sp.run(['./Allrun'], cwd=case_path, check=True, capture_output=True)

    # Extract and write results
    avgP = np.mean(np.loadtxt(case_path / 'postProcessing/pDrop/0/surfaceFieldValue.dat', comments='#', usecols=(1,), unpack=True)[-10:])
    meanT = np.mean(np.loadtxt(case_path / 'postProcessing/outletFluxWeightedTemp/0/surfaceFieldValue.dat', comments='#', usecols=(1,), unpack=True)[-10:])

    if not resultsfile_path.exists():
        with open(resultsfile_path, 'w') as csvfile:
            csvf = csv.writer(csvfile, delimiter=';', lineterminator='\n')
            csvf.writerow(['case', ",".join(vars.keys()), 'avgP', 'meanT'])

    with open(resultsfile_path, 'a') as results:
           csvf = csv.writer(results, delimiter=';', lineterminator='\n')
           csvf.writerow([CASECOUNT, ",".join([str(item) for item in list(vars.values())]), avgP, meanT])

    return [avgP, meanT]  # Return objectives: minimize avgP, maximize meanT

if __name__ == "__main__":
    problem = pp.Problem(3, 2)
    problem.directions[0] = pp.Direction.MINIMIZE
    problem.directions[1] = pp.Direction.MINIMIZE
    problem.types[0] = pp.Real(0, 90)  # var_alpha
    problem.types[1] = pp.Real(0.001, 0.009)  # var_L
    problem.types[2] = pp.Real(0.01, 0.02)  # var_s

    problem.function = run_fcn

    algorithm = pp.NSGAII(problem, population_size=10)
    algorithm.run(100)

    for solution in algorithm.result:
        print(solution.objectives)
