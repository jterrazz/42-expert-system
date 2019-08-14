import re
import sys

from expert_system.helpers.Color import Ft_colors
from expert_system.parsers.ExpertParser import ExpertParser

# tmp = '! ( A + B ) ^ ( D | K )'
# tmp = re.split('\s', tmp)
# infix_to_postfix(tmp)


# Main Function
if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines(1000)
    except:
        print('Error opening file for reading ..!!')

    # TMP
    # content = "A + B => C"
    parser = ExpertParser(content)

    # bcolors = Ft_colors()
    # if ft_parser(content):
    #     print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
    # else:
    #     print(bcolors.FAIL + "KO" + bcolors.ENDC)
