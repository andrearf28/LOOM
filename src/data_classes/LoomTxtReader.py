# src/readers/TxtLoomReader.py

from typing import List
from LOOM.src.data_classes.LoomSet import LoomSet
from LOOM.src.data_classes.LoomRow import LoomRow

class LoomTxtReader:

    def __init__(self, path: str):
        self.path = path

    def read(self) -> LoomSet:
        metadata = {}
        data_rows: List[LoomRow] = []

        with open(self.path, "r") as f:
            lines = f.readlines()

        # Separate sections
        header_lines = []
        data_lines = []
        in_data = False

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("UNIXTime"):
                header = line
                in_data = True
                continue
            if in_data:
                data_lines.append(line)
            else:
                header_lines.append(line)

        # Processing metadata
        scan_info = []
        for line in header_lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Active:"):
                entries = line.split(",")
                active_dict = {}
                for entry in entries:
                    if ":" in entry:
                        key, value = entry.split(":", 1)
                        active_dict[key.strip()] = value.strip()
                scan_info.append(active_dict)
            elif ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        if scan_info:
            metadata["ScanInfo"] = scan_info

        # Processing data rows
        for line in data_lines:
            tokens = line.split(",")
            if len(tokens) < 11:
                continue  

            row = LoomRow(
                unixtime=float(tokens[0]),
                revolverpos=int(tokens[1]),
                samplepos=float(tokens[2]),
                pmtpos=float(tokens[3]),
                wavelength=float(tokens[4]),
                current=float(tokens[5]),
                current_std=float(tokens[6]),
                dc=float(tokens[6]),
                dc_std=float(tokens[7]),
                temperature=float(tokens[9]),
                humidity=float(tokens[10])
            )
            data_rows.append(row)

        print("✅ LoomSet object created.")
        return LoomSet(metadata=metadata, data=data_rows)