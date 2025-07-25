
# A quick test script to read and print some data from a LoomTxtReader

from LOOM.src.data_classes.LoomTxtReader import LoomTxtReader

file_path = "/home/dunelab/cernbox/LabIFIC/Reflectivities_Jose/Runs/20250714_Measurement5_2.txt"

loom_reader = LoomTxtReader(file_path)
loomset = loom_reader.read()

print("Wavelengths:", loomset.wavelengths[:3])
print("Currents:", loomset.data[0].pmtpos)
print("Metadata:", loomset.metadata)

print("UserTag:", loomset.metadata["User Tag"])
