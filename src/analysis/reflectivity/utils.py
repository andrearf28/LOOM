def extract_revolver_labels(metadata: dict) -> dict:
    """
    Returns a dictionary mapping each revolver position (revpos) to its corresponding label.
    If multiple labels exist for the same revpos, only the first occurrence is kept.
    """
    labels = {}

    scan_info = metadata.get("ScanInfo", [])
    for entry in scan_info:
        if not isinstance(entry, dict):
            continue
        revpos = entry.get("Rev.Pos")
        label = entry.get("Label")
        if revpos is not None and label is not None:
            revpos_int = int(revpos)
            if revpos_int not in labels:
                labels[revpos_int] = label.strip()

    return labels

def plot_intensities_subplot(ax, wavelength_groups, rev_label):
    for wl, entries in sorted(wavelength_groups.items()):
        entries.sort(key=lambda e: e.pmtpos)
        x = [e.pmtpos for e in entries]
        y = [e.current - e.dc for e in entries]
        y_err = [getattr(e, 'current_std', 0) for e in entries]
        ax.errorbar(x, y, yerr=y_err, fmt='o-', label=f"{wl:.0f} nm")
    
    ax.set_title(f"{rev_label}")
    ax.set_xlabel("PMT Position (º)")
    ax.set_ylabel("Intensity (A)")
    ax.grid(True)
    ax.legend(fontsize='x-small', loc='best')
    if len(set(x)) > 6:
        ax.tick_params(axis='x', rotation=45)

def compute_integrated_intensities(grouped_data) -> dict:
    """
    Computes the integrated intensity for each wavelength in the grouped data.

    Returns:
        dict: {revpos: {wavelength: integrated_intensity}}
    """
    from collections import defaultdict

    integrated = defaultdict(lambda: defaultdict(float))
    for revpos, wavelengths in grouped_data.items():
        for wl, rows in wavelengths.items():
            integrated[revpos][wl] = sum(r.current for r in rows)
    return integrated