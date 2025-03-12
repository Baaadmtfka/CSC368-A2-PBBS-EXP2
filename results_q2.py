# results Q2
import matplotlib.pyplot as plt

def plot_sweep(x_values, raw_data, consts, title, xlabel, output_filename):
    plt.figure(figsize=(8,10))
    
    # Define distinct markers for each benchmark
    markers = {
        "BFS": "o",       # Circle
        "KNN": "s",       # Square
        "LRS": "^",       # Triangle Up
        "SORT": "D"       # Diamond
    }
    
    # For each benchmark, compute accuracies and plot its line
    for benchmark, cond_incorrect_list in raw_data.items():
        const = consts[benchmark]
        accuracies = [(const - ci) / const for ci in cond_incorrect_list]
        plt.plot(x_values, accuracies, marker=markers.get(benchmark, "o"), linestyle='-', label=benchmark)
        for xi, acc in zip(x_values, accuracies):
            plt.annotate(f'{acc:.3f}', (xi, acc), textcoords="offset points", xytext=(0,5), ha='center')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Accuracy")
    plt.ylim(0.84, 0.98)
    plt.grid(True)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-large')
    plt.savefig(output_filename, bbox_inches='tight')
    plt.show()

def main():
    cond_predicted = {
        "BFS": 3440,
        "KNN": 711833,
        "LRS": 11970,
        "SORT": 476
    }
    
    # Sweep 1: localPredictorSize
    x_local = [256, 512, 1024, 2048, 4096]
    local_data = {
        "BFS":  [531, 486, 458, 427, 370],
        "KNN":  [22075, 22032, 21985, 21077, 21224],
        "LRS":  [606, 573, 500, 459, 427],
        "SORT": [26, 23, 22, 18, 17]
    }
    
    plot_sweep(
        x_values=x_local,
        raw_data=local_data,
        consts=cond_predicted,
        title="TournamentBP: Accuracy vs. localPredictorSize",
        xlabel="localPredictorSize",
        output_filename="localPredictorSize_sweep_accuracy.pdf"
    )
    
    # Sweep 2: globalPredictorSize
    x_global = [1024, 2048, 4096, 8192, 16384]
    global_data = {
        "BFS":  [438, 451, 450, 427, 423],
        "KNN":  [21209, 21124, 21055, 21077, 21080],
        "LRS":  [492, 499, 464, 459, 449],
        "SORT": [22, 22, 18, 18, 16]
    }
    
    plot_sweep(
        x_values=x_global,
        raw_data=global_data,
        consts=cond_predicted,
        title="TournamentBP: Accuracy vs. globalPredictorSize",
        xlabel="globalPredictorSize",
        output_filename="globalPredictorSize_sweep_accuracy.pdf"
    )

if __name__ == "__main__":
    main()
