import base64
import logging
import sys

from construct import Struct, Const, Float32l, Int32ul, Array, GreedyRange, this
from mesh import Mesh


BMFVec3D = Struct("x" / Float32l, "y" / Float32l, "z" / Float32l)
BMFVec3D.__repr__ = lambda self: f"Vector3D(x={self.x}, y={self.y}, z={self.z})"

BMFFace = Struct("vertex_indices" / Array(3, Int32ul))
BMFFace.__repr__ = lambda self: f"Face(vertex_indices={self.vertex_indices})"

BMFFormat = Struct(
    "header" / Const(b"0FMB"),
    "start_of_vertices" / Const(b"0VoS"),
    "num_vertices" / Int32ul,
    "vertices" / Array(this.num_vertices, BMFVec3D),
    "end_of_vertices" / Const(b"0VoE"),
    "start_of_group" / Const(b"0GoS"),
    "start_of_faces" / Const(b"0FoS"),
    "num_faces" / Int32ul,
    "faces" / Array(this.num_faces, BMFFace),
    "end_of_faces" / Const(b"0FoE"),
    "start_of_normals" / Const(b"0NoS"),
    "num_normals" / Int32ul,
    "normals" / Array(this.num_normals, BMFVec3D),
    "end_of_normals" / Const(b"0NoE"),
    "end_of_group" / Const(b"0GoE"),
    "footer" / Const(b"0BMF"),
)


def bmf_to_stl(bmf_file: str, stl_file_path: str) -> None:
    with open(bmf_file, "rb") as file:
        logging.info(f"Reading BMF file: {bmf_file}")

        bmf_data = file.read()
        bmf_decoded = base64.b64decode(bmf_data)

        bmf_parsed = BMFFormat.parse(bmf_decoded)
        logging.info(f"BMF parsed.")

        mesh = Mesh.from_bmf(bmf_parsed)
        logging.info(f"Generated Mesh: {mesh}")

        mesh.to_stl(stl_file_path)
        logging.info(f"STL file written to: {stl_file_path}")


def run():
    bmf_to_stl("models/left.bmf", "models/left.stl")
    bmf_to_stl("models/right.bmf", "models/right.stl")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    run()
