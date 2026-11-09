
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Decompiled by @xvaLuex.
#Buy your lua tool : @xvaLuex.
import itertools as it
import math
import struct
import shutil
import os
import sys
import uuid
import hashlib
import platform
import subprocess
import requests
import base64
import zlib
import ctypes
import re as _ptre
import marshal as _ptmarshal
import dis as _ptdis
import ast as _ptast
from io import StringIO as _ptSIO
from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePath, Path
from typing import List, Dict, Tuple, Optional, Any
import time
import json
import csv
import zipfile
import stat
import bisect
from collections import defaultdict
import tempfile
import random
import string
from datetime import datetime, timedelta
import getpass
import socket

try:
    import pytz
except ImportError:
    os.system("pip install pytz")
    import pytz

try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests

try:
    import gmalg
except ImportError:
    os.system("pip install gmalg")
    import gmalg

try:
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import unpad, pad
except ImportError:
    os.system("pip install pycryptodome")
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import unpad, pad

try:
    from zstandard import ZstdDecompressor, ZstdCompressionDict, DICT_TYPE_AUTO, ZstdCompressor
except ImportError:
    os.system("pip install zstandard")
    from zstandard import ZstdDecompressor, ZstdCompressionDict, DICT_TYPE_AUTO, ZstdCompressor

try:
    import colorama
    from termcolor import colored
    colorama.init(autoreset=True)
except ImportError:
    os.system("pip install colorama termcolor")
    import colorama
    from termcolor import colored
    colorama.init(autoreset=True)

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn, BarColumn,
        TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn,
        TransferSpeedColumn,
    )
    from rich.table import Table
    from rich import print as rprint
    from rich.markup import escape
    from rich.text import Text
    from rich.align import Align
    from rich.box import HEAVY_EDGE, ROUNDED, DOUBLE_EDGE, HEAVY, SIMPLE, SQUARE
    from rich.live import Live
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.style import Style
    from rich.padding import Padding
    from rich.prompt import Prompt, Confirm
except ImportError:
    os.system("pip install rich")
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn, BarColumn,
        TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn,
        TransferSpeedColumn,
    )
    from rich.table import Table
    from rich import print as rprint
    from rich.markup import escape
    from rich.text import Text
    from rich.align import Align
    from rich.box import HEAVY_EDGE, ROUNDED, DOUBLE_EDGE, HEAVY, SIMPLE, SQUARE
    from rich.live import Live
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.style import Style
    from rich.padding import Padding
    from rich.prompt import Prompt, Confirm

console = Console()
zsdic_console = Console()

try:
    from Crypto.Cipher import AES as _ptAES
    from Crypto.Random import get_random_bytes as _ptrand
    _PT_CRYPTO_OK = True
except ImportError:
    _PT_CRYPTO_OK = False

TEXT_COLOR   = "#F0F0F5"
DIM_COLOR    = "#7C7C8A"
BRIGHT_COLOR = "#00D9FF"
BORDER_COLOR = "#8B5CF6"
SUCCESS      = "#00FFA3"
ERROR        = "#FF4D6D"
WARNING      = "#FFB547"
GOLD         = "#FFD700"
MAGENTA      = "#FF6BD9"

ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')

RSA_MOD_1 = bytes.fromhex('CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')

SIMPLE1_DECRYPT_KEY = 121
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16

SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = [
    'xG2qW5lP7lV2iN5fN5pG', 'xT1cJ6dL5wC0kK1rB4dK', 'qC4jS5bZ6fL5xE6nD4zA',
    'gD4jQ2aL3bS3lC3xT0iW', 'xU1yQ8wE9zY3gZ3bT5aE', 'uQ3cO2dX7xY4xU7gH7iS',
    'gW1fR0jK6wQ4oN0oK1kZ', 'aJ4pV7iZ7pU4wP2aC2cZ', 'cX6jT3cM2oT3vK0kJ1qN',
    'iT2vS0cS6yT6cZ1sE1lO', 'hM1pH9iY8wM9hT4lN5uJ', 'kG6bC8jK0fL0dE4sH4mL',
    'dB6lB3vE0eZ8wM8rI0aC', 'tP7sP7nI9rA2vQ4cV5yQ', 'aT0cL1yN4pT3sZ7eM2vY',
    'uV6fU8fC9zN3mP5dH8mN', 'rT6aQ6oZ1yM0gO5tO1aN', 'jU5bH7lQ0fM9hK2kI0oF',
    'iQ0eM0mJ7uT0kV6kL5zY',
]

EM_SIMPLE1 = 1
EM_SIMPLE2 = 16
EM_SM4_2 = 2
EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31
EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE
EM_UNKNOWN_17 = 17

CM_NONE = 0
CM_ZLIB = 1
CM_ZSTD = 6
CM_ZSTD_DICT = 8
CM_MASK = 15

MAX_OVERFLOW_BYTES = 5
mini_BLOCK_SIZE = 65536
zsdic_DEFAULT_MAX_NULLS = 40
zsdic_ENABLE_UTF16LE_ID_SCAN = False

SESSION_USER = "VIP USER"
SESSION_KEY = "LOCAL-BYPASS"
SESSION_EXPIRY = "LIFETIME"
game_key = "BGMI"

CSV_URLS = {
    "PUBG.csv": "https://raw.githubusercontent.com/sellacountvinay-creator/BGMI_CSV/main/PUBG.csv",
    "BGMI.csv": "https://raw.githubusercontent.com/sellacountvinay-creator/BGMI_CSV/main/BGMI.csv",
}

def check_key_press():
    try:
        if sys.platform == 'win32':
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8', errors='ignore').lower()
        else:
            import select
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1).lower()
    except Exception:
        pass
    return None

def to_long_path(path) -> str:
    p = str(path)
    if os.name != "nt":
        return p
    if p.startswith("\\\\?\\"):
        return p
    p = os.path.abspath(p)
    if p.startswith("\\\\"):
        return "\\\\?\\UNC\\" + p[2:]
    return "\\\\?\\" + p

def open_long(path, mode='rb'):
    return open(to_long_path(path), mode)

def get_indian_time():
    tz = pytz.timezone("Asia/Kolkata")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def safe_input(prompt=''):
    clean = _ptre.sub(r'\[/?[^\[\]]*\]', '', prompt)
    try:
        return input(clean)
    except (EOFError, KeyboardInterrupt):
        return ""

def human_size(size):
    if size is None:
        return "N/A"
    size = int(size)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            if unit == 'B':
                return f'{size} B'
            return f'{size:.2f} {unit}'
        size /= 1024.0
    return f'{size:.2f} PB'

def get_real_device_model():
    try:
        if hasattr(sys, 'getandroidapilevel') or os.path.exists('/system/build.prop'):
            try:
                brand = subprocess.check_output(['getprop', 'ro.product.brand'], timeout=3).decode().strip().upper()
                model = subprocess.check_output(['getprop', 'ro.product.model'], timeout=3).decode().strip().upper()
                if brand and model:
                    return f"{brand} {model}" if brand not in model else model
            except Exception:
                pass
    except Exception:
        pass
    try:
        return socket.gethostname().upper()
    except Exception:
        return "UNKNOWN"

def get_hwid():
    try:
        android_id = subprocess.check_output(['settings', 'get', 'secure', 'android_id'], timeout=4).decode().strip()
        if android_id and android_id != "null":
            return hashlib.md5(android_id.encode()).hexdigest().upper()[:16]
    except Exception:
        pass
    try:
        hwid_file = os.path.expanduser("~/UltimateEngine_hwid.key.txt")
        if os.path.exists(hwid_file):
            with open(hwid_file, "r") as f:
                return f.read().strip()
        else:
            new_hwid = hashlib.md5(uuid.uuid4().bytes).hexdigest().upper()[:16]
            with open(hwid_file, "w") as f:
                f.write(new_hwid)
            return new_hwid
    except Exception:
        return "UNKNOWN-DEVICE"

class SM4:
    _S_BOX = bytes([
        52, 102, 37, 116, 137, 120, 228, 169, 90, 65, 188, 122, 214, 22, 33, 35,
        77, 97, 218, 148, 155, 223, 19, 60, 105, 58, 49, 10, 95, 215, 153, 149,
        241, 174, 114, 61, 7, 96, 36, 182, 152, 238, 196, 162, 45, 136, 221, 141,
        4, 234, 187, 17, 202, 62, 93, 161, 246, 63, 176, 151, 128, 71, 43, 166,
        230, 247, 217, 177, 89, 192, 124, 190, 84, 40, 183, 126, 79, 248, 67, 110,
        160, 80, 14, 245, 144, 184, 251, 163, 123, 98, 25, 70, 3, 42, 185, 143,
        159, 119, 180, 91, 131, 135, 8, 235, 226, 30, 66, 240, 15, 232, 113, 106,
        117, 173, 85, 31, 181, 171, 51, 250, 127, 21, 189, 133, 216, 6, 104, 179,
        82, 48, 72, 11, 0, 237, 239, 178, 87, 142, 231, 108, 213, 229, 46, 83,
        130, 5, 249, 129, 244, 86, 191, 140, 75, 227, 219, 74, 145, 76, 44, 211,
        64, 41, 78, 32, 20, 54, 121, 9, 111, 209, 55, 224, 57, 12, 138, 146,
        56, 18, 53, 109, 225, 253, 147, 154, 23, 212, 201, 156, 107, 132, 38, 157,
        175, 118, 193, 158, 208, 150, 197, 203, 233, 115, 73, 210, 205, 100, 195, 199,
        1, 125, 243, 172, 252, 222, 164, 68, 50, 27, 194, 186, 28, 2, 198, 39,
        69, 139, 242, 24, 167, 16, 81, 29, 200, 207, 99, 255, 47, 13, 88, 206,
        101, 165, 220, 26, 59, 134, 254, 34, 92, 168, 94, 103, 170, 236, 112, 204
    ])
    _FK = [1184304796, 1270900830, 1493524870, 3164752158]
    _CK = [964907, 973793155, 2654690407, 2916866751, 2071233739, 1226140771, 3348805095, 2045549823, 388349611, 800627875, 612403927, 3721562911, 1195432523, 3150178931, 612053223, 2445162591, 67183755, 1174197155, 1393249511, 3331183455, 3822152747, 1332317203, 1804781383, 1990130463, 1282653851, 3376591251, 2910902311, 925872959, 332098219, 735840931, 396665415, 3588844719]

    @staticmethod
    def ROL32(x, n):
        return (x << n) & 0xFFFFFFFF | (x >> (32 - n))

    @staticmethod
    def _BS(X):
        return (SM4._S_BOX[X >> 24 & 255] << 24 |
                SM4._S_BOX[X >> 16 & 255] << 16 |
                SM4._S_BOX[X >> 8 & 255] << 8 |
                SM4._S_BOX[X & 255])

    @staticmethod
    def _T0(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 2) ^ SM4.ROL32(X, 10) ^ SM4.ROL32(X, 18) ^ SM4.ROL32(X, 24)

    @staticmethod
    def _T1(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 13) ^ SM4.ROL32(X, 23)

    @staticmethod
    def _key_expand(key: bytes, rkey: list):
        K0 = int.from_bytes(key[0:4], 'big') ^ SM4._FK[0]
        K1 = int.from_bytes(key[4:8], 'big') ^ SM4._FK[1]
        K2 = int.from_bytes(key[8:12], 'big') ^ SM4._FK[2]
        K3 = int.from_bytes(key[12:16], 'big') ^ SM4._FK[3]
        for i in range(0, 32, 4):
            K0 = K0 ^ SM4._T1(K1 ^ K2 ^ K3 ^ SM4._CK[i])
            rkey[i] = K0
            K1 = K1 ^ SM4._T1(K2 ^ K3 ^ K0 ^ SM4._CK[i + 1])
            rkey[i + 1] = K1
            K2 = K2 ^ SM4._T1(K3 ^ K0 ^ K1 ^ SM4._CK[i + 2])
            rkey[i + 2] = K2
            K3 = K3 ^ SM4._T1(K0 ^ K1 ^ K2 ^ SM4._CK[i + 3])
            rkey[i + 3] = K3

    @classmethod
    def key_length(cls): return 16
    @classmethod
    def block_length(cls): return 16

    def __init__(self, key: bytes):
        if len(key) != self.key_length():
            raise ValueError(f'Key must be {self.key_length()} bytes')
        self._key = key
        self._rkey = [0] * 32
        SM4._key_expand(self._key, self._rkey)
        self._block_buffer = bytearray()
        if not hasattr(SM4, '_T_TABLES'):
            SM4._T_TABLES = SM4._make_t_tables()

    def encrypt(self, block: bytes) -> bytes:
        if len(block) != self.block_length():
            raise ValueError(f'Block must be {self.block_length()} bytes')
        RK = self._rkey
        X0 = int.from_bytes(block[0:4], 'big')
        X1 = int.from_bytes(block[4:8], 'big')
        X2 = int.from_bytes(block[8:12], 'big')
        X3 = int.from_bytes(block[12:16], 'big')
        for i in range(0, 32, 4):
            X0 = X0 ^ SM4._T0(X1 ^ X2 ^ X3 ^ RK[i])
            X1 = X1 ^ SM4._T0(X2 ^ X3 ^ X0 ^ RK[i + 1])
            X2 = X2 ^ SM4._T0(X3 ^ X0 ^ X1 ^ RK[i + 2])
            X3 = X3 ^ SM4._T0(X0 ^ X1 ^ X2 ^ RK[i + 3])
        B = self._block_buffer; B.clear()
        B.extend(X3.to_bytes(4, 'big')); B.extend(X2.to_bytes(4, 'big'))
        B.extend(X1.to_bytes(4, 'big')); B.extend(X0.to_bytes(4, 'big'))
        return bytes(B)

    def decrypt(self, block: bytes) -> bytes:
        if len(block) != self.block_length():
            raise ValueError(f'Block must be {self.block_length()} bytes')
        RK = self._rkey
        X0 = int.from_bytes(block[0:4], 'big')
        X1 = int.from_bytes(block[4:8], 'big')
        X2 = int.from_bytes(block[8:12], 'big')
        X3 = int.from_bytes(block[12:16], 'big')
        for i in range(0, 32, 4):
            X0 = X0 ^ SM4._T0(X1 ^ X2 ^ X3 ^ RK[31 - i])
            X1 = X1 ^ SM4._T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
            X2 = X2 ^ SM4._T0(X3 ^ X0 ^ X1 ^ RK[29 - i])
            X3 = X3 ^ SM4._T0(X0 ^ X1 ^ X2 ^ RK[28 - i])
        B = self._block_buffer; B.clear()
        B.extend(X3.to_bytes(4, 'big')); B.extend(X2.to_bytes(4, 'big'))
        B.extend(X1.to_bytes(4, 'big')); B.extend(X0.to_bytes(4, 'big'))
        return bytes(B)

    @classmethod
    def _make_t_tables(cls):
        S = cls._S_BOX
        def rol(x, n): return (x << n) & 0xFFFFFFFF | (x >> (32 - n))
        def L(y): return y ^ rol(y, 2) ^ rol(y, 10) ^ rol(y, 18) ^ rol(y, 24)
        T0 = [0] * 256
        T1 = [0] * 256
        T2 = [0] * 256
        T3 = [0] * 256
        for i in range(256):
            s = S[i]
            T0[i] = L(s << 24)
            T1[i] = L(s << 16)
            T2[i] = L(s << 8)
            T3[i] = L(s)
        return (T0, T1, T2, T3)

    def _bulk(self, data: bytes, rk) -> bytes:
        n = len(data)
        out = bytearray(n)
        T0, T1, T2, T3 = self._T_TABLES
        unpack_from = struct.unpack_from
        pack_into = struct.pack_into
        idx = 0
        while idx < n:
            X0, X1, X2, X3 = unpack_from('>IIII', data, idx)
            for i in range(0, 32, 4):
                t = X1 ^ X2 ^ X3 ^ rk[i]
                X0 ^= T0[t >> 24] ^ T1[t >> 16 & 255] ^ T2[t >> 8 & 255] ^ T3[t & 255]
                t = X2 ^ X3 ^ X0 ^ rk[i + 1]
                X1 ^= T0[t >> 24] ^ T1[t >> 16 & 255] ^ T2[t >> 8 & 255] ^ T3[t & 255]
                t = X3 ^ X0 ^ X1 ^ rk[i + 2]
                X2 ^= T0[t >> 24] ^ T1[t >> 16 & 255] ^ T2[t >> 8 & 255] ^ T3[t & 255]
                t = X0 ^ X1 ^ X2 ^ rk[i + 3]
                X3 ^= T0[t >> 24] ^ T1[t >> 16 & 255] ^ T2[t >> 8 & 255] ^ T3[t & 255]
            pack_into('>IIII', out, idx, X3, X2, X1, X0)
            idx += 16
        return bytes(out)

    def encrypt_bulk(self, data: bytes) -> bytes:
        lib = _load_fast_sm4()
        if lib is not None:
            data = bytes(data)
            n = len(data)
            inbuf = ctypes.create_string_buffer(data)
            outbuf = ctypes.create_string_buffer(n)
            lib.sm4_ecb(ctypes.create_string_buffer(self._key), inbuf, outbuf, n, 1)
            return outbuf.raw
        return self._bulk(data, self._rkey)

    def decrypt_bulk(self, data: bytes) -> bytes:
        lib = _load_fast_sm4()
        if lib is not None:
            data = bytes(data)
            n = len(data)
            inbuf = ctypes.create_string_buffer(data)
            outbuf = ctypes.create_string_buffer(n)
            lib.sm4_ecb(ctypes.create_string_buffer(self._key), inbuf, outbuf, n, 0)
            return outbuf.raw
        return self._bulk(data, self._rkey[::-1])

_FAST_SM4_LIB = None
_FAST_SM4_TRIED = False

def _sm4_c_source() -> str:
    sbox = SM4._S_BOX
    fk = SM4._FK
    ck = SM4._CK
    L = []
    L.append('#include <stdint.h>')
    L.append('#include <stddef.h>')
    L.append('static const uint8_t SBOX[256] = { ' + ', '.join(str(x) for x in sbox) + ' };')
    L.append('static const uint32_t FK[4] = { ' + ', '.join(hex(x) for x in fk) + ' };')
    L.append('static const uint32_t CK[32] = { ' + ', '.join(hex(x) for x in ck) + ' };')
    L.append('static inline uint32_t rotl(uint32_t x, int n){ return (x << n) | (x >> (32 - n)); }')
    L.append('static inline uint32_t load_be(const uint8_t* p){ return ((uint32_t)p[0]<<24)|((uint32_t)p[1]<<16)|((uint32_t)p[2]<<8)|(uint32_t)p[3]; }')
    L.append('static inline void store_be(uint8_t* p, uint32_t v){ p[0]=(uint8_t)(v>>24); p[1]=(uint8_t)(v>>16); p[2]=(uint8_t)(v>>8); p[3]=(uint8_t)v; }')
    L.append('static inline uint32_t sb(uint32_t x){ return ((uint32_t)SBOX[(x>>24)&0xff]<<24)|((uint32_t)SBOX[(x>>16)&0xff]<<16)|((uint32_t)SBOX[(x>>8)&0xff]<<8)|(uint32_t)SBOX[x&0xff]; }')
    L.append('static inline uint32_t t0(uint32_t x){ x = sb(x); return x ^ rotl(x,2) ^ rotl(x,10) ^ rotl(x,18) ^ rotl(x,24); }')
    L.append('static inline uint32_t t1(uint32_t x){ x = sb(x); return x ^ rotl(x,13) ^ rotl(x,23); }')
    L.append('static void expand(const uint8_t* key, uint32_t rk[32]){')
    L.append('    uint32_t k0 = load_be(key) ^ FK[0];')
    L.append('    uint32_t k1 = load_be(key+4) ^ FK[1];')
    L.append('    uint32_t k2 = load_be(key+8) ^ FK[2];')
    L.append('    uint32_t k3 = load_be(key+12) ^ FK[3];')
    L.append('    for (int i = 0; i < 32; i++){')
    L.append('        k0 ^= t1(k1 ^ k2 ^ k3 ^ CK[i]); rk[i] = k0;')
    L.append('        k1 ^= t1(k2 ^ k3 ^ k0 ^ CK[++i]); rk[i] = k1;')
    L.append('        k2 ^= t1(k3 ^ k0 ^ k1 ^ CK[++i]); rk[i] = k2;')
    L.append('        k3 ^= t1(k0 ^ k1 ^ k2 ^ CK[++i]); rk[i] = k3;')
    L.append('    }')
    L.append('}')
    L.append('static void crypt_block(const uint8_t* in, uint8_t* out, const uint32_t* rk){')
    L.append('    uint32_t x0 = load_be(in);')
    L.append('    uint32_t x1 = load_be(in+4);')
    L.append('    uint32_t x2 = load_be(in+8);')
    L.append('    uint32_t x3 = load_be(in+12);')
    L.append('    for (int i = 0; i < 32; i += 4){')
    L.append('        x0 ^= t0(x1 ^ x2 ^ x3 ^ rk[i]);')
    L.append('        x1 ^= t0(x2 ^ x3 ^ x0 ^ rk[i+1]);')
    L.append('        x2 ^= t0(x3 ^ x0 ^ x1 ^ rk[i+2]);')
    L.append('        x3 ^= t0(x0 ^ x1 ^ x2 ^ rk[i+3]);')
    L.append('    }')
    L.append('    store_be(out, x3); store_be(out+4, x2); store_be(out+8, x1); store_be(out+12, x0);')
    L.append('}')
    L.append('void sm4_ecb(const uint8_t* key, const uint8_t* in, uint8_t* out, size_t len, int encrypt){')
    L.append('    uint32_t rk[32];')
    L.append('    expand(key, rk);')
    L.append('    if (!encrypt){')
    L.append('        for (int i = 0; i < 16; i++){ uint32_t tmp = rk[i]; rk[i] = rk[31-i]; rk[31-i] = tmp; }')
    L.append('    }')
    L.append('    for (size_t off = 0; off < len; off += 16){ crypt_block(in + off, out + off, rk); }')
    L.append('}')
    return '\n'.join(L)

def _load_fast_sm4():
    global _FAST_SM4_LIB, _FAST_SM4_TRIED
    if _FAST_SM4_TRIED:
        return _FAST_SM4_LIB
    _FAST_SM4_TRIED = True
    try:
        tool_dir = Path(__file__).resolve().parent
        src_path = tool_dir / 'sm4_fast.c'
        so_path = tool_dir / 'sm4_fast.so'
        c_src = _sm4_c_source()
        if not src_path.exists() or src_path.read_text() != c_src:
            src_path.write_text(c_src)
        recompile = (not so_path.exists()) or (so_path.stat().st_mtime < src_path.stat().st_mtime)
        if recompile:
            for cc in ('gcc', 'cc', 'clang'):
                try:
                    r = subprocess.run([cc, '-O2', '-shared', '-fPIC', str(src_path), '-o', str(so_path)],
                                       capture_output=True, timeout=120)
                    if r.returncode == 0 and so_path.exists():
                        break
                except Exception:
                    continue
        if not so_path.exists():
            return None
        lib = ctypes.CDLL(str(so_path))
        lib.sm4_ecb.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_int]
        lib.sm4_ecb.restype = None
        _FAST_SM4_LIB = lib
        return lib
    except Exception:
        return None

class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        assert n > 0
        padding = n - len(data) % n
        return data if padding == n else data + b'\x00' * padding

    @staticmethod
    def align_up(x: int, n: int) -> int:
        return (x + n - 1) // n * n

class Reader:
    def __init__(self, buffer, cursor=0):
        self._buffer = buffer
        self._cursor = cursor

    def u1(self, move_cursor=True): return self.unpack('B', move_cursor=move_cursor)[0]
    def u4(self, move_cursor=True): return self.unpack('<I', move_cursor=move_cursor)[0]
    def u8(self, move_cursor=True): return self.unpack('<Q', move_cursor=move_cursor)[0]
    def i1(self, move_cursor=True): return self.unpack('b', move_cursor=move_cursor)[0]
    def i4(self, move_cursor=True): return self.unpack('<i', move_cursor=move_cursor)[0]
    def i8(self, move_cursor=True): return self.unpack('<q', move_cursor=move_cursor)[0]
    def s(self, n: int, move_cursor=True): return self.unpack(f'{n}s', move_cursor=move_cursor)[0]

    def unpack(self, f: str, offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor:
            self._cursor += struct.calcsize(f)
        return x

    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0:
            return str()
        assert length > 0
        offset = 0 if move_cursor else 4
        return self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00').decode(errors='ignore')

class PakInfo:
    def __init__(self, buffer, keystream: List[int]):
        def decrypt_index_encrypted(x):
            return (x ^ keystream[3]) & 255

        def decrypt_magic(x):
            return x ^ keystream[2]

        def decrypt_index_hash(x):
            key = struct.pack('<5I', *keystream[4:][:5])
            assert len(x) == len(key)
            return bytes((a ^ b for a, b in zip(x, key)))

        def decrypt_index_size(x):
            return x ^ (keystream[10] << 32 | keystream[11])

        def decrypt_index_offset(x):
            return x ^ (keystream[0] << 32 | keystream[1])

        reader = Reader(buffer[-PakInfo._mem_size((-1)):])
        self.index_encrypted = decrypt_index_encrypted(reader.u1()) == 1
        self.magic = decrypt_magic(reader.u4())
        self.version = reader.u4()
        self.index_hash = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size = decrypt_index_size(reader.u8())
        self.index_offset = decrypt_index_offset(reader.u8())
        if self.version <= 3:
            self.index_encrypted = False

    @staticmethod
    def _mem_size(_): return 45

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: List[int]):
        def decrypt_unk(x):
            key = struct.pack('<8I', *keystream[7:][:8])
            assert len(x) == len(key)
            return bytes((a ^ b for a, b in zip(x, key)))

        def decrypt_stem_hash(x):
            return x ^ keystream[8]

        def decrypt_unk_hash(x):
            return x ^ keystream[9]

        super().__init__(buffer, keystream)
        reader = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1 = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
        self.unk2 = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash = reader.s(20) if self.version >= 12 else bytes()

    @staticmethod
    def _mem_size(version: int) -> int:
        s7 = 32 if version >= 7 else 0
        s8 = 768 if version >= 8 else 0
        s9 = 8 if version >= 9 else 0
        s12 = 20 if version >= 12 else 0
        return PakInfo._mem_size(version) + s7 + s8 + s9 + s12

class PakCompressedBlock:
    def __init__(self, reader: Reader):
        self.start = reader.u8()
        self.end = reader.u8()

@dataclass
class TencentPakEntry:
    def __init__(self, reader: Reader, version: int):
        self.content_hash = reader.s(20)
        if version <= 1:
            _ = reader.u8()
        self.offset = reader.u8()
        self.uncompressed_size = reader.u8()
        self.compression_method = reader.u4() & CM_MASK
        self.size = reader.u8()
        self.unk1 = reader.u1() if version >= 5 else 0
        self.unk2 = reader.s(20) if version >= 5 else bytes()
        if self.compression_method != 0 and version >= 3:
            self.compressed_blocks = [PakCompressedBlock(reader) for _ in range(reader.u4())]
        else:
            self.compressed_blocks = []
        self.compression_block_size = reader.u4() if version >= 4 else 0
        self.encrypted = reader.u1() == 1 if version >= 4 else False
        self.encryption_method = reader.u4() if version >= 12 else 0
        self.index_new_sep = reader.u4() if version >= 12 else 0

