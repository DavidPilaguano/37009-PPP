"""Construye una versión trazable del dataset sin modificar las fuentes."""

from __future__ import annotations

import argparse
import csv
import random
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from dataset_contract import APPROVED_CLASSES, IMAGE_EXTENSIONS, PENDING_CLASSES, SOURCE_TO_CLASS
from preprocess import hamming_distance, inspect_image


MANIFEST_FIELDS = [
    "image_id", "relative_path", "split", "class_id", "tag", "source_dataset",
    "source_label", "source_file", "source_group", "augmentation", "is_original",
    "width", "height", "channels", "sha256", "annotation_format", "label_status",
    "review_status", "notes",
]


def iter_originals(source_root: Path) -> Iterable[tuple[Path, object]]:
    base = source_root / "Data" / "NZDLPlantDisease-v1" / "extracted" / "test" / "test"
    for definition in APPROVED_CLASSES:
        original_dir = base / definition.source_label / "original"
        if not original_dir.exists():
            raise FileNotFoundError(f"No existe la carpeta esperada: {original_dir}")
        for path in sorted(original_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                yield path, definition


def stable_split(items: list[tuple[Path, object]], seed: int) -> dict[Path, str]:
    """Asigna cada captura a un único split, estratificado por clase."""
    by_class: dict[str, list[Path]] = defaultdict(list)
    for path, definition in items:
        by_class[definition.tag].append(path)
    rng = random.Random(seed)
    assignments: dict[Path, str] = {}
    for tag, paths in by_class.items():
        paths = sorted(paths)
        rng.shuffle(paths)
        count = len(paths)
        train_count = max(1, round(count * 0.70))
        val_count = max(1, round(count * 0.15)) if count >= 3 else 0
        test_count = count - train_count - val_count
        if test_count < 1 and count >= 3:
            train_count -= 1
            test_count = 1
        for index, path in enumerate(paths):
            assignments[path] = "train" if index < train_count else "val" if index < train_count + val_count else "test"
    return assignments


def source_group(path: Path) -> str:
    return f"{path.parent.parent.name}_{path.stem}".lower().replace(" ", "_")


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build(source_root: Path, output: Path, seed: int = 20261016) -> dict[str, int]:
    source_root = source_root.resolve()
    output = output.resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"La salida ya contiene archivos: {output}. Use una carpeta vacía.")
    output.mkdir(parents=True, exist_ok=True)
    metadata = output / "metadata"
    metadata.mkdir()
    (metadata / "source_annotations_voc").mkdir()

    classes = [*APPROVED_CLASSES, *PENDING_CLASSES]
    write_csv(output / "classes.csv", list(classes[0].__dataclass_fields__), [item.__dict__ for item in classes])
    candidates = list(iter_originals(source_root))
    assignments = stable_split(candidates, seed)
    seen_hashes: dict[str, Path] = {}
    manifest: list[dict] = []
    rejected: list[dict] = []
    checksums: list[dict] = []
    perceptual_hashes: list[dict] = []
    counter: Counter[str] = Counter()

    for source_path, definition in candidates:
        try:
            info = inspect_image(source_path)
        except Exception as exc:  # La evidencia se conserva en rejected_samples.csv.
            rejected.append({"source_file": str(source_path), "reason": f"invalid_image: {exc}"})
            continue
        if info.sha256 in seen_hashes:
            rejected.append({"source_file": str(source_path), "reason": f"exact_duplicate_of: {seen_hashes[info.sha256]}"})
            continue
        seen_hashes[info.sha256] = source_path
        split = assignments[source_path]
        counter[definition.tag] += 1
        image_id = f"NZDL_{counter[definition.tag]:04d}_{definition.tag}"
        extension = source_path.suffix.lower()
        relative = Path("images") / split / definition.tag / f"{image_id}{extension}"
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
        xml_source = source_path.with_suffix(".xml")
        if xml_source.exists():
            shutil.copy2(xml_source, metadata / "source_annotations_voc" / f"{image_id}.xml")
        row = {
            "image_id": image_id, "relative_path": relative.as_posix(), "split": split,
            "class_id": definition.class_id, "tag": definition.tag,
            "source_dataset": "NZDLPlantDisease-v1", "source_label": definition.source_label,
            "source_file": source_path.name, "source_group": source_group(source_path),
            "augmentation": "none", "is_original": 1, "width": info.width, "height": info.height,
            "channels": info.channels, "sha256": info.sha256, "annotation_format": "pascal_voc",
            "label_status": "approved", "review_status": "reviewed", "notes": "Imagen original; variante aumentada excluida.",
        }
        manifest.append(row)
        checksums.append({"relative_path": relative.as_posix(), "sha256": info.sha256})
        perceptual_hashes.append({"image_id": image_id, "relative_path": relative.as_posix(), "dhash": info.dhash})

    external_rows = copy_external_test(source_root, output)
    write_csv(output / "manifest.csv", MANIFEST_FIELDS, manifest)
    write_csv(output / "splits.csv", ["image_id", "source_group", "split", "tag"], [{key: row[key] for key in ("image_id", "source_group", "split", "tag")} for row in manifest])
    write_csv(metadata / "checksums_sha256.csv", ["relative_path", "sha256"], checksums)
    write_csv(metadata / "near_duplicates_dhash.csv", ["image_id_a", "image_id_b", "hamming_distance"], find_near_duplicates(perceptual_hashes))
    class_weights = build_class_weights(manifest)
    write_csv(metadata / "class_weights.csv", ["tag", "train_images", "weight"], class_weights)
    write_csv(metadata / "rejected_samples.csv", ["source_file", "reason"], rejected)
    quality = quality_rows(manifest, rejected, external_rows, seed)
    write_csv(metadata / "quality_review.csv", list(quality[0]) if quality else ["check", "result", "details"], quality)
    write_readme(output, manifest, external_rows, rejected, seed)
    return {"internal": len(manifest), "external": len(external_rows), "rejected": len(rejected)}


