import random
import numpy as np
import matplotlib.pyplot as plt


economic_col     = [88.0, 66.0, 83] # Min
risk_col         = [120, 18, 10] # Min
reliability_col  = [200, 12, 22] # Max
performance_col  = [800, 250, 300] # Min
power_col        = [2, 4, 5] # Min

# Criteria flags Max (True) Min (False) thingy
maximize_flags = [True, False, False, False, True]

columns = [
    (economic_col,    maximize_flags[0]),
    (risk_col,        maximize_flags[1]),
    (reliability_col, maximize_flags[2]),
    (performance_col, maximize_flags[3]),
    (power_col,       maximize_flags[4])
]


def normalize_column(col_values, maximize=True):
    col_min = min(col_values)
    col_max = max(col_values)
    if maximize:
        return [round(9 * ((x - col_min) / (col_max - col_min)) + 1, 4) for x in col_values]
    else:
        return [round(9 * ((col_max - x) / (col_max - col_min)) + 1, 4) for x in col_values]

normalized_columns = []
for col_data, maximize_flag in columns:
    norm_col = normalize_column(col_data, maximize=maximize_flag)
    normalized_columns.append(norm_col)

normalized_values = list(zip(*normalized_columns))
normalized_values = [list(tup) for tup in normalized_values]

design_names = ["Design A", "Design B", "Design C"]
print("Normalized Values:")
for i, design in enumerate(design_names):
    print(f"{design}: {[f'{val:.4f}' for val in normalized_values[i]]}")

fixed_importance = [0.20, 0.225, 0.25, 0.175, 0.15]

def shuffled_importance(weights):
    shuffled = weights[:]
    random.shuffle(shuffled)
    return shuffled

def compute_score(design_normalized, importance):
    return sum(pc * imp for pc, imp in zip(design_normalized, importance))


num_iterations = 120

randomized_scores = { "Design A": [], "Design B": [], "Design C": [] }

print("\n Importance Scores ")
for i in range(num_iterations):
    rand_weights = shuffled_importance(fixed_importance)
    for idx, design in enumerate(design_names):
        score = compute_score(normalized_values[idx], rand_weights)
        randomized_scores[design].append(score)


#Count the highest score 
tally = { "Design A": 0, "Design B": 0, "Design C": 0 }
for i in range(num_iterations):
    scores = { design: randomized_scores[design][i] for design in design_names }
    max_score = max(scores.values())
    for design, score in scores.items():
        if score == max_score:
            tally[design] += 1

print("\nTally of Highest Scores (Randomized Importance):")
for design in design_names:
    print(f"{design}: {tally[design]} times")


for idx, design in enumerate(design_names):
    fixed_score = compute_score(normalized_values[idx], fixed_importance)
    print(f"{design} Score (Fixed): {fixed_score:.4f}")

# Create radar chart with 120 iterations 
angles = np.linspace(0, 2 * np.pi, num_iterations, endpoint=False).tolist()
angles += angles[:1] 

plt.figure(figsize=(10, 10))
ax = plt.subplot(111, polar=True)

#y-axis limits
ax.set_ylim(0, 10)

for design, color in zip(design_names, ['blue', 'red', 'green']):
    scores = randomized_scores[design]
    scores += scores[:1]  
    ax.plot(angles, scores, label=design, color=color, linewidth=2)

ax.set_title(f"Radar Chart of Randomized Scores over {num_iterations} Iterations", size=15, y=1.05)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(range(1, num_iterations + 1), fontsize=8) 
ax.set_yticks(range(0, 11, 2))  
ax.set_rlabel_position(0)

plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
plt.show()