class PakCrypto:

    class _LCG:
        def __init__(self, seed: int):
            self.state = seed

        def next(self) -> int:
            MASK_32 = 4294967295
            MSB_1 = 2147483648

            def wrap(x):
                x &= MASK_32
                return x if not x & MSB_1 else (x + MSB_1 & MASK_32) - MSB_1

            x1 = wrap(1103515245 * self.state)
            self.state = wrap(x1 + 12345)
            x2 = wrap(x1 + 77880) if self.state < 0 else self.state
            return (x2 >> 16 & MASK_32) % 32767

    @staticmethod
    def zuc_keystream() -> List[int]:
        zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]

    @staticmethod
    def _xorxor(buffer, x):
        return bytes((buffer[i] ^ x[i % len(x)] for i in range(len(buffer))))

    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        result = bytes()
        for i in range(math.ceil(n / SHA1.digest_size)):
            result += SHA1.new(buffer).digest()
        if len(result) >= n:
            return result[:n]
        return result + b'\x00' * (n - len(result))

    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]

        if len(buffer) < 43:
            return bytes()
        x1 = buffer[1:][:SHA1.digest_size]
        x2 = buffer[SHA1.digest_size + 1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
        part1, m = (x2[:SHA1.digest_size], x2[SHA1.digest_size:])
        if part1 != SHA1.new(b'\x00' * SHA1.digest_size).digest():
            return bytes()
        return unpad(m)

    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature, 'little')
        n = int.from_bytes(modulus, 'little')
        e = 65537
        m = pow(c, e, n).to_bytes(256, 'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))

    @staticmethod
    def _decrypt_simple1(ciphertext) -> bytes:
        return bytes((x ^ SIMPLE1_DECRYPT_KEY for x in ciphertext))

    @staticmethod
    def _decrypt_simple2(ciphertext) -> bytes:
        class RollingKey:
            def __init__(self, v):
                self._value = v

            def update(self, x):
                self._value ^= x
                return self._value

        assert len(ciphertext) % SIMPLE2_BLOCK_SIZE == 0
        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rk = RollingKey(initial_key)
        plaintext = (struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(ciphertext)//4}I', ciphertext))
        return bytes(it.chain.from_iterable(plaintext))

    @staticmethod
    @lru_cache(maxsize=128)
    def _derive_sm4_key(file_path: PurePath, encryption_method: int) -> bytes:
        part1 = file_path.stem.lower()
        if encryption_method == EM_SM4_2:
            secret = SM4_SECRET_2
        else:
            if encryption_method == EM_SM4_4:
                secret = SM4_SECRET_4
            else:
                index = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
                secret = f'{SM4_SECRET_NEW[index]}{encryption_method}'
        return SHA1.new(str(part1 + secret).encode()).digest()[:SM4.key_length()]

    @staticmethod
    @lru_cache(maxsize=128)
    def _sm4_context_for_key(key: bytes) -> SM4:
        return SM4(key)

    @staticmethod
    def _decrypt_sm4(ciphertext, file_path, encryption_method) -> bytes:
        assert len(ciphertext) % SM4.block_length() == 0
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        return PakCrypto._sm4_context_for_key(key).decrypt_bulk(ciphertext)

    @staticmethod
    def decrypt_index(ciphertext, pak_info):
        if pak_info.version > 7:
            key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            aes = AES.new(key, MODE_CBC, iv[:16])
            return unpad(aes.decrypt(ciphertext), AES.block_size)
        return bytes(PakCrypto._decrypt_simple1(ciphertext))

    @staticmethod
    def _is_simple1_method(m): return m == EM_SIMPLE1

    @staticmethod
    def _is_simple2_method(m): return m == EM_SIMPLE2 or m == 17

    @staticmethod
    def _is_sm4_method(m):
        return m == EM_SM4_2 or m == EM_SM4_4 or m & EM_SM4_NEW_MASK != 0

    @staticmethod
    def align_encrypted_content_size(n, m):
        if PakCrypto._is_simple2_method(m):
            return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        if PakCrypto._is_sm4_method(m):
            return Misc.align_up(n, SM4.block_length())
        return n

    @staticmethod
    def decrypt_block(ciphertext, file, encryption_method):
        if PakCrypto._is_simple1_method(encryption_method):
            return PakCrypto._decrypt_simple1(ciphertext)
        if PakCrypto._is_simple2_method(encryption_method):
            return PakCrypto._decrypt_simple2(ciphertext)
        if PakCrypto._is_sm4_method(encryption_method):
            return PakCrypto._decrypt_sm4(ciphertext, file, encryption_method)
        raise ValueError(f'Unknown encryption method: {encryption_method}')

    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n, encryption_method):
        if not PakCrypto._is_sm4_method(encryption_method):
            return list(range(n))
        perm = []
        lcg = PakCrypto._LCG(n)
        while len(perm) != n:
            x = lcg.next() % n
            if x not in perm:
                perm.append(x)
        inv = [0] * len(perm)
        for i, x in enumerate(perm):
            inv[x] = i
        return inv

class PakCompression:

    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_decompressor(d):
        return ZstdDecompressor(d)

    @staticmethod
    def zstd_dictionary(d):
        return ZstdCompressionDict(d, DICT_TYPE_AUTO)

    @staticmethod
    def decompress_block(block, dict, compression_method):
        if compression_method == CM_ZLIB:
            try:
                return zlib.decompress(block)
            except zlib.error:
                return block
        if compression_method in (CM_ZSTD, CM_ZSTD_DICT):
            if compression_method != CM_ZSTD_DICT:
                dict = None
            return PakCompression._zstd_decompressor(dict).decompress(block)
        raise ValueError(f'Unknown compression method: {compression_method}')

class TencentPakFile:
    def __init__(self, file_path, is_od=False, silent=False):
        self._silent = silent
        self._file_path = file_path
        with open_long(file_path, 'rb') as f:
            self._file_content = memoryview(f.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._zstd_dict_entry = None
        self._files = []
        self._index = {}
        try:
            ks = PakCrypto.zuc_keystream()
        except Exception:
            ks = [0] * 16
        self._pak_info = TencentPakInfo(self._file_content, ks)
        self._verify_stem_hash()
        self._tencent_load_index()

    def _get_method_str(self, m, is_enc):
        if is_enc:
            if PakCrypto._is_simple1_method(m):
                return "SIMPLE1"
            if PakCrypto._is_simple2_method(m):
                return "SIMPLE2"
            if PakCrypto._is_sm4_method(m):
                return f"SM4 (Type {m})"
            return "NONE" if m == 0 else "UNKNOWN"
        if m == CM_NONE:
            return "NONE"
        if m == CM_ZLIB:
            return "ZLIB"
        if m == CM_ZSTD:
            return "ZSTD"
        if m == CM_ZSTD_DICT:
            return "ZSTD_DICT"
        return "UNKNOWN"

    def _verify_stem_hash(self):
        if not self._is_od and self._pak_info.version >= 9:
            try:
                assert self._pak_info.stem_hash == zlib.crc32(self._file_path.stem.encode('utf-32le'))
            except AssertionError:
                if not self._silent:
                    console.print(f"[bold {WARNING}]Warning: pak filename differs from original stem.[/]")

    def _tencent_load_index(self):
        raw_index = bytes(self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size])

        def _try_aes_decrypt(data, mod):
            try:
                key = PakCrypto.rsa_extract(self._pak_info.packed_key, mod)
                iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, mod)
                if not key or not iv or len(key) < 16 or len(iv) < 16:
                    return None
                aes = AES.new(key, MODE_CBC, iv[:16])
                decrypted = aes.decrypt(data)
                try:
                    result = unpad(decrypted, AES.block_size)
                except Exception:
                    result = decrypted.rstrip(b'\x00')
                    if not result:
                        return None
                r = Reader(result)
                r.string()
                n = r.u4()
                if 0 <= n <= 200000:
                    return result
                return None
            except Exception:
                return None

        candidates = []

        if self._pak_info.index_encrypted:
            d = _try_aes_decrypt(raw_index, RSA_MOD_1)
            if d:
                candidates.append(d)
            d = _try_aes_decrypt(raw_index, RSA_MOD_2)
            if d:
                candidates.append(d)
            try:
                candidates.append(PakCrypto._decrypt_simple1(raw_index))
            except Exception:
                pass

        candidates.append(raw_index)

        for data in candidates:
            try:
                self._files = []
                self._index = {}
                self._load_index(data)
                if self._index:
                    return
            except Exception:
                continue

        self._files = []
        self._index = {}

    @staticmethod
    def _construct_mount_point(mp):
        result = PurePath()
        for part in PurePath(mp).parts:
            if part != '..':
                result /= part
        return result

    def _peek_content(self, offset, size, encryption_method):
        size = PakCrypto.align_encrypted_content_size(size, encryption_method)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block, encryption_method):
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, encryption_method)
        return self._file_content[block.start:][:size]

    def _construct_zstd_dict(self, dict_entry):
        try:
            data = self._peek_content(dict_entry.offset, dict_entry.size, dict_entry.encryption_method)
            if dict_entry.encrypted:
                data = PakCrypto.decrypt_block(data, PurePath("zstddic"), dict_entry.encryption_method)
            reader = Reader(data)
            dict_size = reader.u8()
            _ = reader.u4()
            _ = reader.u4()
            dict_data = reader.s(dict_size)
            if ZstdCompressionDict:
                self._zstd_dict = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO)
        except Exception as e:
            if not self._silent:
                console.print(f"[red]Dictionary Load Error: {e}[/red]")

    def _load_index(self, index_data):
        if self._pak_info.version <= 10:
            raise ValueError(f'Unsupported version: {self._pak_info.version}')
        reader = Reader(index_data)
        self._mount_point = self._construct_mount_point(reader.string())
        n_files = min(reader.u4(), 200000)
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(n_files)]
        dirs_count = min(reader.u8(), 200000)
        for _ in range(dirs_count):
            dir_path = PurePath(reader.string())
            file_count = min(reader.u8(), 200000)
            e = {}
            for _ in range(file_count):
                name = reader.string()
                idx = reader.i4()
                mapped = ~idx
                if 0 <= mapped < len(self._files):
                    e[name] = self._files[mapped]
                else:
                    e[name] = None
            if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                if e:
                    self._zstd_dict_entry = e[[*e.keys()][0]]
                    self._construct_zstd_dict(self._zstd_dict_entry)
                continue
            self._index.update({PurePath(dir_path): e})

    def _write_to_disk(self, file_path, entry):
        encryption_method = entry.encryption_method
        compression_method = entry.compression_method

        file_path = Path(*[str(p).replace('\x00', '') for p in Path(file_path).parts])
        parent_dir = file_path.parent
        os.makedirs(to_long_path(parent_dir), exist_ok=True)

        with open_long(file_path, 'wb') as file:
            if compression_method == CM_NONE:
                data = self._peek_content(entry.offset, entry.size, encryption_method)
                if entry.encrypted:
                    data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                file.write(data[:entry.uncompressed_size])
                return

            if not entry.compressed_blocks:
                if entry.size:
                    data = self._peek_content(entry.offset, entry.size, encryption_method)
                    if entry.encrypted:
                        data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                    data = PakCompression.decompress_block(data, self._zstd_dict, compression_method)
                    file.write(data)
                return

            try:
                for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), encryption_method):
                    data = self._peek_block_content(entry.compressed_blocks[x], encryption_method)
                    if entry.encrypted:
                        data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                    data = PakCompression.decompress_block(data, self._zstd_dict, compression_method)
                    file.write(data)
            except Exception as exc:
                file.seek(0)
                file.truncate()
                raw = bytearray()
                for blk in entry.compressed_blocks:
                    raw += self._peek_block_content(blk, encryption_method)
                file.write(raw)

    def dump(self, out_path):
        out_path = out_path / self._mount_point
        out_path.mkdir(parents=True, exist_ok=True)
        total_files = sum(len(d) for d in self._index.values())
        if total_files == 0:
            console.print(Panel("[yellow]No files in PAK index.[/yellow]", border_style="yellow"))
            return False

        console.print(Panel(
            Align.center(Text.from_markup(
                f"[bold {BRIGHT_COLOR}]\\[S][/bold {BRIGHT_COLOR}] PAUSE / RESUME    "
                f"[bold {DIM_COLOR}]◆[/bold {DIM_COLOR}]    "
                f"[bold {ERROR}]\\[B][/bold {ERROR}] STOP / CANCEL"
            )),
            title=f"[bold black on {BRIGHT_COLOR}] LIVE CONTROLS [/]",
            border_style=BORDER_COLOR,
            box=HEAVY_EDGE,
        ))
        console.print()

        is_paused = False
        is_cancelled = False

        with Progress(
            SpinnerColumn("dots", style=f"bold {BRIGHT_COLOR}"),
            TextColumn(f"[bold {BRIGHT_COLOR}][EXTRACT][/] {{task.description}}"),
            BarColumn(bar_width=40, complete_style=f"bold {TEXT_COLOR}"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Extracting files...", total=total_files)

            for dir_path, dir_content in self._index.items():
                if is_cancelled:
                    break
                current_out_path = out_path / dir_path
                current_out_path.mkdir(parents=True, exist_ok=True)

                for file_name, entry in dir_content.items():
                    if is_cancelled:
                        break

                    while True:
                        key = check_key_press()
                        if key == 's':
                            is_paused = not is_paused
                            if is_paused:
                                progress.update(task, description=f"[blink bold {WARNING}]PAUSED — press [S] to resume[/]")
                                console.print(f"[bold {WARNING}]PAUSED[/] — press [bold {BRIGHT_COLOR}]S[/] to resume")
                            else:
                                progress.update(task, description="Extracting files...")
                                console.print(f"[bold {TEXT_COLOR}]RESUMED[/]")
                        elif key == 'b':
                            is_cancelled = True
                            console.print(f"[bold {ERROR}]STOP requested...[/]")
                            break

                        if not is_paused:
                            break
                        time.sleep(0.1)

                    if is_cancelled:
                        break

                    if entry is None:
                        progress.update(task, advance=1)
                        continue

                    short_name = file_name if len(file_name) < 45 else file_name[:20] + "..." + file_name[-20:]

                    try:
                        self._write_to_disk(current_out_path / file_name, entry)
                        console.print(f"[bold {BRIGHT_COLOR}]→[/] [bold {TEXT_COLOR}]{short_name}[/]")
                    except Exception as e:
                        console.print(f"[bold {ERROR}]FAIL:[/] {short_name} [dim]({e})[/dim]")

                    progress.update(task, advance=1)

        console.print()
        if is_cancelled:
            console.print(Panel(
                f"[bold {ERROR}]EXTRACTION CANCELLED BY USER![/bold {ERROR}]\n"
                f"[white]Partial files already written.[/white]",
                border_style=ERROR,
                box=HEAVY_EDGE,
            ))
            return False
        else:
            console.print(Panel(
                f"[bold {BRIGHT_COLOR}]Successfully unpacked {total_files} files![/]",
                border_style=BORDER_COLOR,
                box=DOUBLE_EDGE,
            ))
            return True

    def dump_single_file(self, target_file_name, out_path_base, single_dir_name):
        entry_found = None
        dir_of_file = None
        for dir_path, dir_content in self._index.items():
            if target_file_name in dir_content:
                entry_found = dir_content[target_file_name]
                dir_of_file = dir_path.relative_to(self._mount_point) if dir_path.parts and dir_path.parts[0] == self._mount_point.name else dir_path
                break

        if entry_found is None:
            console.print(Panel(f"[red]Error: '{target_file_name}' not found in PAK.[/red]"))
            return

        pak_stem = Path(self._file_path).stem
        current_out_path = out_path_base / single_dir_name / pak_stem / dir_of_file
        os.makedirs(to_long_path(current_out_path), exist_ok=True)
        target_path = current_out_path / target_file_name

        console.print(f"[dim]|[/] [bold {BRIGHT_COLOR}]SINGLE UNPACK:[/] [green]{target_file_name}[/] [dim]from {self._file_path.name}[/dim]")
        try:
            self._write_to_disk(target_path, entry_found)
            console.print(Panel(f"[green]Successfully extracted: {target_file_name}[/green]"))
        except Exception as e:
            console.print(Panel(f"[red]Error writing {target_file_name}: {e}[/red]"))

def _encrypt_plaintext(plaintext: bytes, pak_relative_path: PurePath, encryption_method: int) -> bytes:
    if PakCrypto._is_simple1_method(encryption_method):
        return bytes((b ^ SIMPLE1_DECRYPT_KEY for b in plaintext))
    if PakCrypto._is_simple2_method(encryption_method):
        pad_len = -len(plaintext) % SIMPLE2_BLOCK_SIZE
        plaintext += b'\x00' * pad_len
        key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rolling = key
        out = []
        for x, in struct.iter_unpack('<I', plaintext):
            c = rolling ^ x
            out.append(c)
            rolling ^= c
        return struct.pack(f'<{len(out)}I', *out)
    if PakCrypto._is_sm4_method(encryption_method):
        key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        pad_len = -len(plaintext) % 16
        if pad_len > 0:
            plaintext = plaintext + b'\x00' * pad_len
        return sm4.encrypt_bulk(plaintext)
    return plaintext

def _best_compress(chunk, cm, zstd_dict=None, fast=False):
    if cm == CM_ZLIB:
        return zlib.compress(chunk, 1 if fast else 9)
    if cm in (CM_ZSTD, CM_ZSTD_DICT):
        zd = zstd_dict if cm == CM_ZSTD_DICT else None
        levels = [6, 3, 1] if fast else [22, 19, 16, 13, 10, 7, 4, 1]
        for lvl in levels:
            try:
                return ZstdCompressor(level=lvl, dict_data=zd, threads=1).compress(chunk)
            except Exception:
                continue
    return chunk

def _pw_string(s):
    if not s:
        return struct.pack('<i', 0)
    b = s.encode('utf-8') + b'\x00'
    return struct.pack('<i', len(b)) + b

def _pw_entry(e, v):
    w = bytearray(e.content_hash)
    w += struct.pack('<Q', e.offset)
    w += struct.pack('<Q', e.uncompressed_size)
    w += struct.pack('<I', e.compression_method)
    w += struct.pack('<Q', e.size)
    if v >= 5:
        w += bytes([e.unk1])
        w += e.unk2
    if e.compression_method != CM_NONE and v >= 3:
        w += struct.pack('<I', len(e.compressed_blocks))
        for b in e.compressed_blocks:
            w += struct.pack('<QQ', b.start, b.end)
    if v >= 4:
        w += struct.pack('<I', e.compression_block_size)
        w += bytes([1 if e.encrypted else 0])
    if v >= 12:
        w += struct.pack('<II', e.encryption_method, e.index_new_sep)
    return bytes(w)

def _get_all_dirs_and_mp(pak_file):
    raw = bytes(pak_file._file_content[pak_file._pak_info.index_offset:][:pak_file._pak_info.index_size])
    if pak_file._pak_info.index_encrypted:
        raw = PakCrypto.decrypt_index(raw, pak_file._pak_info)
    r = Reader(raw)
    mp = r.string()
    num_files = r.u4()
    for _ in range(num_files):
        TencentPakEntry(r, pak_file._pak_info.version)
    dirs = {}
    for _ in range(r.u8()):
        dp = r.string()
        cnt = r.u8()
        dirs[dp] = {r.string(): pak_file._files[~r.i4()] for _ in range(cnt)}
    return mp, dirs

def _write_entry_into_buf(out_buf, ne, new_raw, pak_rel, template_entry, zstd_dict):
    ne.compression_method = template_entry.compression_method
    ne.encryption_method = template_entry.encryption_method
    ne.encrypted = template_entry.encrypted
    ne.unk1 = template_entry.unk1
    ne.index_new_sep = template_entry.index_new_sep
    ne.uncompressed_size = len(new_raw)

    if ne.compression_method == CM_NONE:
        if ne.encrypted:
            padded = new_raw
            if PakCrypto._is_sm4_method(ne.encryption_method):
                pad_len = -len(padded) % 16
                if pad_len > 0:
                    padded = padded + b'\x00' * pad_len
            cipher = _encrypt_plaintext(padded, pak_rel, ne.encryption_method)
        else:
            cipher = new_raw
        ne.offset = len(out_buf)
        ne.size = len(cipher)
        ne.compression_block_size = 0
        ne.compressed_blocks = []
        out_buf += cipher
    else:
        cs = template_entry.compression_block_size if template_entry.compression_block_size > 0 else 65536
        ne.compression_block_size = cs
        chunks = [new_raw[i:i + cs] for i in range(0, len(new_raw), cs)]

        if not chunks:
            ne.compressed_blocks = []
            ne.offset = len(out_buf)
            ne.size = 0
            return

        n = len(chunks)
        cipher_logical = []
        for chunk in chunks:
            compressed = _best_compress(chunk, ne.compression_method, zstd_dict)
            if ne.encrypted:
                if PakCrypto._is_sm4_method(ne.encryption_method):
                    pad_len = -len(compressed) % 16
                    if pad_len > 0:
                        compressed = compressed + b'\x00' * pad_len
                cipher = _encrypt_plaintext(compressed, pak_rel, ne.encryption_method)
            else:
                cipher = compressed
            cipher_logical.append(cipher)

        if ne.encrypted and PakCrypto._is_sm4_method(ne.encryption_method):
            order = PakCrypto.generate_block_indices(n, ne.encryption_method)
        else:
            order = list(range(n))

        phys_cipher = [b''] * n
        for logical_i in range(n):
            phys_cipher[order[logical_i]] = cipher_logical[logical_i]

        phys_blks = []
        for phys_i in range(n):
            bd = phys_cipher[phys_i]
            blk = PakCompressedBlock.__new__(PakCompressedBlock)
            blk.start = len(out_buf)
            blk.end = blk.start + len(bd)
            out_buf += bd
            phys_blks.append(blk)

        logical_blks = [None] * n
        for logical_i in range(n):
            phys_i = order[logical_i]
            logical_blks[logical_i] = phys_blks[phys_i]

        ne.compressed_blocks = logical_blks
        ne.offset = phys_blks[0].start if phys_blks else len(out_buf)
        ne.size = sum(b.end - b.start for b in phys_blks)

    stored_bytes = bytes(out_buf[ne.offset:ne.offset + ne.size])
    ne.content_hash = SHA1.new(stored_bytes).digest()
    ne.unk2 = b'\x00' * 20

def _extract_entry_plaintext(pak_file, entry, full_path):
    em = entry.encryption_method
    cm = entry.compression_method
    path = PurePath(full_path)
    if cm == CM_NONE:
        data = pak_file._peek_content(entry.offset, entry.size, em)
        if entry.encrypted:
            data = PakCrypto.decrypt_block(data, path, em)
        return bytes(data[:entry.uncompressed_size])
    out = bytearray()
    for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), em):
        data = pak_file._peek_block_content(entry.compressed_blocks[x], em)
        if entry.encrypted:
            data = PakCrypto.decrypt_block(data, path, em)
        out += PakCompression.decompress_block(data, pak_file._zstd_dict, cm)
    return bytes(out)

def _copy_original_content(out_buf, pak_file, ne, old_entry):
    em = old_entry.encryption_method
    if old_entry.compression_method == CM_NONE:
        read_sz = (PakCrypto.align_encrypted_content_size(old_entry.size, em)
                   if old_entry.encrypted else old_entry.size)
        ne.offset = len(out_buf)
        out_buf += bytes(pak_file._file_content[old_entry.offset: old_entry.offset + read_sz])
    elif old_entry.compressed_blocks:
        new_blks = []
        for ob in old_entry.compressed_blocks:
            unc = ob.end - ob.start
            enc = (PakCrypto.align_encrypted_content_size(unc, em)
                   if old_entry.encrypted else unc)
            nb = PakCompressedBlock.__new__(PakCompressedBlock)
            nb.start = len(out_buf)
            nb.end = nb.start + unc
            out_buf += bytes(pak_file._file_content[ob.start: ob.start + enc])
            new_blks.append(nb)
        ne.compressed_blocks = new_blks
        ne.offset = new_blks[0].start
    ne.encryption_method = old_entry.encryption_method
    ne.encrypted = old_entry.encrypted

