"""Execute the benchmark notebook with UTF-8 IO (Windows default cp1252 broke `jupyter execute`)."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

NB = Path(__file__).parent / "CAP417_HandsOn04_Benchmark.ipynb"

with open(NB, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": str(NB.parent)}})
client.execute()

with open(NB, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print(f"Executed {len(nb.cells)} cells, saved -> {NB}")
