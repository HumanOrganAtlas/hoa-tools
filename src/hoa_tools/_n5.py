import codecs
import json
import numbers
import re
import struct
import sys
from collections.abc import AsyncIterator, Iterable, Sequence
from typing import Any

import numpy as np
import numpy.typing as npt
from numcodecs.abc import Codec
from numcodecs.registry import get_codec, register_codec
from zarr.abc.store import ByteRequest
from zarr.core.buffer import Buffer, BufferPrototype, default_buffer_prototype
from zarr.storage import FsspecStore

zarr_group_meta_key = ".zgroup"
zarr_array_meta_key = ".zarray"
zarr_attrs_key = ".zattrs"
n5_attrs_key = "attributes.json"
N5_FORMAT = "2.0.0"
ZARR_FORMAT = 2

zarr_to_n5_keys = [
    ("chunks", "blockSize"),
    ("dtype", "dataType"),
    ("compressor", "compression"),
    ("shape", "dimensions"),
]
n5_keywords = ["n5", "dataType", "dimensions", "blockSize", "compression"]


class N5FSStore(FsspecStore):
    async def get(
        self,
        key: str,
        prototype: BufferPrototype,
        byte_range: ByteRequest | None = None,
    ) -> Buffer | None:
        if key.endswith(zarr_group_meta_key):
            key_new = key.replace(zarr_group_meta_key, n5_attrs_key)
            value = group_metadata_to_zarr(await self._load_n5_attrs(key_new))

            return prototype.buffer.from_bytes(json_dumps(value))

        if key.endswith(zarr_array_meta_key):
            key_new = key.replace(zarr_array_meta_key, n5_attrs_key)
            top_level = key == zarr_array_meta_key
            value = array_metadata_to_zarr(
                await self._load_n5_attrs(key_new), top_level=top_level
            )
            return prototype.buffer.from_bytes(json_dumps(value))

        if key.endswith(zarr_attrs_key):
            key_new = key.replace(zarr_attrs_key, n5_attrs_key)
            value = attrs_to_zarr(await self._load_n5_attrs(key_new))
            return prototype.buffer.from_bytes(json_dumps(value))

        key_new = invert_chunk_coords(key) if is_chunk_key(key) else key

        return await super().get(key_new, prototype=prototype, byte_range=byte_range)

    async def get_partial_values(
        self,
        prototype: BufferPrototype,
        key_ranges: Iterable[tuple[str, ByteRequest | None]],
    ) -> list[Buffer | None]:
        raise NotImplementedError

    async def exists(self, key: str) -> bool:
        if key.endswith(zarr_group_meta_key):
            key_new = key.replace(zarr_group_meta_key, n5_attrs_key)
            if not await super().exists(key_new):
                return False
            # group if not a dataset (attributes do not contain 'dimensions')
            return "dimensions" not in await self._load_n5_attrs(key_new)

        if key.endswith(zarr_array_meta_key):
            key_new = key.replace(zarr_array_meta_key, n5_attrs_key)
            # array if attributes contain 'dimensions'
            return "dimensions" in await self._load_n5_attrs(key_new)

        if key.endswith(zarr_attrs_key):
            key_new = key.replace(zarr_attrs_key, n5_attrs_key)
            return await self._contains_attrs(key_new)

        key_new = invert_chunk_coords(key) if is_chunk_key(key) else key

        return await super().exists(key_new)

    @property
    def supports_writes(self) -> bool:  # type: ignore[override]
        return False

    async def set(
        self,
        key: str,
        value: Buffer,
        byte_range: tuple[int, int] | None = None,
    ) -> None:
        raise NotImplementedError

    @property
    def supports_deletes(self) -> bool:  # type: ignore[override]
        return False

    async def delete(self, key: str) -> None:
        raise NotImplementedError

    @property
    def supports_listing(self) -> bool:  # type: ignore[override]
        return False

    def list(self) -> AsyncIterator[str]:
        raise NotImplementedError

    def list_prefix(self, prefix: str) -> AsyncIterator[str]:
        raise NotImplementedError

    def list_dir(self, prefix: str) -> AsyncIterator[str]:
        # This method should be async, like overridden methods in child classes.
        # However, that's not straightforward:
        # https://stackoverflow.com/questions/68905848
        raise NotImplementedError

    async def _load_n5_attrs(self, path: str) -> dict[str, Any]:
        try:
            s = await super().get(path, prototype=default_buffer_prototype())
            if s is None:
                raise RuntimeError(f"No N5 attributes at path {path}")
            return json_loads(s.to_bytes())
        except KeyError:
            return {}

    async def _contains_attrs(self, path: str | None) -> bool:
        if path is None:
            attrs_key = n5_attrs_key
        elif not path.endswith(n5_attrs_key):
            attrs_key = f"{path}/{n5_attrs_key}"
        else:
            attrs_key = path

        attrs = attrs_to_zarr(await self._load_n5_attrs(attrs_key))
        return len(attrs) > 0


