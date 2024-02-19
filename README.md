Code to parse volumetric BMF models used by Volumental.

The code currently:

1. Parses the model into ASCII STL.
2. Computes averaged face normals from the vertex normals, so there is a loss of information.

Format specification credits: https://paulbourke.net/dataformats/bmf_2/

Dependency: `Construct` library to parse to BMF binary format.
