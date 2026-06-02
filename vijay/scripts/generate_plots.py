import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, gamma
import os
from matplotlib_venn import venn2
import networkx as nx

# Ensure assets directory exists
os.makedirs('assets', exist_ok=True)

def generate_venn():
    plt.figure(figsize=(6, 4))
    # P(6) = 4/52, P(Red) = 26/52, P(6 and Red) = 2/52
    # Venn2 handles (Ab, aB, AB) where A is set 1, B is set 2
    # 10: only A, 01: only B, 11: both
    # A = "6", B = "Red"
    # P(6 and not Red) = 4/52 - 2/52 = 2/52
    # P(Red and not 6) = 26/52 - 2/52 = 24/52
    # P(6 and Red) = 2/52
    venn2(subsets=(2, 24, 2), set_labels=('Event A: 6', 'Event B: Red'))
    plt.title("Venn Diagram of Drawing a 6 and a Red Card")
    plt.savefig('assets/venn_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_histogram():
    n, p = 3, 0.25
    x = np.arange(0, n + 1)
    pmf = binom.pmf(x, n, p)
    
    plt.figure(figsize=(8, 5))
    plt.bar(x, pmf, color='skyblue', edgecolor='navy', alpha=0.7)
    plt.xlabel('Number of Defective Items (X)')
    plt.ylabel('Probability P(X = x)')
    plt.title('Probability Histogram for Binomial Distribution (n=3, p=0.25)')
    plt.xticks(x)
    for i, val in enumerate(pmf):
        plt.text(x[i], val + 0.01, f'{val:.4f}', ha='center')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('assets/histogram.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_gamma_plots():
    x = np.linspace(0, 20, 1000)
    parameters = [(1, 2), (2, 2), (3, 2), (5, 1), (9, 0.5)]
    
    plt.figure(figsize=(10, 6))
    for a, b in parameters:
        # scipy.stats.gamma uses a=alpha, scale=1/beta
        y = gamma.pdf(x, a, scale=1/b)
        plt.plot(x, y, label=f'α={a}, β={b}')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Gamma Distribution PDF for Various Parameters')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('assets/gamma_plots.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_tree_diagram():
    G = nx.Graph()
    # Level 0
    G.add_node("Root", pos=(0, 0))
    # Level 1
    G.add_node("D1", pos=(1, 2))
    G.add_node("N1", pos=(1, -2))
    G.add_edge("Root", "D1")
    G.add_edge("Root", "N1")
    # Level 2
    G.add_node("D1D2", pos=(2, 3))
    G.add_node("D1N2", pos=(2, 1))
    G.add_node("N1D2", pos=(2, -1))
    G.add_node("N1N2", pos=(2, -3))
    G.add_edge("D1", "D1D2")
    G.add_edge("D1", "D1N2")
    G.add_edge("N1", "N1D2")
    G.add_edge("N1", "N1N2")
    # Level 3
    G.add_node("DDD", pos=(3, 3.5))
    G.add_node("DDN", pos=(3, 2.5))
    G.add_node("DND", pos=(3, 1.5))
    G.add_node("DNN", pos=(3, 0.5))
    G.add_node("NDD", pos=(3, -0.5))
    G.add_node("NDN", pos=(3, -1.5))
    G.add_node("NND", pos=(3, -2.5))
    G.add_node("NNN", pos=(3, -3.5))
    G.add_edge("D1D2", "DDD")
    G.add_edge("D1D2", "DDN")
    G.add_edge("D1N2", "DND")
    G.add_edge("D1N2", "DNN")
    G.add_edge("N1D2", "NDD")
    G.add_edge("N1D2", "NDN")
    # Missing edges?
    G.add_edge("N1N2", "NND")
    G.add_edge("N1N2", "NNN")

    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold", arrows=True)
    plt.title("Tree Diagram: 3 Item Inspection (D/N)")
    plt.savefig('assets/tree_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    generate_venn()
    generate_histogram()
    generate_gamma_plots()
    generate_tree_diagram()
    print("Plots generated successfully in assets/ directory.")