# match strings of numbers with "." between
# (e.g., "1.2.4", "1.2", "5")
_prog_ckey = re.compile(r"^(\d+)(\.\d+)+$")


def is_chunk_key(key: str) -> bool:
    rv = False
    segments = list(key.split("/"))
    if segments:
        last_segment = segments[-1]
        rv = bool(_prog_ckey.match(last_segment))
    return rv


def invert_chunk_coords(key: str) -> str:
    segments = list(key.split("/"))
    if segments:
        last_segment = segments[-1]
        if _prog_ckey.match(last_segment):
            coords = list(last_segment.split("."))
            last_segment = "/".join(coords[::-1])
            segments = [*segments[:-1], last_segment]
            key = "/".join(segments)
    return key


def group_metadata_to_zarr(group_metadata: dict[str, Any]) -> dict[str, Any]:
    """Convert group metadata from N5 to zarr format."""
    return {"zarr_format": ZARR_FORMAT}


def array_metadata_to_zarr(
    array_metadata: dict[str, Any], *, top_level: bool = False
) -> dict[str, Any]:
    """
    Convert array metadata from N5 to zarr format.

    If the `top_level` keyword argument is True,
    then the `N5` key will be removed from metadata
    """
    for t, f in zarr_to_n5_keys:
        array_metadata[t] = array_metadata.pop(f)
    if top_level:
        array_metadata.pop("n5")
    array_metadata["zarr_format"] = ZARR_FORMAT

    array_metadata["shape"] = array_metadata["shape"][::-1]
    array_metadata["chunks"] = array_metadata["chunks"][::-1]
    array_metadata["fill_value"] = 0  # also if None was requested
    array_metadata["order"] = "C"
    array_metadata["filters"] = None
    array_metadata["dimension_separator"] = "."
    array_metadata["dtype"] = np.dtype(array_metadata["dtype"]).str

    compressor_config = array_metadata["compressor"]
    compressor_config = compressor_config_to_zarr(compressor_config)
    array_metadata["compressor"] = {
        "id": N5ChunkWrapper.codec_id,
        "compressor_config": compressor_config,
        "dtype": array_metadata["dtype"],
        "chunk_shape": array_metadata["chunks"],
    }

    return array_metadata


def attrs_to_zarr(attrs: dict[str, Any]) -> dict[str, Any]:
    """
    Get all zarr attributes from an N5 attributes dictionary.

       (i.e.,
    all non-keyword attributes).

    """
    # remove all N5 keywords
    for n5_key in n5_keywords:
        attrs.pop(n5_key, None)

    return attrs


def json_loads(s: bytes | str) -> dict[str, Any]:
    """Read JSON in a consistent way."""
    return json.loads(ensure_text(s, "utf-8"))  # type: ignore[no-any-return]


def json_dumps(o: Any) -> bytes:
    """Write JSON in a consistent, human-readable way."""
    return json.dumps(
        o,
        indent=4,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ": "),
        cls=NumberEncoder,
    ).encode("ascii")


class NumberEncoder(json.JSONEncoder):
    def default(self, o: Any) -> float:
        # See json.JSONEncoder.default docstring for explanation
        # This is necessary to encode numpy dtype
        if isinstance(o, numbers.Integral):
            return int(o)
        if isinstance(o, numbers.Real):
            return float(o)
        return json.JSONEncoder.default(self, o)  # type: ignore[no-any-return]


def ensure_text(s: bytes | str, encoding: str = "utf-8") -> str:
    if not isinstance(s, str):
        return codecs.decode(s, encoding)
    return s


def compressor_config_to_zarr(
    compressor_config: dict[str, Any],
) -> dict[str, Any] | None:
    codec_id = compressor_config["type"]
    zarr_config = {"id": codec_id}

    if codec_id == "bzip2":
        zarr_config["id"] = "bz2"
        zarr_config["level"] = compressor_config["blockSize"]

    elif codec_id == "blosc":
        zarr_config["cname"] = compressor_config["cname"]
        zarr_config["clevel"] = compressor_config["clevel"]
        zarr_config["shuffle"] = compressor_config["shuffle"]
        zarr_config["blocksize"] = compressor_config["blocksize"]

    elif codec_id == "lzma":
        zarr_config["format"] = compressor_config["format"]
        zarr_config["check"] = compressor_config["check"]
        zarr_config["preset"] = compressor_config["preset"]
        zarr_config["filters"] = compressor_config["filters"]

    elif codec_id == "xz":
        zarr_config["id"] = "lzma"
        zarr_config["format"] = 1  # lzma.FORMAT_XZ
        zarr_config["check"] = -1
        zarr_config["preset"] = compressor_config["preset"]
        zarr_config["filters"] = None

    elif codec_id == "gzip":
        if compressor_config.get("useZlib"):
            zarr_config["id"] = "zlib"
            zarr_config["level"] = compressor_config["level"]
        else:
            zarr_config["id"] = "gzip"
            zarr_config["level"] = compressor_config["level"]

    elif codec_id == "raw":
        return None

    else:
        zarr_config.update({k: v for k, v in compressor_config.items() if k != "type"})

    return zarr_config


