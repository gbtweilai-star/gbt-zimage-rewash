# zimage_rewash

**One capability bit from GBT V8, packaged standalone.** No. 61 of 341,
`creation` domain (Creation).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> 洗图流水线（看图→反推提示词→重绘→放大）：**放大环已可用**（ffmpeg lanczos+unsharp，零依赖）；反推环**已接线**（2026-10-15 起 zimage_rewash_cap 走 vision 通道；2026-10-16 增形式化反推件 tools/codex-scripts/img-reverse.py）；**语义反推**仍待外部理解通道（teamorouter 401 / 本地 8111 未监听）——缺什么就写什么；重绘环**未接线**（未装 ComfyUI；pollinations img2img 需公网可达图 URL）；含降噪强度口径表 0.15→0.85 四档。⚠️ **2026-10-13 收敛（主人令「每一个调节都要触手可控」）**：本位是**历史腿**，主腿 = `comfy_native.upscale_4k`（PIL LANCZOS + USM；`vision_print.polish` 的清晰度腿走它）。收敛**分两类做、不搞假统一**：① **几何旋钮真统一** —— `scale`（新名，倍数）＝旧名 `factor`，且都接受 `size`（目标绝对宽，按源图宽换算成倍数走同一条路）；两个名字同时给且不等 ⇒ **fail-closed**。② **锐化旋钮不统一、且显式拒** —— 本位只有 `unsharp`（**ffmpeg unsharp 滤镜的 amount**），主腿是 `sharpen`（**PIL USM 的 percent 比例**），**两个算法两个量纲**；把 `sharpen` 传给本位 ⇒ **当场 fail-closed 并指路主腿**（改名冒充＝假统一，更害人）。参数判在**过门之前**（参数错不消耗授权）。

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-zimage-rewash.git
cd gbt-zimage-rewash
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_zimage_rewash info                  # capability card
python -m gbt_zimage_rewash spec --json           # machine-readable contract
python -m gbt_zimage_rewash check --payload '{}'
python -m gbt_zimage_rewash run   --payload '{}'
```

Real `info` output from this machine:

```text
zimage_rewash  (creation)  v1.0.0
----------------------------------------
洗图流水线（看图→反推提示词→重绘→放大）：**放大环已可用**（ffmpeg lanczos+unsharp，零依赖）；反推环**已接线**（2026-10-15 起 zimage_rewash_cap 走 vision 通道；2026-10-16 增形式化反推件 tools/codex-scripts/img-reverse.py）；**语义反推**仍待外部理解通道（teamorouter 401 / 本地 8111 未监听）——缺什么就写什么；重绘环**未接线**（未装 ComfyUI；pollinations img2img 需公网可达图 URL）；含降噪强度口径表 0.15→0.85 四档。⚠️ **2026-10-13 收敛（主人令「每一个调节都要触手可控」）**：本位是**历史腿**，主腿 = `comfy_native.upscale_4k`（PIL LANCZOS + USM；`vision_print.polish` 的清晰度腿走它）。收敛**分两类做、不搞假统一**：① **几何旋钮真统一** —— `scale`（新名，倍数）＝旧名 `factor`，且都接受 `size`（目标绝对宽，按源图宽换算成倍数走同一条路）；两个名字同时给且不等 ⇒ **fail-closed**。② **锐化旋钮不统一、且显式拒** —— 本位只有 `unsharp`（**ffmpeg unsharp 滤镜的 amount**），主腿是 `sharpen`（**PIL USM 的 percent 比例**），**两个算法两个量纲**；把 `sharpen` 传给本位 ⇒ **当场 fail-closed 并指路主腿**（改名冒充＝假统一，更害人）。参数判在**过门之前**（参数错不消耗授权）。

gated      : True   <- needs explicit consent
external   : False
multi-op   : False
params     : (none)
```

Wire a real implementation:

```python
from gbt_zimage_rewash import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Single-action bit.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.12s
```

## Provenance

| field | value |
|---|---|
| capability | `zimage_rewash` |
| domain | `creation` |
| handler | `zimage_rewash` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [creation/zimage_rewash](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/creation/zimage_rewash.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
