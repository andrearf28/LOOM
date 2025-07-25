import numpy as np
from pathlib import Path
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from collections import defaultdict
import matplotlib.pyplot as plt

from LOOM.src.data_classes.LoomAnalysis import LoomInputParams, LoomAnalysis
from LOOM.src.data_classes.LoomTxtReader import LoomTxtReader
from LOOM.src.data_classes.LoomTxtMultiReader import LoomTxtMultiReader
from LOOM.src.data_classes.LoomSet import LoomSet
from LOOM.src.analysis.reflectivity import utils as ru

class Analysis1(LoomAnalysis):

    def __init__(self):
        pass
        
    @classmethod
    def get_input_params_model(
        cls
    ) -> type:
        """Implements the LoomAnalysis.get_input_params_model()
        abstract method. Returns the InputParams class, which is a
        Pydantic model class that defines the input parameters for
        this example analysis.        
        Returns
        -------
        type
            The InputParams class, which is a Pydantic model class
        """
        class InputParams(LoomInputParams):
            input_path: List[str] = Field(
                default_factory=list,
                description="List of input .txt file paths (1 for single file, >1 for multiple files)"
            )
            output_path: str = Field(
                default="output",
                description="Path to the output folder"
            )
        return InputParams

    def initialize(self, input_parameters: LoomInputParams) -> None:
        self.params = input_parameters
        self.LoomSet: Optional[LoomSet] = None
        self.grouped_data = defaultdict(lambda: defaultdict(list))

    def read_input(self) -> bool:
        input_paths = getattr(self.params, 'input_path', None)

        if not input_paths:
            raise ValueError("'input_path' must be a non-empty list of file paths.")

        if not isinstance(input_paths, list):
            raise TypeError("'input_path' must be a list of strings.")

        if len(input_paths) == 1:
            self.LoomSet = LoomTxtReader(input_paths[0]).read()
        else:
            self.LoomSet = LoomTxtMultiReader(input_paths).read()

        return True

    def analyze(self) -> bool:
        if not self.LoomSet:
            raise RuntimeError("No data. Execute first 'read_input()'.")

        data = self.LoomSet.data
    
        for row in data:
            self.grouped_data[row.revolverpos][row.wavelength].append(row)

        return True

    def plot(self) -> None:
        if not self.grouped_data:
            raise RuntimeError("No data for plotting. Execute 'analyze()' first.")

        revolver_labels = ru.extract_revolver_labels(self.LoomSet.metadata)

        # ==================================================
        # 1. FIGURE: Intensity vs PMT position per revolver
        # ==================================================

        # Adjust the subplot grid based on the number of revolvers
        n_panels = len(self.grouped_data)
        n_cols = 3
        n_rows = -(-n_panels // n_cols)

        fig1, axs = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), squeeze=False)

        for idx, (revolverpos, wavelength) in enumerate(sorted(self.grouped_data.items())):
            ax = axs[idx // n_cols][idx % n_cols]
            label = f"Revolver {revolverpos}: {revolver_labels.get(revolverpos, 'Unknown')}"
            ru.plot_intensities_subplot(ax, wavelength, label)

        for idx in range(n_panels, n_rows * n_cols):
            axs[idx // n_cols][idx % n_cols].axis('off')

        fig1.suptitle("Intensity vs PMT Position per Revolver", fontsize=16)
        fig1.tight_layout(rect=[0, 0, 1, 0.95])
        plt.figure(fig1.number)
        plt.show(block=False)

        # ========================================================
        # 2. FIGURA: Intensidad integrada vs longitud de onda
        # ========================================================
        integrated_by_wavelength = ru.compute_integrated_intensities(self.grouped_data)

        fig2, ax2 = plt.subplots(figsize=(10, 6))

        # integrated_by_wavelength: {revpos: {wavelength: integrated_intensity}}
        for revpos, wavelength_to_intensity in sorted(integrated_by_wavelength.items()):
            wavelengths = sorted(wavelength_to_intensity.keys())
            integrated_intensities = [wavelength_to_intensity[wl] for wl in wavelengths]
            label = f"Revolver {revpos}: {revolver_labels.get(revpos, 'Unknown')}"
            ax2.plot(wavelengths, integrated_intensities, marker='o', label=label)

        ax2.set_title("Integrated Intensity vs Wavelength")
        ax2.set_xlabel("Wavelength (nm)")
        ax2.set_ylabel("Integrated Intensity (A)")  
        ax2.legend()
        ax2.grid(True)
        fig2.tight_layout()
        plt.figure(fig2.number)
        plt.show(block=False)

        # ===================================================
        # 3. FIGURA: Refelectivity: ratio muestra / no sample
        # ===================================================
        no_sample_revpos = next((rp for rp, lbl in revolver_labels.items() if "no sample" in lbl.lower()), None)
        if no_sample_revpos is None:
            print("Warning: No 'No sample' position found in metadata. Skipping reflectivity ratio plot.")
            return

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        for revpos, wl_data in sorted(integrated_by_wavelength.items()):
            if revpos == no_sample_revpos:
                continue  # Skip "no sample"

            common_wavelengths = sorted(set(wl_data) & set(integrated_by_wavelength[no_sample_revpos]))
            ratios = [
                wl_data[wl] / integrated_by_wavelength[no_sample_revpos][wl]
                if integrated_by_wavelength[no_sample_revpos][wl] != 0 else 0
                for wl in common_wavelengths
            ]
            label = f"Revolver {revpos}: {revolver_labels.get(revpos, 'Unknown')}"
            ax3.plot(common_wavelengths, ratios, marker='o', label=label)

        ax3.set_title("Reflectivity Ratio (Sample / No Sample) vs Wavelength")
        ax3.set_xlabel("Wavelength (nm)")
        ax3.set_ylabel("Ratio")
        ax3.legend()
        ax3.grid(True)
        fig3.tight_layout()
        plt.figure(fig3.number)
        plt.show(block=False)

        plt.show()

    def write_output(self) -> bool:
        return True