class N5ChunkWrapper(Codec):  # type: ignore[misc]
    codec_id = "n5_wrapper"
    chunk_shape: tuple[int, ...]
    dtype: np.dtype

    def __init__(
        self,
        dtype: npt.DTypeLike,
        chunk_shape: Sequence[int],
        compressor_config: dict[str, Any] | None = None,
        compressor: Codec | None = None,
    ):
        self.dtype = np.dtype(dtype)
        self.chunk_shape = tuple(chunk_shape)
        # is the dtype a little endian format?
        self._little_endian = self.dtype.byteorder == "<" or (
            self.dtype.byteorder == "=" and sys.byteorder == "little"
        )

        if compressor is not None:
            if compressor_config is not None:
                raise ValueError(
                    "Only one of compressor_config or compressor should be given."
                )
            compressor_config = compressor.get_config()

        if compressor_config is None or compressor_config["id"] == "raw":
            self.compressor_config = None
            self._compressor = None
        else:
            self._compressor = get_codec(compressor_config)
            self.compressor_config = self._compressor.get_config()

    def get_config(self) -> dict[str, Any]:
        return {"id": self.codec_id, "compressor_config": self.compressor_config}

    def encode(self, chunk: npt.NDArray[Any]) -> bytes:
        assert chunk.flags.c_contiguous, "Chunk is not C contiguous"  # noqa: S101

        header = self._create_header(chunk)
        chunk = self._to_big_endian(chunk)

        if self._compressor:
            return header + self._compressor.encode(chunk)  # type: ignore[no-any-return]
        return header + chunk.tobytes(order="A")

    def decode(
        self, chunk: bytes, out: npt.NDArray[Any] | None = None
    ) -> npt.NDArray[Any]:
        len_header, chunk_shape = self._read_header(chunk)
        chunk = chunk[len_header:]

        if out is not None:
            # out should only be used if we read a complete chunk
            assert chunk_shape == self.chunk_shape, (  # noqa: S101
                f"Expected chunk of shape {self.chunk_shape}, found {chunk_shape}"
            )

            if self._compressor:
                self._compressor.decode(chunk, out)
            else:
                raise RuntimeError("Can't handle case with no compressor")
                # ndarray_copy(chunk, out)

            # we can byteswap in-place
            if self._little_endian:
                out.byteswap(inplace=True)

            return out

        if self._compressor:
            chunk = self._compressor.decode(chunk)

        # more expensive byteswap
        chunk = self._from_big_endian(chunk)  # type: ignore[assignment]

        # read partial chunk
        if chunk_shape != self.chunk_shape:
            chunk = np.frombuffer(chunk, dtype=self.dtype)  # type: ignore[assignment]
            chunk = chunk.reshape(chunk_shape)  # type: ignore[attr-defined]
            complete_chunk = np.zeros(self.chunk_shape, dtype=self.dtype)
            target_slices = tuple(slice(0, s) for s in chunk_shape)
            complete_chunk[target_slices] = chunk
            chunk = complete_chunk  # type: ignore[assignment]

        return chunk  # type: ignore[return-value]

    @staticmethod
    def _create_header(chunk: npt.NDArray[Any]) -> bytes:
        mode = struct.pack(">H", 0)
        num_dims = struct.pack(">H", len(chunk.shape))
        shape = b"".join(struct.pack(">I", d) for d in chunk.shape[::-1])

        return mode + num_dims + shape

    @staticmethod
    def _read_header(chunk: bytes) -> tuple[int, tuple[int, ...]]:
        num_dims = struct.unpack(">H", chunk[2:4])[0]
        shape = tuple(
            struct.unpack(">I", chunk[i : i + 4])[0]
            for i in range(4, num_dims * 4 + 4, 4)
        )[::-1]

        len_header = 4 + num_dims * 4

        return len_header, shape

    def _to_big_endian(self, data: npt.NDArray[Any]) -> npt.NDArray[Any]:
        # assumes data is ndarray

        if self._little_endian:
            return data.byteswap()
        return data

    def _from_big_endian(self, data: bytes) -> npt.NDArray[Any]:
        # assumes data is byte array in big endian

        if not self._little_endian:
            return data  # type:ignore[return-value]

        a = np.frombuffer(data, self.dtype.newbyteorder(">"))
        return a.astype(self.dtype)


register_codec(N5ChunkWrapper, N5ChunkWrapper.codec_id)
