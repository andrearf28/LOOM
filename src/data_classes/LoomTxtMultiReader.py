# src/readers/MultiTxtLoomReader.py

from typing import List, Dict
from LOOM.src.data_classes.LoomSet import LoomSet
from LOOM.src.data_classes.LoomRow import LoomRow
from LOOM.src.data_classes.LoomTxtReader import LoomTxtReader
import os

class LoomTxtMultiReader:

    def __init__(self, paths: List[str]):
        self.paths = paths

    def read(self) -> LoomSet:
        combined_rows: List[LoomRow] = []
        combined_metadata: Dict[str, dict] = {}

        for path in self.paths:
            reader = LoomTxtReader(path)
            loom_set = reader.read()

            filename = os.path.basename(path)
            combined_metadata[filename] = loom_set.metadata
            combined_rows.extend(loom_set.data)

        print(f"✅ Merged {len(self.paths)} files into one LoomSet (metadata kept per file).")
        return LoomSet(metadata=combined_metadata, data=combined_rows)
