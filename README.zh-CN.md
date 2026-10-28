# zimage_rewash · 创作域能力位

> **用途一句话**：洗图流水线

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
<img alt="capability" src="https://img.shields.io/badge/capability-61%20%2F%20341-orange">
</p>

这是 **GBT V8 的 341 个原生能力位中的第 61 个**（创作域 · `creation`），
单独抽出来做成的独立仓库：可安装、可测试、零运行时依赖。

---

## 一、这一位是什么

> 洗图流水线（看图→反推提示词→重绘→放大）：**放大环已可用**（ffmpeg lanczos+unsharp，零依赖）；反推环**已接线**（2026-10-15 起 zimage_rewash_cap 走 vision 通道；2026-10-16 增形式化反推件 tools/codex-scripts/img-reverse.py）；**语义反推**仍待外部理解通道（teamorouter 401 / 本地 8111 未监听）——缺什么就写什么；重绘环**未接线**（未装 ComfyUI；pollinations img2img 需公网可达图 URL）；含降噪强度口径表 0.15→0.85 四档。⚠️ **2026-10-13 收敛（主人令「每一个调节都要触手可控」）**：本位是**历史腿**，主腿 = `comfy_native.upscale_4k`（PIL LANCZOS + USM；`vision_print.polish` 的清晰度腿走它）。收敛**分两类做、不搞假统一**：① **几何旋钮真统一** —— `scale`（新名，倍数）＝旧名 `factor`，且都接受 `size`（目标绝对宽，按源图宽换算成倍数走同一条路）；两个名字同时给且不等 ⇒ **fail-closed**。② **锐化旋钮不统一、且显式拒** —— 本位只有 `unsharp`（**ffmpeg unsharp 滤镜的 amount**），主腿是 `sharpen`（**PIL USM 的 percent 比例**），**两个算法两个量纲**；把 `sharpen` 传给本位 ⇒ **当场 fail-closed 并指路主腿**（改名冒充＝假统一，更害人）。参数判在**过门之前**（参数错不消耗授权）。

上面这句是**注册表原文**，逐字复制，没有改写。`tests/test_spec.py` 会把它钉死——
描述漂移会让测试失败，而不是悄悄发版。

---

## 二、用途：它解决什么问题

### 2.1 这一域在管什么

把「一句话意图」变成可交付的视觉资产：分镜、构图、材质、动作、渲染、混音、封装。这一域里的能力位覆盖了从美术简报（art_brief）到成片（machine_film）的整条链路，中间夹着三维（blender / tripo / cadgen）、二维生成（comfyui / zimage_rewash / lobehub）、数字人绑骨（dh_pose / rig_audit / rig_fix）、以及交付前的审计（anim_audit / render_evolution）。

### 2.2 为什么这么设计

创作最容易失控的地方不是「生成不出来」，而是「生成出来不可复现、不可审计」。所以这一域的每个能力位都被设计成**有明确输入、有落盘产物、有校验口**，而不是一个只会返回图片链接的黑盒。

### 2.3 具体到 `zimage_rewash`

**该用它的时候**：

- 你的任务可以概括为「洗图流水线」，并且
- 它不需要任何必填参数，可以直接调用，并且
- 你已经接受它可能触及**不可逆状态**（注册表 `safe: false`，见第七节）。

**不该用它的时候**：

- 你只是想要一个「大概能做这件事」的模糊入口 —— 这一位有明确契约，不是万能入口。
- 你需要它**替你做决定**。它执行，不做价值判断；要不要执行是调用方的事。
- 你希望它自带模型/密钥/机器。它不自带，见 4.5 节接后端。

---

## 三、安装

```bash
git clone https://github.com/gbtweilai-star/gbt-zimage-rewash.git
cd gbt-zimage-rewash
python -m pip install -e ".[dev]"
```

零运行时依赖，只有 `pytest` 是开发期依赖。

---

## 四、使用方式

### 4.1 看它是什么（人类可读）

```bash
python -m gbt_zimage_rewash info
```

真实输出（本机捕获，非示意）：

```text
zimage_rewash  (creation)  v1.0.0
----------------------------------------
洗图流水线（看图→反推提示词→重绘→放大）：**放大环已可用**（ffmpeg lanczos+unsharp，零依赖）；反推环**已接线**（2026-10-15 起 zimage_rewash_cap 走 vision 通道；2026-10-16 增形式化反推件 tools/codex-scripts/img-reverse.py）；**语义反推**仍待外部理解通道（teamorouter 401 / 本地 8111 未监听）——缺什么就写什么；重绘环**未接线**（未装 ComfyUI；pollinations img2img 需公网可达图 URL）；含降噪强度口径表 0.15→0.85 四档。⚠️ **2026-10-13 收敛（主人令「每一个调节都要触手可控」）**：本位是**历史腿**，主腿 = `comfy_native.upscale_4k`（PIL LANCZOS + USM；`vision_print.polish` 的清晰度腿走它）。收敛**分两类做、不搞假统一**：① **几何旋钮真统一** —— `scale`（新名，倍数）＝旧名 `factor`，且都接受 `size`（目标绝对宽，按源图宽换算成倍数走同一条路）；两个名字同时给且不等 ⇒ **fail-closed**。② **锐化旋钮不统一、且显式拒** —— 本位只有 `unsharp`（**ffmpeg unsharp 滤镜的 amount**），主腿是 `sharpen`（**PIL USM 的 percent 比例**），**两个算法两个量纲**；把 `sharpen` 传给本位 ⇒ **当场 fail-closed 并指路主腿**（改名冒充＝假统一，更害人）。参数判在**过门之前**（参数错不消耗授权）。

gated      : True   <- needs explicit consent
external   : False
multi-op   : False
params     : (none)
```

