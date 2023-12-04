from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle


def make():
    file: str = "utils/images/continuous_example2.png"
    fig, ax = plt.subplots()
    box = Rectangle(xy=(0, 0), width=5, height=5, alpha=0.1)
    item0 = Rectangle(xy=(0, 0), width=2, height=2, alpha=0.2, linewidth=1, edgecolor='k')
    item1 = Rectangle(xy=(2, 0), width=2, height=4, alpha=0.2, linewidth=1, edgecolor='k',
                      facecolor='r')
    item2 = Rectangle(xy=(0, 2), width=3, height=1, alpha=0.2, linewidth=1, edgecolor='k',
                      facecolor='g')
    ax.add_patch(box)
    ax.add_patch(item0)
    ax.add_patch(item1)
    ax.add_patch(item2)
    ax.annotate(0, (1, 1), color='black', weight='bold', fontsize=10, ha='center', va='center')
    ax.annotate(1, (3, 2), color='black', weight='bold', fontsize=10, ha='center', va='center')
    ax.annotate(2, (1.5, 2.5), color='black', weight='bold', fontsize=10, ha='center',
                va='center')
    # for x in range(5):
    #     for y in range(5):
    #         ax.add_patch(Circle(xy=(x, y), radius=0.05, facecolor='black'))
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.savefig(file)
    plt.close()
    return None
