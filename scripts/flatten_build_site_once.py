from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
LAYERS = [
    ("v06", SCRIPTS / "build_site_v06.py", None),
    ("v08", SCRIPTS / "build_site_v08.py", "v06"),
    ("v09", SCRIPTS / "build_site_v09.py", "v08"),
    ("current", SCRIPTS / "build_site.py", "v09"),
]
PREFIX = {"v06": "_compat06__", "v08": "_compat08__", "v09": "_compat09__", "current": ""}
ALIASES = {"_v06": "v06", "_v08": "v08", "_v09": "v09"}


def assigned_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    if isinstance(node, ast.Name):
        names.add(node.id)
    elif isinstance(node, (ast.Tuple, ast.List)):
        for item in node.elts:
            names |= assigned_names(item)
    return names


def is_internal_import(node: ast.AST) -> bool:
    if isinstance(node, ast.ImportFrom):
        if node.module and node.module.startswith("scripts.build_site_v"):
            return True
        if node.module == "scripts":
            return any(alias.name.startswith("build_site_v") for alias in node.names)
    return False


def is_main_guard(node: ast.AST) -> bool:
    if not isinstance(node, ast.If):
        return False
    test = node.test
    return (
        isinstance(test, ast.Compare)
        and isinstance(test.left, ast.Name)
        and test.left.id == "__name__"
        and len(test.ops) == 1
        and isinstance(test.ops[0], ast.Eq)
        and len(test.comparators) == 1
        and isinstance(test.comparators[0], ast.Constant)
        and test.comparators[0].value == "__main__"
    )


def alias_assignment(node: ast.AST) -> bool:
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        return False
    target = node.targets[0]
    return isinstance(target, ast.Name) and target.id in ALIASES


def top_defs(tree: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                names |= assigned_names(target)
        elif isinstance(node, ast.AnnAssign):
            names |= assigned_names(node.target)
    return {name for name in names if name not in ALIASES}


def public(mapping: dict[str, str]) -> dict[str, str]:
    return {name: value for name, value in mapping.items() if not name.startswith("_")}


def attr_chain(node: ast.Attribute) -> tuple[str | None, list[str]]:
    attrs: list[str] = []
    current: ast.AST = node
    while isinstance(current, ast.Attribute):
        attrs.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        return current.id, list(reversed(attrs))
    return None, []


class Rewriter(ast.NodeTransformer):
    def __init__(self, layer: str, own: set[str], inherited: dict[str, str], resolutions: dict[str, dict[str, str]]):
        self.layer = layer
        self.own = own
        self.inherited = inherited
        self.resolutions = resolutions

    def resolve_name(self, name: str) -> str:
        if name in self.own:
            return PREFIX[self.layer] + name
        return self.inherited.get(name, name)

    def resolve_module_attr(self, target_layer: str, name: str) -> str:
        resolved = self.resolutions[target_layer].get(name)
        if resolved is not None:
            return resolved
        if name.startswith("_"):
            return PREFIX[target_layer] + name
        return name

    def visit_FunctionDef(self, node: ast.FunctionDef):
        original = node.name
        node = self.generic_visit(node)
        if original in self.own:
            node.name = PREFIX[self.layer] + original
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        original = node.name
        node = self.generic_visit(node)
        if original in self.own:
            node.name = PREFIX[self.layer] + original
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        original = node.name
        node = self.generic_visit(node)
        if original in self.own:
            node.name = PREFIX[self.layer] + original
        return node

    def visit_Call(self, node: ast.Call):
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "hasattr"
            and len(node.args) >= 2
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id in ALIASES
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str)
        ):
            target_layer = ALIASES[node.args[0].id]
            resolved = self.resolve_module_attr(target_layer, node.args[1].value)
            return ast.copy_location(
                ast.Compare(
                    left=ast.Constant(resolved),
                    ops=[ast.In()],
                    comparators=[ast.Call(func=ast.Name(id="globals", ctx=ast.Load()), args=[], keywords=[])],
                ),
                node,
            )
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if node.id in ALIASES:
            return node
        resolved = self.resolve_name(node.id)
        if resolved != node.id:
            return ast.copy_location(ast.Name(id=resolved, ctx=node.ctx), node)
        return node

    def visit_Attribute(self, node: ast.Attribute):
        root, attrs = attr_chain(node)
        if root in ALIASES and attrs:
            target_layer = ALIASES[root]
            final: str | None = None
            for attr in attrs:
                if attr in ALIASES:
                    target_layer = ALIASES[attr]
                else:
                    if final is not None:
                        return self.generic_visit(node)
                    final = attr
            if final is not None:
                resolved = self.resolve_module_attr(target_layer, final)
                return ast.copy_location(ast.Name(id=resolved, ctx=node.ctx), node)
        return self.generic_visit(node)


