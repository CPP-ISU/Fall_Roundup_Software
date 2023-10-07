import matplotlib.pyplot as plt

# Sample data for leaderboard
names = ['Alice', 'Bob', 'Charlie', 'David']
scores = [95, 88, 92, 78]

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.barh(names, scores, color='skyblue')

# Customize the appearance
plt.xlabel('Scores')
plt.title('Leaderboard')
plt.xlim(0, max(scores) + 10)  # Set x-axis limit

# Display the scores on the bars
for i, v in enumerate(scores):
    plt.text(v + 1, i, str(v), va='center', fontsize=12)

# Invert the y-axis to display the highest score at the top
plt.gca().invert_yaxis()

# Show the chart
plt.show()
