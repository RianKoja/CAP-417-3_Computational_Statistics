import sys
import os

# Add the current directory to sys.path to allow importing from 'scripts'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils import export_to_typst
from part1_analysis import run_part1
from part2_analysis import run_part2
from part3_analysis import run_part3


def main():
    print("Starting full analysis...")

    metrics = {}

    print("Running Part 1...")
    metrics.update(run_part1())

    print("Running Part 2...")
    metrics.update(run_part2())

    print("Running Part 3...")
    metrics.update(run_part3())

    print("Exporting metrics to Typst...")
    export_to_typst(metrics, "report/metrics.typ")

    print("Analysis complete!")


if __name__ == "__main__":
    main()
