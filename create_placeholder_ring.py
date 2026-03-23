#!/usr/bin/env python3
"""
create_placeholder_ring.py
Generates a minimal valid GLB (binary glTF) file as a gold torus placeholder.
Run: python3 create_placeholder_ring.py
Outputs: models/ring.glb
"""

import struct, json, math, os

def float32(v): return struct.pack('<f', v)
def uint16(v):  return struct.pack('<H', v)
def uint32(v):  return struct.pack('<I', v)

def build_torus_glb(R=0.5, r=0.11, segs=40, sides=20):
    positions = []
    normals   = []
    indices   = []

    for i in range(segs):
        theta  = 2*math.pi*i/segs
        for j in range(sides):
            phi = 2*math.pi*j/sides
            x = (R + r*math.cos(phi)) * math.cos(theta)
            y = r * math.sin(phi)
            z = (R + r*math.cos(phi)) * math.sin(theta)
            nx = math.cos(phi)*math.cos(theta)
            ny = math.sin(phi)
            nz = math.cos(phi)*math.sin(theta)
            positions += [x, y, z]
            normals   += [nx, ny, nz]

        a = i*sides
        b = ((i+1)%segs)*sides
        for j in range(sides):
            nj = (j+1)%sides
            indices += [a+j, b+j, a+nj, b+j, b+nj, a+nj]

    # Binary buffers
    pos_bytes = b''.join(float32(v) for v in positions)
    nrm_bytes = b''.join(float32(v) for v in normals)
    idx_bytes = b''.join(uint16(v) for v in indices)

    # Pad to 4-byte boundary
    def pad4(b): return b + b'\x00'*((-len(b))%4)
    pos_bytes = pad4(pos_bytes)
    nrm_bytes = pad4(nrm_bytes)
    idx_bytes = pad4(idx_bytes)

    bin_data  = pos_bytes + nrm_bytes + idx_bytes

    bv_pos = {"buffer":0,"byteOffset":0,            "byteLength":len(pos_bytes)}
    bv_nrm = {"buffer":0,"byteOffset":len(pos_bytes),"byteLength":len(nrm_bytes)}
    bv_idx = {"buffer":0,"byteOffset":len(pos_bytes)+len(nrm_bytes),"byteLength":len(idx_bytes)}

    n_verts = len(positions)//3
    n_idx   = len(indices)

    # Min/max for positions
    xs = positions[0::3]; ys = positions[1::3]; zs = positions[2::3]
    pos_min = [min(xs), min(ys), min(zs)]
    pos_max = [max(xs), max(ys), max(zs)]

    gltf = {
        "asset": {"version":"2.0","generator":"Aurē placeholder"},
        "scene": 0,
        "scenes": [{"nodes":[0]}],
        "nodes":  [{"mesh":0}],
        "meshes": [{
            "name": "ring",
            "primitives": [{
                "attributes": {"POSITION":0,"NORMAL":1},
                "indices": 2,
                "material": 0,
                "mode": 4
            }]
        }],
        "materials": [{
            "name": "gold",
            "pbrMetallicRoughness": {
                "baseColorFactor": [0.788, 0.659, 0.298, 1.0],
                "metallicFactor":  0.98,
                "roughnessFactor": 0.12
            }
        }],
        "accessors": [
            {"bufferView":0,"componentType":5126,"count":n_verts,"type":"VEC3",
             "min":pos_min,"max":pos_max},
            {"bufferView":1,"componentType":5126,"count":n_verts,"type":"VEC3"},
            {"bufferView":2,"componentType":5123,"count":n_idx, "type":"SCALAR"}
        ],
        "bufferViews": [bv_pos, bv_nrm, bv_idx],
        "buffers": [{"byteLength": len(bin_data)}]
    }

    json_bytes = json.dumps(gltf, separators=(',',':')).encode('utf-8')
    json_bytes = json_bytes + b' '*((-len(json_bytes))%4)  # pad

    # GLB structure
    MAGIC   = 0x46546C67  # glTF
    VERSION = 2
    JSON_CHUNK = 0x4E4F534A  # JSON
    BIN_CHUNK  = 0x004E4942  # BIN

    chunk_json = uint32(len(json_bytes)) + uint32(JSON_CHUNK) + json_bytes
    chunk_bin  = uint32(len(bin_data))   + uint32(BIN_CHUNK)  + bin_data
    total_len  = 12 + len(chunk_json) + len(chunk_bin)

    header = uint32(MAGIC) + uint32(VERSION) + uint32(total_len)
    glb = header + chunk_json + chunk_bin

    os.makedirs('models', exist_ok=True)
    with open('models/ring.glb', 'wb') as f:
        f.write(glb)
    print(f"✔ models/ring.glb written ({len(glb)} bytes, {n_verts} verts, {n_idx//3} tris)")

if __name__ == '__main__':
    build_torus_glb()