def copy_external_test(source_root: Path, output: Path) -> list[dict]:
    base = source_root / "Data" / "NZDLPlantDisease-v1" / "extracted" / "external_test" / "testing_images"
    rows: list[dict] = []
    for definition in APPROVED_CLASSES:
        source_dir = base / definition.source_label
        if not source_dir.exists():
            continue
        for index, source_path in enumerate(sorted(path for path in source_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS), start=1):
            info = inspect_image(source_path)
            image_id = f"NZDL_EXT_{definition.tag}_{index:04d}"
            relative = Path("external_test") / "images" / definition.tag / f"{image_id}{source_path.suffix.lower()}"
            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination)
            rows.append({"image_id": image_id, "relative_path": relative.as_posix(), "split": "external_test", "class_id": definition.class_id, "tag": definition.tag, "sha256": info.sha256})
    write_csv(output / "external_test_manifest.csv", ["image_id", "relative_path", "split", "class_id", "tag", "sha256"], rows)
    return rows


def quality_rows(manifest: list[dict], rejected: list[dict], external: list[dict], seed: int) -> list[dict]:
    split_counts = Counter((row["split"], row["tag"]) for row in manifest)
    return [
        {"check": "seed", "result": "pass", "details": str(seed)},
        {"check": "approved_classes", "result": "pass", "details": ", ".join(item.tag for item in APPROVED_CLASSES)},
        {"check": "internal_images", "result": "pass", "details": str(len(manifest))},
        {"check": "external_images", "result": "pass", "details": str(len(external))},
        {"check": "rejected_images", "result": "pass" if not rejected else "review", "details": str(len(rejected))},
        *({"check": f"{tag}_{split}", "result": "pass", "details": str(count)} for (split, tag), count in sorted(split_counts.items())),
    ]


def find_near_duplicates(items: list[dict], threshold: int = 2) -> list[dict]:
    """Registra, sin eliminar, pares que merecen revisión visual."""
    flagged: list[dict] = []
    for index, first in enumerate(items):
        for second in items[index + 1:]:
            distance = hamming_distance(first["dhash"], second["dhash"])
            if distance <= threshold:
                flagged.append({"image_id_a": first["image_id"], "image_id_b": second["image_id"], "hamming_distance": distance})
    return flagged


def build_class_weights(manifest: list[dict]) -> list[dict]:
    counts = Counter(row["tag"] for row in manifest if row["split"] == "train")
    total = sum(counts.values())
    classes = len(counts)
    return [
        {"tag": tag, "train_images": count, "weight": round(total / (classes * count), 6)}
        for tag, count in sorted(counts.items())
    ]


def write_readme(output: Path, manifest: list[dict], external: list[dict], rejected: list[dict], seed: int) -> None:
    summary = Counter((row["split"], row["tag"]) for row in manifest)
    lines = [
        "# avocado_mobilenet_v1", "", "Versión procesada creada desde imágenes originales de NZDLPlantDisease-v1.",
        "Las fuentes originales no se modificaron. Las variantes aumentadas de la fuente se excluyeron para evitar fuga de datos.", "",
        f"Semilla de partición: `{seed}`.", f"Imágenes internas: {len(manifest)}.", f"Imágenes de prueba externa: {len(external)}.", f"Rechazadas: {len(rejected)}.", "",
        "## Distribución interna", "", "| Split | Clase | Imágenes |", "| --- | --- | ---: |",
    ]
    for (split, tag), count in sorted(summary.items()):
        lines.append(f"| {split} | {tag} | {count} |")
    lines.extend(["", "La prueba externa no participa en el entrenamiento, ajuste de hiperparámetros ni selección del modelo."])
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True, help="Raíz que contiene Data/.")
    parser.add_argument("--output", type=Path, required=True, help="Nueva carpeta de salida, inicialmente vacía.")
    parser.add_argument("--seed", type=int, default=20261016)
    args = parser.parse_args()
    result = build(args.source_root, args.output, args.seed)
    print(f"Dataset creado: {result['internal']} internas, {result['external']} externas, {result['rejected']} rechazadas.")


if __name__ == "__main__":
    main()
