# results Q1
import matplotlib.pyplot as plt
import numpy as np

def generate_bar_chart():
    # Hard-coded accuracy values.
    data = {
        "BFS": {"LocalBP": (3440 - 1035) / 3440, "TournamentBP": (3440 - 427) / 3440},
        "KNN": {"LocalBP": (711833 - 32484) / 711833, "TournamentBP": (711833 - 21077) / 711833},
        "LRS": {"LocalBP": (11970 - 1126) / 11970, "TournamentBP": (11970 - 459) / 11970},
        "SORT": {"LocalBP": (476 - 149) / 476, "TournamentBP": (476 - 18) / 476}
    }
    
    benchmarks = list(data.keys())
    predictors = list(next(iter(data.values())).keys())

    x = np.arange(len(benchmarks))
    width = 0.8 / len(predictors)
    offset = -width * (len(predictors) - 1) / 2.0

    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, predictor in enumerate(predictors):
        values = [data[bench][predictor] for bench in benchmarks]
        bars = ax.bar(x + offset + i * width, values, width, label=predictor)
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    ax.set_ylabel('Branch Prediction Accuracy')
    ax.set_title('Branch Prediction Accuracy by Benchmark and Predictor')
    ax.set_xticks(x)
    ax.set_xticklabels(benchmarks)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig("branch_accuracy_chart.pdf")
    plt.show()

if __name__ == "__main__":
    generate_bar_chart()
