#!/usr/bin/env python
import csv
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def read_csv_file(filename):
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def plot_particles(data):
    x = [float(row[" x"]) for row in data]
    y = [float(row[" y"]) for row in data]
    cluster_ids = [int(row[" clusterId"]) for row in data]

    # Create a custom color map
    cmap = LinearSegmentedColormap.from_list("", ["blue", "purple", "red", "orange", "yellow"])

    plt.scatter(x, y, c=cluster_ids, cmap=cmap, s=1, alpha=0.8)
    plt.colorbar(label="clusterId", fraction=0.046, pad=0.04)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Particle Plot")

    # Set the background color to white
    plt.gca().set_facecolor("white")

    # Save the plot to an SVG file
    plt.savefig("result.svg", format="svg", dpi=1200)

    # Show the plot
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    data = read_csv_file(filename)

    if data:
        plot_particles(data)


if __name__ == "__main__":
    main()
