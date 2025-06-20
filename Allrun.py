from pathlib import Path
import subprocess as sp
import numpy as np
import platypus as pp

CASECOUNT = 0

def run(X):
    global CASECOUNT
    print(f'Running case {CASECOUNT} with parameters: {X}')
    current_path = Path(__file__).parent
    case_path = current_path / f'case{CASECOUNT:04d}'
    template_path = current_path / 'template'
    results_path = current_path / 'results.txt'

    sp.run(['cp', '-r', str(template_path), str(case_path)], check=True, capture_output=True)

    vars = {'alpha': X[0],
            's': X[1]}

    for file in list(case_path.glob('**/*.py')):
        content = file.read_text()
        for key, value in vars.items():
            content = content.replace("{"+str(key)+"}", str(value))
        file.write_text(content)
            
    sp.run(['./Allrun'], cwd=case_path, check=True, capture_output=True)

    pDrop = np.mean(np.loadtxt(case_path / 'postProcessing/pDrop/0/surfaceFieldValue.dat', comments='#', usecols=(1,), unpack=True)[-10:])
    TMean = np.mean(np.loadtxt(case_path / 'postProcessing/outletFluxWeightedTemp/0/surfaceFieldValue.dat', comments='#', usecols=(1,), unpack=True)[-10:])

    if not results_path.exists():
        with open(results_path, 'w') as results_file:
            results_file.write('#Case, alpha, s, pDrop, TMean\n')

    with open(results_path, 'a') as results_file:
        results_file.write(f'{CASECOUNT:04d}, {X[0]}, {X[1]}, {pDrop}, {TMean}\n')

    CASECOUNT += 1

    return [pDrop, -TMean]

if __name__ == '__main__':

    problem = pp.Problem(2, 2)
    problem.directions[0] = pp.Direction.MINIMIZE
    problem.directions[1] = pp.Direction.MINIMIZE

    problem.types[0] = pp.Real(0, 90)
    problem.types[1] = pp.Real(0.008, 0.04)

    problem.function = run

    algorithm = pp.NSGAIII(problem, divisions_outer=12, population_size=20)
    algorithm.run(100)