def build() -> str:
    parsed: dict[str, ast.Module] = {}
    defs: dict[str, set[str]] = {}
    for layer, path, _base in LAYERS:
        parsed[layer] = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        defs[layer] = top_defs(parsed[layer])

    resolutions: dict[str, dict[str, str]] = {}
    inherited_by_layer: dict[str, dict[str, str]] = {}
    for layer, _path, base in LAYERS:
        inherited = public(resolutions[base]) if base else {}
        inherited_by_layer[layer] = inherited
        current = dict(inherited)
        for name in defs[layer]:
            current[name] = PREFIX[layer] + name
        resolutions[layer] = current

    import_texts: list[str] = []
    seen_imports: set[str] = set()
    layer_bodies: dict[str, list[ast.stmt]] = {}
    current_main: list[ast.stmt] = []

    for layer, _path, _base in LAYERS:
        body: list[ast.stmt] = []
        for node in parsed[layer].body:
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                continue
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if is_internal_import(node):
                    continue
                text = ast.unparse(node)
                if text not in seen_imports:
                    seen_imports.add(text)
                    import_texts.append(text)
                continue
            if alias_assignment(node):
                continue
            if is_main_guard(node):
                if layer == "current":
                    current_main.append(node)
                continue
            body.append(node)

        transformer = Rewriter(layer, defs[layer], inherited_by_layer[layer], resolutions)
        layer_bodies[layer] = [ast.fix_missing_locations(transformer.visit(node)) for node in body]
        if layer == "current":
            current_main = [ast.fix_missing_locations(transformer.visit(node)) for node in current_main]

    out: list[str] = [
        "from __future__ import annotations",
        "",
        "# Generated once from the accepted historical builder layers.",
        "# The current runtime is intentionally a single module with no executable",
        "# historical builder import chain and no cross-module global mutation.",
    ]
    out.extend(import_texts)

    for layer in ("v06", "v08", "v09", "current"):
        out.extend(["", f"# ---- {layer} compatibility foundation ----" if layer != "current" else "# ---- current v1.0 builder ----"])
        out.extend(ast.unparse(node) for node in layer_bodies[layer])

    current_defs = defs["current"]
    aliases = []
    for name, resolved in sorted(public(resolutions["current"]).items()):
        if name in current_defs:
            continue
        if resolved != name:
            aliases.append(f"{name} = {resolved}")
    if aliases:
        out.extend(["", "# Public compatibility names retained for callers/tests."])
        out.extend(aliases)

    if current_main:
        out.extend(["", "# ---- command-line entrypoint ----"])
        out.extend(ast.unparse(node) for node in current_main)

    result = "\n".join(out).rstrip() + "\n"
    ast.parse(result)
    forbidden = (
        "from scripts import build_site_v",
        "from scripts.build_site_v",
        "import scripts.build_site_v",
        "_v06.",
        "_v08.",
        "_v09.",
    )
    for needle in forbidden:
        if needle in result:
            raise SystemExit(f"flattened builder still contains forbidden runtime dependency marker: {needle}")
    return result


def main() -> None:
    target = SCRIPTS / "build_site.py"
    flattened = build()
    target.write_text(flattened, encoding="utf-8")
    print(f"wrote {target} ({len(flattened.splitlines())} lines)")


if __name__ == "__main__":
    main()
