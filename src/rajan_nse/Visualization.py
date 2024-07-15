import matplotlib.pyplot as plt
import seaborn as sns

class Visualization:
    def plotDistribution(self, data, save=False, filePath='distribution_plot.png'):
        # Plotting using seaborn
        plt.figure(figsize=(10, 6))
        sns.histplot(data, kde=True, bins=30, color='blue', edgecolor='black')
        plt.title('Distribution Plot of CH_TOT_TRADED_QTY')
        plt.xlabel('CH_TOT_TRADED_QTY')
        plt.ylabel('Frequency')
        plt.grid(True)

        if save:
            plt.savefig(filePath)
        else:
            plt.show()