# ◈ Aurē — Virtual Ring Try-On

A browser-based virtual ring try-on experience using:
- **MediaPipe Hands** for real-time 21-point hand landmark detection
- **Three.js** for 3D ring rendering & placement
- **getUserMedia** for webcam / phone camera access
- **Pure static HTML/CSS/JS** — zero build step required

---

## 🗂 Project Structure

```
ring-tryon/
├── index.html                  ← Entry point
├── src/
│   ├── app.js                  ← Main logic (camera + hand tracking + Three.js)
│   └── style.css               ← Luxury dark UI styles
├── models/
│   └── ring.glb                ← 3D ring model (replace with your own!)
├── create_placeholder_ring.py  ← Generates a gold torus placeholder GLB
├── generate-ring.mjs           ← Alternative Node.js GLB generator
└── README.md
```

---

## 🚀 Deployment

### Option A — GitHub Pages (Recommended, Free)

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source → Deploy from a branch → `main` / `root`**
3. Your app will be live at `https://<your-username>.github.io/<repo-name>/`

> ⚠️ Camera access requires **HTTPS**. GitHub Pages serves over HTTPS automatically.

### Option B — Netlify / Vercel (Drag & Drop)

1. Zip the entire project folder
2. Drag & drop onto [netlify.com/drop](https://app.netlify.com/drop) or [vercel.com/new](https://vercel.com/new)
3. Done — live in seconds

### Option C — Local (with HTTPS)

Camera APIs require a secure context. Use one of:

```bash
# Python (HTTP only — camera won't work)
python3 -m http.server 8080

# Node http-server with self-signed HTTPS
npx http-server -S -C cert.pem -K key.pem -p 8443

# Or use VS Code Live Server extension (localhost is allowed)
```

> `localhost` is treated as a secure context by browsers, so plain `http://localhost` works for development.

---

## 💍 Using Your Own Ring Model

1. Export your ring as `.glb` (binary glTF)
2. Replace `models/ring.glb` with your file
3. That's it — the loader auto-normalises the scale

**Alternatively**, click **"⬆ Upload Ring (.glb)"** in the UI to test any `.glb` file without replacing the default.

### Tips for a good ring model
- Keep poly count under 50k triangles for smooth mobile performance
- Ensure the ring's "hole" axis is along **Y** (up)
- Use PBR metallic/roughness materials for realistic gold appearance
- Free sources: [Sketchfab](https://sketchfab.com), [Poly Pizza](https://poly.pizza)

---

## 🖐 How It Works

```
getUserMedia → <video> frame
        ↓
MediaPipe Hands → 21 landmarks (x, y, z) per hand
        ↓
Pick finger MCP + PIP keypoints
        ↓
Map normalised (0–1) landmark coords → Three.js orthographic scene coords
        ↓
Position ring pivot at midpoint, rotate along finger vector, scale to segment length
        ↓
Three.js renders ring on transparent canvas layered above mirrored video
```

---

## 🎛 Features

| Feature | Description |
|---|---|
| Finger selector | Choose ring / index, left / right hand |
| Ring Size slider | Fine-tune the fit (0.4× – 2.0×) |
| Upload custom GLB | Try any `.glb` ring model live |
| Rear / front camera | Uses rear cam on mobile, falls back to front |
| Placeholder ring | Gold torus rendered if `ring.glb` is missing |

---

## 🐛 Troubleshooting

| Issue | Fix |
|---|---|
| Camera not working | Must be on HTTPS or localhost |
| Ring not visible | Ensure hand is well-lit and fully visible |
| Ring misaligned | Adjust Ring Size slider; try different finger option |
| GLB fails to load | Check file is valid glTF 2.0 binary; try re-exporting |
| MediaPipe CDN slow | First load may take 5–10 s; subsequent loads use browser cache |

---

## 📄 License

MIT — free to use, modify, and deploy.
