class Vector3D:
    def __init__(self):
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0

    @staticmethod
    def from_obj(bmf_data) -> "Vector3D":
        v = Vector3D()
        v.x = bmf_data.x
        v.y = bmf_data.y
        v.z = bmf_data.z
        return v

    @staticmethod
    def from_tuple(t: tuple[float, float, float]) -> "Vector3D":
        v = Vector3D()
        v.x = t[0]
        v.y = t[1]
        v.z = t[2]
        return v

    def __repr__(self):
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"


class Face:
    def __init__(
        self,
        vertex_indices,
        vertex_normals,
    ):
        vi = vertex_indices
        vn = vertex_normals

        self.vertex_indices: tuple[int, int, int] = [vi[0], vi[1], vi[2]]
        self.vertex_normals = [
            Vector3D.from_obj(vn[0]),
            Vector3D.from_obj(vn[1]),
            Vector3D.from_obj(vn[2]),
        ]
        self.face_normal = Face.calc_avg_normal(vertex_normals)

    def __repr__(self):
        return f"Face(vertex_indices={self.vertex_indices}, vertex_normals={self.vertex_normals})"

    @staticmethod
    def calc_avg_normal(normals: list[Vector3D]) -> Vector3D:
        avg_x = sum(normal.x for normal in normals) / len(normals)
        avg_y = sum(normal.y for normal in normals) / len(normals)
        avg_z = sum(normal.z for normal in normals) / len(normals)

        magnitude = (avg_x**2 + avg_y**2 + avg_z**2) ** 0.5
        avg_normal = Vector3D.from_tuple(
            (avg_x / magnitude, avg_y / magnitude, avg_z / magnitude)
        )
        return avg_normal


class Mesh:
    def __init__(self, vertices: list[Vector3D], faces: list[Face]):
        self.vertices: list[Vector3D] = vertices
        self.faces: list[Face] = faces

    @staticmethod
    def from_bmf(bmf_data) -> "Mesh":
        vertices = [Vector3D.from_obj(v) for v in bmf_data.vertices]
        chunked_normals = [
            bmf_data.normals[i : i + 3] for i in range(0, len(bmf_data.normals), 3)
        ]
        faces = [
            Face(f.vertex_indices, n) for f, n in zip(bmf_data.faces, chunked_normals)
        ]
        return Mesh(vertices, faces)

    def __repr__(self):
        return f"Mesh(num_vertices={len(self.vertices)}, num_faces={len(self.faces)})"

    def to_stl(self, stl_file_path: str) -> None:
        with open(stl_file_path, "w") as stl_file:
            # Write STL header
            stl_file.write("solid mesh\n")

            # Write face data
            for face in self.faces:
                fn = face.face_normal
                stl_file.write(f"facet normal {fn.x} {fn.y} {fn.z}\n")
                stl_file.write("outer loop\n")

                # Write vertex data
                for index in face.vertex_indices:
                    vertex = self.vertices[index]
                    stl_file.write(f"vertex {vertex.x} {vertex.y} {vertex.z}\n")

                stl_file.write("endloop\n")
                stl_file.write("endfacet\n")

            # Write STL footer
            stl_file.write("endsolid mesh\n")
