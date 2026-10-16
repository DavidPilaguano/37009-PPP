"""Validación, hashes y preparación no destructiva de imágenes."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps


@dataclass(frozen=True)
class ImageInfo:
    width: int
    height: int
    channels: int
    sha256: str
    dhash: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_image(path: Path) -> ImageInfo:
    """Comprueba que una imagen pueda abrirse como RGB sin tocar el origen."""
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        width, height = rgb.size
    if width <= 0 or height <= 0:
        raise ValueError("La imagen no tiene dimensiones positivas.")
    return ImageInfo(width=width, height=height, channels=3, sha256=sha256_file(path), dhash=difference_hash(path))


def difference_hash(path: Path) -> str:
    """Hash perceptual compacto para marcar imágenes visualmente casi iguales."""
    with Image.open(path) as image:
        grayscale = ImageOps.exif_transpose(image).convert("L").resize((9, 8), Image.Resampling.LANCZOS)
        pixels = np.asarray(grayscale, dtype=np.int16)
    bits = pixels[:, 1:] > pixels[:, :-1]
    return f"{int(''.join('1' if bit else '0' for bit in bits.flat), 2):016x}"


def hamming_distance(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def prepare_for_inference(path: Path, size: int = 224) -> np.ndarray:
    """Devuelve una imagen RGB centrada y normalizada para una entrada MobileNet.

    Esta función se usa en cámara/inferencia. No escribe ni redimensiona la
    fuente; el cargador de entrenamiento aplica su propia normalización.
    """
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image = ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS)
        return np.asarray(image, dtype=np.float32) / 255.0


def augment_training_image(image: Image.Image, seed: int | None = None) -> Image.Image:
    """Aumento moderado y determinista para pruebas locales, solo en train."""
    rng = np.random.default_rng(seed)
    result = ImageOps.exif_transpose(image).convert("RGB")
    if rng.random() < 0.5:
        result = ImageOps.mirror(result)
    angle = float(rng.uniform(-12, 12))
    result = result.rotate(angle, resample=Image.Resampling.BILINEAR)
    result = ImageEnhance.Brightness(result).enhance(float(rng.uniform(0.9, 1.1)))
    return result
