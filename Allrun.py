#import openturns.coupling_tools as ct
from pathlib import Path
import subprocess as sp

CASECOUNT = 0

def replace_variables(casePath, vars):
    cwd = Path(__file__).parent
    for file in cwd.glob(f"{casePath}/**/*"):
        if file.is_file():
            content = file.read_text()
            for key, value in vars.items():
                content = content.replace(key, str(value))
            file.write_text(content)

def write_parameter_file(casePath, vars):
    with open(Path(casePath) / 'parameters', 'w') as f:
        for key, value in vars.items():
            f.write(f"{key} {value}\n")

def create_case_from_template(casePath):
    template_path = Path(__file__).parent / 'template'
    sp.run(['cp', '-r', str(template_path), casePath], check=True, capture_output=True)

def simulate(casePath):
    sp.run(['./Allrun'], cwd=Path(casePath), check=True, capture_output=True)

def run(vars):
    global CASECOUNT
    CASECOUNT += 1
    print('############## CASE %05d ##############' % (CASECOUNT))
    casePath = "case%05d" % (CASECOUNT)
    create_case_from_template(casePath) 
    replace_variables(casePath, vars)
    write_parameter_file(casePath, vars)
    simulate(casePath)

if __name__ == "__main__":

    vars = {
        'var_alpha': 10,
        'var_L': 0.003,
        'var_s': 0.01
    }

    run(vars)

    vars = {
        'var_alpha': 20,
        'var_L': 0.003,
        'var_s': 0.01
    }

    run(vars)
