/**
 * generate-ring.mjs
 * Run: node generate-ring.mjs
 * Outputs: models/ring.glb  (gold torus as placeholder)
 *
 * This is ONLY needed if you don't have a real ring.glb.
 * Replace models/ring.glb with your actual jewellery model.
 */
import * as THREE from 'three';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';
import { writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const scene = new THREE.Scene();

// Outer ring band
const torusGeo = new THREE.TorusGeometry(0.5, 0.12, 32, 128);
const goldMat  = new THREE.MeshStandardMaterial({
  color: 0xC9A84C,
  metalness: 0.98,
  roughness: 0.12,
});
const torus = new THREE.Mesh(torusGeo, goldMat);
scene.add(torus);

// Small diamond-like gem on top
const gemGeo = new THREE.OctahedronGeometry(0.18, 0);
const gemMat = new THREE.MeshStandardMaterial({
  color: 0xaae4ff,
  metalness: 0.0,
  roughness: 0.0,
  transparent: true,
  opacity: 0.85,
});
const gem = new THREE.Mesh(gemGeo, gemMat);
gem.position.set(0, 0.62, 0);
gem.scale.set(1, 1.4, 1);
scene.add(gem);

const exporter = new GLTFExporter();
exporter.parse(
  scene,
  (result) => {
    const buffer = Buffer.from(result);
    mkdirSync(path.join(__dirname, 'models'), { recursive: true });
    writeFileSync(path.join(__dirname, 'models', 'ring.glb'), buffer);
    console.log('✔ models/ring.glb written (' + buffer.length + ' bytes)');
  },
  (err) => console.error(err),
  { binary: true }
);