def _write_pak_index_footer(pak_file, mp_str, all_dirs, new_files, old_to_new, out_buf, output_path):
    version = pak_file._pak_info.version
    keystream = PakCrypto.zuc_keystream()
    eidx = {id(new_files[i]): i for i in range(len(new_files))}
    old_id_to_new_idx = {id(pak_file._files[i]): i for i in range(len(pak_file._files))}

    idx = bytearray(_pw_string(mp_str))
    idx += struct.pack('<I', len(new_files))
    for ne in new_files:
        idx += _pw_entry(ne, version)
    idx += struct.pack('<Q', len(all_dirs))

    for dp_str, dir_files in all_dirs.items():
        idx += _pw_string(dp_str)
        idx += struct.pack('<Q', len(dir_files))
        for name, old_e in dir_files.items():
            idx += _pw_string(name)
            found_idx = eidx.get(id(old_e))
            if found_idx is None:
                found_idx = old_id_to_new_idx.get(id(old_e))
            if found_idx is None:
                copy_of = next((k for k, v in old_to_new.items() if v is old_e), None)
                if copy_of is not None:
                    found_idx = eidx.get(id(old_to_new[copy_of]))
            if found_idx is None:
                for i, e in enumerate(new_files):
                    if e.offset == old_e.offset and e.size == old_e.size:
                        found_idx = i
                        break
            idx += struct.pack('<i', ~found_idx if found_idx is not None else -1)

    index_plain = bytes(idx)
    new_sha1 = SHA1.new(index_plain).digest()

    if pak_file._pak_info.index_encrypted:
        key = PakCrypto.rsa_extract(pak_file._pak_info.packed_key, RSA_MOD_1)
        iv = PakCrypto.rsa_extract(pak_file._pak_info.packed_iv, RSA_MOD_1)
        aes = AES.new(key, MODE_CBC, iv[:16])
        pad_len = (-len(index_plain)) % AES.block_size or AES.block_size
        index_bytes = aes.encrypt(index_plain + bytes([pad_len] * pad_len))
    else:
        index_bytes = index_plain

    new_idx_offset = len(out_buf)
    new_idx_size = len(index_bytes)
    out_buf += index_bytes

    footer_sz = TencentPakInfo._mem_size(version)
    new_footer = bytearray(pak_file._file_content[-footer_sz:])
    h_key = struct.pack('<5I', *keystream[4:9])
    new_footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
    new_footer[-16:-8] = ((new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little'))
    new_footer[-8:] = ((new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little'))
    out_buf += new_footer

    with open(output_path, 'wb') as f:
        f.write(out_buf)

def download_csv_files(csv_dir: Path) -> bool:
    csv_dir.mkdir(parents=True, exist_ok=True)
    existing = [f for f in csv_dir.iterdir() if f.suffix.lower() == '.csv' and f.stat().st_size > 100]
    if len(existing) >= 2:
        console.print(f"[dim {DIM_COLOR}]CSV cache ready[/dim {DIM_COLOR}]")
        return True

    console.print(Panel(
        f"[bold {BRIGHT_COLOR}]Fetching signature databases...[/bold {BRIGHT_COLOR}]",
        title=f"[bold black on {BRIGHT_COLOR}] SIGNATURE SYNC [/]",
        border_style=BORDER_COLOR,
        box=HEAVY_EDGE,
    ))

    success_count = 0
    for filename, url in CSV_URLS.items():
        target = csv_dir / filename
        if target.exists() and target.stat().st_size > 100:
            success_count += 1
            continue

        try:
            with Progress(
                TextColumn(f"[bold {BRIGHT_COLOR}]{{task.description}}"),
                BarColumn(bar_width=40, complete_style=f"bold {TEXT_COLOR}"),
                TextColumn("[bold {BRIGHT_COLOR}]{task.percentage:>3.0f}%"),
                TextColumn(f"[dim {DIM_COLOR}]({{task.fields[fs]}})[/dim {DIM_COLOR}]"),
                TransferSpeedColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(f"{filename}", total=100, fs="")
                r = requests.get(url, stream=True, timeout=60)
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0

                with open(target, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                pct = int((downloaded / total_size) * 100)
                                progress.update(task, completed=pct, fs=f"{downloaded/(1024*1024):.2f} MB")

            console.print(f"[bold {BRIGHT_COLOR}]Synced:[/] [bold {TEXT_COLOR}]{filename}[/]")
            success_count += 1
        except Exception as e:
            console.print(f"[bold {ERROR}]Failed {filename}: {e}[/]")

    return success_count >= 1

def _select_csv_source(csv_dir):
    csv_files = [f for f in csv_dir.iterdir() if f.suffix.lower() == '.csv']
    if not csv_files:
        console.print(Panel(f"[{ERROR}]No signature files found![/]", border_style=ERROR))
        return None, None, None

    csv_table = Table(
        title=f"[bold {BRIGHT_COLOR}]Select Signature Source[/bold {BRIGHT_COLOR}]",
        box=DOUBLE_EDGE,
        border_style=BORDER_COLOR,
        header_style=f"bold black on {BRIGHT_COLOR}",
    )
    csv_table.add_column("#", justify="center", style=f"bold {BRIGHT_COLOR}", width=4)
    csv_table.add_column("Game", style=f"bold {TEXT_COLOR}")
    csv_table.add_column("Size", justify="right", style=f"bold {TEXT_COLOR}")

    for i, f in enumerate(csv_files, 1):
        sz = f.stat().st_size
        sz_str = f"{sz/1024:.1f} KB" if sz < 1024 * 1024 else f"{sz/(1024*1024):.2f} MB"
        label = {"BGMI.csv": "BGMI 4.5", "PUBG.csv": "PUBG 4.5"}.get(f.name, f.name)
        csv_table.add_row(str(i), label, sz_str)
    csv_table.add_row("0", f"[{ERROR}]BACK[/]", "[dim]-[/dim]")
    console.print(csv_table)

    try:
        sel = console.input(f"[bold {BRIGHT_COLOR}]Select source (0 = back): [/bold {BRIGHT_COLOR}]").strip()
        if not sel or sel == "0":
            return None, None, None
        idx = int(sel) - 1
        if idx < 0 or idx >= len(csv_files):
            console.print(f"[bold {ERROR}]Invalid selection[/]")
            return None, None, None
    except ValueError:
        console.print(f"[bold {ERROR}]Invalid input[/]")
        return None, None, None

    selected_csv = csv_files[idx]
    is_bgmi = selected_csv.name == "BGMI.csv"
    game_label = "BGMI" if is_bgmi else "PUBG"
    return selected_csv, is_bgmi, game_label

def _load_csv_path_map(selected_csv):
    file_path_map = {}
    try:
        with open(selected_csv, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                for part in line.split(','):
                    part = part.strip()
                    if part:
                        file_path_map[Path(part).name] = part
    except Exception as e:
        console.print(f"[bold {ERROR}]Signature read error: {e}[/]")
        return {}
    return file_path_map

def _resolve_paths_from_csv(edit_dir, file_path_map, is_bgmi):
    edit_files = [p for p in edit_dir.rglob('*') if p.is_file()]
    resolved_files = []
    unresolved = []
    ingame_csv_folder = edit_dir / "InGame" / "EvoBase" / "CSV"

    for p in edit_files:
        filename = p.name
        try:
            p.relative_to(ingame_csv_folder)
            in_ingame = True
        except ValueError:
            in_ingame = False

        if in_ingame:
            if is_bgmi:
                rp = f"Content/MultiRegion/Content/IN/CSV/InGame/EvoBase/CSV/{filename}"
            else:
                rp = f"Content/CSV/InGame/EvoBase/CSV/{filename}"
            resolved_files.append((p, rp))
        else:
            matches = [k for k in file_path_map if k.lower() == filename.lower()]
            if not matches:
                matches = [k for k in file_path_map if filename.lower() in k.lower()]
            if matches:
                resolved_files.append((p, file_path_map[matches[0]]))
            else:
                unresolved.append(p)
    return resolved_files, unresolved

def build_new_pak(data_path: Path) -> None:
    import copy as _cp

    build_root = data_path / "BUILD_PAK"
    csv_dir = build_root / "CSV"
    edit_dir = build_root / "EDIT"
    template_dir = build_root / "TEMPLATE"
    output_dir = build_root / "OUTPUT"

    for d in (csv_dir, edit_dir, template_dir, output_dir):
        d.mkdir(parents=True, exist_ok=True)

    console.print(Panel(
        f"[bold {BRIGHT_COLOR}]INTELLIGENT ARCHIVE FOUNDRY[/bold {BRIGHT_COLOR}]\n"
        f"[dim {DIM_COLOR}]Signature resolver + template archive → game-ready output[/dim {DIM_COLOR}]",
        border_style=BORDER_COLOR,
        box=DOUBLE_EDGE,
    ))

    if not download_csv_files(csv_dir):
        console.print(Panel(
            f"[bold {ERROR}]Signature sync failed![/]\n"
            f"[{WARNING}]Check network.[/]",
            border_style=ERROR,
            box=HEAVY_EDGE,
        ))
        return

    selected_csv, is_bgmi, game_label = _select_csv_source(csv_dir)
    if selected_csv is None:
        return

    console.print(f"[bold {BRIGHT_COLOR}]Loading {selected_csv.name}...[/]")
    file_path_map = _load_csv_path_map(selected_csv)
    if not file_path_map:
        console.print(Panel(f"[{ERROR}]Signature file empty![/]", border_style=ERROR))
        return
    console.print(f"[bold {BRIGHT_COLOR}]Loaded {len(file_path_map)} paths from {game_label}[/]")

    pak_files = [f for f in template_dir.iterdir() if f.suffix.lower() in ('.pak', '.obb')]
    if not pak_files:
        console.print(Panel(
            f"[{ERROR}]No template archive![/]\n"
            f"[{WARNING}]Place a .pak / .obb file in:[/]\n"
            f"[bold {BRIGHT_COLOR}]{template_dir}[/]",
            border_style=ERROR,
            box=HEAVY_EDGE,
        ))
        return

    if len(pak_files) == 1:
        template_pak_path = pak_files[0]
        console.print(f"[bold {BRIGHT_COLOR}]Template:[/] [bold {TEXT_COLOR}]{template_pak_path.name}[/]")
    else:
        pak_table = Table(title="Select Template Archive", box=DOUBLE_EDGE, border_style=BORDER_COLOR,
                          header_style=f"bold black on {BRIGHT_COLOR}")
        pak_table.add_column("#", justify="center", width=4, style=f"bold {BRIGHT_COLOR}")
        pak_table.add_column("File Name", style=f"bold {TEXT_COLOR}")
        pak_table.add_column("Size", justify="right", style=f"bold {TEXT_COLOR}")
        for i, f in enumerate(pak_files, 1):
            sz = f.stat().st_size / (1024 * 1024)
            pak_table.add_row(str(i), f.name, f"{sz:.2f} MB")
        console.print(pak_table)
        try:
            sel = console.input(f"[bold {BRIGHT_COLOR}]Select template (1-{len(pak_files)}): [/bold {BRIGHT_COLOR}]").strip()
            idx = int(sel) - 1
            if idx < 0 or idx >= len(pak_files):
                console.print(f"[bold {ERROR}]Invalid[/]")
                return
            template_pak_path = pak_files[idx]
        except ValueError:
            console.print(f"[bold {ERROR}]Invalid[/]")
            return

    edit_files = [p for p in edit_dir.rglob('*') if p.is_file()]
    if not edit_files:
        console.print(Panel(
            f"[{ERROR}]No source files![/]\n"
            f"[{WARNING}]Place files in:[/]\n"
            f"[bold {BRIGHT_COLOR}]{edit_dir}[/]",
            border_style=ERROR,
            box=HEAVY_EDGE,
        ))
        return

    resolved_files, unresolved = _resolve_paths_from_csv(edit_dir, file_path_map, is_bgmi)
    if not resolved_files:
        console.print(Panel(
            f"[{ERROR}]No files matched signature paths![/]",
            border_style=ERROR,
            box=HEAVY_EDGE,
        ))
        return

    lines = [f"[bold {BRIGHT_COLOR}]Signature: {game_label} ({selected_csv.name})[/bold {BRIGHT_COLOR}]", ""]
    for p, rp in resolved_files:
        lines.append(f"  [bold {BRIGHT_COLOR}]✓[/] [{TEXT_COLOR}]{p.name}[/] [dim {DIM_COLOR}]→[/] [bold {BRIGHT_COLOR}]{rp}[/]")
    if unresolved:
        lines += ["", f"[bold {WARNING}] {len(unresolved)} file(s) unmatched (skipped):[/]"]
        for p in unresolved:
            lines.append(f"  [dim {WARNING}]x {p.name}[/dim {WARNING}]")
    lines.append("")
    lines.append(f"[bold {BRIGHT_COLOR}]Total: {len(resolved_files)} files will be built[/bold {BRIGHT_COLOR}]")

    console.print(Panel("\n".join(lines), border_style=BORDER_COLOR, box=HEAVY_EDGE,
                        title=f"[bold black on {BRIGHT_COLOR}] PATH RESOLVER [/]"))

    confirm = console.input(f"\n[bold {BRIGHT_COLOR}]Proceed with FOUNDRY? (y/n): [/bold {BRIGHT_COLOR}]").strip().lower()
    if confirm not in ('y', 'yes'):
        console.print(f"[{WARNING}]Cancelled[/]")
        return

    output_pak = output_dir / template_pak_path.name

    try:
        console.print(f"[bold {BRIGHT_COLOR}]Forging archive...[/]")

        template_pak = TencentPakFile(template_pak_path, is_od=True)
        version = template_pak._pak_info.version
        keystream = PakCrypto.zuc_keystream()

        raw = bytes(template_pak._file_content[
            template_pak._pak_info.index_offset:][:template_pak._pak_info.index_size])
        if template_pak._pak_info.index_encrypted:
            raw = PakCrypto.decrypt_index(raw, template_pak._pak_info)
        r = Reader(raw)
        mp_str = r.string()

        template_entry = None
        for _dp, _files in template_pak._index.items():
            for _n, _e in _files.items():
                template_entry = _e
                break
            if template_entry:
                break

        if template_entry is None:
            console.print(Panel(f"[{ERROR}]Template archive empty![/]", border_style=ERROR))
            return

        out_buf = bytearray()
        new_files = []
        all_dirs = {}

        with Progress(
            SpinnerColumn(style=f"bold {BRIGHT_COLOR}"),
            TextColumn(f"[bold {BRIGHT_COLOR}][FORGE][/] {{task.description}}"),
            BarColumn(complete_style=f"bold {TEXT_COLOR}"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Forging...", total=len(resolved_files))

            for p, fp in resolved_files:
                dir_key = str(PurePath(fp).parent).replace('\\', '/')
                if dir_key and not dir_key.endswith('/'):
                    dir_key += '/'
                if dir_key == '.':
                    dir_key = ''

                ne = _cp.copy(template_entry)
                ne.compressed_blocks = []
                new_raw = p.read_bytes()
                pak_rel = PurePath(fp)

                _write_entry_into_buf(out_buf, ne, new_raw, pak_rel, template_entry, template_pak._zstd_dict)
                ne.unk2 = SHA1.new((mp_str + fp).lower().encode('utf-8')).digest()

                new_files.append(ne)
                all_dirs.setdefault(dir_key, {})[p.name] = ne
                progress.update(task, advance=1, description=p.name)

        id_to_idx = {id(ne): i for i, ne in enumerate(new_files)}
        idx = bytearray(_pw_string(mp_str))
        idx += struct.pack('<I', len(new_files))
        for ne in new_files:
            idx += _pw_entry(ne, version)
        idx += struct.pack('<Q', len(all_dirs))
        for dp_str, dir_files in all_dirs.items():
            idx += _pw_string(dp_str)
            idx += struct.pack('<Q', len(dir_files))
            for name, e in dir_files.items():
                idx += _pw_string(name)
                idx += struct.pack('<i', ~id_to_idx[id(e)])

        index_plain = bytes(idx)
        new_sha1 = SHA1.new(index_plain).digest()

        if template_pak._pak_info.index_encrypted:
            try:
                key = PakCrypto.rsa_extract(template_pak._pak_info.packed_key, RSA_MOD_1)
                iv = PakCrypto.rsa_extract(template_pak._pak_info.packed_iv, RSA_MOD_1)
                if key and iv and len(key) == 32 and len(iv) >= 16:
                    aes = AES.new(key, MODE_CBC, iv[:16])
                    pad_len = (-len(index_plain)) % AES.block_size or AES.block_size
                    index_bytes = aes.encrypt(index_plain + bytes([pad_len] * pad_len))
                else:
                    index_bytes = index_plain
            except Exception:
                index_bytes = index_plain
        else:
            index_bytes = index_plain

        new_idx_offset = len(out_buf)
        new_idx_size = len(index_bytes)
        out_buf += index_bytes

        orig_fc = template_pak._file_content
        footer_sz = TencentPakInfo._mem_size(version)
        new_footer = bytearray(orig_fc[-footer_sz:])
        h_key = struct.pack('<5I', *keystream[4:9])
        new_footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
        new_footer[-16:-8] = ((new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little'))
        new_footer[-8:] = ((new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little'))
        out_buf += new_footer

        with open(output_pak, 'wb') as f:
            f.write(out_buf)

        console.print()
        console.print(Panel(
            f"[bold {BRIGHT_COLOR}]ARCHIVE FORGED SUCCESSFULLY![/bold {BRIGHT_COLOR}]\n\n"
            f"[bold {BRIGHT_COLOR}]Signature:[/]    [{TEXT_COLOR}]{selected_csv.name}[/{TEXT_COLOR}]\n"
            f"[bold {BRIGHT_COLOR}]Template:[/]     [{TEXT_COLOR}]{template_pak_path.name}[/{TEXT_COLOR}]\n"
            f"[bold {BRIGHT_COLOR}]Files Built:[/]  [bold {BRIGHT_COLOR}]{len(new_files)}[/]\n"
            f"[bold {BRIGHT_COLOR}]Output:[/]       [bold {BRIGHT_COLOR}]{output_pak}[/]\n"
            f"[bold {BRIGHT_COLOR}]Game:[/]         [bold {BRIGHT_COLOR}]{game_label}[/]",
            title=f"[bold black on {BRIGHT_COLOR}] FORGE COMPLETE [/]",
            border_style=BORDER_COLOR,
            box=DOUBLE_EDGE,
        ))

        try:
            TencentPakFile(output_pak, is_od=True)
            console.print(Panel(f"[bold {BRIGHT_COLOR}]VERIFICATION PASSED[/]",
                                border_style=BORDER_COLOR,
                                box=HEAVY_EDGE))
        except Exception as ve:
            console.print(Panel(f"[bold {WARNING}]Verify note: {ve}[/]",
                                border_style=WARNING,
                                box=HEAVY_EDGE))

    except Exception as e:
        console.print(Panel(f"[bold {ERROR}]Forge failed: {escape(str(e))}[/]",
                            border_style=ERROR,
                            box=HEAVY_EDGE))
        import traceback
        traceback.print_exc()

def repack_pak_file_full(pak_file, edited_root, output_path, target_path=None, force_add=False):
    import copy as _cp

    console.print(f'[bold {BRIGHT_COLOR}]Full Reconstruction Mode[/]')
    if target_path:
        console.print(f'[bold {BRIGHT_COLOR}]Target path: {target_path}[/]')

    edit_files = [p for p in Path(edited_root).rglob('*') if p.is_file()]
    if not edit_files:
        console.print(f'[bold {ERROR}]No files found in EDIT folder![/]')
        return 0
    console.print(f'[bold {BRIGHT_COLOR}]Found {len(edit_files)} files in EDIT folder[/]')

    version = pak_file._pak_info.version
    keystream = PakCrypto.zuc_keystream()
    orig_fc = pak_file._file_content
    mp_str, all_dirs = _get_all_dirs_and_mp(pak_file)

    if target_path and force_add:
        target_path = target_path.replace('\\', '/')
        matched_dir = None
        for existing_dir in all_dirs.keys():
            if existing_dir.strip('/').lower() == target_path.strip('/').lower():
                matched_dir = existing_dir
                break
        if matched_dir:
            target_path = matched_dir
        else:
            target_path = target_path.strip('/') + '/'

    pak_name_map = {}
    for dir_path, files in pak_file._index.items():
        for name, entry in files.items():
            full_path = str(PurePath(dir_path) / name).replace('\\', '/')
            pak_name_map.setdefault(name.lower(), []).append((full_path, entry))

    edited = {}
    for p in edit_files:
        fl = p.name.lower()
        found_match = False

        if fl in pak_name_map:
            cands = pak_name_map[fl]
            if target_path:
                target_candidates = [(fp, e) for fp, e in cands if target_path.strip('/') in fp]
                if target_candidates:
                    sz = p.stat().st_size
                    sm = [(fp, e) for fp, e in target_candidates if e.uncompressed_size == sz]
                    fp, ent = sm[0] if sm else target_candidates[0]
                    edited[fp] = (p, ent)
                    found_match = True

            if not found_match:
                sz = p.stat().st_size
                sm = [(fp, e) for fp, e in cands if e.uncompressed_size == sz]
                fp, ent = sm[0] if sm else cands[0]
                if target_path:
                    edited[f"{target_path.rstrip('/')}/{p.name}"] = (p, ent)
                else:
                    edited[fp] = (p, ent)
                found_match = True

        if not found_match:
            stem = p.stem.lower()
            ext = p.suffix.lower()
            for dir_path, files in pak_file._index.items():
                for name, entry in files.items():
                    if Path(name).stem.lower() == stem and Path(name).suffix.lower() == ext:
                        full_path = str(PurePath(dir_path) / name).replace('\\', '/')
                        if target_path:
                            edited[f"{target_path.rstrip('/')}/{p.name}"] = (p, entry)
                        else:
                            edited[full_path] = (p, entry)
                        found_match = True
                        break
                if found_match:
                    break

        if not found_match and force_add and target_path:
            template_entry = None
            for dir_path, files in pak_file._index.items():
                for name, entry in files.items():
                    if Path(name).suffix.lower() == p.suffix.lower():
                        template_entry = entry
                        break
                if template_entry:
                    break
            if not template_entry:
                for dir_path, files in pak_file._index.items():
                    for name, entry in files.items():
                        template_entry = entry
                        break
                    if template_entry:
                        break
            if template_entry:
                new_fp = f"{target_path.rstrip('/')}/{p.name}"
                edited[new_fp] = (p, template_entry)

    if not edited:
        console.print(f'[bold {ERROR}]No files to repack![/]')
        return 0
    console.print(f'  [bold {BRIGHT_COLOR}]Files to repack: {len(edited)}[/]')

    new_files = []
    for e in pak_file._files:
        ne = _cp.copy(e)
        ne.compressed_blocks = [_cp.copy(b) for b in e.compressed_blocks]
        new_files.append(ne)
    old_to_new = {id(pak_file._files[i]): new_files[i] for i in range(len(pak_file._files))}

    edited_paths = {fp: p for fp, (p, _) in edited.items()}
    out_buf = bytearray()

    for dp_str, dir_files in list(all_dirs.items()):
        for name, old_entry in list(dir_files.items()):
            full_path = str(PurePath(dp_str) / name).replace('\\', '/')
            ne = old_to_new.get(id(old_entry), None)
            if ne is None:
                ne = _cp.copy(old_entry)
                ne.compressed_blocks = [_cp.copy(b) for b in old_entry.compressed_blocks]
                new_files.append(ne)
                old_to_new[id(old_entry)] = ne

            em = old_entry.encryption_method
            cm = old_entry.compression_method

            if full_path in edited_paths:
                p, template = edited[full_path]
                new_raw = p.read_bytes()
                pak_rel = PurePath(full_path)

                fresh = _cp.copy(old_entry)
                fresh.compressed_blocks = []
                _write_entry_into_buf(out_buf, fresh, new_raw, pak_rel, old_entry, pak_file._zstd_dict)
                fresh.unk2 = SHA1.new((mp_str + full_path).lower().encode('utf-8')).digest()

                for i, e in enumerate(new_files):
                    if id(e) == id(old_to_new[id(old_entry)]):
                        new_files[i] = fresh
                        old_to_new[id(old_entry)] = fresh
                        break
                console.print(f'[bold {BRIGHT_COLOR}]Processed: {full_path}[/]')
            else:
                if cm == CM_NONE:
                    read_sz = (PakCrypto.align_encrypted_content_size(old_entry.size, em)
                               if old_entry.encrypted else old_entry.size)
                    ne.offset = len(out_buf)
                    out_buf += bytes(orig_fc[old_entry.offset: old_entry.offset + read_sz])
                elif old_entry.compressed_blocks:
                    new_blks = []
                    for ob in old_entry.compressed_blocks:
                        unc = ob.end - ob.start
                        enc = (PakCrypto.align_encrypted_content_size(unc, em)
                               if old_entry.encrypted else unc)
                        nb = PakCompressedBlock.__new__(PakCompressedBlock)
                        nb.start = len(out_buf)
                        nb.end = nb.start + unc
                        out_buf += bytes(orig_fc[ob.start: ob.start + enc])
                        new_blks.append(nb)
                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start

    if target_path and force_add:
        for fp, (p, template) in edited.items():
            already_processed = False
            for dp_str, dir_files in all_dirs.items():
                for name in dir_files.keys():
                    if str(PurePath(dp_str) / name).replace('\\', '/') == fp:
                        already_processed = True
                        break
                if already_processed:
                    break
            if not already_processed:
                ne = _cp.copy(template)
                ne.compressed_blocks = []
                new_raw = p.read_bytes()
                pak_rel = PurePath(fp)
                _write_entry_into_buf(out_buf, ne, new_raw, pak_rel, template, pak_file._zstd_dict)
                ne.unk2 = SHA1.new((mp_str + fp).lower().encode('utf-8')).digest()
                new_files.append(ne)
                if target_path not in all_dirs:
                    all_dirs[target_path] = {}
                all_dirs[target_path][p.name] = ne

    eidx = {id(new_files[i]): i for i in range(len(new_files))}
    old_id_to_new_idx = {id(pak_file._files[i]): i for i in range(len(pak_file._files))}

    idx = bytearray(_pw_string(mp_str))
    idx += struct.pack('<I', len(new_files))
    for ne in new_files:
        idx += _pw_entry(ne, version)
    idx += struct.pack('<Q', len(all_dirs))
    for dp_str, dir_files in all_dirs.items():
        idx += _pw_string(dp_str)
        idx += struct.pack('<Q', len(dir_files))
        for name, old_e in dir_files.items():
            idx += _pw_string(name)
            found_idx = eidx.get(id(old_e))
            if found_idx is None:
                found_idx = old_id_to_new_idx.get(id(old_e))
            if found_idx is None:
                copy_of = next((k for k, v in old_to_new.items() if v is old_e), None)
                if copy_of is not None:
                    found_idx = eidx.get(id(old_to_new[copy_of]))
            if found_idx is None:
                for i, e in enumerate(new_files):
                    if e.offset == old_e.offset and e.size == old_e.size:
                        found_idx = i
                        break
            if found_idx is not None:
                idx += struct.pack('<i', ~found_idx)
            else:
                idx += struct.pack('<i', -1)

    index_plain = bytes(idx)
    new_sha1 = SHA1.new(index_plain).digest()

    if pak_file._pak_info.index_encrypted:
        key = PakCrypto.rsa_extract(pak_file._pak_info.packed_key, RSA_MOD_1)
        iv = PakCrypto.rsa_extract(pak_file._pak_info.packed_iv, RSA_MOD_1)
        aes = AES.new(key, MODE_CBC, iv[:16])
        pad_len = (-len(index_plain)) % AES.block_size or AES.block_size
        index_bytes = aes.encrypt(index_plain + bytes([pad_len] * pad_len))
    else:
        index_bytes = index_plain

    new_idx_offset = len(out_buf)
    new_idx_size = len(index_bytes)
    out_buf += index_bytes

    footer_sz = TencentPakInfo._mem_size(version)
    new_footer = bytearray(orig_fc[-footer_sz:])
    h_key = struct.pack('<5I', *keystream[4:9])
    new_footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
    new_footer[-16:-8] = ((new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little'))
    new_footer[-8:] = ((new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little'))
    out_buf += new_footer

    with open(output_path, 'wb') as f:
        f.write(out_buf)
    return len(edited)

def repack_to_path_with_csv(pak_file, edit_dir, csv_dir, output_path):
    import copy as _cp

    if not download_csv_files(csv_dir):
        console.print(Panel(f"[bold {ERROR}]Signature sync failed![/]", border_style=ERROR, box=HEAVY_EDGE))
        return 0

    selected_csv, is_bgmi, game_label = _select_csv_source(csv_dir)
    if selected_csv is None:
        return 0

    console.print(f"[bold {BRIGHT_COLOR}]Loading {selected_csv.name}...[/]")
    file_path_map = _load_csv_path_map(selected_csv)
    if not file_path_map:
        console.print(Panel(f"[{ERROR}]Signature file empty![/]", border_style=ERROR))
        return 0
    console.print(f"[bold {BRIGHT_COLOR}]Loaded {len(file_path_map)} paths from {game_label}[/]")

    edit_files = [p for p in edit_dir.rglob('*') if p.is_file()]
    if not edit_files:
        console.print(Panel(f"[{ERROR}]No files in EDIT folder[/]", border_style=ERROR))
        return 0

    resolved_files, unresolved = _resolve_paths_from_csv(edit_dir, file_path_map, is_bgmi)
    if not resolved_files:
        console.print(Panel(f"[{ERROR}]No files matched signature![/]", border_style=ERROR, box=HEAVY_EDGE))
        return 0

    lines = [f"[bold {BRIGHT_COLOR}]Signature: {game_label} ({selected_csv.name})[/bold {BRIGHT_COLOR}]", ""]
    for p, rp in resolved_files:
        lines.append(f"  [bold {BRIGHT_COLOR}]✓[/] [{TEXT_COLOR}]{p.name}[/] [dim {DIM_COLOR}]→[/] [bold {BRIGHT_COLOR}]{rp}[/]")
    if unresolved:
        lines += ["", f"[bold {WARNING}] {len(unresolved)} unmatched:[/]"]
        for p in unresolved:
            lines.append(f"  [dim {WARNING}]x {p.name}[/dim {WARNING}]")
    lines.append("")
    lines.append(f"[bold {BRIGHT_COLOR}]Total: {len(resolved_files)} files[/bold {BRIGHT_COLOR}]")
    console.print(Panel("\n".join(lines), border_style=BORDER_COLOR, box=HEAVY_EDGE,
                        title=f"[bold black on {BRIGHT_COLOR}] PATH RESOLVER [/]"))

    confirm = console.input(f"\n[bold {BRIGHT_COLOR}]Proceed with inject? (y/n): [/bold {BRIGHT_COLOR}]").strip().lower()
    if confirm not in ('y', 'yes'):
        return 0

    mp_str, all_dirs = _get_all_dirs_and_mp(pak_file)
    version = pak_file._pak_info.version
    keystream = PakCrypto.zuc_keystream()
    orig_fc = pak_file._file_content

    pak_name_map = {}
    for dir_path, files in pak_file._index.items():
        for name, entry in files.items():
            full_path = str(PurePath(dir_path) / name).replace('\\', '/')
            pak_name_map.setdefault(name.lower(), []).append((full_path, entry))

    edited = {}
    for p, resolved_path in resolved_files:
        filename = p.name
        exact_entry = None
        actual_path = resolved_path

        for fp, entry in pak_name_map.get(filename.lower(), []):
            if fp.lower() == resolved_path.lower():
                exact_entry = entry
                actual_path = fp
                break

        if exact_entry is None:
            cands = pak_name_map.get(filename.lower(), [])
            if cands:
                actual_path, exact_entry = cands[0]

        if exact_entry is None:
            ext = p.suffix.lower()
            template = None
            for _dp, _files in pak_file._index.items():
                for _n, _e in _files.items():
                    if Path(_n).suffix.lower() == ext:
                        template = _e
                        break
                if template:
                    break
            if not template and pak_file._files:
                template = pak_file._files[0]
            if template:
                edited[actual_path] = (p, template, True)
        else:
            edited[actual_path] = (p, exact_entry, False)

    if not edited:
        console.print(Panel(f"[{ERROR}]No files to repack![/]", border_style=ERROR))
        return 0

    console.print(f"  [bold {BRIGHT_COLOR}]Files to repack: {len(edited)}[/]")

    new_files = []
    for e in pak_file._files:
        ne = _cp.copy(e)
        ne.compressed_blocks = [_cp.copy(b) for b in e.compressed_blocks]
        new_files.append(ne)
    old_to_new = {id(pak_file._files[i]): new_files[i] for i in range(len(pak_file._files))}

    existing_full_paths = set()
    for dp_str, dir_files in all_dirs.items():
        for name in dir_files.keys():
            full_path = str(PurePath(dp_str) / name).replace('\\', '/')
            existing_full_paths.add(full_path)

    out_buf = bytearray()

    for dp_str, dir_files in list(all_dirs.items()):
        for name, old_entry in list(dir_files.items()):
            full_path = str(PurePath(dp_str) / name).replace('\\', '/')
            ne = old_to_new.get(id(old_entry))
            if ne is None:
                ne = _cp.copy(old_entry)
                ne.compressed_blocks = [_cp.copy(b) for b in old_entry.compressed_blocks]
                new_files.append(ne)
                old_to_new[id(old_entry)] = ne

            if full_path in edited:
                p, template, is_new = edited[full_path]
                new_raw = p.read_bytes()
                pak_rel = PurePath(full_path)

                fresh = _cp.copy(old_entry)
                fresh.compressed_blocks = []

                _write_entry_into_buf(out_buf, fresh, new_raw, pak_rel, old_entry, pak_file._zstd_dict)
                fresh.unk2 = SHA1.new((mp_str + full_path).lower().encode('utf-8')).digest()

                for i, e in enumerate(new_files):
                    if id(e) == id(old_to_new[id(old_entry)]):
                        new_files[i] = fresh
                        old_to_new[id(old_entry)] = fresh
                        break

                console.print(f'[bold {BRIGHT_COLOR}]Replaced:[/] {full_path} [dim]({fresh.size} bytes)[/dim]')
            else:
                if old_entry.compression_method == CM_NONE:
                    read_sz = (PakCrypto.align_encrypted_content_size(old_entry.size, old_entry.encryption_method)
                               if old_entry.encrypted else old_entry.size)
                    ne.offset = len(out_buf)
                    out_buf += bytes(orig_fc[old_entry.offset: old_entry.offset + read_sz])
                elif old_entry.compressed_blocks:
                    new_blks = []
                    for ob in old_entry.compressed_blocks:
                        unc = ob.end - ob.start
                        enc = (PakCrypto.align_encrypted_content_size(unc, old_entry.encryption_method)
                               if old_entry.encrypted else unc)
                        nb = PakCompressedBlock.__new__(PakCompressedBlock)
                        nb.start = len(out_buf)
                        nb.end = nb.start + unc
                        out_buf += bytes(orig_fc[ob.start: ob.start + enc])
                        new_blks.append(nb)
                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start

    for resolved_path, (p, template, is_new) in edited.items():
        if resolved_path in existing_full_paths:
            continue

        ne = _cp.copy(template) if template else None
        if ne is None:
            continue
        ne.compressed_blocks = []
        new_raw = p.read_bytes()
        pak_rel = PurePath(resolved_path)

        _write_entry_into_buf(out_buf, ne, new_raw, pak_rel, template, pak_file._zstd_dict)
        ne.unk2 = SHA1.new((mp_str + resolved_path).lower().encode('utf-8')).digest()
        new_files.append(ne)

        dir_key = str(PurePath(resolved_path).parent).replace('\\', '/')
        if dir_key and not dir_key.endswith('/'):
            dir_key += '/'
        if dir_key == '.':
            dir_key = ''
        all_dirs.setdefault(dir_key, {})[p.name] = ne
        console.print(f'[bold {BRIGHT_COLOR}]Added new:[/] {resolved_path} [dim]({ne.size} bytes)[/dim]')

    eidx = {id(new_files[i]): i for i in range(len(new_files))}
    idx = bytearray(_pw_string(mp_str))
    idx += struct.pack('<I', len(new_files))
    for ne in new_files:
        idx += _pw_entry(ne, version)
    idx += struct.pack('<Q', len(all_dirs))
    for dp_str, dir_files in all_dirs.items():
        idx += _pw_string(dp_str)
        idx += struct.pack('<Q', len(dir_files))
        for name, old_e in dir_files.items():
            idx += _pw_string(name)
            found_idx = eidx.get(id(old_e))
            if found_idx is None:
                for i, e in enumerate(new_files):
                    if e.offset == old_e.offset and e.size == old_e.size:
                        found_idx = i
                        break
            idx += struct.pack('<i', ~found_idx if found_idx is not None else -1)

    index_plain = bytes(idx)
    new_sha1 = SHA1.new(index_plain).digest()

    if pak_file._pak_info.index_encrypted:
        key = PakCrypto.rsa_extract(pak_file._pak_info.packed_key, RSA_MOD_1)
        iv = PakCrypto.rsa_extract(pak_file._pak_info.packed_iv, RSA_MOD_1)
        aes = AES.new(key, MODE_CBC, iv[:16])
        pad_len = (-len(index_plain)) % AES.block_size or AES.block_size
        index_bytes = aes.encrypt(index_plain + bytes([pad_len] * pad_len))
    else:
        index_bytes = index_plain

    new_idx_offset = len(out_buf)
    new_idx_size = len(index_bytes)
    out_buf += index_bytes

    footer_sz = TencentPakInfo._mem_size(version)
    new_footer = bytearray(orig_fc[-footer_sz:])
    h_key = struct.pack('<5I', *keystream[4:9])
    new_footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
    new_footer[-16:-8] = ((new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little'))
    new_footer[-8:] = ((new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little'))
    out_buf += new_footer

    with open(output_path, 'wb') as f:
        f.write(out_buf)

    return len(edited)

def inject_edit_files(pak_file, edit_root, output_path, protect_new=False, sm4_type=47):
    import copy as _cp
    version = pak_file._pak_info.version

    edit_files = [p for p in Path(edit_root).rglob('*') if p.is_file()]
    if not edit_files:
        raise ValueError(f'No files found in EDIT folder: {edit_root}')

    mp_str, all_dirs = _get_all_dirs_and_mp(pak_file)

    injections = {}
    for p in edit_files:
        rel = p.relative_to(edit_root)
        parts = rel.parts
        file_name = parts[-1]
        rel_dir = '/'.join(parts[:-1]).replace('\\', '/')

        target_dir = _find_existing_dir(all_dirs, rel_dir) if rel_dir.strip('/') else ''
        if target_dir is None:
            target_dir = _normalize_dir_key(rel_dir)

        existing = None
        if target_dir in all_dirs:
            for name, e in list(all_dirs[target_dir].items()):
                if name.lower() == file_name.lower():
                    existing = (name, e)
                    break

        if existing:
            full_path = target_dir + existing[0]
            injections[full_path] = (p, existing[1], False)
        else:
            full_path = target_dir + file_name
            template = _pick_template(pak_file, all_dirs, target_dir, file_name)
            injections[full_path] = (p, template, True)

        console.print(f'  [bold {BRIGHT_COLOR}]>>[/] [white]{full_path}[/white]')

    new_files = []
    for e in pak_file._files:
        ne = _cp.copy(e)
        ne.compressed_blocks = [_cp.copy(b) for b in e.compressed_blocks]
        new_files.append(ne)
    old_to_new = {id(pak_file._files[i]): new_files[i] for i in range(len(pak_file._files))}

    out_buf = bytearray()
    edited_count = 0
    new_count = 0

    for dp_str, dir_files in list(all_dirs.items()):
        for name, old_entry in list(dir_files.items()):
            full_path = str(PurePath(dp_str) / name).replace('\\', '/')
            ne = old_to_new.get(id(old_entry), None)
            if ne is None:
                ne = _cp.copy(old_entry)
                ne.compressed_blocks = [_cp.copy(b) for b in old_entry.compressed_blocks]
                new_files.append(ne)
                old_to_new[id(old_entry)] = ne

            if full_path in injections:
                p, template, is_new = injections[full_path]
                new_raw = p.read_bytes()
                pak_rel = PurePath(full_path)

                fresh = _cp.copy(old_entry) if not is_new else (_cp.copy(template) if template else None)

                if fresh is None:
                    fresh = TencentPakEntry.__new__(TencentPakEntry)
                    fresh.content_hash = b'\x00' * 20
                    fresh.offset = 0
                    fresh.uncompressed_size = 0
                    fresh.compression_method = CM_NONE
                    fresh.size = 0
                    fresh.unk1 = 0
                    fresh.unk2 = b'\x00' * 20
                    fresh.compressed_blocks = []
                    fresh.compression_block_size = 0
                    fresh.encrypted = False
                    fresh.encryption_method = 0
                    fresh.index_new_sep = 0

                fresh.compressed_blocks = []
                if protect_new and is_new:
                    fresh.encryption_method = sm4_type
                    fresh.encrypted = True

                _write_entry_into_buf(out_buf, fresh, new_raw, pak_rel, fresh, pak_file._zstd_dict)
                fresh.unk2 = SHA1.new((mp_str + full_path).lower().encode('utf-8')).digest()

                if is_new:
                    new_files.append(fresh)
                    dp_key = full_path.rsplit('/', 1)[0] + '/' if '/' in full_path else ''
                    all_dirs.setdefault(dp_key, {})[full_path.rsplit('/', 1)[-1]] = fresh
                    new_count += 1
                else:
                    for i, e in enumerate(new_files):
                        if id(e) == id(old_to_new[id(old_entry)]):
                            new_files[i] = fresh
                            old_to_new[id(old_entry)] = fresh
                            break
                    edited_count += 1

                console.print(f'  [bold {BRIGHT_COLOR}]OK:[/] {full_path}')
            else:
                _copy_original_content(out_buf, pak_file, ne, old_entry)

    _write_pak_index_footer(pak_file, mp_str, all_dirs, new_files, old_to_new, out_buf, output_path)
    return edited_count, new_count

def protect_pak_file(pak_file, output_path, sm4_type=47):
    import copy as _cp
    version = pak_file._pak_info.version
    mp_str, all_dirs = _get_all_dirs_and_mp(pak_file)

    new_files = []
    for e in pak_file._files:
        ne = _cp.copy(e)
        ne.compressed_blocks = [_cp.copy(b) for b in e.compressed_blocks]
        new_files.append(ne)
    old_to_new = {id(pak_file._files[i]): new_files[i] for i in range(len(pak_file._files))}

    out_buf = bytearray()
    protected = 0
    skipped = 0

    for dp_str, dir_files in list(all_dirs.items()):
        for name, old_entry in list(dir_files.items()):
            full_path = str(PurePath(dp_str) / name).replace('\\', '/')
            ne = old_to_new.get(id(old_entry), None)
            if ne is None:
                ne = _cp.copy(old_entry)
                ne.compressed_blocks = [_cp.copy(b) for b in old_entry.compressed_blocks]
                new_files.append(ne)
                old_to_new[id(old_entry)] = ne

            is_marker = (old_entry.compression_method == CM_NONE and old_entry.size == 0)
            is_zdict = (pak_file._zstd_dict_entry is not None and old_entry is pak_file._zstd_dict_entry)

            if is_marker or is_zdict:
                _copy_original_content(out_buf, pak_file, ne, old_entry)
                skipped += 1
                continue

            try:
                plaintext = _extract_entry_plaintext(pak_file, old_entry, full_path)
            except Exception:
                _copy_original_content(out_buf, pak_file, ne, old_entry)
                skipped += 1
                console.print(f"  [bold {ERROR}]![/] Skipped: {full_path}")
                continue

            fresh = _cp.copy(old_entry)
            fresh.compressed_blocks = []
            fresh.encryption_method = sm4_type
            fresh.encrypted = True
            if fresh.compression_method == CM_NONE:
                fresh.compression_method = CM_ZLIB

            _write_entry_into_buf(out_buf, fresh, plaintext, PurePath(full_path), fresh, pak_file._zstd_dict)

            for i, e in enumerate(new_files):
                if id(e) == id(old_to_new[id(old_entry)]):
                    new_files[i] = fresh
                    old_to_new[id(old_entry)] = fresh
                    break

            protected += 1
            if protected <= 12 or protected % 250 == 0:
                console.print(f'  [bold {BRIGHT_COLOR}]LOCKED:[/] {full_path}')

    _write_pak_index_footer(pak_file, mp_str, all_dirs, new_files, old_to_new, out_buf, output_path)
    return protected, skipped

def _normalize_dir_key(path_str):
    s = str(path_str).replace('\\', '/').strip('/')
    return (s + '/') if s else ''

def _find_existing_dir(all_dirs, want_dir):
    want = _normalize_dir_key(want_dir).strip('/').lower()
    if not want:
        return ''
    for k in all_dirs:
        if k.strip('/').lower() == want:
            return k
    best = None
    for k in all_dirs:
        key = k.strip('/').lower()
        if key and want.endswith('/' + key):
            if best is None or len(key) > len(best):
                best = k
    return best

def _pick_template(pak_file, all_dirs, target_dir, file_name):
    ext = Path(file_name).suffix.lower()
    if target_dir in all_dirs:
        for name, e in all_dirs[target_dir].items():
            if Path(name).suffix.lower() == ext:
                return e
    for dp, files in all_dirs.items():
        for name, e in files.items():
            if Path(name).suffix.lower() == ext:
                return e
    for dp, files in all_dirs.items():
        for name, e in files.items():
            return e
    return pak_file._files[0] if pak_file._files else None

def _default_compression(pak_file):
    cm_counter = {}
    for e in pak_file._files:
        cm = e.compression_method
        if cm in (CM_ZLIB, CM_ZSTD, CM_ZSTD_DICT):
            cm_counter[cm] = cm_counter.get(cm, 0) + 1
    if pak_file._is_zstd_with_dict and cm_counter.get(CM_ZSTD_DICT, 0):
        return CM_ZSTD_DICT
    if cm_counter.get(CM_ZSTD, 0):
        return CM_ZSTD
    if cm_counter.get(CM_ZSTD_DICT, 0):
        return CM_ZSTD
    return CM_ZLIB

def _strip_mount_prefix(pak_file, rel_dir):
    mp = str(pak_file._mount_point).replace('\\', '/').strip('/')
    rd = str(rel_dir).replace('\\', '/').strip('/')
    if mp and (rd.lower() == mp.lower() or rd.lower().startswith(mp.lower() + '/')):
        return rd[len(mp):].lstrip('/')
    return rd

mini_BASE_DIR = ""
mini_MINI_ICON_DIR = ""
mini_INPUT_DIR = ""
mini_OUTPUT_DIR = ""
mini_TXTS_DIR = ""
mini_MODSKIN_FILE = ""
mini_CHANGELOG_PATH = ""
mini_NULL_TXT_PATH = ""
mini_NULLED_TXT_PATH = ""
mini_ALL_TXT_PATH = ""
mini_INDEX_FILE_PATH = ""
mini_AUTO_THEME_BASE = ""
mini_AUTO_THEME_FILES = ""
mini_AUTO_THEME_RESULT = ""
mini_AUTO_THEME_TXT = ""
mini_LOBBY_FILE = ""
mini_HIT_EFFECT_DIR = ""
mini_LOOTCRATES_DIR = ""
mini_HIT_ORIG = ""
mini_HIT_MODIFIED = ""
mini_LOOT_ORIG = ""
mini_LOOT_MODIFIED = ""
mini_HIT_TXT_PATH = ""
mini_changelog_entries = []
mini_modified_blocks_map = {}

def mini_clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def mini_display_tool_name():
    mini_clear_screen()
    try:
        width = os.get_terminal_size().columns
    except Exception:
        width = 80

    G = "\033[1;38;2;0;217;255m"
    D = "\033[38;2;124;124;138m"
    RESET = "\033[0m"

    banner_lines = [
        r"   _____ __ __  ____   _  __  ______ ____   ____   __ ",
        r"  / ___// //_/ /  _/  / |/ /  /_  __// __ \ / __ \ / / ",
        r"  \__ \/ ,<    / /   /  |/ /    / /  / / / // / / // /  ",
        r" ___/ / /| | _/ /   / /|  /    / /  / /_/ // /_/ // /___",
        r"/____/_/ |_|/___/  /_/ |_/    /_/   \____/ \____//_____/",
    ]

    for line in banner_lines:
        print((G + line + RESET).center(width))

    print()
    print((D + "              Premium Suite" + RESET).center(width))
    print()

def mini_load_all_skins_data():
    skins_by_id = {}
    if not os.path.exists(mini_ALL_TXT_PATH):
        print(f"{colorama.Fore.RED}ALL.txt not found at {mini_ALL_TXT_PATH}")
        return skins_by_id
    try:
        with open(mini_ALL_TXT_PATH, "r", encoding="utf-8", errors='ignore') as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 2:
                    skin_id = parts[0].strip()
                    hex_val = parts[1].strip().lower()
                    skin_name = parts[2].strip() if len(parts) >= 3 else ""
                    skins_by_id[skin_id] = {'hex': hex_val, 'name': skin_name}
    except Exception as e:
        print(f"{colorama.Fore.RED}Error loading ALL.txt: {e}")
    return skins_by_id

def mini_load_index_data():
    index_data = {}
    if not os.path.exists(mini_INDEX_FILE_PATH):
        print(f"{colorama.Fore.YELLOW}index.txt not found at {mini_INDEX_FILE_PATH}")
        return index_data
    try:
        with open(mini_INDEX_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    name = parts[2].strip()
                    index_hex = parts[3].strip().lower()
                    index_data.setdefault(name, []).append(index_hex)
    except Exception as e:
        print(f"{colorama.Fore.RED}Error loading index.txt: {e}")
    return index_data

def mini_load_modskin_pairs():
    pairs = []
    if not os.path.exists(mini_MODSKIN_FILE):
        print(f"{colorama.Fore.RED}modskin.txt not found at {mini_MODSKIN_FILE}")
        return pairs
    try:
        with open(mini_MODSKIN_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = _ptre.split(r'[,\s\->]+', line)
                if len(parts) >= 2:
                    pairs.append((parts[0].strip(), parts[1].strip()))
    except Exception as e:
        print(f"{colorama.Fore.RED}Error loading modskin.txt: {e}")
    return pairs

def mini_mark_block_as_modified(file_path, byte_offset):
    block_idx = byte_offset // mini_BLOCK_SIZE
    if file_path not in mini_modified_blocks_map:
        mini_modified_blocks_map[file_path] = set()
    mini_modified_blocks_map[file_path].add(block_idx)
    if block_idx > 0:
        mini_modified_blocks_map[file_path].add(block_idx - 1)
    mini_modified_blocks_map[file_path].add(block_idx + 1)

def mini_write_changelog():
    os.makedirs(mini_OUTPUT_DIR, exist_ok=True)
    try:
        with open(mini_CHANGELOG_PATH, "w", encoding="utf-8") as f:
            f.write("Premium Studio Changelog\n")
            f.write("==============================\n\n")
            for idx, entry in enumerate(mini_changelog_entries, 1):
                f.write("==============================\n")
                f.write(f"{idx}. ID PAIR: {entry['id_pair']}\n")
                f.write(f"FILE NAME: {entry['file_name']}\n")
                f.write(f"Source Item: {entry['source_item']}\n")
                f.write(f"Target Item: {entry['target_item']}\n")
                f.write(f"CHANGED HEX FROM: {entry['source_hex']} TO: {entry['target_hex']}\n")
                if entry.get('index_occurrences', 0) > 0:
                    f.write(f"INDEX CHANGED FROM: {entry['source_index']} TO: {entry['target_index']} ({entry['index_occurrences']} occurrence(s))\n")
                elif entry.get('index_failure_reason'):
                    f.write(f"Index replacement note: {entry['index_failure_reason']}\n")
                f.write("==============================\n\n")
    except Exception:
        pass

def mini_remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def mini_copy_files_to_output():
    print(f"\n{colorama.Fore.CYAN}Step 1: Syncing source assets to staging...")

    if not os.path.exists(mini_INPUT_DIR):
        print(f"{colorama.Fore.RED}INPUT directory not found: {mini_INPUT_DIR}")
        return False

    if os.path.exists(mini_OUTPUT_DIR):
        try:
            shutil.rmtree(mini_OUTPUT_DIR, onerror=mini_remove_readonly)
        except Exception as e:
            print(f"{colorama.Fore.RED}Error cleaning OUTPUT: {e}")
            return False

    try:
        shutil.copytree(mini_INPUT_DIR, mini_OUTPUT_DIR)
        file_count = sum(len(files) for _, _, files in os.walk(mini_OUTPUT_DIR))
        print(f"{colorama.Fore.GREEN}Synced {file_count} files to staging directory")
        return True
    except Exception as e:
        print(f"{colorama.Fore.RED}Error copying files: {e}")
        return False

def mini_process_mod_skin():
    global mini_modified_blocks_map
    mini_modified_blocks_map = {}

    print(f"\n{colorama.Fore.LIGHTBLUE_EX}Step 2: Applying aesthetic replacements...")

    mode_str = "REPLACE (One-Way)"
    print(f"{colorama.Fore.CYAN}Mode: {colorama.Fore.LIGHTGREEN_EX}{mode_str} [AUTO SELECTED]")

    skins_data = mini_load_all_skins_data()
    index_data = mini_load_index_data()
    id_pairs = mini_load_modskin_pairs()

    if not id_pairs:
        print(f"{colorama.Fore.RED}No ID pairs found in modskin.txt")
        return

    print(f"{colorama.Fore.LIGHTGREEN_EX}Found {len(id_pairs)} ID pairs to process")

    resolved_ops = []
    missing_ids = set()

    for s_id, t_id in id_pairs:
        if s_id not in skins_data:
            missing_ids.add(s_id)
            continue
        if t_id not in skins_data:
            missing_ids.add(t_id)
            continue

        s_hex = skins_data[s_id]['hex']
        s_name = skins_data[s_id]['name']
        t_hex = skins_data[t_id]['hex']
        t_name = skins_data[t_id]['name']

        resolved_ops.append({
            'search_hex': t_hex,
            'replace_hex': s_hex,
            'search_name': t_name,
            'replace_name': s_name,
            'label': f"{s_id} -> {t_id}",
            'op_type': "REPLACE"
        })

    if missing_ids:
        print(f"{colorama.Fore.LIGHTBLUE_EX}Warning: {len(missing_ids)} IDs not found in ALL.txt")

    if not resolved_ops:
        print(f"{colorama.Fore.RED}Empty operational queue. Nothing to process.")
        return

    modified_files = 0

    for root, dirs, files in os.walk(mini_OUTPUT_DIR):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.lower().endswith('.txt'):
                continue

            try:
                with open(file_path, 'rb') as f:
                    content_bytes = f.read()
            except Exception:
                continue

            hex_data = content_bytes.hex()
            file_modified = False

            for op in resolved_ops:
                s_hex = op['search_hex']
                r_hex = op['replace_hex']
                s_name = op['search_name']
                r_name = op['replace_name']

                if s_hex not in hex_data:
                    continue

                occ = hex_data.count(s_hex)
                if occ >= 2:
                    first_pos = hex_data.find(s_hex)
                    second_pos = hex_data.find(s_hex, first_pos + len(s_hex))

                    if second_pos != -1:
                        hex_data = hex_data[:second_pos] + r_hex + hex_data[second_pos + len(s_hex):]
                        file_modified = True
                        mini_mark_block_as_modified(file_path, second_pos // 2)

                        idx_occ = 0
                        idx_reason = ""
                        mod_idx_from = "N/A"
                        mod_idx_to = "N/A"

                        if s_name in index_data and r_name in index_data:
                            search_candidates = index_data[s_name]
                            replacement_index = index_data[r_name][0]
                            window_start = max(0, first_pos - 60)
                            window = hex_data[window_start:first_pos]
                            found = False

                            for candidate in search_candidates:
                                if candidate in window:
                                    mod_idx_from = candidate
                                    mod_idx_to = replacement_index
                                    window_replaced = window.replace(candidate, replacement_index, 1)
                                    local_idx = window.find(candidate)
                                    real_idx = window_start + local_idx
                                    hex_data = hex_data[:window_start] + window_replaced + hex_data[first_pos:]
                                    idx_occ = 1
                                    found = True
                                    mini_mark_block_as_modified(file_path, real_idx // 2)
                                    break

                            if not found:
                                idx_reason = "Index hex not found in window"
                        else:
                            idx_reason = "Index names missing"

                        rel_path = os.path.relpath(file_path, mini_OUTPUT_DIR)
                        mini_changelog_entries.append({
                            'id_pair': f"{op['label']} ({op['op_type']})",
                            'file_name': rel_path,
                            'source_item': f"{s_name} [Found]",
                            'target_item': f"{r_name} [Applied]",
                            'source_hex': s_hex,
                            'target_hex': r_hex,
                            'source_index': mod_idx_from,
                            'target_index': mod_idx_to,
                            'index_occurrences': idx_occ,
                            'index_failure_reason': idx_reason
                        })

            if file_modified:
                try:
                    with open(file_path, 'wb') as f:
                        f.write(bytes.fromhex(hex_data))
                    modified_files += 1
                except Exception:
                    pass

    print(f"{colorama.Fore.LIGHTGREEN_EX}Modified {modified_files} files")

def mini_build_pattern_groups(hex_list):
    groups = {}
    for hx in hex_list:
        try:
            b = bytes.fromhex(hx)
        except ValueError:
            continue
        if not b:
            continue
        groups.setdefault(len(b), set()).add(b)
    return groups

def mini_null_bytes_in_file(file_path, pattern_groups, dirty_blocks, target_counts={2}):
    try:
        data = Path(file_path).read_bytes()
    except Exception:
        return 0

    ba = bytearray(data)
    total_hits = 0
    modified = False
    file_size = len(ba)

    for block_idx in dirty_blocks:
        start_offset = block_idx * mini_BLOCK_SIZE
        if start_offset >= file_size:
            continue
        end_offset = min(start_offset + mini_BLOCK_SIZE, file_size)
        block_len = end_offset - start_offset
        block_mv = memoryview(ba)[start_offset:end_offset]

        for L, patterns in pattern_groups.items():
            if L <= 0 or block_len < L:
                continue
            zero = b"\x00" * L
            occurrences = {}
            i = 0
            end = block_len - L

            while i <= end:
                chunk = bytes(block_mv[i:i + L])
                if chunk in patterns:
                    if chunk not in occurrences:
                        occurrences[chunk] = []
                    occurrences[chunk].append(i)
                    i += L
                else:
                    i += 1

            for pat, positions in occurrences.items():
                count = len(positions)
                if count in target_counts:
                    for pos in positions:
                        abs_pos = start_offset + pos
                        ba[abs_pos:abs_pos + L] = zero
                    total_hits += count
                    modified = True

    if modified:
        Path(file_path).write_bytes(ba)
    return total_hits

def mini_process_size_fix():
    skins_data = mini_load_all_skins_data()
    if not skins_data:
        return

    protected_ids = set()
    protected_hexes_from_ids = set()

    if os.path.exists(mini_MODSKIN_FILE):
        try:
            with open(mini_MODSKIN_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = _ptre.split(r'[,\s\->]+', line)
                    for part in parts:
                        part = part.strip()
                        if part:
                            protected_ids.add(part)
        except Exception:
            pass

    for skin_id in protected_ids:
        if skin_id in skins_data:
            protected_hex = skins_data[skin_id]['hex']
            protected_hexes_from_ids.add(protected_hex.lower())

    valid_entries = []
    exclude_keywords = {"face", "hair", "head", "male", "female"}

    for skin_id, info in skins_data.items():
        hex_code = info['hex']
        skin_name = info['name'].lower()
        if skin_id in protected_ids:
            continue
        if any(keyword in skin_name for keyword in exclude_keywords):
            continue
        if "0000" in hex_code:
            continue
        valid_entries.append((hex_code, skin_name))

    exclude_hexes = set()
    for entry in mini_changelog_entries:
        exclude_hexes.add(entry.get('source_hex', '').lower())
        exclude_hexes.add(entry.get('target_hex', '').lower())
        if entry.get('source_index', "N/A") != "N/A":
            exclude_hexes.add(entry['source_index'].lower())
        if entry.get('target_index', "N/A") != "N/A":
            exclude_hexes.add(entry['target_index'].lower())

    exclude_hexes.update(protected_hexes_from_ids)

    print(f"{colorama.Fore.CYAN}Nulling Mode: {colorama.Fore.LIGHTGREEN_EX}AUTO NULL SYSTEM [AUTO SELECTED]")

    target_counts = {2}
    final_hexes = []
    for hx, name in valid_entries:
        if hx in exclude_hexes:
            continue
        final_hexes.append(hx)

    pattern_groups = mini_build_pattern_groups(final_hexes)

    files_to_process = []
    for root, dirs, files in os.walk(mini_OUTPUT_DIR):
        for file_name in files:
            if not file_name.lower().endswith('.txt'):
                files_to_process.append(os.path.join(root, file_name))

    total_nulled = 0
    files_modified = 0

    with console.status("[bold cyan]Scanning and Nulling Hex values...[/]", spinner="dots"):
        for file_path in files_to_process:
            dirty_blocks = mini_modified_blocks_map.get(file_path, set())
            if not dirty_blocks:
                continue
            hits = mini_null_bytes_in_file(file_path, pattern_groups, dirty_blocks, target_counts)
            if hits > 0:
                files_modified += 1
                total_nulled += hits

    print()
    try:
        with open(mini_NULLED_TXT_PATH, 'w', encoding='utf-8') as f:
            f.write("Nulled Hex Values Report\n========================\n")
            f.write(f"Files modified: {files_modified}\n")
            f.write(f"Unique hex values nulled: {len(final_hexes)}\n")
            f.write(f"Total occurrences replaced: {total_nulled}\n")
    except Exception:
        pass

    print(f"{colorama.Fore.LIGHTGREEN_EX}Size fix processing complete.")

def mini_run_hit_loot_tool():
    mini_display_tool_name()

    zsdic_console.print(Panel(
        f"[bold {BRIGHT_COLOR}]IMPACT & CRATE STUDIO[/bold {BRIGHT_COLOR}]\n"
        f"[dim]ID pairs from modskin.txt | Files from MINI[/dim]",
        border_style=BORDER_COLOR,
        box=HEAVY_EDGE
    ))

    global game_key, mini_BASE_DIR

    if 'game_key' not in globals() or game_key not in ["BGMI", "PUBG"]:
        game_key = "BGMI"

    game_folder = f"{game_key}_SKIN"
    game_base = os.path.join("PSYCO TOOL", "SKIN_TOOL", game_folder)

    zsdic_base = os.path.join(game_base, "ZSDIC")
    zsdic_modskin = os.path.join(zsdic_base, "modskin.txt")

    mini_base = os.path.join(game_base, "MINI")
    mini_icon = os.path.join(mini_base, "MINI_ICON")
    mini_txts = os.path.join(mini_icon, "TXTS")
    mini_all = os.path.join(mini_txts, "ALL.txt")

    mini_HIT_ORIG = os.path.join(mini_base, "HIT EFFECT", "org")
    mini_HIT_MODIFIED = os.path.join(mini_base, "HIT EFFECT", "modified")
    mini_LOOT_ORIG = os.path.join(mini_base, "LOOTCRATES", "org")
    mini_LOOT_MODIFIED = os.path.join(mini_base, "LOOTCRATES", "modified")

    if not os.path.exists(mini_all):
        zsdic_console.print(Panel(
            f"[red]ALL.txt not found![/red]\n"
            f"[dim]Expected: {mini_all}[/dim]",
            border_style=ERROR,
            box=ROUNDED
        ))
        return

    id_pairs = []

    if os.path.exists(zsdic_modskin):
        with open(zsdic_modskin, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = _ptre.split(r'[,\s]+', line.strip())
                if len(parts) >= 2:
                    id_pairs.append((parts[0].strip(), parts[1].strip()))

        zsdic_console.print(Panel(
            f"[bold {BRIGHT_COLOR}]Loaded {len(id_pairs)} pairs from modskin.txt[/bold {BRIGHT_COLOR}]",
            border_style=BORDER_COLOR,
            box=ROUNDED
        ))
    else:
        zsdic_console.print(Panel(
            f"[red]modskin.txt not found![/red]",
            border_style=ERROR,
            box=ROUNDED
        ))
        return

    if not id_pairs:
        zsdic_console.print(Panel(
            f"[{WARNING}]No ID pairs found in modskin.txt[/]",
            border_style=WARNING,
            box=ROUNDED
        ))
        return

    id_to_entry = {}
    by_name = {}

    with open(mini_all, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                idv = parts[0].strip()
                hx = parts[1].strip().lower()
                name = parts[2].strip()
                id_to_entry[idv] = {"hex": hx, "name": name, "base": name}
                by_name.setdefault(name, {})[0] = hx

    zsdic_console.print(Panel(
        f"[bold {BRIGHT_COLOR}]Loaded {len(id_to_entry)} entries from ALL.txt[/bold {BRIGHT_COLOR}]",
        border_style=BORDER_COLOR,
        box=ROUNDED
    ))

    pairs_hit, pairs_loot = [], []

    for a_raw, b_raw in id_pairs:
        if a_raw not in id_to_entry:
            continue

        first_hex = id_to_entry[a_raw]["hex"]

        if b_raw in id_to_entry:
            hit_hex = id_to_entry[b_raw]["hex"]
            loot_hex = id_to_entry[b_raw]["hex"]
        else:
            hit_hex = b_raw
            loot_hex = b_raw

        pairs_hit.append((first_hex, hit_hex))
        if len(first_hex) == len(loot_hex):
            pairs_loot.append((first_hex, loot_hex))

    with Live(refresh_per_second=30, console=zsdic_console) as live:
        for i in range(101):
            if i % 5 == 0:
                bar_length = 30
                filled = int((i / 100) * bar_length)
                bar = "█" * filled + "░" * (bar_length - filled)

                progress_text = (
                    f"[bold {BRIGHT_COLOR}]Processing...[/bold {BRIGHT_COLOR}]\n\n"
                    f"[bold {BRIGHT_COLOR}]{bar}[/] [bold {TEXT_COLOR}]{i}%[/bold {TEXT_COLOR}]\n"
                    f"[dim]{i}% complete[/dim]"
                )

                live.update(Panel(
                    progress_text,
                    title=f"[bold black on {BRIGHT_COLOR}] PROCESSING [/]",
                    border_style=BORDER_COLOR,
                    box=HEAVY_EDGE
                ))
            time.sleep(0.02)

    for path in [mini_HIT_MODIFIED, mini_LOOT_MODIFIED]:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception:
                pass
        os.makedirs(path, exist_ok=True)

    def process_files(orig_dir, mod_dir, pairs):
        if not os.path.exists(orig_dir):
            return 0

        files = []
        for r, _, fs in os.walk(orig_dir):
            for fn in fs:
                files.append(os.path.join(r, fn))

        if not files:
            return 0

        count = 0
        for src in files:
            try:
                with open(src, 'rb') as fh:
                    data = fh.read()
            except Exception:
                continue

            orig = data
            for first_hex, second_hex in pairs:
                try:
                    to_b = bytes.fromhex(second_hex)
                    from_raw = bytes.fromhex(first_hex)
                except Exception:
                    continue

                if len(from_raw) < len(to_b):
                    replacement = from_raw + b'\x00' * (len(to_b) - len(from_raw))
                elif len(from_raw) > len(to_b):
                    replacement = from_raw[:len(to_b)]
                else:
                    replacement = from_raw

                if data.count(to_b):
                    data = data.replace(to_b, replacement)
                if data.count(to_b[::-1]):
                    data = data.replace(to_b[::-1], replacement[::-1])

            if data != orig:
                rel = os.path.relpath(src, orig_dir)
                outp = os.path.join(mod_dir, rel)
                os.makedirs(os.path.dirname(outp), exist_ok=True)
                with open(outp, 'wb') as outfh:
                    outfh.write(data)
                count += 1

        return count

    hit_count = process_files(mini_HIT_ORIG, mini_HIT_MODIFIED, pairs_hit)
    loot_count = process_files(mini_LOOT_ORIG, mini_LOOT_MODIFIED, pairs_loot)

    zsdic_console.print(Panel(
        f"[bold {BRIGHT_COLOR}]Modified {hit_count} HIT files & {loot_count} LOOT files.[/bold {BRIGHT_COLOR}]",
        border_style=BORDER_COLOR,
        box=HEAVY_EDGE
    ))

def mini_run_auto_theme():
    DEFAULT_HEX = "7480100C"

    while True:
        mini_display_tool_name()

        menu_table = Table(show_header=False, box=SIMPLE, expand=True)
        menu_table.add_column("OPT", style=f"bold {BRIGHT_COLOR}", justify="center", width=4)
        menu_table.add_column("COMMAND", style=f"bold {BRIGHT_COLOR}")

        menu_table.add_row("1", f"[bold {BRIGHT_COLOR}]SWAP LOBBY INDEX[/]")
        menu_table.add_row("2", f"[bold {ERROR}]BACK TO MAIN MENU[/]")

        console.print(Panel(
            menu_table,
            border_style=BORDER_COLOR,
            box=HEAVY_EDGE,
            title=f"[bold black on {BRIGHT_COLOR}] ATMOSPHERE DESIGNER [/]"
        ))

        choice = safe_input(f"[bold {BRIGHT_COLOR}]ENTER COMMAND > [/bold {BRIGHT_COLOR}]").strip()

        if choice == "1":
            lobbies = []
            try:
                with open(mini_LOBBY_FILE, "r") as file:
                    for line in file:
                        parts = line.strip().split("|")
                        if len(parts) == 3:
                            lobbies.append((parts[1].strip(), parts[2].strip()))
            except FileNotFoundError:
                pass

            if not lobbies:
                console.print(f"[red]lobby.txt not found or empty.[/red]")
                time.sleep(1)
                continue

            console.print(f"\n[bold {BRIGHT_COLOR}]-- AVAILABLE ATMOSPHERES --[/bold {BRIGHT_COLOR}]\n")
            for i, (_, name) in enumerate(lobbies, 1):
                console.print(f"[bold {TEXT_COLOR}]{i:02d}.[/] [bold {BRIGHT_COLOR}]{name}[/]")

            lobby_choice = safe_input(f"\n[bold {BRIGHT_COLOR}]Select an atmosphere theme ID[/bold {BRIGHT_COLOR}]")
            try:
                lobby_idx = int(lobby_choice) - 1
                if 0 <= lobby_idx < len(lobbies):
                    target_hex, lobby_name = lobbies[lobby_idx]

                    with console.status(f"[bold {BRIGHT_COLOR}]Applying {lobby_name} theme...[/]"):
                        default_hex_bytes = bytes.fromhex(DEFAULT_HEX)
                        target_hex_bytes = bytes.fromhex(target_hex)
                        for filename in os.listdir(mini_AUTO_THEME_FILES):
                            file_path = os.path.join(mini_AUTO_THEME_FILES, filename)
                            with open(file_path, "rb") as file:
                                file_data = file.read()
                            updated_data = bytearray(file_data)

                            default_pos = target_pos = None
                            for i in range(len(file_data) - len(default_hex_bytes), 7, -1):
                                if file_data[i:i + len(default_hex_bytes)] == default_hex_bytes:
                                    default_index = file_data[i - 8]
                                    default_pos = i - 8
                                    break
                            for i in range(len(file_data) - len(target_hex_bytes), 7, -1):
                                if file_data[i:i + len(target_hex_bytes)] == target_hex_bytes:
                                    target_index = file_data[i - 8]
                                    target_pos = i - 8
                                    break

                            if default_pos is not None and target_pos is not None:
                                updated_data[default_pos] = target_index
                                updated_data[target_pos] = default_index
                                result_path = os.path.join(mini_AUTO_THEME_RESULT, filename)
                                os.makedirs(mini_AUTO_THEME_RESULT, exist_ok=True)
                                with open(result_path, "wb") as file:
                                    file.write(updated_data)

                    console.print(f"[bold {BRIGHT_COLOR}]SUCCESS: Atmosphere Swap Applied![/]")
                else:
                    console.print(f"[red]Invalid ID.[/red]")
            except ValueError:
                console.print(f"[red]Invalid input.[/red]")
        elif choice == "2":
            break
        time.sleep(1)

def mini_full_flow():
    console.print(Panel(
        f"[bold {BRIGHT_COLOR}]AESTHETIC STUDIO MASTER ENGINE[/bold {BRIGHT_COLOR}]\n\n"
        f"[bold {TEXT_COLOR}]M A S T E R   A U T O M A T E D   P I P E L I N E[/bold {TEXT_COLOR}]\n"
        f"[dim {DIM_COLOR}]----------------------------------------------[/dim {DIM_COLOR}]\n"
        f"[bold {TEXT_COLOR}]Pipeline Status : [bold {BRIGHT_COLOR}]READY FOR EXECUTION[/][/bold {TEXT_COLOR}]",
        expand=True,
        border_style=BORDER_COLOR,
        box=HEAVY_EDGE,
        padding=(1, 2),
        title=f"[bold black on {BRIGHT_COLOR}] MASTER ENGINE INITIALIZED [/]",
        title_align="center"
    ))

    if not mini_copy_files_to_output():
        console.print(Panel(f"[bold {ERROR}]SYNC FAILED[/]", border_style=ERROR, expand=True))
        return

    mini_process_mod_skin()
    mini_write_changelog()
    mini_process_size_fix()

    console.print(Panel(
        f"[bold {BRIGHT_COLOR}]MASTER PIPELINE EXECUTED SUCCESSFULLY![/]\n\n"
        f"  [dim {DIM_COLOR}]* Pipeline Status      :[/dim {DIM_COLOR}] [bold {BRIGHT_COLOR}]SYSTEM FULLY OPTIMIZED[/]\n"
        f"  [dim {DIM_COLOR}]* Asset Verification   :[/dim {DIM_COLOR}] [bold {TEXT_COLOR}]ALL ASSETS VERIFIED & PATCHED[/]",
        border_style=BORDER_COLOR,
        box=HEAVY_EDGE,
        expand=True,
        title=f"[bold black on {BRIGHT_COLOR}] EXECUTION COMPLETED [/]",
        padding=(1, 2)
    ))

    safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter to continue...[/]")

def mini_menu():
    while True:
        mini_display_tool_name()
        b_color = BRIGHT_COLOR

        menu_table = Table(
            show_header=True,
            header_style=f"bold black on {BRIGHT_COLOR}",
            box=DOUBLE_EDGE,
            title="[reverse]  AESTHETIC STUDIO  [/]",
            border_style=BORDER_COLOR,
            expand=True
        )
        menu_table.add_column("OPT", justify="center", style=f"bold {BRIGHT_COLOR}", width=4)
        menu_table.add_column("COMMAND", style=f"bold {TEXT_COLOR}")
        menu_table.add_column("DESCRIPTION", style=f"dim {DIM_COLOR}")

        menu_table.add_row(
            "1",
            f"[bold {BRIGHT_COLOR}]MOD SKIN & SIZE FIX[/]",
            f"[dim]VIP Mod Skin & Size Fix[/dim]"
        )
        menu_table.add_row(
            "2",
            f"[bold {BRIGHT_COLOR}]IMPACT & CRATE STUDIO[/]",
            f"[dim]Customize impacts & crates[/dim]"
        )
        menu_table.add_row(
            "3",
            f"[bold {BRIGHT_COLOR}]ATMOSPHERE DESIGNER[/]",
            f"[dim]Swap lobby index theme[/dim]"
        )
        menu_table.add_row(
            "0",
            f"[bold {ERROR}]BACK[/]",
            f"[dim]Return to Main Menu[/dim]"
        )

        console.print(Panel(menu_table, border_style=BORDER_COLOR, box=HEAVY_EDGE))

        choice = safe_input(f"[bold {BRIGHT_COLOR}]ENTER COMMAND > [/bold {BRIGHT_COLOR}]").strip()

        if choice == "1":
            mini_full_flow()
        elif choice == "2":
            mini_run_hit_loot_tool()
            safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter to continue...[/]")
        elif choice == "3":
            mini_run_auto_theme()
        elif choice == "0":
            break
        else:
            console.print(f"[bold {ERROR}]Invalid! Enter 0, 1, 2, or 3[/]")
            time.sleep(1)

def mini_skin_tool_main(data_path):
    global mini_BASE_DIR, mini_MINI_ICON_DIR, mini_INPUT_DIR, mini_OUTPUT_DIR
    global mini_TXTS_DIR, mini_MODSKIN_FILE, mini_CHANGELOG_PATH
    global mini_NULL_TXT_PATH, mini_NULLED_TXT_PATH, mini_ALL_TXT_PATH
    global mini_INDEX_FILE_PATH, mini_AUTO_THEME_BASE, mini_AUTO_THEME_FILES
    global mini_AUTO_THEME_RESULT, mini_AUTO_THEME_TXT, mini_LOBBY_FILE
    global mini_HIT_EFFECT_DIR, mini_LOOTCRATES_DIR, mini_HIT_ORIG
    global mini_HIT_MODIFIED, mini_LOOT_ORIG, mini_LOOT_MODIFIED
    global mini_HIT_TXT_PATH, game_key

    while True:
        mini_clear_screen()
        print_banner()

        select_table = Table(
            show_header=True,
            header_style=f"bold black on {BRIGHT_COLOR}",
            box=DOUBLE_EDGE,
            title="[reverse]  SELECT TARGET PROFILE  [/]",
            border_style=BORDER_COLOR,
            expand=True
        )
        select_table.add_column("OPT", justify="center", style=f"bold {BRIGHT_COLOR}", width=4)
        select_table.add_column("GAME", style=f"bold {TEXT_COLOR}")
        select_table.add_column("DESCRIPTION", style=f"dim {DIM_COLOR}")
        select_table.add_row("1", "BGMI_SKIN", "Aesthetic BGMI profiles")
        select_table.add_row("2", "PUBG_SKIN", "Aesthetic PUBG profiles")
        select_table.add_row("0", f"[{ERROR}]BACK[/]", "Return")
        console.print(Panel(select_table, border_style=BORDER_COLOR, box=HEAVY_EDGE))

        game_choice = safe_input(f"[bold {BRIGHT_COLOR}]SELECT (1/2/0) > [/bold {BRIGHT_COLOR}]").strip()

        if game_choice == "0":
            return
        if game_choice not in ("1", "2"):
            console.print(f"[bold {ERROR}]Invalid![/]")
            time.sleep(1)
            continue

        selected_game = "BGMI_SKIN" if game_choice == "1" else "PUBG_SKIN"
        game_key = "BGMI" if game_choice == "1" else "PUBG"
        GAME_BASE = data_path / "SKIN_TOOL" / selected_game

        mini_BASE_DIR = str(GAME_BASE / "MINI")
        mini_MINI_ICON_DIR = str(Path(mini_BASE_DIR) / "MINI_ICON")
        mini_INPUT_DIR = str(Path(mini_MINI_ICON_DIR) / "INPUT")
        mini_OUTPUT_DIR = str(Path(mini_MINI_ICON_DIR) / "OUTPUT")
        mini_TXTS_DIR = str(Path(mini_MINI_ICON_DIR) / "TXTS")
        mini_MODSKIN_FILE = str(Path(mini_BASE_DIR) / "modskin.txt")
        mini_CHANGELOG_PATH = str(Path(mini_BASE_DIR) / "changelog.txt")
        mini_NULL_TXT_PATH = str(Path(mini_TXTS_DIR) / "null.txt")
        mini_NULLED_TXT_PATH = str(Path(mini_BASE_DIR) / "nulled.txt")
        mini_ALL_TXT_PATH = str(Path(mini_TXTS_DIR) / "ALL.txt")
        mini_INDEX_FILE_PATH = str(Path(mini_TXTS_DIR) / "index.txt")
        mini_AUTO_THEME_BASE = str(Path(mini_BASE_DIR) / "AUTO_THEME")
        mini_AUTO_THEME_FILES = str(Path(mini_AUTO_THEME_BASE) / "FILES")
        mini_AUTO_THEME_RESULT = str(Path(mini_AUTO_THEME_BASE) / "MODIFIED")
        mini_AUTO_THEME_TXT = str(Path(mini_AUTO_THEME_BASE) / "TXT")
        mini_LOBBY_FILE = str(Path(mini_AUTO_THEME_TXT) / "lobby.txt")
        mini_HIT_EFFECT_DIR = str(Path(mini_BASE_DIR) / "HIT EFFECT")
        mini_LOOTCRATES_DIR = str(Path(mini_BASE_DIR) / "LOOTCRATES")
        mini_HIT_ORIG = str(Path(mini_HIT_EFFECT_DIR) / "org")
        mini_HIT_MODIFIED = str(Path(mini_HIT_EFFECT_DIR) / "modified")
        mini_LOOT_ORIG = str(Path(mini_LOOTCRATES_DIR) / "org")
        mini_LOOT_MODIFIED = str(Path(mini_LOOTCRATES_DIR) / "modified")
        mini_HIT_TXT_PATH = str(Path(mini_BASE_DIR) / "hit.txt")

        for d in [mini_BASE_DIR, mini_MINI_ICON_DIR, mini_INPUT_DIR, mini_OUTPUT_DIR,
                  mini_TXTS_DIR, mini_AUTO_THEME_BASE, mini_AUTO_THEME_FILES,
                  mini_AUTO_THEME_RESULT, mini_AUTO_THEME_TXT, mini_HIT_EFFECT_DIR,
                  mini_LOOTCRATES_DIR, mini_HIT_ORIG, mini_HIT_MODIFIED,
                  mini_LOOT_ORIG, mini_LOOT_MODIFIED]:
            Path(d).mkdir(parents=True, exist_ok=True)

        mini_menu()
        return

zsdic_BASE_DIR = ""
zsdic_GAME_BASE = ""
zsdic_GAME_DIRS = {}
zsdic_OUTPUT_DIR_NAME = "skindats"
zsdic_EDITED_DIR_NAME = "edited"
zsdic_SIZE_DIR_NAME = "size"
zsdic_MODSKIN_TXT = ""
zsdic_OUTFITS_TXT = ""
zsdic_NULL_TXT = ""
zsdic_CHANGELOG_TXT = ""
zsdic_NULLED_LOG_TXT = ""
zsdic_SWAP_OFFSETS_TXT = ""
zsdic_OUTFITS_FILES = {"AvatarSuitsTable.uasset", "GoldClothBattleEffect.uasset"}
zsdic_ID_ASCII_RE = _ptre.compile(rb"(?<![0-9])[0-9]{3,}(?![0-9])")
zsdic_ID_UTF16LE_RE = _ptre.compile(rb"(?:(?:[0-9]\x00){3,})")

def zsdic_build_safe_pattern(ascii_bytes: bytes):
    return _ptre.compile(rb"(?<![0-9])" + _ptre.escape(ascii_bytes) + rb"(?![0-9])")

def zsdic_pad_pattern(src: bytes, target_len: int) -> bytes:
    cur = bytearray(src)
    to_insert = target_len - len(cur)
    idx = cur.find(0x00)
    if idx < 0:
        cur.extend(b"\x00" * to_insert)
    else:
        for _ in range(to_insert):
            cur.insert(idx, 0x00)
    return bytes(cur)

def zsdic_truncate_pattern(src: bytes, target_len: int) -> bytes:
    cur = bytearray(src)
    to_remove = len(cur) - target_len
    while to_remove > 0:
        idx = cur.find(0x00)
        if idx < 0:
            break
        del cur[idx]
        to_remove -= 1
    if to_remove > 0:
        del cur[-to_remove:]
    return bytes(cur)

def zsdic_iter_files(root_dir: str):
    for r, _, files in os.walk(root_dir):
        for fn in files:
            abs_path = os.path.join(r, fn)
            if os.path.isfile(abs_path):
                yield abs_path, os.path.relpath(abs_path, root_dir)

def zsdic_parse_id_pairs(path: str):
    pairs = []
    if not os.path.isfile(path):
        return pairs
    with open(path, encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith(("#", "//", ";")):
                continue
            parts = [p for p in _ptre.split(r"[,\s]+", line) if p]
            if len(parts) >= 2:
                pairs.append((parts[0].strip(), parts[1].strip()))
    return pairs

def zsdic_op_regex(pat: bytes):
    return _ptre.compile(rb"(?<![0-9])" + _ptre.escape(pat) + rb"(?![0-9])")

def zsdic_load_null_id_set(null_txt_path: str) -> set:
    ids = set()
    if not os.path.isfile(null_txt_path):
        return ids
    with open(null_txt_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            for m in _ptre.finditer(r"\b(\d{3,})\b", line):
                ids.add(m.group(1))
    return ids

def zsdic_load_swap_offsets(path: str):
    if not os.path.isfile(path):
        return None
    out = {}
    current_file = None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("FILE|"):
                current_file = line.split("|", 1)[1]
                out.setdefault(current_file, [])
            elif line.startswith("OFFSETS|") and current_file is not None:
                rest = line.split("|", 1)[1].strip()
                if rest:
                    parts = [p.strip() for p in rest.split(",") if p.strip().isdigit()]
                    out[current_file].extend(int(p) for p in parts)
    for k in list(out.keys()):
        out[k] = sorted(set(out[k]))
    return out

def zsdic_write_swap_offsets(path: str, offsets_map: dict):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("=== SWAP OFFSETS LOG ===\nGenerated by Premium Engine.\n\n")
            for rel in sorted(offsets_map.keys()):
                offs = sorted(set(offsets_map[rel]))
                f.write(f"FILE|{rel}\nOFFSETS|" + ",".join(str(x) for x in offs) + "\n\n")
    except Exception as e:
        zsdic_console.print(f"[{WARNING}]Failed writing {path}: {e}[/]")

def zsdic_nearest_distance(pos: int, sorted_offsets: list) -> int:
    i = bisect.bisect_left(sorted_offsets, pos)
    best = 10**18
    if i < len(sorted_offsets):
        best = min(best, abs(sorted_offsets[i] - pos))
    if i > 0:
        best = min(best, abs(sorted_offsets[i - 1] - pos))
    return best

def zsdic_find_ascii_id_candidates(orig_bytes: bytes, swap_offsets: list, null_id_set: set, mod_ids: set):
    candidates = []
    if not swap_offsets:
        return candidates
    swap_offsets = sorted(swap_offsets)
    for m in zsdic_ID_ASCII_RE.finditer(orig_bytes):
        start, end = m.start(), m.end()
        if end + 5 > len(orig_bytes):
            continue
        id_str = orig_bytes[start:end].decode("ascii", errors="ignore")
        if not id_str or id_str in mod_ids or id_str.startswith("40") or id_str not in null_id_set:
            continue
        longhex = orig_bytes[start:end + 5]
        dist = zsdic_nearest_distance(start, swap_offsets)
        candidates.append((dist, start, id_str, longhex))
    return candidates

def zsdic_find_utf16le_id_candidates(orig_bytes: bytes, swap_offsets: list, null_id_set: set, mod_ids: set):
    candidates = []
    if not swap_offsets:
        return candidates
    swap_offsets = sorted(swap_offsets)
    for m in zsdic_ID_UTF16LE_RE.finditer(orig_bytes):
        start, end = m.start(), m.end()
        if end + 5 > len(orig_bytes):
            continue
        id_str = orig_bytes[start:end][0::2].decode("ascii", errors="ignore")
        if not id_str or len(id_str) < 3 or id_str in mod_ids or id_str.startswith("40") or id_str not in null_id_set:
            continue
        longhex = orig_bytes[start:end + 5]
        dist = zsdic_nearest_distance(start, swap_offsets)
        candidates.append((dist, start, id_str, longhex))
    return candidates

def zsdic_apply_nulling_nearest(orig_bytes: bytes, swap_offsets: list, null_id_set: set, mod_ids: set, max_nulls: int):
    if not swap_offsets:
        return orig_bytes, []
    candidates = zsdic_find_ascii_id_candidates(orig_bytes, swap_offsets, null_id_set, mod_ids)
    if zsdic_ENABLE_UTF16LE_ID_SCAN:
        candidates += zsdic_find_utf16le_id_candidates(orig_bytes, swap_offsets, null_id_set, mod_ids)
    if not candidates:
        return orig_bytes, []
    candidates.sort(key=lambda x: (x[0], x[1]))
    data = bytearray(orig_bytes)
    nulled = []
    used_spans = []

    def overlaps(a0, a1):
        return any(not (a1 <= b0 or a0 >= b1) for b0, b1 in used_spans)

    for dist, start, id_str, longhex in candidates:
        if len(nulled) >= max_nulls:
            break
        end = start + len(longhex)
        if end > len(data) or overlaps(start, end):
            continue
        before = data[start - 1:start] if start > 0 else None
        after = data[end:end + 1] if end < len(data) else None
        if (before and before in b"0123456789") or (after and after in b"0123456789"):
            continue
        data[start:end] = b"\x00" * (end - start)
        used_spans.append((start, end))
        nulled.append((start, id_str, longhex.hex(), dist))
    return bytes(data), nulled

def zsdic_find_ascii_global_candidates(orig_bytes: bytes, null_id_set: set, mod_ids: set):
    candidates = []
    for m in zsdic_ID_ASCII_RE.finditer(orig_bytes):
        start, end = m.start(), m.end()
        if end + 5 > len(orig_bytes):
            continue
        id_str = orig_bytes[start:end].decode("ascii", errors="ignore")
        if not id_str or id_str in mod_ids or id_str.startswith("40") or id_str not in null_id_set:
            continue
        candidates.append((start, id_str, orig_bytes[start:end + 5]))
    return candidates

def zsdic_find_utf16le_global_candidates(orig_bytes: bytes, null_id_set: set, mod_ids: set):
    candidates = []
    for m in zsdic_ID_UTF16LE_RE.finditer(orig_bytes):
        start, end = m.start(), m.end()
        if end + 5 > len(orig_bytes):
            continue
        id_str = orig_bytes[start:end][0::2].decode("ascii", errors="ignore")
        if not id_str or len(id_str) < 3 or id_str in mod_ids or id_str.startswith("40") or id_str not in null_id_set:
            continue
        candidates.append((start, id_str, orig_bytes[start:end + 5]))
    return candidates

def zsdic_apply_nulling_global(orig_bytes: bytes, null_id_set: set, mod_ids: set, max_nulls: int):
    candidates = zsdic_find_ascii_global_candidates(orig_bytes, null_id_set, mod_ids)
    if zsdic_ENABLE_UTF16LE_ID_SCAN:
        candidates += zsdic_find_utf16le_global_candidates(orig_bytes, null_id_set, mod_ids)
    if not candidates:
        return orig_bytes, []
    candidates.sort(key=lambda x: x[0])
    data = bytearray(orig_bytes)
    nulled = []
    used_spans = []

    def overlaps(a0, a1):
        return any(not (a1 <= b0 or a0 >= b1) for b0, b1 in used_spans)

    for start, id_str, longhex in candidates:
        if len(nulled) >= max_nulls:
            break
        end = start + len(longhex)
        if end > len(data) or overlaps(start, end):
            continue
        before = data[start - 1:start] if start > 0 else None
        after = data[end:end + 1] if end < len(data) else None
        if (before and before in b"0123456789") or (after and after in b"0123456789"):
            continue
        data[start:end] = b"\x00" * (end - start)
        used_spans.append((start, end))
        nulled.append((start, id_str, longhex.hex(), -1))
    return bytes(data), nulled

def zsdic_apply_nulling_even_parts(orig_bytes: bytes, null_id_set: set, mod_ids: set, max_nulls: int, part_size: int = 65536):
    if max_nulls < 1:
        return orig_bytes, []
    if part_size <= 0:
        part_size = 65536
    candidates = zsdic_find_ascii_global_candidates(orig_bytes, null_id_set, mod_ids)
    if zsdic_ENABLE_UTF16LE_ID_SCAN:
        candidates += zsdic_find_utf16le_global_candidates(orig_bytes, null_id_set, mod_ids)
    if not candidates:
        return orig_bytes, []
    candidates.sort(key=lambda x: x[0])

    file_len = len(orig_bytes)
    num_full = file_len // part_size
    remainder = file_len % part_size
    num_parts = num_full + (1 if remainder else 0)
    if num_parts <= 0:
        num_parts = 1

    buckets = [[] for _ in range(num_parts)]
    for start, id_str, longhex in candidates:
        part_idx = start // part_size
        if part_idx >= num_parts:
            part_idx = num_parts - 1
        buckets[part_idx].append((start, id_str, longhex))

    data = bytearray(orig_bytes)
    nulled = []
    used_spans = []

    def overlaps(a0, a1):
        return any(not (a1 <= b0 or a0 >= b1) for b0, b1 in used_spans)

    ptrs = [0] * num_parts
    progress_made = True
    while len(nulled) < max_nulls and progress_made:
        progress_made = False
        for part_idx in range(num_parts):
            if len(nulled) >= max_nulls:
                break
            bucket = buckets[part_idx]
            if not bucket:
                continue
            while ptrs[part_idx] < len(bucket) and len(nulled) < max_nulls:
                start, id_str, longhex = bucket[ptrs[part_idx]]
                ptrs[part_idx] += 1
                end = start + len(longhex)
                if end > len(data) or overlaps(start, end):
                    continue
                before = data[start - 1:start] if start > 0 else None
                after = data[end:end + 1] if end < len(data) else None
                if (before and before in b"0123456789") or (after and after in b"0123456789"):
                    continue
                data[start:end] = b"\x00" * (end - start)
                used_spans.append((start, end))
                nulled.append((start, id_str, longhex.hex(), -2))
                progress_made = True
                break
    return bytes(data), nulled

def zsdic_get_pair_ops(pairs, cache):
    pair_ops = {}
    for id1, id2 in pairs:
        a1, a2 = id1.encode(), id2.encode()
        p1, p2 = zsdic_build_safe_pattern(a1), zsdic_build_safe_pattern(a2)
        pos1 = pos2 = None
        d1 = d2 = b""
        for data in cache.values():
            if pos1 is None and (m := p1.search(data)):
                pos1, d1 = m.start(), data
            if pos2 is None and (m := p2.search(data)):
                pos2, d2 = m.start(), data
            if pos1 is not None and pos2 is not None:
                break
        if pos1 is None or pos2 is None:
            continue
        lh1 = a1 + d1[pos1 + len(a1): pos1 + len(a1) + 5]
        lh2 = a2 + d2[pos2 + len(a2): pos2 + len(a2) + 5]
        digit_len_diff = abs(len(a1) - len(a2))
        ops = []

        if digit_len_diff <= 1:
            if len(lh1) == len(lh2):
                mode = "TWO-WAY"
                ops.append({"from": lh1, "to": lh2, "rx": zsdic_op_regex(lh1)})
                ops.append({"from": lh2, "to": lh1, "rx": zsdic_op_regex(lh2)})
            elif len(lh1) > len(lh2):
                mode = "TWO-WAY(ADJUSTED)"
                ops.append({"from": lh1, "to": zsdic_pad_pattern(lh2, len(lh1)), "rx": zsdic_op_regex(lh1)})
                ops.append({"from": lh2, "to": zsdic_truncate_pattern(lh1, len(lh2)), "rx": zsdic_op_regex(lh2)})
            else:
                mode = "TWO-WAY(ADJUSTED)"
                ops.append({"from": lh2, "to": zsdic_pad_pattern(lh1, len(lh2)), "rx": zsdic_op_regex(lh2)})
                ops.append({"from": lh1, "to": zsdic_truncate_pattern(lh2, len(lh1)), "rx": zsdic_op_regex(lh1)})
        else:
            shorter_lh, longer_lh = (lh1, lh2) if len(a1) < len(a2) else (lh2, lh1)
            src, dst = longer_lh, shorter_lh
            if len(dst) < len(src):
                dst = zsdic_pad_pattern(dst, len(src))
            elif len(dst) > len(src):
                dst = zsdic_truncate_pattern(dst, len(src))
            mode = "ONE-WAY(PADDED)"
            ops.append({"from": src, "to": dst, "rx": zsdic_op_regex(src)})

        pair_ops[(id1, id2)] = {"mode": mode, "ops": ops, "lhs": lh1, "rhs": lh2}
    return pair_ops

def zsdic_mod_skin_flow(game: str):
    mini_display_tool_name()

    zsdic_console.print(
        Panel(
            f"[bold {BRIGHT_COLOR}]PRISM CORE ENGINE[/bold {BRIGHT_COLOR}]\n\n"
            f"[bold {TEXT_COLOR}]M O D   S K I N   &   A U T O   S I Z E   F I X E R[/bold {TEXT_COLOR}]\n"
            f"[dim {DIM_COLOR}]----------------------------------------------[/dim {DIM_COLOR}]\n"
            f"[bold {TEXT_COLOR}]Target Profile : [bold {BRIGHT_COLOR}]{game.upper()}[/bold {BRIGHT_COLOR}][/bold {TEXT_COLOR}]",
            expand=True,
            border_style=BORDER_COLOR,
            box=HEAVY_EDGE,
            padding=(1, 2),
            title=f"[bold black on {BRIGHT_COLOR}] SYSTEM INITIALIZED [/]",
            title_align="center"
        )
    )

    game_base_dir = zsdic_GAME_DIRS.get(game, "")
    if not game_base_dir:
        zsdic_console.print(Panel(
            f"[{ERROR}]Game directory not set: {game}[/]",
            border_style=ERROR,
            expand=True
        ))
        return

    modskin_path = zsdic_MODSKIN_TXT
    outfits_path = zsdic_OUTFITS_TXT
    output_dir = os.path.join(game_base_dir, zsdic_OUTPUT_DIR_NAME)
    edited_dir = os.path.join(game_base_dir, zsdic_EDITED_DIR_NAME)
    size_dir = os.path.join(game_base_dir, zsdic_SIZE_DIR_NAME)
    swap_offsets_path = zsdic_SWAP_OFFSETS_TXT

    pairs_modskin = zsdic_parse_id_pairs(modskin_path) if os.path.isfile(modskin_path) else []
    pairs_outfits = zsdic_parse_id_pairs(outfits_path) if os.path.isfile(outfits_path) else []

    if not pairs_modskin and not pairs_outfits:
        zsdic_console.print(Panel(
            f"[bold {WARNING}]No valid ID pairs configuration found![/]",
            border_style=WARNING,
            box=ROUNDED,
            expand=True
        ))
        time.sleep(1)
        return

    all_files = list(zsdic_iter_files(output_dir))
    if not all_files:
        zsdic_console.print(Panel(
            f"[bold {ERROR}]No asset files detected in directory:\n{output_dir}[/]",
            border_style=ERROR,
            expand=True
        ))
        return

    cache, rel_map = {}, {}
    for abs_path, rel_path in all_files:
        try:
            cache[abs_path] = open(abs_path, "rb").read()
            rel_map[abs_path] = rel_path
        except Exception:
            pass

    pair_ops_modskin = zsdic_get_pair_ops(pairs_modskin, cache) if pairs_modskin else {}
    pair_ops_outfits = zsdic_get_pair_ops(pairs_outfits, cache) if pairs_outfits else {}

    all_rxs = []
    for pinfo in pair_ops_modskin.values():
        all_rxs.extend(op["rx"] for op in pinfo["ops"])
    for pinfo in pair_ops_outfits.values():
        all_rxs.extend(op["rx"] for op in pinfo["ops"])

    valid_files = [p for p, data in cache.items() if any(rx.search(data) for rx in all_rxs)]
    if not valid_files:
        zsdic_console.print(Panel(
            f"[bold {ERROR}]Zero matching pattern signatures found in cached assets. Process halted.[/]",
            border_style=ERROR,
            expand=True
        ))
        return

    if os.path.isdir(edited_dir):
        shutil.rmtree(edited_dir)
    os.makedirs(edited_dir, exist_ok=True)

    file_changes = {}
    swap_offsets_map = {}
    null_id_set = zsdic_load_null_id_set(zsdic_NULL_TXT)
    mod_ids = set()

    total_pairs = len(pairs_modskin) + len(pairs_outfits)
    auto_max_nulls = total_pairs * 3 if total_pairs < 500 else total_pairs * 2

    for a, b in pairs_modskin + pairs_outfits:
        if a.isdigit():
            mod_ids.add(a)
        if b.isdigit():
            mod_ids.add(b)

    def get_progress_table(file_logs):
        table = Table(
            title=f"[bold black on {BRIGHT_COLOR}] PRISM LIVE ENGINE [/]",
            border_style=BORDER_COLOR,
            box=HEAVY_EDGE,
            expand=True,
            show_lines=True
        )
        table.add_column("TARGET ASSET FILE", style=f"bold {BRIGHT_COLOR}", header_style=f"bold black on {BRIGHT_COLOR}", ratio=2)
        table.add_column("PIPELINE STATUS", style="bold", header_style=f"bold black on {BRIGHT_COLOR}", ratio=1, justify="center")
        for fname, status in file_logs:
            table.add_row(fname, status)
        return table

    file_logs = []
    success_count = 0

    with Live(get_progress_table(file_logs), refresh_per_second=15, console=zsdic_console) as live:
        for src in sorted(valid_files):
            rel = rel_map.get(src, os.path.basename(src))
            short_name = rel if len(rel) < 35 else "..." + rel[-32:]

            file_logs.append([f"[bold {TEXT_COLOR}]{short_name}[/]", f"[blink bold {WARNING}]PATCHING...[/]"])
            if len(file_logs) > 8:
                file_logs.pop(0)
            live.update(get_progress_table(file_logs))

            edited_path = os.path.join(edited_dir, rel)
            os.makedirs(os.path.dirname(edited_path), exist_ok=True)

            try:
                shutil.copy2(src, edited_path)
                orig = open(edited_path, "rb").read()
            except Exception:
                file_logs[-1][1] = f"[bold {ERROR}]COPY ERROR[/]"
                live.update(get_progress_table(file_logs))
                continue

            new = bytearray(orig)
            changed = False
            active_pair_ops = pair_ops_outfits if os.path.basename(rel) in zsdic_OUTFITS_FILES else pair_ops_modskin

            for pair, pinfo in active_pair_ops.items():
                for op in pinfo["ops"]:
                    matches = list(op["rx"].finditer(orig))
                    if not matches:
                        continue
                    frm, to = op["from"], op["to"]
                    for m in matches:
                        start = m.start()
                        new[start: start + len(frm)] = to
                        swap_offsets_map.setdefault(rel, set()).add(start)
                        changed = True

            if changed:
                offsets = list(swap_offsets_map.get(rel, set()))
                if offsets:
                    new_bytes, _ = zsdic_apply_nulling_nearest(bytes(new), offsets, null_id_set, mod_ids, auto_max_nulls)
                else:
                    new_bytes, _ = zsdic_apply_nulling_global(bytes(new), null_id_set, mod_ids, auto_max_nulls)
                new = bytearray(new_bytes)

            if changed and new != orig:
                try:
                    with open(edited_path, "wb") as f:
                        f.write(new)
                    size_path = os.path.join(size_dir, rel)
                    os.makedirs(os.path.dirname(size_path), exist_ok=True)
                    with open(size_path, "wb") as f:
                        f.write(new)
                except Exception:
                    pass

                file_changes.setdefault(rel, active_pair_ops)
                success_count += 1

            file_logs[-1][1] = f"[bold {BRIGHT_COLOR}]SUCCESS[/]"
            live.update(get_progress_table(file_logs))

    zsdic_console.print(Panel(
        f"[bold {BRIGHT_COLOR}]PRISM CORE PIPELINE EXECUTED SUCCESSFULLY![/]\n\n"
        f"  [dim {DIM_COLOR}]* Total Asset Files Evaluated :[/dim {DIM_COLOR}] [bold {BRIGHT_COLOR}]{len(valid_files)}[/]\n"
        f"  [dim {DIM_COLOR}]* Successfully Patched & Fixed :[/dim {DIM_COLOR}] [bold {BRIGHT_COLOR}]{success_count}[/]\n"
        f"  [dim {DIM_COLOR}]* Dynamic Null Allocation    :[/dim {DIM_COLOR}] [bold {WARNING}]{auto_max_nulls} nulls/file[/]",
        border_style=BORDER_COLOR,
        box=HEAVY_EDGE,
        expand=True,
        title=f"[bold black on {BRIGHT_COLOR}] SESSION EXECUTION SUMMARY [/]",
        padding=(1, 2)
    ))

    if not file_changes:
        return

    try:
        with open(zsdic_CHANGELOG_TXT, "w", encoding="utf-8") as f:
            f.write("PRISM MOD SKIN CHANGELOG\n==============================\n\n")
            for rel_file, pairs_info in file_changes.items():
                f.write(f"FILE: {rel_file}\n")
                for pair, pinfo in pairs_info.items():
                    f.write(f"  PAIR: {pair[0]} -> {pair[1]} ({pinfo['mode']})\n")
                    for op in pinfo["ops"]:
                        frm_hex = op["from"].hex().upper()
                        to_hex = op["to"].hex().upper()
                        f.write(f"     - Replaced successfully\n       FROM: {frm_hex}\n       TO  : {to_hex}\n")
                f.write("==============================\n\n")
    except Exception as e:
        zsdic_console.print(f"[red]Changelog Error: {e}[/red]")

    zsdic_write_swap_offsets(swap_offsets_path, swap_offsets_map)

    zsdic_console.print(
        Panel(
            f"[bold {BRIGHT_COLOR}]All Operations Finished! Output files secured successfully.[/]",
            expand=True,
            border_style=BORDER_COLOR,
            box=HEAVY_EDGE
        )
    )

def zsdic_repack_size_fix():
    mini_display_tool_name()
    zsdic_console.print(Panel(f"[bold {BRIGHT_COLOR}]Size-Fix Initialized[/]", expand=False, border_style=BORDER_COLOR))

    edited_dir = os.path.join(zsdic_GAME_DIRS.get("BGMI", ""), zsdic_EDITED_DIR_NAME)
    size_dir = os.path.join(zsdic_GAME_DIRS.get("BGMI", ""), zsdic_SIZE_DIR_NAME)
    swap_offsets_path = zsdic_SWAP_OFFSETS_TXT

    if not os.path.isdir(edited_dir):
        zsdic_console.print(f"[red]Edited directory not found: {edited_dir}[/red]")
        return

    swap_offsets = zsdic_load_swap_offsets(swap_offsets_path)
    if not swap_offsets:
        zsdic_console.print(f"[{WARNING}]swap_offsets.txt missing/empty. Using GLOBAL nulling.[/]")
        swap_offsets = {}

    max_nulls_str = Prompt.ask(f"[bold {BRIGHT_COLOR}]Max nulls per file[/]", default=str(zsdic_DEFAULT_MAX_NULLS))
    try:
        max_nulls = int(max_nulls_str)
        if max_nulls < 1:
            max_nulls = zsdic_DEFAULT_MAX_NULLS
    except Exception:
        max_nulls = zsdic_DEFAULT_MAX_NULLS

    zsdic_console.print(f"\n[bold {BRIGHT_COLOR}]Size Fix Mode:[/]")
    zsdic_console.print(f"  [bold {BRIGHT_COLOR}]1)[/] Null Near To Modification  [dim](Nearest/Global)[/dim]")
    zsdic_console.print(f"  [bold {BRIGHT_COLOR}]2)[/] Null Evenly  [dim](64KB parts distribution)[/dim]")
    size_fix_mode = Prompt.ask(f"[bold {BRIGHT_COLOR}]Select mode[/]", choices=["1", "2"], default="1")

    null_id_set = zsdic_load_null_id_set(zsdic_NULL_TXT)
    mod_ids = set()
    for path in [zsdic_MODSKIN_TXT, zsdic_OUTFITS_TXT]:
        if os.path.isfile(path):
            for a, b in zsdic_parse_id_pairs(path):
                if a.isdigit():
                    mod_ids.add(a)
                if b.isdigit():
                    mod_ids.add(b)

    if os.path.isdir(size_dir):
        shutil.rmtree(size_dir)
    os.makedirs(size_dir, exist_ok=True)
    files_to_process = list(zsdic_iter_files(edited_dir))
    if not files_to_process:
        return

    nulled_info = {}
    progress = Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"))

    with Live(progress, refresh_per_second=10) as live:
        task = progress.add_task(f"[cyan]Nulling... ", total=len(files_to_process))
        for abs_path, rel_path in files_to_process:
            progress.update(task, advance=1, description=f"[cyan]Processing {rel_path}[/]")
            try:
                orig_bytes = open(abs_path, "rb").read()
            except Exception:
                continue

            offsets = swap_offsets.get(rel_path, []) if swap_offsets else []
            if size_fix_mode == "1":
                if offsets:
                    mode_used = "NEAREST"
                    new_bytes, entries = zsdic_apply_nulling_nearest(orig_bytes, offsets, null_id_set, mod_ids, max_nulls)
                else:
                    mode_used = "GLOBAL"
                    new_bytes, entries = zsdic_apply_nulling_global(orig_bytes, null_id_set, mod_ids, max_nulls)
            else:
                mode_used = "EVEN_PARTS"
                new_bytes, entries = zsdic_apply_nulling_even_parts(orig_bytes, null_id_set, mod_ids, max_nulls, 65536)

            out_path = os.path.join(size_dir, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(new_bytes)
            nulled_info[rel_path] = {"mode": mode_used, "entries": entries}

    try:
        with open(os.path.join(size_dir, zsdic_NULLED_LOG_TXT), "w", encoding="utf-8") as nf:
            nf.write("=== NULLED LOG ===\n")
            for rel_path in sorted(nulled_info.keys()):
                info = nulled_info[rel_path]
                entries = info.get("entries", [])
                nf.write(f"{rel_path}:\n  Mode: {info.get('mode', 'UNKNOWN')}\n")
                if not entries:
                    nf.write("  (no nulls)\n\n")
                    continue
                for pos, id_str, longhex_hex, dist in entries:
                    dist_str = "[global]" if dist == -1 else ("[even]" if dist == -2 else f"[dist {dist}]")
                    nf.write(f"  [pos {pos}] {dist_str} ID {id_str} -> nulled {longhex_hex}\n")
                nf.write("\n")
    except Exception:
        pass

    zsdic_console.print(Panel(f"[bold {BRIGHT_COLOR}]Size-fix complete![/]", expand=False, border_style=BORDER_COLOR, box=ROUNDED))

def zsdic_main_menu():
    while True:
        mini_display_tool_name()

        b_color = BRIGHT_COLOR
        menu_table = Table(show_header=True, header_style=f"bold black on {BRIGHT_COLOR}",
                           box=DOUBLE_EDGE, title="[reverse]  PRISM ENGINE  [/]",
                           border_style=BORDER_COLOR, expand=True)
        menu_table.add_column("OPT", justify="center", style=f"bold {BRIGHT_COLOR}", width=4)
        menu_table.add_column("COMMAND", style=f"bold {TEXT_COLOR}")
        menu_table.add_column("DESCRIPTION", style=f"dim {DIM_COLOR}")

        menu_table.add_row("1", "MOD SKIN", "Advanced Mod Skin")
        menu_table.add_row("0", f"[{ERROR}]BACK[/]", "Return to Menu")

        console.print(Panel(menu_table, border_style=BORDER_COLOR, box=HEAVY_EDGE))

        choice = safe_input(f"[bold {BRIGHT_COLOR}]ENTER CHOICE (0-1) > [/bold {BRIGHT_COLOR}]").strip()

        if choice == "1":
            global game_key
            zsdic_mod_skin_flow(game_key)
            safe_input(f"\n[bold {TEXT_COLOR}]Press Enter to return...[/]")
        elif choice == "0":
            break
        else:
            console.print(f"[red]Invalid! Enter 0 or 1[/red]")
            time.sleep(1)

def zsdic_skin_tool_main(data_path):
    global zsdic_BASE_DIR, zsdic_GAME_BASE, zsdic_GAME_DIRS
    global zsdic_MODSKIN_TXT, zsdic_OUTFITS_TXT, zsdic_NULL_TXT
    global zsdic_CHANGELOG_TXT, zsdic_NULLED_LOG_TXT, zsdic_SWAP_OFFSETS_TXT
    global game_key

    while True:
        mini_clear_screen()
        print_banner()

        select_table = Table(
            show_header=True,
            header_style=f"bold black on {BRIGHT_COLOR}",
            box=DOUBLE_EDGE,
            title="[reverse]  SELECT TARGET PROFILE (PRISM)  [/]",
            border_style=BORDER_COLOR,
            expand=True
        )
        select_table.add_column("OPT", justify="center", style=f"bold {BRIGHT_COLOR}", width=4)
        select_table.add_column("GAME", style=f"bold {TEXT_COLOR}")
        select_table.add_column("DESCRIPTION", style=f"dim {DIM_COLOR}")
        select_table.add_row("1", "BGMI", "Aesthetic BGMI profiles")
        select_table.add_row("2", "PUBG", "Aesthetic PUBG profiles")
        select_table.add_row("0", f"[{ERROR}]BACK[/]", "Return")
        console.print(Panel(select_table, border_style=BORDER_COLOR, box=HEAVY_EDGE))

        game_choice = safe_input(f"[bold {BRIGHT_COLOR}]SELECT (1/2/0) > [/bold {BRIGHT_COLOR}]").strip()

        if game_choice == "0":
            return
        if game_choice not in ("1", "2"):
            console.print(f"[bold {ERROR}]Invalid![/]")
            time.sleep(1)
            continue

        selected_game = "BGMI_SKIN" if game_choice == "1" else "PUBG_SKIN"
        game_key = "BGMI" if game_choice == "1" else "PUBG"
        GAME_BASE = data_path / "SKIN_TOOL" / selected_game

        zsdic_BASE_DIR = str(GAME_BASE / "ZSDIC")
        zsdic_GAME_BASE = str(Path(zsdic_BASE_DIR) / game_key)
        zsdic_GAME_DIRS = {game_key: zsdic_GAME_BASE}
        zsdic_MODSKIN_TXT = str(Path(zsdic_BASE_DIR) / "modskin.txt")
        zsdic_OUTFITS_TXT = str(Path(zsdic_BASE_DIR) / "outfits.txt")
        zsdic_NULL_TXT = str(Path(zsdic_BASE_DIR) / "null.txt")
        zsdic_CHANGELOG_TXT = str(Path(zsdic_BASE_DIR) / "changelog.txt")
        zsdic_NULLED_LOG_TXT = str(Path(zsdic_BASE_DIR) / "nulled.txt")
        zsdic_SWAP_OFFSETS_TXT = str(Path(zsdic_BASE_DIR) / "swap_offsets.txt")

        for d in [
            zsdic_BASE_DIR,
            zsdic_GAME_BASE,
            os.path.join(zsdic_GAME_BASE, zsdic_OUTPUT_DIR_NAME),
            os.path.join(zsdic_GAME_BASE, zsdic_EDITED_DIR_NAME),
            os.path.join(zsdic_GAME_BASE, zsdic_SIZE_DIR_NAME),
        ]:
            Path(d).mkdir(parents=True, exist_ok=True)

        zsdic_main_menu()
        return

LUA_XOR_KEY = b''
SERVER_LUA_XOR_KEY_HEX = "112136474657a78d9d8490d8ab008c35261af7e45805b8b31507d02c1e8ff6c8"

BGMI_STD = {
    0: 13, 1: 14, 2: 15, 3: 16, 4: 17, 5: 18, 14: 27, 16: 29, 17: 0, 18: 1,
    20: 3, 21: 4, 22: 5, 23: 6, 24: 7, 25: 8, 26: 9, 27: 10, 28: 11, 29: 12,
    30: 30, 31: 31, 32: 32, 33: 33, 34: 34, 36: 36, 37: 37, 38: 38, 39: 39,
    40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 45,
}
STD_BGMI = {v: k for k, v in BGMI_STD.items()}
STD_FMT = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 1, 0, 3]

def process_lua_file(data, is_encrypt=False):
    class RW:
        def __init__(self):
            self.b = bytearray()

        def byte(self, v):
            self.b.append(int(v) & 0xFF)

        def u32(self, v):
            self.b.extend(struct.pack('<I', int(v) & 0xFFFFFFFF))

        def i32(self, v):
            self.b.extend(struct.pack('<i', int(v)))

        def raw(self, d):
            self.b.extend(d)

    class R:
        def __init__(self, d):
            self.d = bytes(d)
            self.p = 0

        def need(self, n, what='data'):
            if n < 0 or self.p + n > len(self.d):
                raise ValueError(f"truncated: {what} at {self.p}")

        def byte(self):
            self.need(1, 'byte')
            v = self.d[self.p]
            self.p += 1
            return v

        def u32(self):
            self.need(4, 'u32')
            v = struct.unpack_from('<I', self.d, self.p)[0]
            self.p += 4
            return v

        def i32(self):
            self.need(4, 'i32')
            v = struct.unpack_from('<i', self.d, self.p)[0]
            self.p += 4
            return v

        def raw(self, n):
            self.need(n, f'raw({n})')
            v = self.d[self.p:self.p + n]
            self.p += n
            return v

    if len(data) < 4:
        raise ValueError('File too small (less than 4 bytes)')

    if data[:4] != b'\x1bLua':
        raise ValueError(
            'Not a Lua bytecode file (missing \\x1bLua magic). '
            f'First 8 bytes: {data[:8].hex()}'
        )

    version_byte = data[4]

    if version_byte == 0x51:
        return data
    if version_byte == 0x52:
        return data
    if version_byte == 0x54:
        return data

    if version_byte != 0x53:
        raise ValueError(f'Unsupported Lua version byte: 0x{version_byte:02x}')

    size_t_byte = data[13]

    if size_t_byte == 8:
        return data

    if size_t_byte != 4:
        return data

    r = R(data)
    w = RW()

    hdr = bytearray(r.raw(33))

    if is_encrypt:
        hdr[13] = 4
    else:
        hdr[13] = 8

    w.raw(hdr)
    w.byte(r.byte())

    key = bytes(LUA_XOR_KEY or b'')

    def read_t24_string():
        sz = r.byte()
        if sz == 0xFF:
            sz = r.u32()
        if sz == 0:
            return None
        if sz < 1:
            raise ValueError(f'invalid T24 string size {sz}')
        payload_len = sz - 1
        enc = r.raw(payload_len)
        if key:
            enc = bytes(enc[i] ^ key[i % len(key)] for i in range(len(enc)))
        return enc

    def read_standard_string():
        sz = r.byte()
        if sz == 0xFF:
            r.need(8, 'size_t')
            sz = struct.unpack_from('<Q', r.d, r.p)[0]
            r.p += 8
        if sz == 0:
            return None
        if sz < 1:
            raise ValueError(f'invalid std string size {sz}')
        return r.raw(sz - 1)

    def write_t24_string(s):
        if s is None:
            w.byte(0)
            return
        e = bytes(s)
        if key:
            e = bytes(e[i] ^ key[i % len(key)] for i in range(len(e)))
        sz = len(e) + 1
        if sz < 0xFF:
            w.byte(sz)
        else:
            w.byte(0xFF)
            w.u32(sz)
        w.raw(e)

    def write_standard_string(s):
        if s is None:
            w.byte(0)
            return
        e = bytes(s)
        sz = len(e) + 1
        if sz < 0xFF:
            w.byte(sz)
        else:
            w.byte(0xFF)
            w.raw(struct.pack('<Q', sz))
        w.raw(e)

    def read_string():
        return read_standard_string() if is_encrypt else read_t24_string()

    def write_string(s):
        if is_encrypt:
            write_t24_string(s)
        else:
            write_standard_string(s)

    def translate_instruction(raw):
        op = raw & 0x3F
        A = (raw >> 6) & 0xFF
        C = (raw >> 14) & 0x1FF
        B = (raw >> 23) & 0x1FF
        Bx = (raw >> 14) & 0x3FFFF
        Ax = (raw >> 6) & 0x3FFFFFF

        if is_encrypt:
            dop = STD_BGMI.get(op, op)
        else:
            dop = BGMI_STD.get(op, op)

        if dop < 0 or dop >= 64:
            dop = op

        fmt = STD_FMT[dop] if dop < len(STD_FMT) else 0
        if fmt == 0:
            return (dop & 0x3F) | (A << 6) | (C << 14) | (B << 23)
        if fmt == 1:
            return (dop & 0x3F) | (A << 6) | (Bx << 14)
        if fmt == 2:
            return (dop & 0x3F) | (A << 6) | (Bx << 14)
        if fmt == 3:
            return (dop & 0x3F) | (Ax << 6)
        return (dop & 0x3F) | (A << 6) | (Bx << 14)

    MAX_COUNT = 2_000_000

    def convert_proto(depth=0):
        if depth > 50:
            raise ValueError('Nested prototype too deep')

        source = read_string()
        write_string(source)
        w.i32(r.i32())
        ldef = r.i32()
        w.i32(ldef)

        w.byte(r.byte())
        w.byte(r.byte())
        w.byte(r.byte())

        ncode = r.u32()
        if ncode > MAX_COUNT:
            raise ValueError(f'invalid code count {ncode}')
        w.u32(ncode)
        for _ in range(ncode):
            w.u32(translate_instruction(r.u32()))

        nk = r.u32()
        if nk > MAX_COUNT:
            raise ValueError(f'invalid constant count {nk}')
        w.u32(nk)
        for _ in range(nk):
            tag = r.byte()
            w.byte(tag)
            if tag == 0:
                continue
            if tag == 1:
                w.byte(r.byte())
            elif tag in (3, 19):
                w.raw(r.raw(8))
            elif tag in (4, 20):
                write_string(read_string())
            else:
                raise ValueError(f'unsupported constant tag {tag}')

        nups = r.u32()
        if nups > MAX_COUNT:
            raise ValueError(f'invalid upvalue count {nups}')
        w.u32(nups)
        for _ in range(nups):
            w.byte(r.byte())
            w.byte(r.byte())

        npt = r.u32()
        if npt > MAX_COUNT:
            raise ValueError(f'invalid prototype count {npt}')
        w.u32(npt)
        for _ in range(npt):
            convert_proto(depth + 1)

        nln = r.u32()
        if nln > MAX_COUNT:
            raise ValueError(f'invalid line-info count {nln}')

        if is_encrypt:
            lines = [r.i32() for _ in range(nln)]
            w.u32(nln)
            prev = ldef
            for ln in lines:
                w.byte((ln - prev) & 0xFF)
                prev = ln
            w.u32(0)
        else:
            cur = ldef
            lines = []
            for _ in range(nln):
                d = r.byte()
                cur += d if d <= 127 else d - 256
                lines.append(cur)
            nab = r.u32()
            if nab > MAX_COUNT:
                raise ValueError(f'invalid absolute-line count {nab}')
            for _ in range(nab):
                pc = r.u32()
                ln = r.i32()
                if pc < nln:
                    lines[pc] = ln
            w.u32(nln)
            for ln in lines:
                w.i32(ln)

        nloc = r.u32()
        if nloc > MAX_COUNT:
            raise ValueError(f'invalid local count {nloc}')
        w.u32(nloc)
        for _ in range(nloc):
            write_string(read_string())
            w.i32(r.i32())
            w.i32(r.i32())

        nupn = r.u32()
        if nupn > MAX_COUNT:
            raise ValueError(f'invalid upvalue-name count {nupn}')
        w.u32(nupn)
        for _ in range(nupn):
            write_string(read_string())

    convert_proto()
    return bytes(w.b)

def _download_jar(url, dest):
    urls_to_try = [url]
    if 'unluac' in dest.name.lower():
        urls_to_try = [
            url,
            "https://github.com/HansWessels/unluac/releases/download/v1.2.3/unluac.jar",
            "https://github.com/HansWessels/unluac/releases/latest/download/unluac.jar",
            "https://github.com/unluac/unluac/releases/download/2023-04-24/unluac.jar",
            "https://github.com/unluac/unluac/releases/download/2021-11-28/unluac.jar",
        ]

    last_error = None
    for try_url in urls_to_try:
        try:
            console.print(f"[{DIM_COLOR}]Trying: {try_url[:70]}...[/]")
            import urllib.request
            urllib.request.urlretrieve(try_url, to_long_path(dest))
            if dest.exists() and dest.stat().st_size > 1000:
                console.print(f"[bold {BRIGHT_COLOR}]Downloaded {dest.name} ({dest.stat().st_size:,} bytes)[/]")
                return True
            else:
                dest.unlink(missing_ok=True)
                last_error = "File too small or missing"
                continue
        except Exception as e:
            last_error = e
            continue

    console.print(f"[bold {ERROR}]Failed to download {dest.name}: {last_error}[/]")
    return False

def _detect_lua_version(path):
    try:
        with open(path, 'rb') as fh:
            magic = fh.read(5)
        if magic[:4] == b'\x1bLua':
            vb = magic[4]
            return vb, False
        with open(path, 'rb') as fh:
            magic2 = fh.read(3)
        if magic2 == b'\x1bLJ':
            return None, True
    except Exception:
        pass
    return None, False

def _find_local_unluac(script_dir, lua_base):
    candidates = [
        lua_base / "unluac_patched.jar",
        script_dir / "unluac_patched.jar",
        lua_base / "unluac.jar",
        script_dir / "unluac.jar",
        script_dir / "EXES" / "unluac.jar",
        script_dir / "EXES" / "unluac_pro.jar",
    ]
    for p in candidates:
        try:
            if p.is_file() and p.stat().st_size > 1000:
                return p
        except Exception:
            pass

    exes_dir = script_dir / "EXES"
    if exes_dir.is_dir():
        try:
            for jar_file in exes_dir.glob("*.jar"):
                if jar_file.is_file() and jar_file.stat().st_size > 1000:
                    return jar_file
        except Exception:
            pass
    return None

def _ensure_jar_for_file(luac_path, lua_base, script_dir):
    vb, is_luajit = _detect_lua_version(luac_path)
    ljd_path = lua_base / "ljd.jar"
    unluac_path = lua_base / "unluac.jar"

    if is_luajit:
        if not ljd_path.exists():
            _download_jar(
                "https://github.com/nicktindall/luajit-decompiler-v2/releases/latest/download/ljd.jar",
                ljd_path
            )
        return ljd_path if ljd_path.exists() else None
    else:
        local_jar = _find_local_unluac(script_dir, lua_base)
        if local_jar is not None:
            return local_jar
        _download_jar(
            "https://github.com/HansWessels/unluac/releases/latest/download/unluac.jar",
            unluac_path
        )
        return unluac_path if unluac_path.exists() else None

def run_lua_tool(data_path):
    global LUA_XOR_KEY, SERVER_LUA_XOR_KEY_HEX

    console.clear()
    print_banner()

    b_color = BRIGHT_COLOR
    console.print(Panel(
        f"[bold {BRIGHT_COLOR}]BYTECODE FORGE[/bold {BRIGHT_COLOR}]\n"
        f"[dim {DIM_COLOR}]Extract, Edit, and Repack game Lua Bytecode[/dim {DIM_COLOR}]",
        border_style=BORDER_COLOR,
        box=DOUBLE_EDGE
    ))

    lua_base = data_path / "LUA_TOOL"
    lua_org = lua_base / "Lua_org"
    lua_dec = lua_base / "Lua_Decript"
    lua_res = lua_base / "Lua_Rueslt"

    re_lua_any_size = lua_base / "RE_LUA ANY SIZE"
    lua_edit = re_lua_any_size / "EDIT_LUA"
    lua_org_pak = re_lua_any_size / "ORGNAL_PAK"
    lua_mod_repack = re_lua_any_size / "REPACK_MOD"

    lua_custom = lua_base / "LUA_CUSTOM"
    lua_custom_edit = lua_custom / "EDIT"
    lua_custom_pak = lua_custom / "PAK"
    lua_custom_result = lua_custom / "RESULT"

    for d in [lua_org, lua_dec, lua_res, lua_edit, lua_org_pak, lua_mod_repack,
              lua_custom, lua_custom_edit, lua_custom_pak, lua_custom_result]:
        os.makedirs(to_long_path(d), exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    unluac_path = lua_base / "unluac.jar"

    if _find_local_unluac(script_dir, lua_base) is None:
        _download_jar(
            "https://github.com/HansWessels/unluac/releases/latest/download/unluac.jar",
            unluac_path
        )

    if subprocess.call("command -v luac5.3", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        console.print(f"[{WARNING}]Installing Lua 5.3 Compiler via pkg...[/]")
        subprocess.call("pkg install lua53 -y", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    lua_key_file = lua_base / "lua_xor_key.txt"
    if SERVER_LUA_XOR_KEY_HEX:
        try:
            LUA_XOR_KEY = bytes.fromhex(SERVER_LUA_XOR_KEY_HEX.strip())
        except ValueError:
            LUA_XOR_KEY = b""
    elif lua_key_file.exists():
        try:
            local_key_hex = lua_key_file.read_text(encoding="utf-8").strip()
            LUA_XOR_KEY = bytes.fromhex(local_key_hex)
        except (OSError, ValueError):
            LUA_XOR_KEY = b""

    while True:
        console.clear()
        print_banner()

        menu_table = Table(
            show_header=True,
            header_style=f"bold black on {BRIGHT_COLOR}",
            box=DOUBLE_EDGE,
            title="[reverse]  BYTECODE FORGE  [/]",
            border_style=BORDER_COLOR,
            expand=True
        )
        menu_table.add_column("OPT", justify="center", style=f"bold {BRIGHT_COLOR}", width=4)
        menu_table.add_column("COMMAND", style=f"bold {TEXT_COLOR}")
        menu_table.add_column("DESCRIPTION", style=f"dim {DIM_COLOR}")

        menu_table.add_row("1", "BYTECODE DECOMPILE", "Org → Decript (.lua)")
        menu_table.add_row("2", "BYTECODE RECOMPILE", "Edited → Result (.lua)")
        menu_table.add_row("3", "ARCHIVE INJECT", "Inject edited Lua into PAK")
        menu_table.add_row("4", "SIGNATURE INJECTOR", "Auto path from signature")
        menu_table.add_row("5", "COMPILE PLAIN", ".lua → .luac (plain)")
        menu_table.add_row("0", f"[{ERROR}]BACK[/]", "Return to Main Menu")

        console.print(Panel(menu_table, border_style=BORDER_COLOR, box=HEAVY_EDGE))

        choice = safe_input(f"[bold {BRIGHT_COLOR}]SELECT OPTION > [/bold {BRIGHT_COLOR}]").strip()

        if choice not in ["1", "2", "3", "4", "5", "0"]:
            continue

        if choice == "1":
            console.clear()
            print_banner()
            console.print(Panel(f"[bold {BRIGHT_COLOR}]Scanning 'Lua_org' directory...[/]",
                                border_style=BORDER_COLOR, box=ROUNDED))
            files = [f for f in lua_org.iterdir() if f.is_file() and f.suffix in ['.lua', '.luac']]
            if not files:
                console.print(Panel(f"[{ERROR}]No files in {lua_org.resolve()}[/]", border_style=ERROR))
            else:
                file_list = "\n".join([f"  [bold {BRIGHT_COLOR}]{i}.[/] [bold {TEXT_COLOR}]{f.name}[/]" for i, f in enumerate(files, 1)])
                console.print(Panel(file_list, title="[bold {BRIGHT_COLOR}]Available Files[/]", border_style=BORDER_COLOR, box=DOUBLE_EDGE))
                sel = safe_input(f"\n[bold {BRIGHT_COLOR}]Select file number(s), 'all', or '0' to Back: [/bold {BRIGHT_COLOR}]").strip()

                selected_files = []
                if sel == '0':
                    continue
                elif sel.lower() == 'all':
                    selected_files = files
                else:
                    for x in sel.split(','):
                        if x.strip().isdigit():
                            idx = int(x.strip()) - 1
                            if 0 <= idx < len(files):
                                selected_files.append(files[idx])

                if not selected_files:
                    console.print(Panel(f"[{ERROR}]Invalid selection![/]", border_style=ERROR))
                else:
                    console.print("")
                    for f in selected_files:
                        try:
                            with open(f, 'rb') as fp:
                                data = fp.read()

                            std_path = lua_dec / f"{f.stem}.std.luac"
                            out_path = lua_dec / f"{f.stem}.lua"

                            try:
                                std_data = process_lua_file(data, is_encrypt=False)
                                with open(std_path, 'wb') as fp:
                                    fp.write(std_data)
                                console.print(f"[dim {DIM_COLOR}]Converted ({len(std_data)} bytes)[/]")
                            except Exception as conv_err:
                                console.print(f"[{WARNING}]Conversion skipped: {conv_err}[/]")
                                with open(std_path, 'wb') as fp:
                                    fp.write(data)

                            jar = _ensure_jar_for_file(std_path, lua_base, script_dir)
                            decompile_ok = False
                            err_detail = ""

                            if jar is None:
                                err_detail = "unluac.jar not available."
                            else:
                                with tempfile.TemporaryDirectory(prefix='unluac_') as tdir:
                                    safe_jar = os.path.join(tdir, jar.name)
                                    safe_luac = os.path.join(tdir, 'target.luac')
                                    shutil.copy2(str(jar), safe_jar)
                                    shutil.copy2(str(std_path), safe_luac)
                                    err_buf = tempfile.NamedTemporaryFile(mode='w', suffix='.err', delete=False)
                                    with open(out_path, 'w', encoding='utf-8', errors='replace') as out_f:
                                        subprocess.run(['java', '-jar', safe_jar, safe_luac],
                                                       stdout=out_f, stderr=err_buf)
                                    err_buf.close()
                                    if out_path.exists() and out_path.stat().st_size > 10:
                                        decompile_ok = True
                                    else:
                                        try:
                                            with open(err_buf.name, 'r') as ef:
                                                err_detail = ef.read(300).strip() or "Empty output."
                                        except Exception:
                                            err_detail = "Empty output."
                                    try:
                                        os.unlink(err_buf.name)
                                    except Exception:
                                        pass

                            if std_path.exists():
                                std_path.unlink()

                            if decompile_ok:
                                console.print(Panel(
                                    f"[bold {BRIGHT_COLOR}]File:[/] [bold {TEXT_COLOR}]{f.name}[/]\n"
                                    f"[bold {BRIGHT_COLOR}]Status:[/] [bold {TEXT_COLOR}]Decompiled Successfully[/]\n"
                                    f"[bold {BRIGHT_COLOR}]Output:[/] [dim {DIM_COLOR}]Lua_Decript/{out_path.name}[/]",
                                    title=f"[bold black on {BRIGHT_COLOR}] DECRYPTION SUCCESS [/]",
                                    border_style=BORDER_COLOR,
                                    box=HEAVY_EDGE
                                ))
                            else:
                                console.print(Panel(
                                    f"[bold {BRIGHT_COLOR}]File:[/] [bold {TEXT_COLOR}]{f.name}[/]\n"
                                    f"[bold {BRIGHT_COLOR}]Status:[/] [bold {ERROR}]Failed[/]\n"
                                    f"[bold {BRIGHT_COLOR}]Reason:[/] [dim {WARNING}]{err_detail}[/]",
                                    title=f"[bold black on {ERROR}] DECOMPILE FAILED [/]",
                                    border_style=ERROR,
                                    box=HEAVY_EDGE
                                ))
                                if out_path.exists():
                                    out_path.unlink()
                            console.print("")
                        except Exception as e:
                            console.print(Panel(f"[bold {ERROR}]Error {f.name}: {e}[/]",
                                                border_style=ERROR, box=HEAVY_EDGE))
            safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")

        elif choice == "2":
            if not LUA_XOR_KEY:
                console.print(Panel(
                    f"[bold {WARNING}]Lua XOR key not available.[/]\n"
                    f"Create: [bold {BRIGHT_COLOR}]{lua_base / 'lua_xor_key.txt'}[/]\n"
                    f"Put key as HEX on one line.",
                    title=f"[bold {WARNING}] KEY REQUIRED [/]",
                    border_style=WARNING,
                    box=HEAVY_EDGE
                ))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            console.clear()
            print_banner()
            files = [f for f in lua_edit.iterdir() if f.is_file() and f.suffix in ['.lua', '.luac']]
            if not files:
                console.print(Panel(f"[{ERROR}]No files in {lua_edit.resolve()}[/]", border_style=ERROR))
            else:
                file_list = "\n".join([f"  [bold {BRIGHT_COLOR}]{i}.[/] [bold {TEXT_COLOR}]{f.name}[/]" for i, f in enumerate(files, 1)])
                console.print(Panel(file_list, title="[bold {BRIGHT_COLOR}]Available Files[/]", border_style=BORDER_COLOR, box=DOUBLE_EDGE))
                sel = safe_input(f"\n[bold {BRIGHT_COLOR}]Select file(s), 'all', or '0': [/bold {BRIGHT_COLOR}]").strip()

                selected_files = []
                if sel == '0':
                    continue
                elif sel.lower() == 'all':
                    selected_files = files
                else:
                    for x in sel.split(','):
                        if x.strip().isdigit():
                            idx = int(x.strip()) - 1
                            if 0 <= idx < len(files):
                                selected_files.append(files[idx])

                if not selected_files:
                    console.print(Panel(f"[{ERROR}]Invalid![/]", border_style=ERROR))
                else:
                    for f in selected_files:
                        try:
                            process_file = f
                            if f.suffix == '.lua':
                                process_file = lua_edit / f"{f.stem}.std.luac"
                                subprocess.run(["luac5.3", "-o", str(process_file), str(f)])

                            with open(process_file, 'rb') as fp:
                                data = fp.read()

                            bgmi_data = process_lua_file(data, is_encrypt=True)
                            final_out = lua_res / f"{f.stem}.lua"
                            with open(final_out, 'wb') as fp:
                                fp.write(bgmi_data)

                            console.print(Panel(
                                f"[bold {BRIGHT_COLOR}]File:[/] [bold {TEXT_COLOR}]{f.name}[/]\n"
                                f"[bold {BRIGHT_COLOR}]Output:[/] [dim {DIM_COLOR}]Lua_Rueslt/{final_out.name}[/]",
                                title=f"[bold black on {BRIGHT_COLOR}] ENCRYPTION SUCCESS [/]",
                                border_style=BORDER_COLOR,
                                box=HEAVY_EDGE
                            ))
                            if f.suffix == '.lua' and process_file.exists():
                                process_file.unlink()
                        except Exception as e:
                            console.print(Panel(f"[bold {ERROR}]Error {f.name}: {e}[/]",
                                                border_style=ERROR, box=HEAVY_EDGE))
            safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")

        elif choice == "3":
            console.clear()
            print_banner()
            console.print(Panel(
                f"[bold {BRIGHT_COLOR}]ARCHIVE INJECT[/bold {BRIGHT_COLOR}]\n"
                f"[dim {DIM_COLOR}]Target path aur Lua files inject karo[/dim {DIM_COLOR}]",
                border_style=BORDER_COLOR, box=HEAVY_EDGE
            ))

            pak_files = [f for f in lua_org_pak.iterdir() if f.is_file() and f.suffix.lower() in ['.pak', '.obb']]
            if not pak_files:
                console.print(Panel(
                    f"[{ERROR}]No Original PAK found in {lua_org_pak.resolve()}[/]",
                    border_style=ERROR, box=HEAVY_EDGE
                ))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            if len(pak_files) == 1:
                target_pak = pak_files[0]
                console.print(f"[bold {BRIGHT_COLOR}]PAK:[/] [bold {TEXT_COLOR}]{target_pak.name}[/]")
            else:
                file_list_str = "\n".join([f"  [bold {BRIGHT_COLOR}]{i}.[/] [bold {TEXT_COLOR}]{f.name}[/]" for i, f in enumerate(pak_files, 1)])
                console.print(Panel(file_list_str, title="[bold {BRIGHT_COLOR}]Select PAK[/]", border_style=BORDER_COLOR, box=DOUBLE_EDGE))
                sel = safe_input(f"[bold {BRIGHT_COLOR}]Select number (0 = back): [/bold {BRIGHT_COLOR}]")
                if not sel.strip().isdigit() or int(sel.strip()) == 0:
                    continue
                if not (1 <= int(sel.strip()) <= len(pak_files)):
                    continue
                target_pak = pak_files[int(sel.strip()) - 1]

            out_pak = lua_mod_repack / target_pak.name

            mod_luas = [f for f in lua_edit.iterdir() if f.is_file()]
            if not mod_luas:
                console.print(Panel(f"[{ERROR}]No edited Lua files in {lua_edit.resolve()}[/]",
                                    border_style=ERROR, box=HEAVY_EDGE))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            console.print()
            console.print(Panel(
                f"[bold {BRIGHT_COLOR}]Target path daalo (PAK ke andar)[/]\n"
                f"[dim {DIM_COLOR}]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core[/dim {DIM_COLOR}]\n"
                f"[dim {DIM_COLOR}]Ya Enter dabao — same naam ki file replace karega[/dim {DIM_COLOR}]",
                border_style=BORDER_COLOR, box=ROUNDED
            ))
            target_path = safe_input(f"[bold {BRIGHT_COLOR}]Path: [/bold {BRIGHT_COLOR}]").strip()
            target_path = target_path.replace('\\', '/').strip('/')

            try:
                console.print(f"\n[bold {BRIGHT_COLOR}]Repacking...[/]")
                pak_editor = TencentPakFile(target_pak)
                out_pak.parent.mkdir(parents=True, exist_ok=True)

                force_add = bool(target_path)
                count = repack_pak_file_full(
                    pak_editor, lua_edit, out_pak,
                    target_path if target_path else None,
                    force_add=force_add
                )

                if count > 0:
                    console.print()
                    console.print(Panel(
                        f"[bold {BRIGHT_COLOR}]Successfully processed {count} files![/]\n"
                        f"[bold {BRIGHT_COLOR}]Output:[/] [bold {TEXT_COLOR}]{out_pak}[/]"
                        + (f"\n[bold {BRIGHT_COLOR}]Target:[/] [bold {TEXT_COLOR}]{target_path}[/]" if target_path else ""),
                        border_style=BORDER_COLOR, box=HEAVY_EDGE
                    ))
                else:
                    console.print(Panel(f"[{ERROR}]No files processed![/]", border_style=ERROR))
            except Exception as e:
                console.print(Panel(f"[{ERROR}]Repack failed: {e}[/]", border_style=ERROR))
                import traceback
                traceback.print_exc()

            safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")

        elif choice == "4":
            console.clear()
            print_banner()

            csv_dir = lua_custom / "PUBG_CSV"
            if not download_csv_files(csv_dir):
                console.print(Panel(f"[{ERROR}]Signature sync failed![/]", border_style=ERROR))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            selected_csv, is_bgmi, game_label = _select_csv_source(csv_dir)
            if selected_csv is None:
                continue

            console.print(f"[bold {BRIGHT_COLOR}]Loading {selected_csv.name}...[/]")
            file_path_map = _load_csv_path_map(selected_csv)
            if not file_path_map:
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue
            console.print(f"[bold {BRIGHT_COLOR}]Loaded {len(file_path_map)} paths from {game_label}[/]")

            pak_files = [f for f in lua_custom_pak.iterdir() if f.suffix.lower() in ['.pak', '.obb']]
            if not pak_files:
                console.print(Panel(f"[{ERROR}]No PAK in LUA_CUSTOM/PAK![/]", border_style=ERROR))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            target_pak = pak_files[0]
            out_pak = lua_custom_result / target_pak.name

            edit_files = [p for p in lua_custom_edit.rglob('*') if p.is_file()]
            if not edit_files:
                console.print(Panel(f"[{ERROR}]No files in LUA_CUSTOM/EDIT![/]", border_style=ERROR))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            resolved_files, unresolved = _resolve_paths_from_csv(lua_custom_edit, file_path_map, is_bgmi)
            if not resolved_files:
                console.print(Panel(f"[{ERROR}]No files matched![/]", border_style=ERROR))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            lines = [f"[bold {BRIGHT_COLOR}]Signature: {game_label} ({selected_csv.name})[/]", ""]
            for p, rp in resolved_files:
                lines.append(f"  [bold {BRIGHT_COLOR}]✓[/] [white]{p.name}[/] [dim]→[/] [bold {BRIGHT_COLOR}]{rp}[/]")
            lines.append("")
            lines.append(f"[bold {BRIGHT_COLOR}]Total: {len(resolved_files)} files[/]")
            console.print(Panel("\n".join(lines), border_style=BORDER_COLOR, box=HEAVY_EDGE,
                                title=f"[bold black on {BRIGHT_COLOR}] PATH RESOLVER [/]"))

            confirm = safe_input(f"\n[bold {BRIGHT_COLOR}]Proceed? (y/n): [/]").strip().lower()
            if confirm not in ('y', 'yes'):
                continue

            try:
                pak = TencentPakFile(target_pak)
                count = repack_pak_file_full(pak, lua_custom_edit, out_pak, target_path=None, force_add=True)
                if count > 0:
                    console.print(Panel(
                        f"[bold {BRIGHT_COLOR}]Processed {count} files![/]\n"
                        f"[bold {BRIGHT_COLOR}]Output:[/] [bold {TEXT_COLOR}]{out_pak}[/]",
                        border_style=BORDER_COLOR, box=HEAVY_EDGE
                    ))
            except Exception as e:
                console.print(Panel(f"[{ERROR}]Failed: {e}[/]", border_style=ERROR))
                import traceback
                traceback.print_exc()

            safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")

        elif choice == "5":
            console.clear()
            print_banner()
            console.print(Panel(
                f"[bold {BRIGHT_COLOR}]COMPILE PLAIN[/]\n"
                f"[dim {DIM_COLOR}]Readable .lua → GAME T24 format[/dim {DIM_COLOR}]",
                border_style=BORDER_COLOR, box=HEAVY_EDGE
            ))

            compile_src = lua_edit
            compile_out = lua_res
            os.makedirs(to_long_path(compile_out), exist_ok=True)

            files = [f for f in compile_src.iterdir() if f.is_file() and f.suffix in ['.lua', '.luac']]
            if not files:
                console.print(Panel(f"[{ERROR}]No files in {compile_src}[/]", border_style=ERROR))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            file_list = "\n".join([f"  [bold {BRIGHT_COLOR}]{i}.[/] [bold {TEXT_COLOR}]{f.name}[/]" for i, f in enumerate(files, 1)])
            console.print(Panel(file_list, title="[bold {BRIGHT_COLOR}]Available Files[/]", border_style=BORDER_COLOR, box=DOUBLE_EDGE))

            sel = safe_input(f"\n[bold {BRIGHT_COLOR}]Select file(s), 'all', or '0': [/]").strip()
            if sel.strip() == '0':
                continue

            selected = []
            if sel.lower() == 'all':
                selected = files
            else:
                for x in sel.split(','):
                    if x.strip().isdigit():
                        idx = int(x.strip()) - 1
                        if 0 <= idx < len(files):
                            selected.append(files[idx])

            if not selected:
                continue

            luac_path = shutil.which("luac5.3")
            if luac_path is None:
                console.print(Panel(f"[{WARNING}]luac5.3 not found! pkg install lua53 -y[/]", border_style=ERROR))
                safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")
                continue

            ok = 0
            for f in selected:
                try:
                    out_file = compile_out / f"{f.stem}.lua"
                    console.print(f"\n[bold {BRIGHT_COLOR}]Compiling: {f.name}...[/]")

                    if f.suffix == '.lua':
                        temp_luac = compile_out / f"{f.stem}.std.luac"
                        result = subprocess.run(
                            ["luac5.3", "-o", str(temp_luac), str(f)],
                            capture_output=True, text=True
                        )
                        if result.returncode != 0 or not temp_luac.exists():
                            err = result.stderr.strip() or "luac5.3 failed"
                            console.print(Panel(f"[{ERROR}]FAILED: {f.name}\n{err[:300]}[/]", border_style=ERROR))
                            continue
                        process_file = temp_luac
                    else:
                        process_file = f

                    with open(process_file, 'rb') as fp:
                        data = fp.read()

                    bgmi_data = process_lua_file(data, is_encrypt=True)

                    with open(out_file, 'wb') as fp:
                        fp.write(bgmi_data)

                    if f.suffix == '.lua' and process_file.exists():
                        process_file.unlink()

                    if out_file.exists() and out_file.stat().st_size > 0:
                        ok += 1
                        size = out_file.stat().st_size
                        console.print(Panel(
                            f"[bold {BRIGHT_COLOR}]COMPILED: {f.name} → {out_file.name} ({size:,} bytes)[/]",
                            border_style=BORDER_COLOR, box=HEAVY_EDGE
                        ))
                except Exception as e:
                    console.print(Panel(f"[{ERROR}]Error: {f.name} - {e}[/]", border_style=ERROR))

            console.print()
            if ok > 0:
                console.print(Panel(
                    f"[bold {BRIGHT_COLOR}]{ok}/{len(selected)} files compiled![/]\n"
                    f"[bold {BRIGHT_COLOR}]Output:[/] [bold {TEXT_COLOR}]{compile_out}[/]",
                    border_style=BORDER_COLOR, box=DOUBLE_EDGE
                ))
            else:
                console.print(Panel(f"[{WARNING}]No files compiled.[/]", border_style=WARNING))

            safe_input(f"\n[bold {BRIGHT_COLOR}]Press Enter...[/]")

        elif choice == "0":
            return

WORK_DIR_BLACK = ""
MODIFIED_DIR_BLACK = ""

TARGET_GROUPS = {
    "1. MATCH START & THEME": [
        "Match starts in <MatchStartInfo>{0}</>", "Match starts in",
        "Your match starts in", "Bonus Challenge match starts",
        "LEAN (BGMI 2026 Theme Song)"
    ],
    "2. CHICKEN DINNER": [
        "WINNER WINNER CHICKEN DINNER!", "WINNER WINNER CHICKEN DINNER",
        "Winner Winner Chicken Dinner", "Winner winner chicken dinner"
    ],
    "3. BETTER LUCK NEXT TIME": [
        "Better Luck Next Time", "BETTER LUCK NEXT TIME"
    ],
    "4. TEAMMATE DAMAGE WARNINGS": [
        "As you attacked your teammate first",
        "As you have maliciously injured your teammate"
    ],
    "5. QUICK CHAT MESSAGES": [
        "Watch your aim and finish them off!",
        "Get behind the wheel and crush them!"
    ],
    "6. BAN PAN SECURITY": [
        "Ban Pan", "Ban Pan - Pan", "BGMI & Ban Pan"
    ],
    "7. SPLASH SCREEN WARNING": [
        "Battlegrounds Mobile India is not a real-world based game"
    ],
    "8. HOME ISLE NOTIFICATIONS": [
        "Home Isle is an island located in the ocean",
        "Now, let me briefly explain removing objects",
        "Lastly, here's an important tip",
        "It's important to note that once you finish building",
        "Your time spent working on your Home has reached a new milestone!",
        "This past year witnessed our growth and progress",
        "There are so many beautiful moments we have shared together."
    ],
    "9. GAME EVENTS & UI": [
        "Sara is a vehicle expert",
        "Vehicle weapons will automatically lock",
        "Try out the DJ stage",
        "You have collected 3 vehicle finishes",
        "Clan Battle is about to start",
        "Try the smart Digi-pal chat",
        "Too many PvE enemy eliminations",
        "Synergy: Some Popularity gifts",
        "Win battles with your friends",
        "The Aerolith has begun absorbing mutants",
        "8. If you have any questions regarding payment",
        "Myriad splendors glazed"
    ]
}

def black_tool_ensure_work_dir():
    global WORK_DIR_BLACK, MODIFIED_DIR_BLACK

    for d in [WORK_DIR_BLACK, MODIFIED_DIR_BLACK]:
        if d and not os.path.exists(d):
            try:
                os.makedirs(d)
            except Exception as e:
                console.print(f"[red]Cannot create directory {d}: {e}[/red]")
                return

def black_tool_list_files_in_dir(extensions=('.uasset', '.uexp')):
    try:
        if not os.path.exists(WORK_DIR_BLACK):
            black_tool_ensure_work_dir()
        all_files = os.listdir(WORK_DIR_BLACK)
        target_files = [f for f in all_files if f.lower().endswith(extensions)]
        target_files.sort()
        return target_files
    except Exception as e:
        console.print(f"[red]Error reading directory: {e}[/red]")
        return []

class UE4StringTool:
    def __init__(self):
        self.MIN_STRING_LEN = 2
        self.MAX_STRING_LEN = 8000

    def read_int(self, f):
        data = f.read(4)
        if len(data) < 4:
            return None
        return struct.unpack('<i', data)[0]

    def is_garbage_text(self, text):
        if not text or len(text.strip()) == 0:
            return True
        allowed_control = {'\n', '\r', '\t'}
        for char in text:
            code = ord(char)
            if code == 0:
                return True
            if code < 32 and char not in allowed_control:
                return True
            if char == '\ufffd':
                return True
        return False

    def is_valid_string_start(self, f, current_pos):
        f.seek(current_pos)
        length = self.read_int(f)
        if length is None:
            return False
        if length == 0:
            return False
        if not (self.MIN_STRING_LEN <= abs(length) <= self.MAX_STRING_LEN):
            return False
        try:
            if length < 0:
                read_len = -length * 2
                data = f.read(read_len)
                if len(data) != read_len:
                    return False
                if data[-2:] != b'\x00\x00':
                    return False
                text = data[:-2].decode('utf-16le')
            else:
                read_len = length
                data = f.read(read_len)
                if len(data) != read_len:
                    return False
                if data[-1:] != b'\x00':
                    return False
                text = data[:-1].decode('utf-8')
            if self.is_garbage_text(text):
                return False
            return True
        except Exception:
            return False

    def extract_file(self, file_name):
        file_path = os.path.join(WORK_DIR_BLACK, file_name)
        if not os.path.exists(file_path):
            return False, f"File not found: {file_name}"

        json_path = file_path + ".json"
        console.print(f"\n[bold {BRIGHT_COLOR}]Create JSON: {file_name}[/]")

        try:
            with open(file_path, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                f.seek(0)

                entries = []
                cursor = 0

                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                              BarColumn(), console=console) as progress:
                    task = progress.add_task("[cyan]Extracting strings...", total=file_size)

                    while cursor < file_size - 4:
                        progress.update(task, completed=cursor)

                        if self.is_valid_string_start(f, cursor):
                            f.seek(cursor)
                            length = self.read_int(f)
                            is_utf16 = length < 0
                            abs_len = abs(length)

                            if is_utf16:
                                raw_data = f.read(abs_len * 2)
                                text = raw_data[:-2].decode('utf-16le')
                                total_size = 4 + (abs_len * 2)
                            else:
                                raw_data = f.read(abs_len)
                                text = raw_data[:-1].decode('utf-8')
                                total_size = 4 + abs_len

                            entries.append({
                                "offset": cursor,
                                "original_len_int": length,
                                "text": text
                            })
                            cursor += total_size
                        else:
                            cursor += 1

                if not entries:
                    return False, "No valid text strings found."

                with open(json_path, 'w', encoding='utf-8') as jf:
                    json.dump(entries, jf, indent=4, ensure_ascii=False)

            return True, f"Exported {len(entries)} strings -> {os.path.basename(json_path)}"
        except Exception as e:
            return False, str(e)

    def repack_file(self, file_name):
        original_file_path = os.path.join(WORK_DIR_BLACK, file_name)
        json_path = original_file_path + ".json"

        if not os.path.exists(original_file_path):
            return False, f"Missing original file: {file_name}"
        if not os.path.exists(json_path):
            return False, f"Missing file: {file_name}.json"

        modified_file_path = os.path.join(MODIFIED_DIR_BLACK, file_name)
        console.print(f"[bold {BRIGHT_COLOR}]Repacking: {file_name}...[/]")

        try:
            with open(json_path, 'r', encoding='utf-8') as jf:
                entries = json.load(jf)
            entries.sort(key=lambda x: x['offset'])

            with open(original_file_path, 'rb') as f_orig, open(modified_file_path, 'wb') as f_out:
                cursor_orig = 0
                count_modified = 0

                for i, entry in enumerate(entries):
                    gap_size = entry['offset'] - cursor_orig
                    if gap_size > 0:
                        f_out.write(f_orig.read(gap_size))
                    elif gap_size < 0:
                        f_orig.seek(entry['offset'])

                    new_text = entry['text']
                    old_len_int = entry['original_len_int']
                    is_utf16 = old_len_int < 0

                    if is_utf16:
                        max_byte_size = abs(old_len_int) * 2
                    else:
                        max_byte_size = abs(old_len_int)

                    f_orig.seek(entry['offset'] + 4)
                    old_raw_display = f_orig.read(max_byte_size)

                    try:
                        if is_utf16:
                            old_text_display = old_raw_display[:-2].decode('utf-16le')
                        else:
                            old_text_display = old_raw_display[:-1].decode('utf-8')
                    except Exception:
                        old_text_display = "<Decode error>"

                    if new_text != old_text_display:
                        count_modified += 1

                    if is_utf16:
                        new_bytes = new_text.encode('utf-16le') + b'\x00\x00'
                    else:
                        new_bytes = new_text.encode('utf-8') + b'\x00'

                    current_byte_size = len(new_bytes)

                    if current_byte_size > max_byte_size:
                        console.print(f"\n[bold {ERROR}]CRITICAL ERROR AT LINE {i+1} (Offset: {entry['offset']})[/]")
                        console.print(f"[bold {ERROR}]New string longer than original ({current_byte_size} > {max_byte_size} bytes)[/]")
                        f_out.close()
                        f_orig.close()
                        if os.path.exists(modified_file_path):
                            os.remove(modified_file_path)
                        return False, "New string length exceeds original string length."

                    f_out.write(struct.pack('<i', old_len_int))
                    f_out.write(new_bytes)

                    pad_len = max_byte_size - current_byte_size
                    if pad_len > 0:
                        f_out.write(b'\x00' * pad_len)

                    f_orig.seek(entry['offset'])
                    len_check = self.read_int(f_orig)
                    skip_len = 4 + (abs(len_check) * 2 if len_check < 0 else abs(len_check))
                    f_orig.seek(entry['offset'] + skip_len)
                    cursor_orig = f_orig.tell()

                f_out.write(f_orig.read())

            return True, f"Updated {count_modified} lines -> {os.path.basename(modified_file_path)}"
        except Exception as e:
            return False, str(e)

def get_live_input_match_start(prompt_text):
    import sys as _s
    _s.stdout.write(prompt_text)
    _s.stdout.flush()
    input_str = ""

    while True:
        try:
            fd = _s.stdin.fileno()
            import termios
            import tty
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(_s.stdin.fileno())
                ch = _s.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            ch = input()[0] if input() else '\r'

        if ch == '\r':
            print()
            break
        elif ch == '\x7f':
            if len(input_str) > 0:
                input_str = input_str[:-1]
        else:
            input_str += ch

        _s.stdout.write('\r' + ' ' * (len(prompt_text) + len(input_str) + 15) + '\r')
        _s.stdout.write(prompt_text)
        display = input_str
        _s.stdout.write(f"\033[93m{display}\033[0m")
        _s.stdout.flush()

    return input_str

def black_tool_do_unpack_fancy(tool):
    console.clear()
    print_banner()
    console.print(Panel(
        f"[bold {BRIGHT_COLOR}]MASTER UNPACK (ALL FILES)[/]\n"
        f"[dim {DIM_COLOR}]Extracting all UEXP/UASSET files to JSON at once...[/dim {DIM_COLOR}]",
        border_style=BORDER_COLOR
    ))

    files = black_tool_list_files_in_dir(('.uasset', '.uexp'))
    if not files:
        console.print(Panel(f"[{ERROR}]No files found to unpack![/]", border_style=ERROR))
        safe_input(f"\n[bold {TEXT_COLOR}]Press Enter to continue...[/]")
        return

    unpacked_count = 0
    console.print(f"\n[bold {BRIGHT_COLOR}]Auto-Unpacking all files...[/]")

    for fname in files:
        success, msg = tool.extract_file(fname)
        if success:
            console.print(f"[bold {BRIGHT_COLOR}]SUCCESS:[/] {fname}")
            unpacked_count += 1
        else:
            console.print(f"[bold {ERROR}]FAILED:[/] {fname}\n   [dim]{msg}[/dim]")

    console.print("\n")
    if unpacked_count > 0:
        console.print(Panel(
            f"[bold {BRIGHT_COLOR}]ALL DONE! {unpacked_count} files unpacked successfully.[/]\n"
            f"[white]JSON files created in ORGNAL folder.[/white]",
            border_style=BORDER_COLOR
        ))
    else:
        console.print(Panel(f"[{WARNING}]No files were unpacked.[/]", border_style=WARNING))

    safe_input("\n[bold white]Press Enter to continue...[/bold white]")

def black_tool_do_repack_fancy(tool):
    console.clear()
    print_banner()
    console.print(Panel(
        f"[bold {BRIGHT_COLOR}]MASTER REPACK (ALL FILES)[/]\n"
        f"[dim {DIM_COLOR}]Converting all JSON back to UEXP at once...[/dim {DIM_COLOR}]",
        border_style=BORDER_COLOR
    ))

    files = black_tool_list_files_in_dir(('.uasset', '.uexp'))
    if not files:
        console.print(Panel(f"[{ERROR}]No files found to repack![/]", border_style=ERROR))
        safe_input(f"\n[bold white]Press Enter to continue...[/bold white]")
        return

    repacked_count = 0
    repacked_files_list = []

    console.print(f"\n[bold {BRIGHT_COLOR}]Auto-Repacking all files...[/]")

    for fname in files:
        json_path = os.path.join(WORK_DIR_BLACK, fname + ".json")
        if os.path.exists(json_path):
            success, msg = tool.repack_file(fname)
            if success:
                console.print(f"[bold {BRIGHT_COLOR}]SUCCESS:[/] {fname}")
                repacked_count += 1
                repacked_files_list.append(fname)
            else:
                console.print(f"[bold {ERROR}]FAILED:[/] {fname}\n   [dim]{msg}[/dim]")
        else:
            console.print(f"[dim {WARNING}]Skipped (No JSON): {fname}[/]")

    console.print("\n")
    if repacked_count > 0:
        console.print(Panel(
            f"[bold {BRIGHT_COLOR}]ALL DONE! {repacked_count} files repacked![/]\n"
            f"[white]Files are in MODDED FILE folder.[/white]",
            border_style=BORDER_COLOR
        ))

        copy_choice = safe_input(
            f"\n[bold {WARNING}]Copy to 'Modified_files' and 'MOD_REPACK'? (y/n): [/]"
        ).strip().lower()

        if copy_choice == 'y':
            base_dir = Path("PSYCO TOOL")
            target_modified = base_dir / "OBB_UNPACKER" / "Modified_files"
            target_enc_open = base_dir / "ANTIRESET_OBB" / "MOD_REPACK"

            os.makedirs(to_long_path(target_modified), exist_ok=True)
            os.makedirs(to_long_path(target_enc_open), exist_ok=True)

            copied_mod = 0
            copied_enc = 0

            for fname in repacked_files_list:
                src = os.path.join(MODIFIED_DIR_BLACK, fname)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(target_modified, fname))
                    copied_mod += 1
                    shutil.copy2(src, os.path.join(target_enc_open, fname))
                    copied_enc += 1

            if copied_mod > 0:
                console.print(f"\n[bold {BRIGHT_COLOR}]{copied_mod} files copied to 'Modified_files'![/]")
            if copied_enc > 0:
                console.print(f"[bold {BRIGHT_COLOR}]{copied_enc} files copied to 'MOD_REPACK'![/]")

    else:
        console.print(Panel(f"[{WARNING}]No files were repacked.[/]", border_style=WARNING))

    safe_input("\n[bold white]Press Enter to continue...[/bold white]")

def black_tool_do_custom_edit_fancy(tool):
    print_banner()
    json_files = [f for f in os.listdir(WORK_DIR_BLACK) if f.endswith('.json')]

    if not json_files:
        console.print(f"[red]No JSON files found![/red]")
        safe_input("\n[bold white]Press Enter...[/bold white]")
        return

    for j_file in json_files:
        json_path = os.path.join(WORK_DIR_BLACK, j_file)
        with open(json_path, 'r', encoding='utf-8') as f:
            entries = json.load(f)

        for group_name, keywords in TARGET_GROUPS.items():
            matching_entries = [e for e in entries if any(kw in e['text'] for kw in keywords)]

            if matching_entries:
                console.print(f"\n[bold cyan]Target:[/] [white]{group_name}[/]")

                if "1. MATCH START" in group_name:
                    try:
                        new_text = get_live_input_match_start(f" \033[1;32mENTER YELLOW TEXT > \033[0m")
                    except Exception:
                        new_text = Prompt.ask(f"[bold {BRIGHT_COLOR}]Enter text[/]")
                else:
                    new_text = Prompt.ask(f"[bold {BRIGHT_COLOR}]Enter normal text[/]")

                if new_text and new_text.strip():
                    processed_text = new_text
                    if "1. MATCH START" in group_name:
                        if "[" in processed_text and "]" in processed_text:
                            parts = processed_text.split("[", 1)
                            pre = parts[0]
                            inner_post = parts[1].split("]", 1)
                            inner = inner_post[0]
                            post = inner_post[1] if len(inner_post) > 1 else ""
                            processed_text = f"{pre}[ <MatchStartInfo>{inner}</>]{post}"
                        else:
                            processed_text = f"<MatchStartInfo>{processed_text}</>"

                    for e in matching_entries:
                        e_max = abs(e['original_len_int'])
                        e['text'] = processed_text[:e_max - 1]

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=4, ensure_ascii=False)

    console.print(Panel(f"[bold {BRIGHT_COLOR}]ALL DONE: Targeted Modding Complete![/]", border_style=BORDER_COLOR))
    safe_input("\nPress Enter to continue...")

def black_tool_main(auto_select_file="mini_obb.pak"):
    global WORK_DIR_BLACK, MODIFIED_DIR_BLACK

    WORK_DIR_BLACK = str(Path("PSYCO TOOL") / "CREDIT_TOOL" / "ORGNAL")
    MODIFIED_DIR_BLACK = str(Path("PSYCO TOOL") / "CREDIT_TOOL" / "MODDED FILE")

    black_tool_ensure_work_dir()

    REQUIRED_FILES = ["LocalizationText_en.uexp", "SplashScreen_BH.uexp"]
    missing_files = [
        f for f in REQUIRED_FILES
        if not os.path.exists(os.path.join(WORK_DIR_BLACK, f))
        or os.path.getsize(os.path.join(WORK_DIR_BLACK, f)) == 0
    ]

    if missing_files:
        console.print(f"\n[bold {WARNING}]Missing files in ORGNAL: {', '.join(missing_files)}[/]")
        obb_folder = Path("PSYCO TOOL") / "OBB_UNPACKER" / "ORGNAL"

        pak_files = []
        if obb_folder.exists():
            pak_files = [
                f for f in obb_folder.iterdir()
                if f.is_file() and f.suffix.lower() in ('.pak', '.obb')
            ]

        if pak_files:
            target_index = -1
            if auto_select_file:
                for i, p in enumerate(pak_files):
                    if p.name.lower() == auto_select_file.lower():
                        target_index = i
                        break

            if target_index != -1:
                pak_path = pak_files[target_index]
                console.print(f"[bold {BRIGHT_COLOR}]AUTO-SELECTING:[/] [white]{pak_path.name}[/white]")
            else:
                for i, p in enumerate(pak_files, 1):
                    console.print(f"  [{BRIGHT_COLOR}]{i}.[/] {p.name}")

                pick = safe_input(f"[bold {BRIGHT_COLOR}]Select OBB/PAK (1-{len(pak_files)}): [/]").strip()
                try:
                    pak_path = pak_files[int(pick) - 1]
                except (ValueError, IndexError):
                    pak_path = pak_files[0]

            console.print(f"\n[bold {BRIGHT_COLOR}]PRO EXTRACTION: Scanning {pak_path.name}...[/]")
            try:
                pak = TencentPakFile(pak_path, silent=True)
                for target_file in missing_files:
                    candidates = []
                    for dir_path, dir_entries in pak._index.items():
                        for fname, entry in dir_entries.items():
                            if fname.lower() == target_file.lower() and entry is not None:
                                candidates.append(entry)
                    if candidates:
                        candidates.sort(key=lambda x: x.size, reverse=True)
                        for entry in candidates:
                            target_dest = Path(WORK_DIR_BLACK) / target_file
                            pak._write_to_disk(target_dest, entry)
                            if os.path.getsize(target_dest) > 1024:
                                console.print(f"[bold {BRIGHT_COLOR}]EXTRACT SUCCESS:[/] {target_file}")
                                break
            except Exception as e:
                console.print(f"[red]Error parsing OBB: {e}[/red]")

            safe_input("\n[bold white]Press Enter to continue...[/bold white]")
        else:
            console.print(f"[bold {ERROR}]No OBB found in {obb_folder}![/]")
            safe_input("\n[bold white]Press Enter...[/bold white]")

    tool = UE4StringTool()

    while True:
        print_banner()

        menu_table = Table(show_header=False, box=SIMPLE, expand=True)
        menu_table.add_column("OPT", style="bold white", justify="center", width=4)
        menu_table.add_column("COMMAND", style=f"bold {BRIGHT_COLOR}")
        menu_table.add_column("DESC", style="dim white")
        menu_table.add_row("1", "UNPACK", "UEXP to JSON")
        menu_table.add_row("2", "REPACK", "JSON to UEXP")
        menu_table.add_row("3", "MASTER CUSTOM EDIT", "Live Color Edit")
        menu_table.add_row("4", "BACK", "Back to Main Menu")

        console.print(Panel(menu_table, border_style=BORDER_COLOR, box=HEAVY_EDGE,
                            title=f"[bold black on {BRIGHT_COLOR}] TEXT RESONANCE LAB [/]"))

        choice = safe_input(f"[bold {BRIGHT_COLOR}]Select option > [/]").strip()

        if choice == '1':
            black_tool_do_unpack_fancy(tool)
        elif choice == '2':
            black_tool_do_repack_fancy(tool)
        elif choice == '3':
            black_tool_do_custom_edit_fancy(tool)
        elif choice == '4':
            return
        else:
            console.print(f"[{ERROR}]Invalid![/]")
            time.sleep(1)

_PT_R = "\033[0m"
_PT_B = "\033[1m"
_PT_D = "\033[2m"

def _pt_rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

_PT_PAL = {
    'pp': [(147, 51, 234), (219, 39, 119)],
    'fire': [(255, 94, 0), (255, 215, 0)],
    'ocean': [(0, 180, 255), (90, 255, 200)],
    'neon': [(0, 255, 200), (255, 0, 200)],
    'rainbow': [(255, 0, 100), (255, 200, 0), (0, 255, 150), (0, 150, 255), (180, 0, 255)],
}

def _pt_interp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def pt_grad(text, pal='pp', bold=True):
    if not text:
        return ''
    p = _PT_PAL[pal]
    n = max(len(text) - 1, 1)
    sc = len(p) - 1
    out = []
    for i, ch in enumerate(text):
        t = i / n
        seg = min(int(t * sc), sc - 1)
        lt = t * sc - seg
        r, g, b = _pt_interp(p[seg], p[seg + 1], lt)
        out.append((_PT_B if bold else '') + _pt_rgb(r, g, b) + ch)
    return ''.join(out) + _PT_R

def pt_grad_multi(*lines, pal='rainbow', bold=True):
    chars = []
    for ln in lines:
        chars.extend(ln)
        chars.append('\n')
    total = max(len(chars) - 1, 1)
    p = _PT_PAL[pal]
    sc = len(p) - 1
    out = []
    for i, ch in enumerate(chars):
        if ch == '\n':
            out.append(ch)
            continue
        t = i / total
        seg = min(int(t * sc), sc - 1)
        lt = t * sc - seg
        r, g, b = _pt_interp(p[seg], p[seg + 1], lt)
        out.append((_PT_B if bold else '') + _pt_rgb(r, g, b) + ch)
    return ''.join(out) + _PT_R

def pt_ok(m):   print(f"  \033[38;2;0;255;150m{_PT_B}\u2713{_PT_R}  \033[38;2;120;255;180m{m}{_PT_R}")
def pt_err(m):  print(f"  \033[38;2;255;80;80m{_PT_B}\u2717{_PT_R}  \033[38;2;255;150;150m{m}{_PT_R}")
def pt_warn(m): print(f"  \033[38;2;255;180;0m{_PT_B}!{_PT_R}  \033[38;2;255;210;120m{m}{_PT_R}")
def pt_info(m): print(f"  \033[38;2;100;200;255m{_PT_B}i{_PT_R}  \033[38;2;160;220;255m{m}{_PT_R}")
def pt_step(m): print(f"  \033[38;2;180;120;255m\u2192{_PT_R}  \033[38;2;220;180;255m{m}{_PT_R}")
def pt_tip(m):  print(f"  \033[38;2;255;200;0m\u25cf  \033[2;38;2;255;220;120m{m}{_PT_R}")

_PT_BASE = None
_PT_ENC = None
_PT_RES = None
_PT_INP = None
_PT_OUT = None

def pt_setup(base):
    global _PT_BASE, _PT_ENC, _PT_RES, _PT_INP, _PT_OUT
    _PT_BASE = base / 'PYTHON TOOL'
    _PT_ENC = _PT_BASE / 'encrypt'
    _PT_RES = _PT_BASE / 'result'
    _PT_INP = _PT_BASE / 'input'
    _PT_OUT = _PT_BASE / 'output'
    for d in (_PT_ENC, _PT_RES, _PT_INP, _PT_OUT):
        d.mkdir(parents=True, exist_ok=True)

def _pt_files(folder):
    if not folder.exists():
        return []
    return [f for f in sorted(folder.iterdir()) if f.is_file()]

def pt_pick(folder, prompt):
    fs = _pt_files(folder)
    if not fs:
        print()
        pt_warn(f"'{folder.name}/' folder empty")
        pt_tip(f"Add files here: {folder}")
        return None
    print()
    print(f"  \033[38;2;180;120;255m\u250c\u2500 Files in \033[38;2;120;220;255m{folder.name}/\033[38;2;180;120;255m \u2500\u2500\u2500\u2500\u2500\u2500\033[0m")
    for i, f in enumerate(fs, 1):
        size = f.stat().st_size
        num = "\033[38;2;0;255;150m" if i % 3 == 1 else "\033[38;2;100;200;255m" if i % 3 == 2 else "\033[38;2;255;120;200m"
        print(f"  {num}{_PT_B}[{i}]{_PT_R}  \033[38;2;240;240;240m{f.name}{_PT_R}  \033[2;38;2;150;150;150m({size:,} bytes){_PT_R}")
    print(f"  \033[38;2;255;80;80m{_PT_B}[0]{_PT_R}  \033[2;38;2;180;180;180m\u21a9  Cancel{_PT_R}")
    print(f"  \033[38;2;180;120;255m\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\033[0m")
    print()
    while True:
        try:
            ch = input(f"  \033[38;2;120;220;255m{_PT_B}{prompt} {_PT_R}\033[2;38;2;150;150;150m[1-{len(fs)}]{_PT_R}\033[38;2;120;220;255m \u25b8 {_PT_R}").strip()
            if ch in ('', '0'):
                return None
            idx = int(ch) - 1
            if 0 <= idx < len(fs):
                return fs[idx]
        except (ValueError, KeyboardInterrupt):
            pass
        pt_err("Wrong choice, try again")

def _pt_obf(k):
    return [b ^ ((i * 7 + 0x5A) & 0xFF) for i, b in enumerate(k)]

_PT_STUB = '''#!/usr/bin/env python3
import sys, base64, zlib
try:
    from Crypto.Cipher import AES
except ImportError:
    print("[Premium Vault] pip install pycryptodome")
    sys.exit(1)

_K = __KEY__
_D = """__DATA__"""

def _run():
    key = bytes((b ^ ((i*7 + 0x5A) & 0xFF)) & 0xFF for i, b in enumerate(_K))
    data = base64.b64decode("".join(_D.split()))
    nonce, tag, ct = data[:12], data[12:28], data[28:]
    c = AES.new(key, AES.MODE_GCM, nonce=nonce)
    raw = zlib.decompress(c.decrypt_and_verify(ct, tag))
    code = compile(raw, "<protected>", "exec")
    ns = {"__name__": "__main__", "__file__": __file__, "__package__": None}
    exec(code, ns, ns)

if __name__ == "__main__":
    _run()
'''

def pt_encrypt_file(raw):
    key = _ptrand(32)
    nonce = _ptrand(12)
    cipher = _ptAES.new(key, _ptAES.MODE_GCM, nonce=nonce)
    compressed = zlib.compress(raw, 9)
    ct, tag = cipher.encrypt_and_digest(compressed)
    payload = nonce + tag + ct
    b64 = base64.b64encode(payload).decode('ascii')
    chunks = "\n".join(b64[i:i + 76] for i in range(0, len(b64), 76))
    stub = _PT_STUB.replace("__KEY__", repr(_pt_obf(key))).replace("__DATA__", chunks)
    return stub.encode('utf-8')

_PT_PYC_MAGICS = {
    b"\x33\x0d\x0d\x0a": "3.6", b"\x42\x0d\x0d\x0a": "3.7",
    b"\x55\x0d\x0d\x0a": "3.8", b"\x61\x0d\x0d\x0a": "3.9",
    b"\x6f\x0d\x0d\x0a": "3.10", b"\xa7\x0d\x0d\x0a": "3.11",
    b"\xcb\x0d\x0d\x0a": "3.12", b"\xf3\x0d\x0d\x0a": "3.13",
}

def pt_is_pyc(b):
    return len(b) >= 4 and b[2:4] == b"\r\n"

def pt_pyc_ver(b):
    for m, v in _PT_PYC_MAGICS.items():
        if b[:4] == m:
            return v
    return "unknown"

def pt_m_pycdc(src):
    for p in [Path.home() / "pycdc" / "pycdc", Path("/usr/local/bin/pycdc"), Path("/usr/bin/pycdc")]:
        if p.exists():
            try:
                r = subprocess.run([str(p), str(src)], capture_output=True, text=True, timeout=60)
                if r.stdout and len(r.stdout) > 100:
                    return r.stdout, None
                return None, "pycdc produced no output"
            except subprocess.TimeoutExpired:
                return None, "timeout"
            except Exception as e:
                return None, str(e)
    return None, "pycdc not installed"

def pt_m_marshal(src):
    try:
        blob = src.read_bytes()
        for hdr in (16, 12, 8):
            try:
                code = _ptmarshal.loads(blob[hdr:])
                lines = ["# Premium Vault Disassembly Output", f"# File: {src.name}", ""]
                def walk(c, d=0):
                    ind = "    " * d
                    lines.append(f"{ind}### Function: {c.co_name}")
                    lines.append(f"{ind}# Args: {c.co_argcount}")
                    lines.append(f"{ind}# Line: {c.co_firstlineno}")
                    if c.co_consts:
                        lines.append(f"{ind}# Constants:")
                        for con in c.co_consts:
                            if isinstance(con, str) and len(con) > 0:
                                lines.append(f"{ind}#   STR: {repr(con[:80])}")
                            elif isinstance(con, (int, float)):
                                lines.append(f"{ind}#   NUM: {con}")
                    if c.co_names:
                        lines.append(f"{ind}# Global refs: {', '.join(c.co_names[:10])}")
                    if c.co_varnames:
                        lines.append(f"{ind}# Vars: {', '.join(c.co_varnames[:10])}")
                    lines.append("")
                    for con in c.co_consts:
                        if hasattr(con, "co_name"):
                            walk(con, d + 1)
                walk(code)
                lines.append("")
                lines.append("=" * 60)
                lines.append("FULL BYTECODE DISASSEMBLY")
                lines.append("=" * 60)
                buf = _ptSIO()
                _ptdis.dis(code, file=buf)
                lines.append(buf.getvalue())
                return "\n".join(lines), None
            except Exception:
                continue
        return None, "marshal load failed"
    except Exception as e:
        return None, str(e)

def pt_m_psyco(text):
    m1 = _ptre.search(r"_K\s*=\s*(\[[^\]]*\])", text)
    m2 = _ptre.search(r'_D\s*=\s*"""(.*?)"""', text, _ptre.DOTALL)
    if not m1 or not m2:
        return None, "not Premium Vault format"
    try:
        kd = _ptast.literal_eval(m1.group(1))
        key = bytes((b ^ ((i * 7 + 0x5A) & 0xFF)) & 0xFF for i, b in enumerate(kd))
        data = base64.b64decode("".join(m2.group(1).split()))
        n, t, c = data[:12], data[12:28], data[28:]
        raw = zlib.decompress(_ptAES.new(key, _ptAES.MODE_GCM, nonce=n).decrypt_and_verify(c, t))
        return raw.decode('utf-8'), None
    except Exception as e:
        return None, str(e)

def pt_m_b64_zlib(blob):
    try:
        text = blob.decode('ascii', errors='ignore')
        for block in _ptre.findall(r"[A-Za-z0-9+/=]{80,}", text):
            try:
                decoded = base64.b64decode(block)
                try:
                    raw = zlib.decompress(decoded)
                    return raw.decode('utf-8', errors='ignore'), None
                except Exception:
                    pass
            except Exception:
                pass
    except Exception:
        pass
    return None, "no base64+zlib"

def pt_m_xor(blob):
    kws = [b"import ", b"def ", b"class ", b"print(", b"return "]
    for k in range(1, 256):
        s = bytes(b ^ k for b in blob[:8192])
        for kw in kws:
            if kw in s:
                return bytes(b ^ k for b in blob).decode('utf-8', errors='ignore'), None
    return None, "no xor key"

def pt_m_strings(blob):
    try:
        strings = _ptre.findall(rb"[\x20-\x7e]{4,}", blob)
        lines = ["# Premium Vault Extracted Strings", f"# {len(strings)} strings found", ""]
        for s in strings:
            try:
                t = s.decode('utf-8', errors='ignore').strip()
                if t:
                    lines.append(f"# {t}")
            except Exception:
                pass
        return "\n".join(lines), None
    except Exception as e:
        return None, str(e)

def pt_do_encrypt():
    print()
    print("  " + pt_grad("\u256d\u2500 \U0001F512  ENCRYPT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", 'ocean'))
    print()
    if not _PT_CRYPTO_OK:
        pt_err("pycryptodome missing  ->  pip install pycryptodome")
        return
    src = pt_pick(_PT_ENC, "Choose a file")
    if not src:
        return
    if src.suffix.lower() != '.py':
        pt_err("Only .py files supported")
        return
    pt_step(f"Reading \033[38;2;240;240;240m{src.name}{_PT_R}...")
    raw = src.read_bytes()
    pt_step(f"Encrypting \033[38;2;255;200;0m{len(raw):,}{_PT_R} bytes...")
    out_data = pt_encrypt_file(raw)
    out = _PT_RES / src.name
    out.write_bytes(out_data)
    try:
        out.chmod(0o755)
    except OSError:
        pass
    print()
    pt_ok(f"Encrypted : \033[1;38;2;240;240;240m{src.name}{_PT_R}  \u2192  \033[38;2;120;220;255mresult/{out.name}{_PT_R}")
    pt_info(f"Size      : {len(raw):,} \u2192 \033[38;2;255;200;0m{len(out_data):,}{_PT_R} bytes")
    print()
    print("  " + pt_grad("\u256d\u2500 \u25b6  HOW TO RUN \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", 'neon'))
    print(f"  \033[38;2;0;255;200m$\033[0m \033[38;2;240;240;240mpython \"PYTHON TOOL/result/{out.name}\"{_PT_R}")
    print(f"  \033[2;38;2;180;180;180m    (no password required){_PT_R}")
    print("  " + pt_grad("\u2570\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", 'neon'))

def pt_do_decrypt():
    print()
    print("  " + pt_grad("\u256d\u2500 \U0001F513  DECRYPT \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", 'fire'))
    print()
    src = pt_pick(_PT_INP, "Choose a file")
    if not src:
        return
    blob = src.read_bytes()
    out_file = _PT_OUT / (src.stem + "_decrypted.py")
    pt_info(f"Size: {len(blob):,} bytes")
    print()
    print(f"  {pt_grad('Trying methods...', 'neon', bold=False)}")
    content = None
    if pt_is_pyc(blob):
        ver = pt_pyc_ver(blob)
        pt_info(f"Type: Python bytecode (.pyc, Python {ver})")
        pt_step("1) pycdc decompiler")
        content, err = pt_m_pycdc(src)
        if content:
            pt_ok("Decompiled with pycdc")
        else:
            pt_info(f"   Failed: {err}")
            pt_step("2) marshal + disassembly")
            content, err = pt_m_marshal(src)
            if content:
                pt_ok("Disassembly successful")
            else:
                pt_info(f"   Failed: {err}")
                pt_step("3) String extraction (last resort)")
                content, err = pt_m_strings(blob)
                if content:
                    pt_ok("Strings extracted")
    else:
        text = blob.decode('utf-8', errors='ignore')
        pt_step("1) Premium Vault decrypt")
        content, err = pt_m_psyco(text)
        if content:
            pt_ok("Premium Vault decrypted")
        else:
            pt_info(f"   Failed: {err}")
            pt_step("2) Base64 + zlib")
            content, err = pt_m_b64_zlib(blob)
            if content:
                pt_ok("Base64+zlib decoded")
            else:
                pt_info(f"   Failed: {err}")
                pt_step("3) XOR brute force")
                content, err = pt_m_xor(blob)
                if content:
                    pt_ok("XOR decoded")
                else:
                    pt_info(f"   Failed: {err}")
                    pt_step("4) String extraction")
                    content, err = pt_m_strings(blob)
                    if content:
                        pt_ok("Strings extracted")
    if not content:
        print()
        pt_err("No method worked")
        return
    out_file.write_text(content, encoding='utf-8')
    print()
    pt_ok(f"OUTPUT FILE: \033[38;2;120;220;255moutput/{out_file.name}{_PT_R}")
    pt_info(f"Size: {out_file.stat().st_size:,} bytes")

def pt_do_run():
    print()
    print("  " + pt_grad("\u256d\u2500 \u25b6  TEST RUN \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", 'fire'))
    print()
    src = pt_pick(_PT_RES, "Which file to run?")
    if not src:
        return
    print()
    print(f"  \033[2;38;2;150;150;150m{'\u2500' * 46}{_PT_R}")
    rc = subprocess.call([sys.executable, src.name], cwd=str(src.parent))
    print(f"  \033[2;38;2;150;150;150m{'\u2500' * 46}{_PT_R}")
    if rc == 0:
        pt_ok("Exit code 0 — file ran successfully")
    else:
        pt_warn(f"Exit code: {rc}")

def python_tool_menu(data_path):
    pt_setup(data_path)
    if os.name == 'nt':
        os.system("")
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        b_lines = [
            "\u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2557   \u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2557 ",
            "\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u255a\u2550\u2550\u2588\u2588\u2588\u2554\u255d\u255a\u2588\u2588\u2557 \u2588\u2588\u2554\u255d\u2588\u2588\u2554\u2550\u2550\u2550\u2550\u255d\u2588\u2588\u2554\u2550\u2550\u2550\u2588\u2588\u2557",
            "\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d  \u2588\u2588\u2588\u2554\u255d  \u255a\u2588\u2588\u2588\u2588\u2554\u255d \u2588\u2588\u2551     \u2588\u2588\u2551   \u2588\u2588\u2551",
            "\u2588\u2588\u2554\u2550\u2550\u2550\u255d  \u2588\u2588\u2588\u2554\u255d    \u255a\u2588\u2588\u2554\u255d  \u2588\u2588\u2551     \u2588\u2588\u2551   \u2588\u2588\u2551",
            "\u2588\u2588\u2551     \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557   \u2588\u2588\u2551   \u255a\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u255a\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d",
            "\u255a\u2550\u255d     \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u255d   \u255a\u2550\u255d    \u255a\u2550\u2550\u2550\u2550\u2550\u255d \u255a\u2550\u2550\u2550\u2550\u2550\u255d ",
        ]
        print(pt_grad_multi(*b_lines, pal='rainbow'))
        print("  " + pt_grad("Premium Vault  \u2022  Encrypt + Decrypt", 'pp', bold=False))
        print()
        top = "  \u2554" + "\u2550" * 62 + "\u2557"
        bot = "  \u255a" + "\u2550" * 62 + "\u255d"
        print(pt_grad(top, 'ocean', bold=False))
        print(pt_grad(f"  \u2551  \U0001F4E5 Encrypt : {str(_PT_ENC):<43} \u2551", 'ocean', bold=False))
        print(pt_grad(f"  \u2551  \U0001F4E4 Result  : {str(_PT_RES):<43} \u2551", 'neon', bold=False))
        print(pt_grad(f"  \u2551  \U0001F4E5 Input   : {str(_PT_INP):<43} \u2551", 'fire', bold=False))
        print(pt_grad(f"  \u2551  \U0001F4E4 Output  : {str(_PT_OUT):<43} \u2551", 'pp', bold=False))
        print(pt_grad(bot, 'ocean', bold=False))
        enc = len(_pt_files(_PT_ENC))
        res = len(_pt_files(_PT_RES))
        inp = len(_pt_files(_PT_INP))
        out = len(_pt_files(_PT_OUT))
        def badge(n):
            if n == 0:
                return f"\033[48;2;180;40;40m\033[38;2;255;255;255m {n} {_PT_R}"
            return f"\033[48;2;0;180;120m\033[38;2;0;0;0m{_PT_B} {n} {_PT_R}"
        print()
        print(f"  \033[38;2;180;120;255m\u250c\u2500\u2500\u2500 \033[38;2;255;200;0m{_PT_B}PREMIUM VAULT MENU{_PT_R}\033[38;2;180;120;255m \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\033[0m")
        print(f"  \033[38;2;180;120;255m\u2502{_PT_R}  \U0001F4E5 encrypt/{_PT_R} {badge(enc)}   \U0001F4E4 result/{_PT_R} {badge(res)}   \U0001F4E5 input/{_PT_R} {badge(inp)}   \U0001F4E4 output/{_PT_R} {badge(out)}")
        print(f"  \033[38;2;180;120;255m\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524{_PT_R}")
        print(f"  \033[38;2;180;120;255m\u2502{_PT_R}  {pt_grad('[1]', 'ocean')}  {pt_grad('Encrypt a .py file', 'ocean')}   \033[38;2;0;255;150m\U0001F512\033[0m")
        print(f"  \033[38;2;180;120;255m\u2502{_PT_R}  {pt_grad('[2]', 'fire')}  {pt_grad('Decrypt a file', 'fire')}       \033[38;2;255;94;0m\U0001F513\033[0m")
        print(f"  \033[38;2;180;120;255m\u2502{_PT_R}  {pt_grad('[3]', 'neon')}  {pt_grad('Test-run encrypted', 'neon')}    \033[38;2;0;255;200m\u25b6\033[0m")
        print(f"  \033[38;2;180;120;255m\u2502{_PT_R}  {pt_grad('[0]', 'pp')}  {pt_grad('Back to Main Menu', 'pp')}       \033[38;2;255;80;80m\u2190\033[0m")
        print(f"  \033[38;2;180;120;255m\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518{_PT_R}")
        print()
        try:
            ch = input(f"  {pt_grad('\u27a4 Choose', 'neon')} \033[2;38;2;150;150;150m[0-3]\033[0m {pt_grad('\u25b8', 'neon')} ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return
        try:
            if ch == '1':
                pt_do_encrypt()
            elif ch == '2':
                pt_do_decrypt()
            elif ch == '3':
                pt_do_run()
            elif ch == '0':
                return
            else:
                pt_err("Wrong option, try again")
        except KeyboardInterrupt:
            print()
            pt_warn("Cancelled")
        except Exception as e:
            pt_err(f"Error: {e}")
        print()
        try:
            input(f"  \033[2;38;2;150;150;150m\u23ce  Press Enter to return to menu...{_PT_R}")
        except (KeyboardInterrupt, EOFError):
            return

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')

    banner_lines = [
        "",
        "    ╔══════════════════════════════════════════════════════════════════╗",
        "    ║                                                                  ║",
        "    ║     ██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗ ║",
        "    ║     ██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝ ║",
        "    ║     ██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗   ║",
        "    ║     ██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝   ║",
        "    ║     ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗ ║",
        "    ║      ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ║",
        "    ║                                                                  ║",
        "    ║             ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗     ║",
        "    ║             ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝     ║",
        "    ║             █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗       ║",
        "    ║             ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝       ║",
        "    ║             ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗     ║",
        "    ║             ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝     ║",
        "    ║                                                                  ║",
        "    ║         ╔═══════════════════════════════════════════════╗         ║",
        "    ║         ║  ◆  EXTRACT • FORGE • INJECT • SHIELD  ◆      ║         ║",
        "    ║         ║  ◆  AESTHETIC • PRISM • FORGE • RESONANCE ◆   ║         ║",
        "    ║         ╚═══════════════════════════════════════════════╝         ║",
        "    ║                                                                  ║",
        "    ║                    ✦ UltimateEngine Suite ✦                      ║",
        "    ║                                                                  ║",
        "    ╚══════════════════════════════════════════════════════════════════╝",
        "",
    ]

    banner_text = Text()
    for line in banner_lines:
        if "UltimateEngine" in line:
            banner_text.append(line + "\n", style=f"bold {BRIGHT_COLOR}")
        elif "◆" in line:
            banner_text.append(line + "\n", style=f"bold {GOLD}")
        else:
            banner_text.append(line + "\n", style=f"bold {TEXT_COLOR}")

    glow_panel = Panel(
        Group(
            banner_text,
            Text(""),
            Align.center(Text(f"{get_indian_time()}", style=f"dim {DIM_COLOR}")),
        ),
        border_style=BORDER_COLOR,
        box=DOUBLE_EDGE,
        padding=(0, 2),
        subtitle=f"[bold black on {BRIGHT_COLOR}] READY [/]",
    )
    console.print(glow_panel)
    console.print()

def print_user_profile():
    from datetime import datetime
    now = datetime.now()

    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")
    grid.add_row(
        f"[bold {BRIGHT_COLOR}]Key:[/] [bold {TEXT_COLOR}]LOCAL-BYPASS[/]",
        f"[bold {BRIGHT_COLOR}]Valid for:[/] [bold {TEXT_COLOR}]99999 Days[/]"
    )
    grid.add_row(
        f"[bold {BRIGHT_COLOR}]Expiry:[/] [bold {TEXT_COLOR}]2300-01-01[/]",
        f"[bold {BRIGHT_COLOR}]Edition:[/] [bold {TEXT_COLOR}]UltimateEngine Suite[/]"
    )
    console.print(Panel(
        grid,
        title=f"[bold black on {BRIGHT_COLOR}] VIP ACCOUNT INFO [/]",
        border_style=BORDER_COLOR,
        box=HEAVY_EDGE,
        padding=(0, 1)
    ))

def print_main_menu():
    menu_title = Text()
    menu_title.append(">> ", style=f"bold {BRIGHT_COLOR}")
    menu_title.append("C O M M A N D", style=f"bold {TEXT_COLOR}")
    menu_title.append("   ", style="dim")
    menu_title.append("C E N T E R", style=f"bold {GOLD}")
    menu_title.append(" <<", style=f"bold {BRIGHT_COLOR}")

    options = [
        ("1", "ARCHIVE EXTRACTION",     "Extract all files (S=pause, B=stop)"),
        ("2", "MODULE INJECTION",       "Multi-file inject with paths"),
        ("3", "ARCHIVE RECONSTRUCTION", "Rebuild with any size files"),
        ("4", "TARGETED DEPLOYMENT",    "Add new files to specific path"),
        ("5", "CIPHER SHIELD",          "Re-encrypt all files with SM4"),
        ("6", "ARCHIVE FOUNDRY",        "Build game-ready PAK from signature paths"),
        ("7", "WORKSPACE PURGE",        "Remove extracted folders"),
        ("8", "AESTHETIC STUDIO",       "VIP Aesthetic & Size Fix"),
        ("9", "PRISM ENGINE",           "Advanced Repacking"),
        ("10", "BYTECODE FORGE",        "Lua Decompile / Recompile"),
        ("11", "TEXT RESONANCE LAB",    "UE4 String Editor"),
        ("12", "PREMIUM VAULT",         "Encrypt or Decrypt Python files"),
        ("0", "TERMINATE",              "Close the tool"),
    ]

    menu_content = []
    menu_content.append(Align.center(menu_title))
    menu_content.append(Text(""))
    menu_content.append(Align.center(Text("═" * 60, style=f"dim {BORDER_COLOR}")))
    menu_content.append(Text(""))

    for num, label, desc in options:
        option_text = Text()
        option_text.append("  [", style="dim")
        option_text.append(f"{num:>2}", style=f"bold {BRIGHT_COLOR}")
        option_text.append("]  ", style="dim")
        option_text.append(f"{label}", style=f"bold {TEXT_COLOR}")
        option_text.append("   ", style="dim")
        option_text.append("◆", style=f"bold {GOLD}")
        option_text.append("   ", style="dim")
        option_text.append(desc, style=f"italic {DIM_COLOR}")
        menu_content.append(Align.left(option_text))

    menu_content.append(Text(""))
    menu_content.append(Align.center(Text("═" * 60, style=f"dim {BORDER_COLOR}")))
    menu_content.append(Text(""))

    tip1 = Text()
    tip1.append("Tip: ", style=f"bold {BRIGHT_COLOR}")
    tip1.append("During EXTRACTION press ", style=f"{DIM_COLOR}")
    tip1.append("S", style=f"bold {TEXT_COLOR}")
    tip1.append(" to pause, ", style=f"{DIM_COLOR}")
    tip1.append("B", style=f"bold {ERROR}")
    tip1.append(" to stop", style=f"{DIM_COLOR}")
    menu_content.append(Align.left(tip1))

    tip2 = Text()
    tip2.append("Structure: ", style=f"bold {BRIGHT_COLOR}")
    tip2.append("SKIN_TOOL/ | LUA_TOOL/ | CREDIT_TOOL/ | BUILD_PAK/ | PYTHON TOOL/", style=f"{DIM_COLOR}")
    menu_content.append(Align.left(tip2))

    menu_content.append(Text(""))
    menu_content.append(Align.center(Text("UltimateEngine Suite", style=f"bold {BRIGHT_COLOR}")))

    menu_panel = Panel(
        Group(*menu_content),
        title=f"[bold black on {BRIGHT_COLOR}] UltimateEngine Suite [/]",
        border_style=BORDER_COLOR,
        box=ROUNDED,
        padding=(1, 3),
        subtitle=f"[bold black on {BRIGHT_COLOR}] {get_indian_time()} [/]",
    )
    console.print(menu_panel)
    console.print()

def delete_folder(data_path):
    folders = []
    for item in data_path.iterdir():
        if item.is_dir() and item.name not in [
            'PAK', 'UNPACK', 'REPACK', 'RESULT', 'PAK TOOL',
            'BUILD_PAK', 'SKIN_TOOL', 'LUA_TOOL', 'CREDIT_TOOL', 'PYTHON TOOL'
        ]:
            folders.append(item)

    if not folders:
        console.print(f'[bold {BRIGHT_COLOR}]No folders found to delete![/]')
        return

    folder_table = Table(
        title=f"[bold {BRIGHT_COLOR}]WORKSPACE PURGE[/]",
        border_style=BORDER_COLOR,
        box=DOUBLE_EDGE,
        header_style=f"bold black on {BRIGHT_COLOR}",
    )
    folder_table.add_column("#", justify="center", style=f"bold {BRIGHT_COLOR}", width=6)
    folder_table.add_column("Folder Name", justify="left", style=f"bold {TEXT_COLOR}")
    folder_table.add_column("Size", justify="right", style=f"bold {TEXT_COLOR}")

    for i, folder in enumerate(folders, 1):
        folder_size = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                fp = os.path.join(root, file)
                if os.path.isfile(fp):
                    folder_size += os.path.getsize(fp)
        folder_table.add_row(str(i), folder.name, human_size(folder_size))

    console.print(folder_table)

    try:
        choice = int(safe_input(f"\n[bold {BRIGHT_COLOR}]Select folder number (1-{len(folders)}): [/]"))
        if 1 <= choice <= len(folders):
            sel = folders[choice - 1]
            confirm = safe_input(f"[bold {ERROR}]Purge {sel.name}? (yes/no): [/]").strip().lower()
            if confirm == 'yes':
                shutil.rmtree(sel)
                console.print(f'[bold {BRIGHT_COLOR}]Purged: {sel.name}[/]')
            else:
                console.print(f'[{WARNING}]Cancelled[/]')
        else:
            console.print(f'[{ERROR}]Invalid selection[/]')
    except ValueError:
        console.print(f'[{ERROR}]Invalid input[/]')

def display_file_selector(title, folder_path, file_pattern="*.pak"):
    files = list(folder_path.glob(file_pattern))
    if not files:
        console.print(f"[bold {ERROR}]ERROR: No {file_pattern} files in {folder_path}[/]")
        return None, None

    selection_table = Table(
        title=f"[bold {BRIGHT_COLOR}]{title}[/]",
        expand=True,
        box=DOUBLE_EDGE,
        border_style=BORDER_COLOR,
        header_style=f"bold black on {BRIGHT_COLOR}",
    )
    selection_table.add_column("#", justify="center", style=f"bold {BRIGHT_COLOR}", width=6)
    selection_table.add_column("File Name", justify="left", style=f"bold {TEXT_COLOR}")
    selection_table.add_column("Size", justify="right", style=f"bold {TEXT_COLOR}")
    selection_table.add_column("Modified", justify="right", style=f"dim {DIM_COLOR}")

    for i, f in enumerate(files, 1):
        size_mb = f.stat().st_size / (1024 * 1024)
        mod_time = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        selection_table.add_row(
            str(i),
            f.name,
            f"{size_mb:.2f} MB",
            f"[dim {DIM_COLOR}]{mod_time}[/dim {DIM_COLOR}]",
        )

    console.print(selection_table)
    try:
        idx = int(console.input(
            f"\n[bold {BRIGHT_COLOR}]Select file number (1-{len(files)}): [/]"
        )) - 1
        if idx < 0 or idx >= len(files):
            console.print(f"[bold {ERROR}]Invalid selection[/]")
            return None, None
        return files[idx], files
    except ValueError:
        console.print(f"[bold {ERROR}]Please enter a valid number[/]")
        return None, None

def dump_unpacking_log(pak_file, output_log_path):
    try:
        with open(output_log_path, 'w', encoding='utf-8') as log_file:
            log_file.write('=' * 80 + '\nARCHIVE EXTRACTION DEBUG LOG\n' + '=' * 80 + '\n\n')
            log_file.write(f'PAK File: {pak_file._file_path}\n')
            log_file.write(f'PAK Info Version: {pak_file._pak_info.version}\n')
            log_file.write(f'Mount Point: {pak_file._mount_point}\n')
            log_file.write('-' * 80 + '\n\n')
            file_count = 0
            for dir_path, files in pak_file._index.items():
                for file_name, entry in files.items():
                    file_count += 1
                    full_path = str(PurePath(dir_path) / file_name).replace('\\', '/')
                    log_file.write(f'\n[{file_count}] {full_path}\n')
                    log_file.write(f'  Uncompressed Size: {entry.uncompressed_size:,} bytes\n')
                    log_file.write(f'  Compressed Size: {entry.size:,} bytes\n')
                    log_file.write(f'  Compression Method: {entry.compression_method}\n')
                    log_file.write(f'  Encryption Method: {entry.encryption_method}\n')
                    log_file.write(f'  Compressed Blocks: {len(entry.compressed_blocks)}\n')
            log_file.write('\n' + '=' * 80 + '\nEND OF LOG\n' + '=' * 80 + '\n')
        console.print(f'[bold {BRIGHT_COLOR}]Debug log saved to: {output_log_path}[/]')
    except Exception as e:
        console.print(f'[{WARNING}]Log save failed: {e}[/]')

def ensure_directories(base_dir):
    (base_dir / "PAK").mkdir(parents=True, exist_ok=True)
    (base_dir / "UNPACK").mkdir(parents=True, exist_ok=True)
    (base_dir / "REPACK").mkdir(parents=True, exist_ok=True)
    (base_dir / "RESULT").mkdir(parents=True, exist_ok=True)

    pak_tool_dir = base_dir / "PAK TOOL"
    (pak_tool_dir / "EDIT").mkdir(parents=True, exist_ok=True)
    (pak_tool_dir / "UNPACK").mkdir(parents=True, exist_ok=True)
    (pak_tool_dir / "RESULT").mkdir(parents=True, exist_ok=True)
    (pak_tool_dir / "PAK").mkdir(parents=True, exist_ok=True)

    build_pak_dir = base_dir / "BUILD_PAK"
    (build_pak_dir / "CSV").mkdir(parents=True, exist_ok=True)
    (build_pak_dir / "EDIT").mkdir(parents=True, exist_ok=True)
    (build_pak_dir / "TEMPLATE").mkdir(parents=True, exist_ok=True)
    (build_pak_dir / "OUTPUT").mkdir(parents=True, exist_ok=True)

    obb_dir = base_dir / "OBB_UNPACKER"
    (obb_dir / "ORGNAL").mkdir(parents=True, exist_ok=True)
    (obb_dir / "Modified_files").mkdir(parents=True, exist_ok=True)
    (obb_dir / "UNPACK").mkdir(parents=True, exist_ok=True)
    (obb_dir / "REPACK").mkdir(parents=True, exist_ok=True)

    skin_tool_root = base_dir / "SKIN_TOOL"
    skin_tool_root.mkdir(parents=True, exist_ok=True)

    for game in ["BGMI_SKIN", "PUBG_SKIN"]:
        game_base = skin_tool_root / game

        mini_base = game_base / "MINI"
        (mini_base / "MINI_ICON" / "INPUT").mkdir(parents=True, exist_ok=True)
        (mini_base / "MINI_ICON" / "OUTPUT").mkdir(parents=True, exist_ok=True)
        (mini_base / "TXTS").mkdir(parents=True, exist_ok=True)
        (mini_base / "AUTO_THEME" / "FILES").mkdir(parents=True, exist_ok=True)
        (mini_base / "AUTO_THEME" / "MODIFIED").mkdir(parents=True, exist_ok=True)
        (mini_base / "AUTO_THEME" / "TXT").mkdir(parents=True, exist_ok=True)
        (mini_base / "HIT EFFECT" / "org").mkdir(parents=True, exist_ok=True)
        (mini_base / "HIT EFFECT" / "modified").mkdir(parents=True, exist_ok=True)
        (mini_base / "LOOTCRATES" / "org").mkdir(parents=True, exist_ok=True)
        (mini_base / "LOOTCRATES" / "modified").mkdir(parents=True, exist_ok=True)

        game_key = "BGMI" if game == "BGMI_SKIN" else "PUBG"
        zsdic_base = game_base / "ZSDIC"
        (zsdic_base / game_key / "skindats").mkdir(parents=True, exist_ok=True)
        (zsdic_base / game_key / "edited").mkdir(parents=True, exist_ok=True)
        (zsdic_base / game_key / "size").mkdir(parents=True, exist_ok=True)

        (game_base / "FINAL").mkdir(parents=True, exist_ok=True)

    lua_base = base_dir / "LUA_TOOL"
    (lua_base / "Lua_org").mkdir(parents=True, exist_ok=True)
    (lua_base / "Lua_Decript").mkdir(parents=True, exist_ok=True)
    (lua_base / "Lua_Rueslt").mkdir(parents=True, exist_ok=True)

    re_lua = lua_base / "RE_LUA ANY SIZE"
    (re_lua / "EDIT_LUA").mkdir(parents=True, exist_ok=True)
    (re_lua / "ORGNAL_PAK").mkdir(parents=True, exist_ok=True)
    (re_lua / "REPACK_MOD").mkdir(parents=True, exist_ok=True)

    lua_custom = lua_base / "LUA_CUSTOM"
    (lua_custom / "EDIT").mkdir(parents=True, exist_ok=True)
    (lua_custom / "PAK").mkdir(parents=True, exist_ok=True)
    (lua_custom / "RESULT").mkdir(parents=True, exist_ok=True)

    credit_base = base_dir / "CREDIT_TOOL"
    (credit_base / "ORGNAL").mkdir(parents=True, exist_ok=True)
    (credit_base / "MODDED FILE").mkdir(parents=True, exist_ok=True)

    (base_dir / "EXES").mkdir(parents=True, exist_ok=True)
    (base_dir / "ANTIRESET_OBB" / "MOD_REPACK").mkdir(parents=True, exist_ok=True)

    py_tool_dir = base_dir / "PYTHON TOOL"
    (py_tool_dir / "encrypt").mkdir(parents=True, exist_ok=True)
    (py_tool_dir / "result").mkdir(parents=True, exist_ok=True)
    (py_tool_dir / "input").mkdir(parents=True, exist_ok=True)
    (py_tool_dir / "output").mkdir(parents=True, exist_ok=True)

def auto_termux_setup():
    if "com.termux" not in os.environ.get("PREFIX", ""):
        return

    needs_setup = False
    try:
        import rich
        import requests
        import gmalg
        import Crypto
        import zstandard
        import colorama
        from termcolor import colored
        if not os.path.exists(os.path.expanduser("~/storage")):
            needs_setup = True
    except ImportError:
        needs_setup = True

    if not needs_setup:
        return

    Y = "\033[1;33m"
    G = "\033[1;32m"
    C = "\033[1;36m"
    RES = "\033[0m"

    os.system("clear")
    print(f"{C}=================================================={RES}")
    print(f"{G}    UltimateEngine Suite AUTO-INSTALLER    {RES}")
    print(f"{C}=================================================={RES}\n")
    print(f"{Y}[*] First time setup detected!{RES}\n")
    time.sleep(1)

    print(f"{C}--------------------------------------------------{RES}")
    print(f"{G}[>] Granting Storage Permissions{RES}")
    if not os.path.exists(os.path.expanduser("~/storage")):
        os.system("yes | termux-setup-storage")
        time.sleep(2)

    print(f"{C}--------------------------------------------------{RES}")
    print(f"{G}[>] Updating packages{RES}")
    os.system("pkg update -y && pkg upgrade -y")

    print(f"{C}--------------------------------------------------{RES}")
    print(f"{G}[>] Installing core packages{RES}")
    os.system("pkg install python python-pip clang make -y")

    print(f"{C}--------------------------------------------------{RES}")
    print(f"{G}[>] Installing Python libraries{RES}")
    os.system("pip install rich pycryptodome zstandard requests gmalg colorama termcolor pytz")

    print(f"{C}--------------------------------------------------{RES}")
    print(f"{G}[>] Setting permissions{RES}")
    os.system("chmod +x *")

    print(f"\n{C}=================================================={RES}")
    print(f"{G} ALL SYSTEMS GO! INITIALIZATION COMPLETE.{RES}")
    print(f"{C}=================================================={RES}\n")
    time.sleep(2)
    os.system("clear")

def main_menu():
    if getattr(sys, 'frozen', False):
        data_path = Path(sys.executable).parent
    else:
        data_path = Path(__file__).parent

    ensure_directories(data_path)

    while True:
        print_banner()
        print_user_profile()
        print_main_menu()

        choice = safe_input(f'[bold {BRIGHT_COLOR}]ENTER YOUR CHOICE: [/]').strip()

        if choice == '1':
            pak_dir = data_path / "PAK"
            if not pak_dir.exists():
                console.print(f"[bold {ERROR}]ERROR: PAK folder not found at {pak_dir}[/]")
                safe_input('\nPress Enter to continue...')
                continue

            pak_file, _ = display_file_selector("Available .pak files to EXTRACT:", pak_dir)
            if not pak_file:
                safe_input('\nPress Enter to continue...')
                continue

            try:
                console.print(f'[bold {BRIGHT_COLOR}]Extracting {pak_file.name}...[/]')
                pak = TencentPakFile(pak_file)
                unpack_path = data_path / "UNPACK" / pak_file.stem
                repack_path = data_path / "REPACK" / pak_file.stem

                success = pak.dump(unpack_path)

                log_path = unpack_path / f'Debug_{pak_file.stem}.log'
                dump_unpacking_log(pak, log_path)

                if success:
                    for dir_path, _ in pak._index.items():
                        current_repack_path = repack_path / pak._mount_point / dir_path
                        current_repack_path.mkdir(parents=True, exist_ok=True)
                    console.print(f'[bold {BRIGHT_COLOR}]SUCCESS: Extracted to {unpack_path}[/]')
                else:
                    console.print(f'[{WARNING}]Partial extraction — stopped by user.[/]')
            except Exception as e:
                console.print(f'[bold {ERROR}]Error: {escape(str(e))}[/]')
            safe_input('\nPress Enter to continue...')

        elif choice == '2':
            pt = data_path / "PAK TOOL"
            pak_dir = pt / "PAK"
            edit_dir = pt / "EDIT"
            result_dir = pt / "RESULT"

            pak_file, _ = display_file_selector("Available .pak files to INJECT INTO:", pak_dir)
            if not pak_file:
                safe_input('\nPress Enter...')
                continue

            if not edit_dir.exists() or not any(edit_dir.iterdir()):
                console.print(f'[bold {ERROR}]ERROR: No files in PAK TOOL/EDIT folder.[/]')
                safe_input('\nPress Enter...')
                continue

            console.print()
            console.print(f'[bold {BRIGHT_COLOR}]Encrypt with SM4?[/]')
            enc_choice = safe_input(f'[bold {BRIGHT_COLOR}]Encrypt injected files? (Y/n): [/]').strip().lower()
            protect_new = enc_choice not in ('n', 'no')

            try:
                console.print(f'[bold {BRIGHT_COLOR}]Injecting files into {pak_file.name}...[/]')
                pak = TencentPakFile(pak_file)
                output_pak = result_dir / pak_file.name

                edited, added = inject_edit_files(pak, edit_dir, output_pak, protect_new=protect_new, sm4_type=47)

                console.print()
                console.print(f'[bold {BRIGHT_COLOR}]Edited: {edited} files | Added: {added} files[/]')
                console.print(f'[bold {BRIGHT_COLOR}]Output: {output_pak}[/]')
            except Exception as e:
                console.print(f'[bold {ERROR}]Inject failed: {e}[/]')
                import traceback
                traceback.print_exc()
            safe_input('\nPress Enter...')

        elif choice == '3':
            pt = data_path / "PAK TOOL"
            pak_dir = pt / "PAK"
            edit_dir = pt / "EDIT"
            result_dir = pt / "RESULT"

            pak_file, _ = display_file_selector("Available .pak files to REBUILD:", pak_dir)
            if not pak_file:
                safe_input('\nPress Enter...')
                continue

            if not edit_dir.exists() or not any(edit_dir.iterdir()):
                console.print(f'[bold {ERROR}]ERROR: No files in EDIT folder.[/]')
                safe_input('\nPress Enter...')
                continue

            try:
                console.print(f'[bold {BRIGHT_COLOR}]Rebuilding {pak_file.name} (Full Rebuild)...[/]')
                pak = TencentPakFile(pak_file)
                output_pak = result_dir / pak_file.name
                count = repack_pak_file_full(pak, edit_dir, output_pak)

                if count > 0:
                    console.print(f'[bold {BRIGHT_COLOR}]Rebuilt {count} files![/]')
                    console.print(f'[bold {BRIGHT_COLOR}]Output: {output_pak}[/]')
                else:
                    console.print(f'[{ERROR}]No files rebuilt![/]')
            except Exception as e:
                console.print(f'[bold {ERROR}]Rebuild failed: {e}[/]')
                import traceback
                traceback.print_exc()
            safe_input('\nPress Enter...')

        elif choice == '4':
            pt = data_path / "PAK TOOL"
            pak_dir = pt / "PAK"
            edit_dir = pt / "EDIT"
            result_dir = pt / "RESULT"
            build_csv_dir = data_path / "BUILD_PAK" / "CSV"

            pak_file, _ = display_file_selector("Available .pak files for TARGETED DEPLOYMENT:", pak_dir)
            if not pak_file:
                safe_input('\nPress Enter...')
                continue

            if not edit_dir.exists() or not any(edit_dir.iterdir()):
                console.print(f'[bold {ERROR}]ERROR: No files in EDIT folder.[/]')
                safe_input('\nPress Enter...')
                continue

            console.print()
            method_table = Table(
                title=f"[bold {BRIGHT_COLOR}]Path Method[/]",
                box=DOUBLE_EDGE, border_style=BORDER_COLOR,
                header_style=f"bold black on {BRIGHT_COLOR}",
            )
            method_table.add_column("OPT", justify="center", style=f"bold {BRIGHT_COLOR}", width=6)
            method_table.add_column("METHOD", style=f"bold {TEXT_COLOR}")
            method_table.add_column("DESCRIPTION", style=f"{DIM_COLOR}")
            method_table.add_row("1", "Manual Path", "Type path yourself (advanced)")
            method_table.add_row("2", "Signature Auto", "Signature auto-resolve (no typing)")
            method_table.add_row("0", f"[{ERROR}]BACK[/]", "[dim]Cancel[/dim]")
            console.print(method_table)

            method_sel = safe_input(f'[bold {BRIGHT_COLOR}]Select method (0/1/2): [/]').strip()

            if method_sel == "1":
                console.print()
                console.print(Panel(
                    f"[bold {BRIGHT_COLOR}]Enter the target path inside the PAK:[/]\n"
                    f"[dim {DIM_COLOR}]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core[/dim {DIM_COLOR}]",
                    border_style=BORDER_COLOR, box=ROUNDED
                ))
                target_path = safe_input(f'[bold {BRIGHT_COLOR}]Path: [/]').strip()

                if not target_path:
                    console.print(f'[bold {ERROR}]No path provided![/]')
                    safe_input('\nPress Enter...')
                    continue

                target_path = target_path.replace('\\', '/').strip('/')

                try:
                    console.print(f'[bold {BRIGHT_COLOR}]Adding files to {target_path}...[/]')
                    pak = TencentPakFile(pak_file)
                    output_pak = result_dir / pak_file.name
                    count = repack_pak_file_full(pak, edit_dir, output_pak, target_path, force_add=True)

                    if count > 0:
                        console.print()
                        console.print(f'[bold {BRIGHT_COLOR}]Processed {count} files to {target_path}![/]')
                        console.print(f'[bold {BRIGHT_COLOR}]Output: {output_pak}[/]')
                except Exception as e:
                    console.print(f'[bold {ERROR}]Rebuild failed: {e}[/]')
                    import traceback
                    traceback.print_exc()
                safe_input('\nPress Enter...')

            elif method_sel == "2":
                try:
                    console.print(f'[bold {BRIGHT_COLOR}]SIGNATURE AUTO mode: resolving paths...[/]')
                    pak = TencentPakFile(pak_file)
                    output_pak = result_dir / pak_file.name
                    count = repack_to_path_with_csv(pak, edit_dir, build_csv_dir, output_pak)

                    if count > 0:
                        console.print()
                        console.print(f'[bold {BRIGHT_COLOR}]Signature auto: {count} files processed![/]')
                        console.print(f'[bold {BRIGHT_COLOR}]Output: {output_pak}[/]')
                except Exception as e:
                    console.print(f'[bold {ERROR}]Signature auto failed: {e}[/]')
                    import traceback
                    traceback.print_exc()
                safe_input('\nPress Enter...')

        elif choice == '5':
            pt = data_path / "PAK TOOL"
            pak_dir = pt / "PAK"
            result_dir = pt / "RESULT"

            pak_file, _ = display_file_selector("Available .pak files to SHIELD:", pak_dir)
            if not pak_file:
                safe_input('\nPress Enter...')
                continue

            console.print()
            console.print(f'[bold {BRIGHT_COLOR}]CIPHER SHIELD MODE[/]')
            console.print(f'[dim {DIM_COLOR}]Re-encrypts EVERY file with SM4.[/dim {DIM_COLOR}]')
            confirm = safe_input(f'[bold {ERROR}]Start CIPHER SHIELD? (yes/no): [/]').strip().lower()

            if confirm not in ('y', 'yes'):
                console.print(f'[{WARNING}]Cancelled.[/]')
                safe_input('\nPress Enter...')
                continue

            try:
                console.print(f'[bold {BRIGHT_COLOR}]Shielding {pak_file.name}...[/]')
                pak = TencentPakFile(pak_file)
                output_pak = result_dir / pak_file.name
                protected, skipped = protect_pak_file(pak, output_pak, sm4_type=47)

                console.print()
                console.print(f'[bold {BRIGHT_COLOR}]SHIELDED: {protected} files (SM4)[/]')
                console.print(f'[{WARNING}]Skipped: {skipped} files[/]')
                console.print(f'[bold {BRIGHT_COLOR}]Output: {output_pak}[/]')
            except Exception as e:
                console.print(f'[bold {ERROR}]Shield failed: {e}[/]')
                import traceback
                traceback.print_exc()
            safe_input('\nPress Enter...')

        elif choice == '6':
            build_new_pak(data_path)
            safe_input('\nPress Enter to continue...')

        elif choice == '7':
            delete_folder(data_path)
            safe_input('\nPress Enter to continue...')

        elif choice == '8':
            mini_skin_tool_main(data_path)
            safe_input('\nPress Enter to continue...')

        elif choice == '9':
            zsdic_skin_tool_main(data_path)
            safe_input('\nPress Enter to continue...')

        elif choice == '10':
            run_lua_tool(data_path)
            safe_input('\nPress Enter to continue...')

        elif choice == '11':
            black_tool_main()
            safe_input('\nPress Enter to continue...')

        elif choice == '12':
            python_tool_menu(data_path)

        elif choice == '0':
            console.print(f"[bold {BRIGHT_COLOR}]Goodbye![/]")
            time.sleep(2)
            break

        else:
            console.print(f'[bold {ERROR}]Invalid choice![/]')
            time.sleep(2)

if __name__ == '__main__':
    try:
        auto_termux_setup()
        main_menu()
    except KeyboardInterrupt:
        console.print(f'\n[bold {BRIGHT_COLOR}]Interrupted. Exiting...[/]')
        sys.exit(0)
    except Exception as e:
        console.print(f'[bold {ERROR}]ERROR:[/] {escape(str(e))}')
        import traceback
        traceback.print_exc()
        safe_input('\nPress Enter to exit...')
        sys.exit(1)