# Source freeze: the revision local compilation must target

After applying both patches, these two files must hash to the stated values. Any other value
means a different revision than the one reviewed here.

| file (post-patch) | sha256 |
|---|---|
| `lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` | `48aa378f6f6db82bfeb0e65920ec2606507364541e72bf77ab969c6c87895dd1` |
| `lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean` | `58707f0495837a89b58d5ac7d131ee855220c74cba28851474489b7a8cdd9e0d` |

| file (input, must stay unchanged) | sha256 |
|---|---|
| `lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` | `6602b9d8f20bbdfd447f2f3fcfa523f2c33d09c247e3d2983be7503df9f2dc9b` |
| `lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean` | `ca74ba1033fead55133670218739a36b4c75173d9b04d765affd19da9d215cc0` |

## Root-closed OAI closure (14 modules), frozen

The closure table records the **pre-patch** state (that is what the patches are made against).
After applying them, the two edited modules take the post-patch hashes in the first table; every
other module in the closure must hash exactly as listed.

| module | sha256 |
|---|---|
| `OAI.Analysis.PlaneSpectrum.Basic` | `6db8eef0290bb1962405e338d049d19a1a77ff9e58a50251ca0aa6835c2b3d16` |
| `OAI.Analysis.PlaneSpectrum.Characters` | `3879bd9d07340af833a1350db7add3ab03d856af920410ce7bb9c24dc17d5f07` |
| `OAI.Analysis.PlaneSpectrum.ConditionalSpectrum` | `6602b9d8f20bbdfd447f2f3fcfa523f2c33d09c247e3d2983be7503df9f2dc9b` |
| `OAI.Analysis.PlaneSpectrum.FourierTests` | `f3625fb3399e28a5db3f531b7d2ac602988a8656fb28e6dd0747167a4be1393c` |
| `OAI.Analysis.PlaneSpectrum.InvariantMean` | `33798cddc6dc5be9c3f2c963d393da2b4b5274f45f0f255dcb9b36c565f4b84b` |
| `OAI.Analysis.PlaneSpectrum.Multipliers` | `6bc285bc0da10d8ed7875b03f8ca49a6d2c8fa19a4597b1bb09b01018bf8c092` |
| `OAI.Analysis.PlaneSpectrum.PhaseCollision` | `10d6acf8d99c8209f225e9b35d1cbb4e4ab0738840b481bf7f72739534bb2627` |
| `OAI.Analysis.PlaneSpectrum.PhaseEncoding` | `e941182ef95925e8472e94f79b1cc8adce7ee289f626d87f06d6d8092270ec54` |
| `OAI.Analysis.PlaneSpectrum.SmallArcs` | `9c317fcfa15cf19a00aef927007704e78cf33269bb82d45065cb8a95160fe690` |
| `OAI.MeasureTheory.CompactFactors.Approximation` | `f6adcc691c345ddbe4fad40746f2e0da11be96b961c528f49af01e9ea8e5c30d` |
| `OAI.MeasureTheory.CompactFactors.Centers` | `de094ea004737839cae2ce4829db40c78a2f1da8031459188ad5c271a7d98634` |
| `OAI.MeasureTheory.CompactFactors.ConditionalLimits` | `ca74ba1033fead55133670218739a36b4c75173d9b04d765affd19da9d215cc0` |
| `OAI.MeasureTheory.CompactFactors.ConditionalSelection` | `2f19feac00b8ec75d265e04707bdda09aecb6bfb44965d34646f568743ca8e66` |
| `OAI.MeasureTheory.CompactFactors.RelativeCenters` | `cae5e5e4cca54436788e66ea37b0a8818ef1156d8ccbbcb443bf7884169f7577` |

## Mathlib

Import roots in this closure: `Mathlib`

Pinned toolchain: Lean 4.34.1 + mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` via
`scripts/fetch_exact_env.sh`; do not substitute another cache.

## Verify

```bash
cd <repo>
sha256sum lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean \
          lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean
```