### 4.2 看它的契约（机器可读）

```bash
python -m gbt_zimage_rewash spec --json
```

输出是一个 JSON 对象，字段与注册表一一对应：`name` / `domain` / `desc` / `handler` /
`safe` / `gated` / `external` / `requires_params` / `params` / `params_hint` /
`multi_op` / `ops` / `ops_hint`。下游可以直接拿它做能力发现，不需要读文档。

### 4.3 只校验、不执行

```bash
python -m gbt_zimage_rewash check --payload '{}'
```

`check` 永远不会抛异常，只返回「哪里不满足契约」。适合在花掉一次模型调用之前，
先把缺的参数摆给用户看。退出码：`0` 通过、`1` 契约不满足、`2` JSON 本身不合法。

### 4.4 执行

```bash
python -m gbt_zimage_rewash run --payload '{}'
```

默认后端是 **stub**，所以你会拿到这样的信封：

```json
{
  "cap": "zimage_rewash",
  "status": "validated",
  "backend": "stub",
  "data": { "executed": false, "reason": "no backend wired" },
  "note": "payload checked against the contract; nothing was executed."
}
```

注意 `status` 是 `"validated"` 而**不是** `"ok"`。这是刻意的：一个把 stub 报成成功的库，
会让调用方停止寻找真正的实现。`bool(result)` 对 stub 结果是 `False`。

### 4.5 接上你自己的后端

```python
from gbt_zimage_rewash import SPEC, run

class MyBackend:
    name = "my-backend"

    def invoke(self, cap, payload):
        # 这里才是真实实现：调模型、调浏览器、调你的服务
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"      # 真实后端才会是 ok
print(result.as_dict())
```

也可以进程级注册一次，之后所有 `run()` 都走它：

```python
from gbt_zimage_rewash.backend import register_backend
register_backend(MyBackend())
```

`Backend` 是一个 `Protocol`，只需要 `name` 属性和 `invoke(cap, payload) -> dict`。
不继承任何基类，你的实现不需要依赖本包。

### 4.6 作为库用

```python
from gbt_zimage_rewash import SPEC, run
from gbt_zimage_rewash.core import check

print(SPEC.name, SPEC.domain, SPEC.gated)

problems = check({})
if problems:
    for p in problems:
        print("缺:", p)
else:
    print(run({}).as_dict())
```

---

## 五、参数

| 参数 | 必填 | 说明 |
|---|---|---|
| — | 否 | 注册表未标注必填参数 |

> 注册表原话（`params_hint`）：（空）


**为什么表里只有「必填/否」两档**：注册表只标注了哪些参数是必填的，没有标注类型与取值范围。
本包没有替它编造类型 —— 编造出来的类型比没有类型更危险，因为调用方会相信它。

---

## 六、返回值

`run()` 返回一个不可变的 `Result`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `cap` | `str` | 能力位名，恒等于 `zimage_rewash` |
| `status` | `str` | `validated`（stub 校验通过）/ `ok`（真实后端执行）/ `error` |
| `backend` | `str` | 实际执行后端的 `name` |
| `data` | `dict` | 后端返回的原始字典 |
| `note` | `str` | 人类可读的补充说明（stub 会在这里说明自己没执行） |
| `elapsed_ms` | `float` | 后端耗时 |

`Result.as_dict()` 可直接 `json.dumps`。

---

## 七、边界与注意

- **需要显式授权**（注册表 `safe: false`）。这一位会改变无法用「反向操作」还原的状态，所以原框架把它放在授权闸后面，用完即焚、不做时间窗复用。本包只负责描述与校验，不负责发授权——授权属于调用方的人类。
- **本包不含真实实现**。这是刻意设计：真实实现依附于原运行时（模型、密钥、机器）。本包发布的是契约、校验、CLI 与类型接缝；接上你自己的 `Backend` 就能跑。

---

## 八、它不会做什么

- **不会假装执行成功**。默认 stub 的 `status` 是 `validated`，`executed` 是 `false`。
- **不会替你决定要不要执行**。授权是人的动作，不是库的动作。
- **不会编造参数类型**。注册表没写的，本包也不写。
- **不会静默吞掉错误**。后端抛异常就往上抛，返回非 dict 就报 `CapError`。
- **不会联网**。零运行时依赖，`run()` 只调用你给的后端。

---

## 九、测试

```bash
python -m pytest
```

真实输出：

```text
20 passed, 3 skipped in 0.12s
```

测试里有一条**漂移守卫**：`test_description_is_verbatim` 把 `SPEC.desc` 与注册表快照逐字比对。
描述被改了一个字，构建立刻失败。

---

## 十、出处与核对

| 项 | 值 |
|---|---|
| 能力位名 | `zimage_rewash` |
| 域 | `creation`（创作域，共 341 位 / 30 域中的一位） |
| 注册表 handler | `zimage_rewash` |
| `safe` | `False` → gated = `True` |
| `external` | `False` |
| `multi_op` | `False` |
| 索引页 | [creation/zimage_rewash](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/creation/zimage_rewash.md) |
| 全量图谱 | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

**关于 341 这个数**：父仓 README 写的是 348，但按 AST 解析注册表实际可枚举的是
`341 个能力位 + 0 个未实现 + 0 个已禁用 = 341`。差出来的 7 个是历史重名/已合并条目。
本仓库按 341 编号，编号与 `gbt-caps` 的索引一致，可逐条核对。

---

## License

MIT。见 [LICENSE](LICENSE)。
