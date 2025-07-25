import matplotlib
matplotlib.use('TkAgg')  # Open interactive plot window

import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

from LOOM.src.data_classes.LoomTxtReader import LoomTxtReader


def main():
    # Load the data
    file_path = "/home/dunelab/cernbox/LabIFIC/Reflectivities_Jose/Runs/20250714_Measurement5_2.txt"
    loomset = LoomTxtReader(file_path).read()
    data = loomset.data

    # Group by revolver position
    grouped_by_rev = defaultdict(list)
    for row in data:
        grouped_by_rev[row.revolverpos].append(row)

    n_plots = len(grouped_by_rev)
    n_cols = 3
    n_rows = (n_plots + n_cols - 1) // n_cols

    fig, axs = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), squeeze=False)

    for idx, (revpos, rows) in enumerate(sorted(grouped_by_rev.items())):
        ax = axs[idx // n_cols][idx % n_cols]

        # Group by wavelength
        grouped_by_wl = defaultdict(list)
        for r in rows:
            grouped_by_wl[r.wavelength].append(r)

        for wl, wl_rows in grouped_by_wl.items():
            wl_rows.sort(key=lambda r: r.pmtpos)

            x = [r.pmtpos for r in wl_rows]
            y = [r.current - r.dc for r in wl_rows]
            y_err = [r.current_std if hasattr(r, 'current_std') else 0 for r in wl_rows]

            ax.errorbar(x, y, yerr=y_err, fmt='o-', label=f"{wl:.0f} nm")

        ax.set_title(f"Revolver Pos: {revpos}")
        ax.set_xlabel("PMT Position (º)")
        ax.set_ylabel("Intensity (A)")
        ax.grid(True)
        ax.legend(fontsize='x-small', loc='best')

        # Rotate ticks if needed (only if there are many)
        if len(set(x)) > 6:
            ax.tick_params(axis='x', rotation=45)

    # Turn off unused subplots
    for j in range(n_plots, n_rows * n_cols):
        axs[j // n_cols][j % n_cols].axis('off')

    fig.suptitle("Reflectivity per Revolver Position", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    print("Showing plot...")
    plt.show()
    print("Plot closed.")


if __name__ == "__main__":
    main()
