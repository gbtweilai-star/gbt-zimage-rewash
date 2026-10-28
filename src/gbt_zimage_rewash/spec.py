"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "zimage_rewash",
 "domain": "creation",
 "desc": "洗图流水线（看图→反推提示词→重绘→放大）：**放大环已可用**（ffmpeg lanczos+unsharp，零依赖）；反推环**已接线**（2026-10-15 起 zimage_rewash_cap 走 vision 通道；2026-10-16 增形式化反推件 tools/codex-scripts/img-reverse.py）；**语义反推**仍待外部理解通道（teamorouter 401 / 本地 8111 未监听）——缺什么就写什么；重绘环**未接线**（未装 ComfyUI；pollinations img2img 需公网可达图 URL）；含降噪强度口径表 0.15→0.85 四档。⚠️ **2026-10-13 收敛（主人令「每一个调节都要触手可控」）**：本位是**历史腿**，主腿 = `comfy_native.upscale_4k`（PIL LANCZOS + USM；`vision_print.polish` 的清晰度腿走它）。收敛**分两类做、不搞假统一**：① **几何旋钮真统一** —— `scale`（新名，倍数）＝旧名 `factor`，且都接受 `size`（目标绝对宽，按源图宽换算成倍数走同一条路）；两个名字同时给且不等 ⇒ **fail-closed**。② **锐化旋钮不统一、且显式拒** —— 本位只有 `unsharp`（**ffmpeg unsharp 滤镜的 amount**），主腿是 `sharpen`（**PIL USM 的 percent 比例**），**两个算法两个量纲**；把 `sharpen` 传给本位 ⇒ **当场 fail-closed 并指路主腿**（改名冒充＝假统一，更害人）。参数判在**过门之前**（参数错不消耗授权）。",
 "handler": "zimage_rewash",
 "safe": false,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": false,
 "ops": [],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
