#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory


def _load_yaml_documents(paths):
    import yaml
    docs = []
    for raw in paths:
        path = Path(raw)
        candidates = sorted(path.rglob("*.yaml")) + sorted(path.rglob("*.yml")) if path.is_dir() else [path]
        for candidate in candidates:
            with candidate.open("r", encoding="utf-8") as fh:
                for doc in yaml.safe_load_all(fh):
                    if isinstance(doc, dict):
                        docs.append((candidate, doc))
    return docs


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_") or "unnamed"


def _quote(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def _label_lines(prop: str, labels: dict) -> list[str]:
    lines = []
    for key, value in sorted((labels or {}).items()):
        lines.append(f"    ; {prop} \"{_quote(key)}={_quote(value)}\"")
    return lines


def _platform(doc: dict) -> str | None:
    metadata = doc.get("metadata", {}) or {}
    annotations = metadata.get("annotations", {}) or {}
    value = annotations.get("socioprophet.io/platform") or annotations.get("prophet.socioprophet.io/platform")
    if value:
        return str(value).lower()
    return None


def _service_to_turtle(source: Path, doc: dict, index: int) -> list[str]:
    metadata = doc.get("metadata", {}) or {}
    spec = doc.get("spec", {}) or {}
    name = metadata.get("name", f"service_{index}")
    node = f"ex:{_safe_name(source.stem)}_{_safe_name(name)}_{index}"
    service_type = spec.get("type", "ClusterIP")
    lines = [
        f"{node} a k8s:Service ;",
        f"    k8s:name \"{_quote(name)}\" ;",
        f"    k8s:serviceType \"{_quote(service_type)}\"",
    ]
    platform = _platform(doc)
    if platform:
        lines.append(f"    ; k8s:platform \"{_quote(platform)}\"")
    lines.extend(_label_lines("k8s:selectorLabel", spec.get("selector", {}) or {}))
    for port in spec.get("ports", []) or []:
        if "nodePort" in port:
            lines.append(f"    ; k8s:nodePort {int(port['nodePort'])}")
    lines[-1] = lines[-1] + " ."
    lines.append("")
    return lines


def _deployment_to_turtle(source: Path, doc: dict, index: int) -> list[str]:
    metadata = doc.get("metadata", {}) or {}
    spec = doc.get("spec", {}) or {}
    template = spec.get("template", {}) or {}
    template_metadata = template.get("metadata", {}) or {}
    template_spec = template.get("spec", {}) or {}
    selector = spec.get("selector", {}) or {}
    name = metadata.get("name", f"deployment_{index}")
    node = f"ex:{_safe_name(source.stem)}_{_safe_name(name)}_{index}"
    lines = [
        f"{node} a k8s:Deployment ;",
        f"    k8s:name \"{_quote(name)}\"",
    ]
    platform = _platform(doc)
    if platform:
        lines.append(f"    ; k8s:platform \"{_quote(platform)}\"")
    lines.extend(_label_lines("k8s:matchLabel", selector.get("matchLabels", {}) or {}))
    lines.extend(_label_lines("k8s:templateLabel", template_metadata.get("labels", {}) or {}))
    lines.extend(_label_lines("k8s:nodeSelectorLabel", template_spec.get("nodeSelector", {}) or {}))
    lines[-1] = lines[-1] + " ."
    lines.append("")
    return lines


def _ingress_to_turtle(source: Path, doc: dict, index: int) -> list[str]:
    metadata = doc.get("metadata", {}) or {}
    spec = doc.get("spec", {}) or {}
    name = metadata.get("name", f"ingress_{index}")
    node = f"ex:{_safe_name(source.stem)}_{_safe_name(name)}_{index}"
    lines = [
        f"{node} a k8s:Ingress ;",
        f"    k8s:name \"{_quote(name)}\"",
    ]
    platform = _platform(doc)
    if platform:
        lines.append(f"    ; k8s:platform \"{_quote(platform)}\"")
    ingress_class = spec.get("ingressClassName")
    if ingress_class:
        lines.append(f"    ; k8s:ingressClass \"{_quote(ingress_class)}\"")
    for rule in spec.get("rules", []) or []:
        if rule.get("host"):
            lines.append(f"    ; k8s:ruleHost \"{_quote(rule['host'])}\"")
    for tls in spec.get("tls", []) or []:
        for host in tls.get("hosts", []) or []:
            lines.append(f"    ; k8s:tlsHost \"{_quote(host)}\"")
    lines[-1] = lines[-1] + " ."
    lines.append("")
    return lines


def _docs_to_turtle(docs) -> str:
    lines = [
        '@prefix k8s: <https://socioprophet.github.io/ontogenesis/k8s#> .',
        '@prefix ex: <https://socioprophet.github.io/ontogenesis/examples/k8s#> .',
        '',
    ]
    for index, (source, doc) in enumerate(docs):
        kind = doc.get("kind")
        if kind == "Service":
            lines.extend(_service_to_turtle(source, doc, index))
        elif kind == "Deployment":
            lines.extend(_deployment_to_turtle(source, doc, index))
        elif kind == "Ingress":
            lines.extend(_ingress_to_turtle(source, doc, index))
    return "\n".join(lines)


def _run_shacl(turtle_text: str, shapes_path: Path):
    from rdflib import Graph
    from pyshacl import validate
    with TemporaryDirectory() as tmpdir:
        data_path = Path(tmpdir) / "k8s.ttl"
        data_path.write_text(turtle_text, encoding="utf-8")
        data_graph = Graph().parse(data_path, format="turtle")
        shacl_graph = Graph().parse(shapes_path, format="turtle")
        conforms, _report_graph, report_text = validate(
            data_graph,
            shacl_graph=shacl_graph,
            inference="rdfs",
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True,
        )
        return bool(conforms), len(data_graph), report_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Run K8s manifest SHACL shape checks.")
    parser.add_argument("--manifest", nargs="+", required=True, help="One or more manifest files or directories.")
    parser.add_argument("--shapes", default="k8s/shapes/k8s.shacl.ttl", help="Path to the K8s SHACL pack.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    shapes_path = (repo_root / args.shapes).resolve() if not Path(args.shapes).is_absolute() else Path(args.shapes)
    docs = _load_yaml_documents(args.manifest)
    ttl = _docs_to_turtle(docs)
    conforms, triples, report_text = _run_shacl(ttl, shapes_path)
    payload = {
        "conforms": conforms,
        "documents": len(docs),
        "triples": triples,
        "shapes_path": str(shapes_path),
        "report_text": report_text,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"conforms={conforms}")
        print(f"documents={len(docs)}")
        print(f"triples={triples}")
        print(report_text)
    return 0 if conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
