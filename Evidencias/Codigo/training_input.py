"""Puente entre el manifiesto reproducible y el entrenamiento MobileNet."""

from __future__ import annotations

import csv
from pathlib import Path


def build_tf_datasets(dataset_root: Path, batch_size: int = 16, image_size: int = 224, seed: int = 20261016):
    """Crea datasets TF con aumento solo para train.

    TensorFlow es opcional para poder validar y construir el dataset sin una GPU.
    """
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise RuntimeError("Instale TensorFlow para usar el cargador de entrenamiento.") from exc
    root = Path(dataset_root)
    with (root / "manifest.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    tags = sorted({row["tag"] for row in rows}, key=lambda tag: int(next(item["class_id"] for item in rows if item["tag"] == tag)))
    tag_to_id = {tag: index for index, tag in enumerate(tags)}

    def make_split(split: str, training: bool):
        chosen = [row for row in rows if row["split"] == split]
        paths = [str(root / row["relative_path"]) for row in chosen]
        labels = [tag_to_id[row["tag"]] for row in chosen]
        ds = tf.data.Dataset.from_tensor_slices((paths, labels))
        if training:
            ds = ds.shuffle(len(paths), seed=seed, reshuffle_each_iteration=True)
        def load(path, label):
            image = tf.io.decode_jpeg(tf.io.read_file(path), channels=3)
            image = tf.image.resize(image, (image_size, image_size))
            image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
            return image, label
        ds = ds.map(load, num_parallel_calls=tf.data.AUTOTUNE)
        if training:
            augmenter = tf.keras.Sequential([
                tf.keras.layers.RandomFlip("horizontal", seed=seed),
                tf.keras.layers.RandomRotation(0.05, seed=seed),
                tf.keras.layers.RandomContrast(0.1, seed=seed),
            ])
            ds = ds.map(lambda image, label: (augmenter(image, training=True), label), num_parallel_calls=tf.data.AUTOTUNE)
        return ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)

    with (root / "metadata" / "class_weights.csv").open(encoding="utf-8", newline="") as handle:
        class_weights = {tag_to_id[row["tag"]]: float(row["weight"]) for row in csv.DictReader(handle)}
    return {
        "train": make_split("train", True), "val": make_split("val", False), "test": make_split("test", False),
        "class_names": tags, "class_weights": class_weights,
    }
