#!/usr/bin/env python3
"""
This tool was developed by:
@VoidPAK

Developer Channel:
https://t.me/Theend2032

IMPORTANT NOTICE:
This tool is completely free. Any tampering with the developer's rights removal of ownership credits, or claiming this work as someone else's is strictly prohibited.

The tool is inspired by the game's own mechanisms and was developed through independent effort.

Respect the developer's rights and use this tool responsibly.
"""
import hashlib
import json
import math
import os
import re
import sys
import struct
import threading
from pathlib import Path

sys.setrecursionlimit(1_000_000)

STRING_XOR_KEY = bytes([
    0x11, 0x21, 0x36, 0x47, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0x35,
    0x26, 0x1A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x15, 0x07, 0xD0, 0x2C, 0x1E, 0x8F, 0xF6, 0xC8,
])

GAME_SIZE_T = 4
STD_SIZE_T = 8
LUAC_DATA = b"\x19\x93\r\n\x1a\n"


def xor_string(data: bytes, key: bytes = STRING_XOR_KEY) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def real_op(op: int) -> int:
    if 17 <= op <= 29:
        return op - 17
    if op <= 16:
        return op + 13
    return op


def game_op(op: int) -> int:
    if op <= 12:
        return op + 17
    if 13 <= op <= 29:
        return op - 13
    return op


def map_code(code, fn):
    return [(w & ~0x3F) | fn(w & 0x3F) for w in code]


class LFunc:
    pass


class Chunk:
    def __init__(self):
        self.fmt = "game"
        self.size_t = GAME_SIZE_T
        self.nup_main = 1
        self.main = None
        self.end = 0
        self.tail = b""


class BadChunk(Exception):
    pass


class _R:
    def __init__(self, b, size_t, fmt):
        self.b, self.p, self.szt, self.fmt = b, 0, size_t, fmt

    def raw(self, n):
        if n < 0 or self.p + n > len(self.b):
            raise BadChunk("truncated")
        v = self.b[self.p:self.p + n]
        self.p += n
        return v

    def u8(self):
        return self.raw(1)[0]

    def u32(self):
        return struct.unpack("<I", self.raw(4))[0]

    def i32(self):
        return struct.unpack("<i", self.raw(4))[0]

    def i64(self):
        return struct.unpack("<q", self.raw(8))[0]

    def f64(self):
        return struct.unpack("<d", self.raw(8))[0]

    def string(self):
        n = self.u8()
        if n == 0:
            return None
        if n == 0xFF:
            n = int.from_bytes(self.raw(self.szt), "little")
        return self.raw(n - 1)

    def count(self, limit=5_000_000):
        n = self.u32()
        if n > limit:
            raise BadChunk("absurd count")
        return n

    def func(self):
        f = LFunc()
        f.source = self.string()
        f.line, f.lastline = self.u32(), self.u32()
        f.nparams, f.vararg, f.maxstack = self.u8(), self.u8(), self.u8()
        n = self.count()
        f.code = list(struct.unpack("<%dI" % n, self.raw(4 * n)))
        f.k = []
        for _ in range(self.count()):
            t = self.u8()
            if t == 0:
                f.k.append((0, None))
            elif t == 1:
                f.k.append((1, bool(self.u8())))
            elif t == 3:
                f.k.append((3, self.f64()))
            elif t == 0x13:
                f.k.append((0x13, self.i64()))
            elif t in (4, 0x14):
                s = self.string()
                if s is None:
                    raise BadChunk("nil string constant")
                f.k.append((t, s))
            else:
                raise BadChunk("bad constant type %d" % t)
        f.up = [(self.u8(), self.u8()) for _ in range(self.count())]
        f.protos = [self.func() for _ in range(self.count())]
        if self.fmt == "game":
            f.lineinfo = list(self.raw(self.count()))
            f.abslineinfo = [(self.u32(), self.u32()) for _ in range(self.count())]
        else:
            n = self.count()
            f.lineinfo = list(struct.unpack("<%di" % n, self.raw(4 * n)))
            f.abslineinfo = []
        f.locvars = [(self.string(), self.u32(), self.u32()) for _ in range(self.count())]
        f.upnames = [self.string() for _ in range(self.count())]
        return f


def looks_like_lua_source(blob: bytes) -> bool:
    head = blob[:4096]
    if not head or b"\x00" in head:
        return False
    try:
        txt = head.decode("utf-8", "ignore")
    except Exception:
        return False
    printable = sum(1 for c in txt if c.isprintable() or c in "\r\n\t")
    return printable / max(1, len(txt)) > 0.95 and bool(
        re.search(r"\b(local|function|require|return|end|if|then)\b", txt))


def parse_chunk(blob: bytes, fmt: str = None) -> Chunk:
    if fmt is None:
        errs = []
        for f in ("game", "std"):
            try:
                return parse_chunk(blob, f)
            except (BadChunk, struct.error, IndexError) as ex:
                errs.append("%s: %s" % (f, ex))
        raise BadChunk("not a readable Lua 5.3 chunk (" + "; ".join(errs) + ")")
    if blob[:4] != b"\x1bLua" or len(blob) < 34:
        if looks_like_lua_source(blob):
            raise BadChunk("this is plain-text Lua SOURCE, not bytecode - nothing to decode")
        raise BadChunk("not Lua bytecode")
    if blob[4] != 0x53 or blob[5] != 0 or blob[6:12] != LUAC_DATA:
        raise BadChunk("not a Lua 5.3 header")
    isz, szt, insz, intsz, numsz = blob[12:17]
    if (isz, insz, intsz, numsz) != (4, 4, 8, 8) or szt not in (4, 8):
        raise BadChunk("unsupported sizes int=%d size_t=%d instr=%d integer=%d number=%d"
                       % (isz, szt, insz, intsz, numsz))
    if struct.unpack_from("<q", blob, 17)[0] != 0x5678 or \
            struct.unpack_from("<d", blob, 25)[0] != 370.5:
        raise BadChunk("header check values differ")
    ch = Chunk()
    ch.fmt, ch.size_t = fmt, szt
    r = _R(blob, szt, fmt)
    r.p = 33
    ch.nup_main = r.u8()
    ch.main = r.func()
    ch.end = r.p
    ch.tail = bytes(blob[ch.end:])
    return ch


def _wstr(s, szt):
    if s is None:
        return b"\x00"
    n = len(s) + 1
    if n < 0xFF:
        return bytes([n]) + s
    return b"\xff" + n.to_bytes(szt, "little") + s


def _wfunc(f, fmt, szt, out):
    out.append(_wstr(f.source, szt))
    out.append(struct.pack("<II", f.line, f.lastline))
    out.append(bytes([f.nparams, f.vararg, f.maxstack]))
    out.append(struct.pack("<I", len(f.code)))
    out.append(struct.pack("<%dI" % len(f.code), *f.code))
    out.append(struct.pack("<I", len(f.k)))
    for t, v in f.k:
        out.append(bytes([t]))
        if t == 1:
            out.append(bytes([1 if v else 0]))
        elif t == 3:
            out.append(struct.pack("<d", v))
        elif t == 0x13:
            out.append(struct.pack("<q", v))
        elif t in (4, 0x14):
            out.append(_wstr(v, szt))
    out.append(struct.pack("<I", len(f.up)))
    for a, b in f.up:
        out.append(bytes([a, b]))
    out.append(struct.pack("<I", len(f.protos)))
    for p in f.protos:
        _wfunc(p, fmt, szt, out)
    if fmt == "game":
        out.append(struct.pack("<I", len(f.lineinfo)))
        out.append(bytes(f.lineinfo))
        out.append(struct.pack("<I", len(f.abslineinfo)))
        for pc, line in f.abslineinfo:
            out.append(struct.pack("<II", pc, line))
    else:
        out.append(struct.pack("<I", len(f.lineinfo)))
        out.append(struct.pack("<%di" % len(f.lineinfo), *f.lineinfo))
    out.append(struct.pack("<I", len(f.locvars)))
    for name, s, e in f.locvars:
        out.append(_wstr(name, szt))
        out.append(struct.pack("<II", s, e))
    out.append(struct.pack("<I", len(f.upnames)))
    for n in f.upnames:
        out.append(_wstr(n, szt))


def write_chunk(ch: Chunk) -> bytes:
    out = [b"\x1bLuaS\x00", LUAC_DATA, bytes([4, ch.size_t, 4, 8, 8]),
           struct.pack("<q", 0x5678), struct.pack("<d", 370.5), bytes([ch.nup_main])]
    _wfunc(ch.main, ch.fmt, ch.size_t, out)
    out.append(getattr(ch, "tail", b""))
    return b"".join(out)


def lines_from_game(f):
    out, prev = [], f.line
    absd = dict(f.abslineinfo)
    for pc, b in enumerate(f.lineinfo):
        d = b - 256 if b > 127 else b
        line = absd[pc] if d == -128 else prev + d
        out.append(line)
        prev = line
    return out


def lineinfo_to_game(lines, linedefined):
    info, ab, prev, iw = [], [], linedefined, 0
    for pc, line in enumerate(lines):
        dif = line - prev
        if abs(dif) >= 0x80:
            need = True
        else:
            need = iw >= 128
            if not need:
                iw += 1
        if need:
            ab.append((pc, line))
            info.append(0x80)
            iw = 1
        else:
            info.append(dif & 0xFF)
        prev = line
    return info, ab


def _xor_func(f):
    f.source = None if f.source is None else xor_string(f.source)
    f.k = [(t, xor_string(v) if t in (4, 0x14) else v) for t, v in f.k]
    f.locvars = [(None if n is None else xor_string(n), s, e) for n, s, e in f.locvars]
    f.upnames = [None if n is None else xor_string(n) for n in f.upnames]


def _copy(f):
    g = LFunc()
    g.__dict__.update(f.__dict__)
    g.protos = [_copy(p) for p in f.protos]
    return g


def _to_std(f):
    _xor_func(f)
    f.code = map_code(f.code, real_op)
    f.lineinfo = lines_from_game(f)
    f.abslineinfo = []
    for p in f.protos:
        _to_std(p)


def _to_game(f, ref):
    _xor_func(f)
    f.code = map_code(f.code, game_op)
    lines = list(f.lineinfo)
    if ref is not None and len(ref.code) == len(f.code) and \
            (ref.code == f.code or lines_from_game(ref) == lines):
        f.lineinfo, f.abslineinfo = list(ref.lineinfo), list(ref.abslineinfo)
    elif len(lines) == len(f.code):
        f.lineinfo, f.abslineinfo = lineinfo_to_game(lines, f.line)
    else:
        f.lineinfo, f.abslineinfo = [], []
    rp = ref.protos if ref is not None and len(ref.protos) == len(f.protos) else [None] * len(f.protos)
    for p, rr in zip(f.protos, rp):
        _to_game(p, rr)


def decode_blob(blob: bytes) -> bytes:
    ch = parse_chunk(blob, "game")
    ch.main = _copy(ch.main)
    _to_std(ch.main)
    ch.fmt, ch.size_t = "std", STD_SIZE_T
    return write_chunk(ch)


def encode_blob(blob: bytes, reference: bytes = None) -> bytes:
    ch = parse_chunk(blob, "std")
    ref = None
    if reference is not None:
        try:
            ref = parse_chunk(reference, "game")
        except BadChunk:
            ref = None
    ch.main = _copy(ch.main)
    _to_game(ch.main, ref.main if ref else None)
    if ref is not None:
        ch.main.source = ref.main.source
    ch.fmt, ch.size_t = "game", GAME_SIZE_T
    return write_chunk(ch)


STD_OPS = ["MOVE", "LOADK", "LOADKX", "LOADBOOL", "LOADNIL", "GETUPVAL", "GETTABUP",
           "GETTABLE", "SETTABUP", "SETUPVAL", "SETTABLE", "NEWTABLE", "SELF", "ADD",
           "SUB", "MUL", "MOD", "POW", "DIV", "IDIV", "BAND", "BOR", "BXOR", "SHL",
           "SHR", "UNM", "BNOT", "NOT", "LEN", "CONCAT", "JMP", "EQ", "LT", "LE",
           "TEST", "TESTSET", "CALL", "TAILCALL", "RETURN", "FORLOOP", "FORPREP",
           "TFORCALL", "TFORLOOP", "SETLIST", "CLOSURE", "VARARG", "EXTRAARG"]
(MOVE, LOADK, LOADKX, LOADBOOL, LOADNIL, GETUPVAL, GETTABUP, GETTABLE, SETTABUP,
 SETUPVAL, SETTABLE, NEWTABLE, SELF, ADD, SUB, MUL, MOD, POW, DIV, IDIV, BAND, BOR,
 BXOR, SHL, SHR, UNM, BNOT, NOT, LEN, CONCAT, JMP, EQ, LT, LE, TEST, TESTSET, CALL,
 TAILCALL, RETURN, FORLOOP, FORPREP, TFORCALL, TFORLOOP, SETLIST, CLOSURE, VARARG,
 EXTRAARG) = range(47)

BINOPS = {ADD: ("+", 10), SUB: ("-", 10), MUL: ("*", 11), MOD: ("%", 11),
          POW: ("^", 14), DIV: ("/", 11), IDIV: ("//", 11), BAND: ("&", 6),
          BOR: ("|", 4), BXOR: ("~", 5), SHL: ("<<", 7), SHR: (">>", 7)}
UNOPS = {UNM: "-", BNOT: "~", NOT: "not ", LEN: "#"}
CMPOPS = {EQ: "==", LT: "<", LE: "<="}
LUA_KEYWORDS = {"and", "break", "do", "else", "elseif", "end", "false", "for", "function",
                "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return",
                "then", "true", "until", "while"}
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def lua_quote(b: bytes) -> str:
    out = ['"']
    i, n = 0, len(b)
    while i < n:
        c = b[i]
        if c < 0x80:
            ch = chr(c)
            if ch == "\\":
                out.append("\\\\")
            elif ch == '"':
                out.append('\\"')
            elif ch == "\n":
                out.append("\\n")
            elif ch == "\r":
                out.append("\\r")
            elif ch == "\t":
                out.append("\\t")
            elif c < 32 or c == 127:
                out.append("\\%03d" % c)
            else:
                out.append(ch)
            i += 1
            continue

        ln = 2 if 0xC2 <= c <= 0xDF else 3 if 0xE0 <= c <= 0xEF else 4 if 0xF0 <= c <= 0xF4 else 0
        if ln and i + ln <= n:
            try:
                out.append(b[i:i + ln].decode("utf-8"))
                i += ln
                continue
            except UnicodeDecodeError:
                pass
        out.append("\\%03d" % c)
        i += 1
    out.append('"')
    return "".join(out)


class E:
    prec = 20
    seq = 0


_SEQ = [0]


def _next_seq():
    _SEQ[0] += 1
    return _SEQ[0]


class Const(E):
    def __init__(self, kind, val):
        self.kind, self.val, self.seq = kind, val, _next_seq()

    def is_true(self):
        return self.kind == "bool" and self.val is True

    def is_false(self):
        return self.kind == "bool" and self.val is False

    def s(self):
        k, v = self.kind, self.val
        if k == "nil":
            return "nil"
        if k == "bool":
            return "true" if v else "false"
        if k == "int":
            return "math.mininteger" if v == -(1 << 63) else str(v)
        if k == "num":
            if v != v:
                return "(0/0)"
            if v in (float("inf"), float("-inf")):
                return "math.huge" if v > 0 else "-math.huge"
            r = repr(v)
            return r
        return lua_quote(v)


class Name(E):
    def __init__(self, n, kind="local"):
        self.n, self.kind, self.seq = n, kind, _next_seq()

    def s(self):
        return self.n


class Vararg(E):
    def __init__(self):
        self.seq = _next_seq()

    def s(self):
        return "..."


class Index(E):
    def __init__(self, obj, key):
        self.obj, self.key, self.seq = obj, key, _next_seq()

    def s(self):
        o = fmt(self.obj, 20, atom=True)
        k = self.key
        if isinstance(k, Const) and k.kind == "str":
            try:
                name = k.val.decode("ascii")
            except UnicodeDecodeError:
                name = None
            if name and _IDENT.match(name) and name not in LUA_KEYWORDS:
                return "%s.%s" % (o, name)
        return "%s[%s]" % (o, fmt(k, 0))


class Method(E):

    def __init__(self, obj, name):
        self.obj, self.name, self.seq = obj, name, _next_seq()

    def s(self):
        return "%s:%s" % (fmt(self.obj, 20, atom=True), self.name)


class Call(E):
    def __init__(self, func, args, nres):
        self.func, self.args, self.nres, self.seq = func, args, nres, _next_seq()
        self.paren = False

    def s(self):
        args = self.args
        if isinstance(self.func, Method):
            f = self.func.s()
            args = args[1:]
        else:
            f = fmt(self.func, 20, atom=True)
            if isinstance(self.func, Func):
                f = "(" + self.func.s() + ")"
        return "%s(%s)" % (f, fmt_args(args))


class Paren(E):
    prec = 20

    def __init__(self, e):
        self.e, self.seq = e, e.seq

    def s(self):
        return "(" + self.e.s() + ")"


class Bin(E):
    def __init__(self, op, l, r, prec, right=False):
        self.op, self.l, self.r, self.prec, self.right = op, l, r, prec, right
        self.seq = _next_seq()

    def s(self):
        p = self.prec
        lp = p if not self.right else p + 1
        rp = p + 1 if not self.right else p
        return "%s %s %s" % (fmt(self.l, lp), self.op, fmt(self.r, rp))


class Un(E):
    prec = 12

    def __init__(self, op, e):
        self.op, self.e, self.seq = op, e, _next_seq()

    def s(self):
        return "%s%s" % (self.op, fmt(self.e, 12))


class Concat(E):
    prec = 9

    def __init__(self, parts):
        self.parts, self.seq = parts, _next_seq()

    def s(self):
        return " .. ".join(fmt(p, 10) for p in self.parts)


class Table(E):
    def __init__(self):
        self.fields = []
        self.seq = _next_seq()

    def s(self):
        items = []
        for _, k, v in sorted(self.fields, key=lambda x: x[0]):
            if k is None:
                items.append(fmt(v, 0))
            elif isinstance(k, Const) and k.kind == "str" and _IDENT.match(
                    k.val.decode("latin-1")) and k.val.decode("latin-1") not in LUA_KEYWORDS \
                    and k.val.isascii():
                items.append("%s = %s" % (k.val.decode("ascii"), fmt(v, 0)))
            else:
                items.append("[%s] = %s" % (fmt(k, 0), fmt(v, 0)))
        if not items:
            return "{}"
        if len(items) > 3 or sum(len(i) for i in items) > 70:
            return "{\n" + "".join("    " + i.replace("\n", "\n    ") + ",\n" for i in items) + "}"
        return "{ " + ", ".join(items) + " }"


class Func(E):
    def __init__(self, dec):
        self.dec, self.seq = dec, _next_seq()

    def s(self, name=None):
        d = self.dec
        head = "function%s(%s)" % ("" if name is None else " " + name, ", ".join(d.param_list()))
        body = d.body_lines()
        if not body:
            return head + " end"
        return head + "\n" + "\n".join("    " + l for l in body) + "\nend"


class MultiPart(E):
    def __init__(self):
        self.seq = _next_seq()

    def s(self):
        return "nil --[[multi]]"


class Bad(E):
    def __init__(self, what):
        self.what, self.seq = what, _next_seq()

    def s(self):
        return "nil --[[?%s]]" % self.what


def _prec_of(e):
    if isinstance(e, Bin):
        return e.prec
    if isinstance(e, (Un,)):
        return 12
    if isinstance(e, Concat):
        return 9
    if isinstance(e, Func):
        return 0
    return 20


def fmt(e, minprec=0, atom=False):
    s = e.s()
    p = _prec_of(e)
    if isinstance(e, Const) and e.kind in ("int", "num") and atom:
        return "(" + s + ")"
    if isinstance(e, Const) and e.kind == "str" and atom:
        return "(" + s + ")"
    if isinstance(e, Table) and atom:
        return "(" + s + ")"
    if atom and not isinstance(e, (Name, Index, Call, Method)):
        return "(" + s + ")"
    if p < minprec:
        return "(" + s + ")"
    return s


def fmt_args(args):
    out = []
    for i, a in enumerate(args):
        t = fmt(a, 0)
        if i == len(args) - 1 and isinstance(a, (Call, Vararg)) and getattr(a, "paren", False):
            t = "(" + t + ")"
        out.append(t)
    return ", ".join(out)


def negate(e):
    if isinstance(e, Const):
        if e.kind == "bool":
            return Const("bool", not e.val)
        if e.kind == "nil":
            return Const("bool", True)
    if isinstance(e, Un) and e.op == "not ":
        return e.e
    if isinstance(e, Bin) and e.op == "==":
        return Bin("~=", e.l, e.r, 3)
    if isinstance(e, Bin) and e.op == "~=":
        return Bin("==", e.l, e.r, 3)
    if isinstance(e, Bin) and e.op in ("and", "or"):

        l, r = negate(e.l), negate(e.r)
        if not (isinstance(l, Un) and l.op == "not " and isinstance(r, Un) and r.op == "not "):
            return land(l, r) if e.op == "or" else lor(l, r)
    return Un("not ", e)


def _truthy_const(e):
    if isinstance(e, Const):
        if e.kind in ("int", "num", "str"):
            return True
        if e.kind == "bool":
            return bool(e.val)
        if e.kind == "nil":
            return False
    return None


def _is_boolish(e):
    return (isinstance(e, Const) and e.kind == "bool") or \
        (isinstance(e, Bin) and e.op in ("==", "~=", "<", "<=", ">", ">=")) or \
        (isinstance(e, Un) and e.op.strip() == "not")


def land(a, b):
    ta = _truthy_const(a)
    if ta is True:
        return b
    if ta is False:
        return a
    if isinstance(b, Const) and b.is_true() and _is_boolish(a):
        return a
    return Bin("and", a, b, 2)


def _is_simple(e):
    return isinstance(e, (Const, Name))


def lor(a, b):
    ta = _truthy_const(a)
    if ta is True:
        return a
    if ta is False:
        return b
    if isinstance(b, Const) and b.is_false() and _is_boolish(a):
        return a

    if (isinstance(a, Bin) and a.op == "and" and isinstance(a.r, Bin) and a.r.op == "or"
            and _is_simple(b) and _is_simple(a.r.r) and a.r.r.s() == b.s()):
        return Bin("or", Bin("and", a.l, a.r.l, 2), b, 1)
    return Bin("or", a, b, 1)


class DecompileError(Exception):
    pass


class Node:

    def __init__(self, j, target, begin, end):
        self.j, self.target, self.begin, self.end = j, target, begin, end


class FuncDec:
    def __init__(self, f, key, is_main=False, parent_name=None, game=True):
        self.f, self.key, self.is_main, self.game = f, key, is_main, game
        if game:
            xs = lambda b: None if b is None else xor_string(b, key).decode("latin-1")
        else:
            xs = lambda b: None if b is None else b.decode("latin-1")
        self.locvars = [(xs(n) or "?", a, b) for n, a, b in f.locvars]
        self.upn = [xs(n) for n in f.upnames]
        self.k = []
        kinds = {0: "nil", 1: "bool", 3: "num", 0x13: "int", 4: "str", 0x14: "str"}
        for t, v in f.k:
            kind = kinds[t]
            if kind == "str":
                self.k.append(Const("str", xor_string(v, key) if game else v))
            else:
                self.k.append(Const(kind, v))
        self.code = []
        for w in f.code:
            op = real_op(w & 0x3F) if game else (w & 0x3F)
            self.code.append((op, (w >> 6) & 0xFF, (w >> 23) & 0x1FF, (w >> 14) & 0x1FF,
                              w >> 14, (w >> 14) - 131071))
        self.n = len(self.code)
        self.subs = [FuncDec(p, key, game=game) for p in f.protos]
        self._active = {}
        self._lines = None
        self.labels = set()
        self.no_decl = 0
        self.in_val = None
        self.opened = set()
        self.repeat_ends = {}
        self.back_jumps = {}
        for p_, (o_, A_, B_, C_, Bx_, sBx_) in enumerate(self.code):
            if o_ == JMP and sBx_ < 0:
                self.back_jumps.setdefault(p_ + 1 + sBx_, []).append(p_)
        for p_, (o_, A_, B_, C_, Bx_, sBx_) in enumerate(self.code):
            if o_ in (EQ, LT, LE, TEST, TESTSET) and p_ + 1 < self.n and \
                    self.code[p_ + 1][0] == JMP and self.code[p_ + 1][5] < 0:
                L_ = p_ + 2 + self.code[p_ + 1][5]
                if self.continue_target(L_, p_ + 1) is None:
                    self.repeat_ends[L_] = max(self.repeat_ends.get(L_, 0), p_ + 2)

    def continue_target(self, tgt, pc):
        best = None
        for b in self.back_jumps.get(tgt, []):
            if b > pc and not (b >= 1 and self.code[b - 1][0] in (EQ, LT, LE, TEST, TESTSET)):
                if best is None or b < best:
                    best = b
        return best


    def active(self, pc):
        a = self._active.get(pc)
        if a is None:
            a = [nm for nm, s, e in self.locvars if s <= pc < e]
            self._active[pc] = a
        return a

    def upname(self, i):
        if i < len(self.upn) and self.upn[i]:
            return self.upn[i]
        return "_up%d" % i

    def param_list(self):
        names = [nm for nm, s, e in self.locvars if s == 0 and e > 0][: self.f.nparams]
        while len(names) < self.f.nparams:
            names.append("arg%d" % len(names))
        if self.f.vararg:
            names.append("...")
        return names


    def rd(self, r, pc, keep=False):
        act = self.active(pc)
        if r < len(act):
            return Name(act[r])
        e = self.regs.get(r)
        if e is None:
            self.errors.append("read of empty R%d at pc %d" % (r, pc))
            return Bad("R%d" % r)
        if not keep:
            del self.regs[r]
        return e

    def rk(self, x, pc):
        if x >= 256:
            c = self.k[x - 256]
            return Const(c.kind, c.val)
        return self.rd(x, pc)

    def upexpr(self, i):
        return Name(self.upname(i), "up")


    def write(self, r, e, pc, stmts):
        if self.in_val is not None and r == self.in_val:
            self.regs[r] = e
            return
        act = self.active(pc)
        if r < len(act):
            stmts.append(("assign", [Name(act[r])], [e]))
        else:
            self.regs[r] = e
            self.check_decl(pc, stmts)

    def check_decl(self, pc, stmts):
        if self.no_decl:
            return
        a0, a1 = self.active(pc), self.active(pc + 1)
        if len(a1) <= len(a0):
            return
        names = a1[len(a0):]
        if names[0].startswith("("):
            return
        regs = range(len(a0), len(a1))
        exprs = []
        for r in regs:
            e = self.regs.pop(r, None)
            if e is None:
                self.errors.append("local %s has no value at pc %d" % (a1[r], pc))
                e = Bad(a1[r])
            if isinstance(e, MultiPart):
                continue
            exprs.append(e)
        stmts.append(("local", names, exprs))


    def body_lines(self):
        if self._lines is None:
            self._lines = self.decompile()
        return self._lines

    def decompile(self):
        self.errors = []
        self.done_labels = set()
        try:
            self.regs = {}
            self.loops = []
            self.gotos = set()
            stmts = self.block(0, self.n)
            if self.errors:
                raise DecompileError("; ".join(self.errors[:3]))
            lines = render(stmts)

            return lines
        except Exception as ex:
            return self.fallback(str(ex))

    def fallback(self, why):
        out = ["-- [decompile failed: %s]" % why.replace("\n", " ")[:120],
               "--[[ disassembly"]
        for pc, (op, A, B, C, Bx, sBx) in enumerate(self.code):
            out.append("  %04d %-9s A=%d B=%d C=%d Bx=%d" % (pc, STD_OPS[op], A, B, C, Bx))
        out.append("]]")
        return out


    def block(self, lo, hi):
        stmts = []
        pc = lo
        stack = self.__dict__.setdefault("_his", [])
        stack.append(hi)
        opened = []
        try:
            while pc < hi:
                if pc in self.labels:
                    stmts.append(("label", pc))
                    self.labels.discard(pc)
                    self.done_labels.add(pc)


                cnt = len(self.active(pc))
                while opened and cnt <= opened[-1][1]:
                    idx, _ = opened.pop()
                    if idx < len(stmts):
                        inner = stmts[idx:]
                        del stmts[idx:]
                        stmts.append(("do", inner))
                before = cnt
                n0 = len(stmts)
                nxt = self.step(pc, hi, stmts)
                if len(self.active(nxt)) > before and nxt <= hi and not self.no_decl:
                    newnames = self.active(nxt)[before:]
                    if not newnames[0].startswith("("):
                        opened.append((n0, before))
                pc = nxt
        finally:
            stack.pop()


        if hi in self.labels and hi not in stack:
            stmts.append(("label", hi))
            self.labels.discard(hi)
            self.done_labels.add(hi)
        return stmts

    def loop_head(self, pc, stmts):
        if pc in self.repeat_ends and pc not in self.opened:
            self.opened.add(pc)
            hi2 = self.repeat_ends[pc]
            self.loops.append(hi2)
            body = self.block(pc, hi2)
            self.loops.pop()
            if body and body[-1][0] == "until":
                cond = body.pop()[1]
                stmts.append(("repeat", body, cond))
                return hi2
            raise DecompileError("repeat without until at pc %d" % pc)
        wb = [b_ for b_ in self.back_jumps.get(pc, [])
              if not (b_ >= 1 and self.code[b_ - 1][0] in (EQ, LT, LE, TEST, TESTSET))]
        if wb and ("w", pc) not in self.opened:
            b = max(wb)
            X = b + 1
            if self.is_cond_while(pc, b, X):
                return None
            self.opened.add(("w", pc))
            self.loops.append(X)
            body = self.block(pc, b)
            self.loops.pop()
            stmts.append(("while", Const("bool", True), body))
            return X
        return None

    def is_cond_while(self, pc, b, X):
        q = pc
        while q < b:
            o = self.code[q][0]
            if o in (EQ, LT, LE, TEST, TESTSET) and q + 1 < self.n and self.code[q + 1][0] == JMP:
                if q + 2 + self.code[q + 1][5] == X:
                    return True
                q += 2
                continue
            if not self.pure_op(o, q) or o == CLOSURE:
                return False

            if o not in (CALL,) and self.code[q][1] < len(self.active(q)):
                return False
            q += 1
        return False

    def pure_op(self, op, pc):
        if op == CALL:
            return self.code[pc][3] == 2
        return op in (MOVE, LOADK, LOADBOOL, LOADNIL, GETUPVAL, GETTABUP, GETTABLE,
                      NEWTABLE, SELF, UNM, BNOT, NOT, LEN, CONCAT, CLOSURE, VARARG,
                      LOADKX) or op in BINOPS

    def is_store(self, q):
        op, A = self.code[q][0], self.code[q][1]
        if op in (SETTABUP, SETUPVAL):
            return True
        n = len(self.active(q))
        if op == SETTABLE:
            return not (A >= n and isinstance(self.regs.get(A), Table))
        if op == MOVE:
            return A < n
        return False

    def pending_temps(self, n):
        return [r for r, e in self.regs.items()
                if r >= n and not isinstance(e, (Table, MultiPart))]

    def try_parallel(self, pc, stmts):
        if getattr(self, "_in_par", False) or not self.is_store(pc) or self.no_decl \
                or self.in_val is not None:
            return None
        n = len(self.active(pc))
        if not self.pending_temps(n):
            return None
        saved_regs, saved_err = dict(self.regs), len(self.errors)
        scratch, q = [], pc
        self._in_par = True
        try:
            while q < self.n and self.is_store(q):
                q = self.step(q, self.n, scratch)
                if not self.pending_temps(n):
                    break
        finally:
            self._in_par = False
        assigns = [s for s in scratch if s[0] == "assign" and len(s[1]) == 1 and len(s[2]) == 1]
        if len(assigns) >= 2 and len(assigns) == len(scratch) and not self.pending_temps(n):
            stmts.append(("assign", [s[1][0] for s in reversed(assigns)],
                          [s[2][0] for s in reversed(assigns)]))
            return q
        self.regs = saved_regs
        del self.errors[saved_err:]
        return None

    def step(self, pc, hi, stmts):
        nxt = self.loop_head(pc, stmts)
        if nxt is not None:
            return nxt
        if self.code[pc][0] in (MOVE, SETTABLE, SETTABUP, SETUPVAL):
            nxt = self.try_parallel(pc, stmts)
            if nxt is not None:
                return nxt
        op, A, B, C, Bx, sBx = self.code[pc]
        f = self.f
        if op == MOVE:
            self.write(A, self.rd(B, pc), pc, stmts)
        elif op == LOADK:
            self.write(A, Const(self.k[Bx].kind, self.k[Bx].val), pc, stmts)
        elif op == LOADKX:
            self.write(A, self.k[self.code[pc + 1][4] if False else self.code[pc + 1][1] * 0 + (self.f.code[pc + 1] >> 6)], pc, stmts)
            return pc + 2
        elif op == LOADBOOL:
            self.write(A, Const("bool", bool(B)), pc, stmts)
            if C:
                self.errors.append("stray LOADBOOL skip at pc %d" % pc)
        elif op == LOADNIL:
            for i in range(B + 1):
                r = A + i
                act = self.active(pc)
                if r < len(act):
                    stmts.append(("assign", [Name(act[r])], [Const("nil", None)]))
                else:
                    self.regs[r] = Const("nil", None)
            self.check_decl(pc, stmts)
        elif op == GETUPVAL:
            self.write(A, self.upexpr(B), pc, stmts)
        elif op == GETTABUP:
            up = self.upname(B)
            key = self.rk(C, pc)
            if up == "_ENV" and isinstance(key, Const) and key.kind == "str" and \
                    _IDENT.match(key.val.decode("latin-1")) and key.val.isascii():
                e = Name(key.val.decode("ascii"), "global")
            else:
                e = Index(self.upexpr(B), key)
            self.write(A, e, pc, stmts)
        elif op == GETTABLE:
            obj = self.rd(B, pc)
            self.write(A, Index(obj, self.rk(C, pc)), pc, stmts)
        elif op == SETTABUP:
            up = self.upname(A)
            key = self.rk(B, pc)
            val = self.rk(C, pc)
            if up == "_ENV" and isinstance(key, Const) and key.kind == "str" and \
                    _IDENT.match(key.val.decode("latin-1")) and key.val.isascii():
                target = Name(key.val.decode("ascii"), "global")
            else:
                target = Index(self.upexpr(A), key)
            stmts.append(("assign", [target], [val]))
        elif op == SETUPVAL:
            stmts.append(("assign", [self.upexpr(B)], [self.rd(A, pc)]))
        elif op == SETTABLE:
            act = self.active(pc)
            key = self.rk(B, pc)
            val = self.rk(C, pc)
            if A >= len(act) and isinstance(self.regs.get(A), Table):
                t = self.regs[A]
                t.fields.append((min(key.seq, val.seq) if hasattr(key, "seq") else val.seq,
                                 key, val))
                self.check_decl(pc, stmts)
            else:
                obj = self.rd(A, pc, keep=False) if A >= len(act) else Name(act[A])
                stmts.append(("assign", [Index(obj, key)], [val]))
        elif op == NEWTABLE:
            self.write(A, Table(), pc, stmts)
        elif op == SELF:
            obj = self.rd(B, pc, keep=B >= len(self.active(pc)))
            key = self.rk(C, pc)
            name = key.val.decode("latin-1") if isinstance(key, Const) and key.kind == "str" else None
            if name is None:
                self.errors.append("SELF with non-string key at pc %d" % pc)
                name = "?"
            self.regs[A + 1] = obj
            self.regs[A] = Method(obj, name)
            self.check_decl(pc, stmts)
        elif op in BINOPS:
            sym, p = BINOPS[op]
            l = self.rk(B, pc)
            r = self.rk(C, pc)
            self.write(A, Bin(sym, l, r, p, right=(op == POW)), pc, stmts)
        elif op in UNOPS:
            self.write(A, Un(UNOPS[op], self.rd(B, pc)), pc, stmts)
        elif op == CONCAT:
            parts = [self.rd(r, pc) for r in range(B, C + 1)]
            flat = []
            for p_ in parts:
                flat.append(p_)
            self.write(A, Concat(flat), pc, stmts)
        elif op == JMP:
            return self.jump(pc, hi, stmts)
        elif op in (EQ, LT, LE, TEST, TESTSET):
            return self.cond_stmt(pc, hi, stmts)
        elif op == CALL:
            self.do_call(pc, stmts)
        elif op == TAILCALL:
            call = self.make_call(pc, nres=0)
            stmts.append(("return", [call]))
            if pc + 1 < self.n and self.code[pc + 1][0] == RETURN:
                return pc + 2
        elif op == RETURN:
            if B == 1:
                if pc != self.n - 1:
                    stmts.append(("return", []))
            else:
                vals = self.collect(A, B - 1 if B else None, pc)
                if B and vals and isinstance(vals[-1], (Call, Vararg)) and not isinstance(vals[-1], Method):
                    vals[-1] = Paren(vals[-1])
                stmts.append(("return", vals))
        elif op == FORPREP:
            return self.for_num(pc, stmts)
        elif op == TFORCALL:
            self.errors.append("stray TFORCALL at pc %d" % pc)
        elif op == SETLIST:
            n = B
            batch = C
            nxt = pc + 1
            if C == 0:
                batch = f.code[pc + 1]
                nxt = pc + 2
            act = self.active(pc)
            t = self.regs.get(A)
            if not isinstance(t, Table):
                self.errors.append("SETLIST on non-table at pc %d" % pc)
                return nxt
            vals = self.collect(A + 1, n if n else None, pc)
            if n and vals and isinstance(vals[-1], (Call, Vararg)) and not isinstance(vals[-1], Method):
                vals[-1] = Paren(vals[-1])
            base = (batch - 1) * 50
            for i, v in enumerate(vals):
                t.fields.append((v.seq, None, v))
            self.check_decl(nxt - 1, stmts)
            return nxt
        elif op == CLOSURE:
            sub = self.subs[Bx]
            fn = Func(sub)
            act = self.active(pc)
            act2 = self.active(pc + 1)
            selfref = (1, A) in [tuple(u) for u in sub.f.up]
            if A < len(act) and A == len(act) - 1 and self.locstart(A, pc) == pc:
                stmts.append(("localfunc", act[A], fn))
            elif selfref and A < len(act2) and A == len(act2) - 1 and len(act2) > len(act) \
                    and self.locstart(A, pc + 1) == pc + 1:
                stmts.append(("localfunc", act2[A], fn))
            else:
                self.write(A, fn, pc, stmts)
        elif op == VARARG:
            v = Vararg()
            if B == 0:
                self.regs[A] = v
                self.open_top = A
            else:
                self.regs[A] = v
                for i in range(1, B - 1):
                    self.regs[A + i] = MultiPart()
            self.check_decl(pc, stmts)
        elif op == FORLOOP or op == TFORLOOP:
            self.errors.append("stray loop end at pc %d" % pc)
        elif op == EXTRAARG:
            pass
        else:
            self.errors.append("unhandled op %s at pc %d" % (STD_OPS[op], pc))
        return pc + 1

    def locstart(self, reg, pc):
        i = -1
        for nm, s, e in self.locvars:
            if s <= pc < e:
                i += 1
                if i == reg:
                    return s
        return None


    def collect(self, first, count, pc):
        act = self.active(pc)
        out = []
        if count is None:
            r = first
            while r in self.regs or r < len(act):
                out.append(self.rd(r, pc))
                r += 1
        else:
            for i in range(count):
                out.append(self.rd(first + i, pc))
        return out

    def make_call(self, pc, nres):
        op, A, B, C, Bx, sBx = self.code[pc]
        args = self.collect(A + 1, (B - 1) if B else None, pc)
        func = self.rd(A, pc)
        call = Call(func, args, nres)
        if args and isinstance(args[-1], (Call, Vararg)) and B != 0 and \
                not isinstance(args[-1], Method):
            args[-1].paren = True
        return call

    def do_call(self, pc, stmts):
        op, A, B, C, Bx, sBx = self.code[pc]
        call = self.make_call(pc, C - 1)
        if C == 1:
            stmts.append(("call", call))
        elif C == 2:
            self.write(A, call, pc, stmts)
        else:
            self.regs[A] = call
            if C > 2:
                for i in range(1, C - 1):
                    self.regs[A + i] = MultiPart()
            self.check_decl(pc, stmts)


    def is_bare_return(self, tgt):
        return 0 <= tgt < self.n and self.code[tgt][0] == RETURN and self.code[tgt][2] == 1

    def jump(self, pc, hi, stmts):
        op, A, B, C, Bx, sBx = self.code[pc]
        tgt = pc + 1 + sBx
        if A > 0 and sBx == 0:
            return pc + 1
        if sBx < 0:
            b = self.continue_target(tgt, pc)
            if b is not None:
                self.labels.add(b)
                stmts.append(("goto", b))
                return pc + 1
            self.errors.append("unexpected backward jump at pc %d" % pc)
            return pc + 1
        if tgt < self.n and self.code[tgt][0] == TFORCALL:
            tA = self.code[tgt][1]
            names = self.active(pc + 1)
            if len(names) > tA + 2 and names[tA].startswith("(for") and \
                    self.locstart(tA, pc + 1) == pc:
                return self.for_in(pc, tgt, stmts)
        if self.loops and tgt == self.loops[-1]:
            stmts.append(("break",))
        elif self.is_bare_return(tgt):
            stmts.append(("return", []))
        else:
            self.labels.add(tgt)
            stmts.append(("goto", tgt))
        return pc + 1

    def cond_node(self, p):
        op, A, B, C, Bx, sBx = self.code[p]
        jop, jA, jB, jC, jBx, jsBx = self.code[p + 1]
        if jop != JMP:
            raise DecompileError("cond without JMP at pc %d" % p)
        tgt = p + 2 + jsBx
        if op in (EQ, LT, LE):
            l = self.rk(B, p)
            r = self.rk(C, p)
            sym = CMPOPS[op]
            if op in (LT, LE):


                nact = len(self.active(p))
                swap = False
                if B >= 256 and C < 256:
                    swap = True
                elif B < 256 and C < 256 and B >= nact and C >= nact and B > C:
                    swap = True
                if swap:
                    l, r, sym = r, l, (">" if op == LT else ">=")
            cmp_ = Bin(sym, l, r, 3)
            j = cmp_ if A == 1 else negate(cmp_) if op == EQ else Un("not ", Bin(sym, l, r, 3))
        elif op == TEST:
            v = self.rd(A, p, keep=True)
            j = v if C == 1 else negate(v)
        else:
            raise DecompileError("TESTSET in statement context at pc %d" % p)
        return Node(j, tgt, p, p + 2)

    def gather(self, pc0):
        nodes = []
        snaps = []
        p = pc0
        while True:
            n = self.cond_node(p)
            nodes.append(n)

            op, A, B, C, Bx, sBx = self.code[p]
            if op in (EQ, LT, LE):
                for x in (B, C):
                    if x < 256 and x >= len(self.active(p)):
                        self.regs.pop(x, None)
            elif op == TEST and A >= len(self.active(p)):
                self.regs.pop(A, None)
            snaps.append(dict(self.regs))
            q = p + 2

            nxt = None
            scratch = []
            save = dict(self.regs)
            ok = True
            while q < self.n:
                o = self.code[q][0]
                if o in (EQ, LT, LE, TEST):


                    if len(self.active(q)) > len(self.active(p + 2)):
                        break
                    nxt = q
                    break
                if not self.pure_op(o, q) or (o == CLOSURE) or \
                        (o == LOADBOOL and self.code[q][3] == 1):
                    break
                nerr = len(self.errors)
                self.no_decl += 1
                try:
                    self.step(q, self.n, scratch)
                except Exception:
                    ok = False
                    break
                finally:
                    self.no_decl -= 1
                    del self.errors[nerr:]
                if scratch:
                    ok = False
                    break
                q += 1
            if nxt is None or not ok:
                self.regs = dict(snaps[-1])
                break
            p = nxt
        return nodes, snaps

    def merge(self, nodes):
        nodes = list(nodes)
        changed = True
        while changed and len(nodes) > 1:
            changed = False
            for i in range(len(nodes) - 1):
                a, b = nodes[i], nodes[i + 1]
                if a.target == b.target:
                    m = Node(lor(a.j, b.j), b.target, a.begin, b.end)
                elif a.target == b.end:
                    m = Node(land(negate(a.j), b.j), b.target, a.begin, b.end)
                else:
                    continue
                nodes[i:i + 2] = [m]
                changed = True
                break
        return nodes

    def bool_value(self, pc):
        saved = dict(self.regs)
        try:
            nodes, snaps = self.gather(pc)
            merged = self.merge(nodes)
            first = merged[0]
            absorbed = 0
            for i, n in enumerate(nodes):
                if n.end <= first.end:
                    absorbed = i + 1
            end, tgt = first.end, first.target
            if end + 1 < self.n and self.code[end][0] == LOADBOOL and self.code[end][3] == 1 \
                    and self.code[end + 1][0] == LOADBOOL and tgt in (end, end + 1):
                self.regs = dict(snaps[absorbed - 1])
                val = first.j if tgt == end + 1 else negate(first.j)
                return self.code[end][1], val, end + 2
        except DecompileError:
            pass
        self.regs = saved
        return None

    def cond_stmt(self, pc, hi, stmts):
        op = self.code[pc][0]
        if op == TESTSET:
            return self.value_chain(pc, stmts)
        bv = self.bool_value(pc)
        if bv is not None:
            dest, val, nxt = bv
            self.write(dest, val, nxt - 1, stmts)
            return nxt
        start_regs = dict(self.regs)
        nodes, snaps = self.gather(pc)
        merged = self.merge(nodes)
        first = merged[0]

        absorbed = 0
        for i, n in enumerate(nodes):
            if n.end <= first.end:
                absorbed = i + 1
        self.regs = dict(snaps[absorbed - 1])
        end = first.end
        tgt = first.target

        if end + 1 < self.n and self.code[end][0] == LOADBOOL and self.code[end][3] == 1 \
                and self.code[end + 1][0] == LOADBOOL:
            dest = self.code[end][1]
            if tgt == end + 1:
                val = first.j
            elif tgt == end:
                val = negate(first.j)
            else:
                raise DecompileError("odd boolean chain at pc %d" % pc)
            val = self.simplify_bool(val)
            self.write(dest, val, end + 1, stmts)
            return end + 2

        if tgt > end and self.is_value_ctx(pc, first):
            self.regs = start_regs
            return self.value_chain(pc, stmts)
        if tgt <= pc:
            cb = self.continue_target(tgt, end - 1)
            if cb is not None and not (tgt in self.repeat_ends and end == self.repeat_ends[tgt]):
                self.labels.add(cb)
                stmts.append(("if", first.j, [("goto", cb)], None))
                return end
            if tgt in self.repeat_ends and end == self.repeat_ends[tgt]:
                stmts.append(("until", negate(first.j)))
                return end
            raise DecompileError("repeat-until at pc %d not in loop context" % pc)


        if tgt > hi and hi < self.n and self.code[hi][0] == JMP and self.code[hi][5] > 0 \
                and hi + 1 + self.code[hi][5] == tgt and hi >= end:
            then_body = self.block(end, hi)
            stmts.append(("if", negate(first.j), then_body, None))
            return hi

        if tgt > hi:
            if self.loops and tgt == self.loops[-1]:
                stmts.append(("if", first.j, [("break",)], None))
            elif self.is_bare_return(tgt):
                stmts.append(("if", first.j, [("return", [])], None))
            else:
                self.labels.add(tgt)
                stmts.append(("if", first.j, [("goto", tgt)], None))
            return end

        cond = negate(first.j)

        back = tgt - 1
        if back > end - 1 and self.code[back][0] == JMP and self.code[back][5] < 0:
            loop_start = back + 1 + self.code[back][5]
            if loop_start <= pc:
                self.loops.append(tgt)
                body = self.block(end, back)
                self.loops.pop()
                stmts.append(("while", cond, body))
                return tgt

        else_end = None
        last = tgt - 1
        if last >= end and self.code[last][0] == JMP and self.code[last][5] > 0 \
                and not (last - 1 >= end and self.code[last - 1][0] in (EQ, LT, LE, TEST, TESTSET)):

            g = last + 1 + self.code[last][5]
            if not (self.loops and g == self.loops[-1]) and g > tgt:


                else_end = min(g, hi)
        if else_end is not None:
            then_body = self.block(end, last)
            else_body = self.block(tgt, else_end)
            stmts.append(("if", cond, then_body, else_body))
            return else_end
        then_body = self.block(end, tgt)
        stmts.append(("if", cond, then_body, None))
        return tgt

    def simplify_bool(self, e):
        return e

    def extend_chain_end(self, pc, M):
        changed = True
        while changed:
            changed = False
            for q in range(pc, min(M, self.n)):
                if self.code[q][0] in (EQ, LT, LE, TEST, TESTSET) and q + 1 < self.n \
                        and self.code[q + 1][0] == JMP:
                    t = q + 2 + self.code[q + 1][5]
                    if t > M:
                        M = t
                        changed = True
        return M

    def is_value_ctx(self, pc, node):
        M = node.target
        if M <= node.end or M > self.n:
            return False
        M = self.extend_chain_end(pc, M)
        if M - 1 <= pc + 1 or M > self.n:
            return False
        last = self.code[M - 1]
        lop = last[0]
        if not (self.pure_op(lop, M - 1) or (lop == CALL and last[3] == 2)):
            return False
        dest = last[1]
        if dest < len(self.active(pc)):
            return False
        for q in range(pc + 2, M - 1):
            o = self.code[q][0]
            if not (self.pure_op(o, q) or o in (EQ, LT, LE, TEST, TESTSET, JMP) or
                    (o == CALL and self.code[q][3] == 2) or

                    (o == CALL and self.code[q][3] == 0 and q + 1 < self.n and
                     self.code[q + 1][0] in (CALL, TAILCALL, RETURN, SETLIST) and
                     self.code[q + 1][2] == 0)):
                return False
        return True

    def value_chain(self, pc, stmts):
        op0, A0 = self.code[pc][0], self.code[pc][1]
        M = pc + 2 + self.code[pc + 1][5]
        changed = True
        while changed:
            changed = False
            for q in range(pc, min(M, self.n)):
                if self.code[q][0] in (EQ, LT, LE, TEST, TESTSET) and q + 1 < self.n \
                        and self.code[q + 1][0] == JMP:
                    t = q + 2 + self.code[q + 1][5]
                    if t > M:
                        M = t
                        changed = True
        if M < self.n and self.code[M][0] == LOADBOOL and self.code[M][3] == 0 and \
                M >= 1 and self.code[M - 1][0] == LOADBOOL and self.code[M - 1][3] == 1:
            M += 1
        if M <= pc + 2 or M > self.n:
            raise DecompileError("bad value chain at pc %d" % pc)
        dest = A0 if op0 == TESTSET else self.code[M - 1][1]
        self.no_decl += 1
        prev_val, self.in_val = self.in_val, dest
        try:
            V, fregs = self.val(pc, M, dest, dict(self.regs))
        finally:
            self.no_decl -= 1
            self.in_val = prev_val
        self.regs = fregs
        self.write(dest, V, M - 1, stmts)
        return M

    def val(self, p, M, dest, regs):
        self.regs = dict(regs)
        while p < M:
            op, A, B, C, Bx, sBx = self.code[p]
            if op == JMP:
                t = p + 1 + sBx
                if t == M:
                    break
                if t < p:
                    raise DecompileError("backward jump in value chain at pc %d" % p)
                p = t
                continue
            if op in (TEST, EQ, LT, LE) and not (op == TEST and A == dest and
                                                 A >= len(self.active(p))):
                bv = self.bool_value(p)
                if bv is not None:
                    d2, v2, p = bv
                    self.regs[d2] = v2
                    continue
            if op in (TESTSET, TEST, EQ, LT, LE):
                jt = p + 2 + self.code[p + 1][5]
                carried = None
                if op == TESTSET:
                    carried = self.rd(B, p)
                elif op == TEST and A == dest and A >= len(self.active(p)):
                    carried = self.rd(A, p)
                else:
                    n = self.cond_node(p)
                    j = n.j
                    if op == TEST and A >= len(self.active(p)):
                        self.regs.pop(A, None)
                    if op in (EQ, LT, LE):
                        for x in (B, C):
                            if x < 256 and x >= len(self.active(p)):
                                self.regs.pop(x, None)
                after = dict(self.regs)
                F, fregs = self.val(p + 2, M, dest, after)
                if carried is not None:
                    x = carried
                    if jt == M:
                        V = lor(x, F) if C == 1 else land(x, F)
                    else:
                        Jv, _ = self.val(jt, M, dest, after)
                        V = lor(land(x, F), Jv) if C == 0 else lor(land(negate(x), F), Jv)
                else:
                    Jv, _ = self.val(jt, M, dest, after)
                    if isinstance(Jv, Const) and Jv.is_true():

                        V = lor(j, F)
                    elif isinstance(F, Bin) and F.op == "and" and F.r.s() == Jv.s() and \
                            not isinstance(Jv, Call):
                        V = land(lor(j, F.l), Jv)
                    else:
                        V = lor(land(negate(j), F), Jv)
                return V, fregs
            scratch = []
            nerr = len(self.errors)
            self.step(p, self.n, scratch)
            if scratch:
                raise DecompileError("statement inside value chain at pc %d" % p)
            p += 1
        e = self.regs.pop(dest, None)
        if e is None:
            raise DecompileError("value chain leaves no value (R%d) at pc %d" % (dest, p))
        return e, self.regs

    def for_in(self, pc, tcall, stmts):
        op, A, B, C, Bx, sBx = self.code[tcall]
        names = self.active(pc + 1)
        vars_ = names[A + 3:A + 3 + C]
        if len(vars_) != C:
            vars_ = ["k", "v", "v3", "v4"][:C]
        exprs = []
        e0 = self.regs.pop(A, None)
        if e0 is None:
            raise DecompileError("for-in without iterator at pc %d" % pc)
        exprs.append(e0)
        for r in (A + 1, A + 2):
            e = self.regs.pop(r, None)
            if e is None or isinstance(e, MultiPart):
                continue
            exprs.append(e)
        while len(exprs) > 1 and isinstance(exprs[-1], Const) and exprs[-1].kind == "nil":
            exprs.pop()
        self.loops.append(tcall + 2)
        body = self.block(pc + 1, tcall)
        self.loops.pop()
        stmts.append(("forin", vars_, exprs, body))
        return tcall + 2

    def for_num(self, pc, stmts):
        op, A, B, C, Bx, sBx = self.code[pc]
        loop = pc + 1 + sBx
        names = self.active(pc + 1)
        var = names[A + 3] if len(names) > A + 3 else "i"
        vals = []
        for r in (A, A + 1, A + 2):
            e = self.regs.pop(r, None)
            if e is None:
                raise DecompileError("numeric for without bound R%d at pc %d" % (r, pc))
            vals.append(e)
        start, stop, step = vals
        self.loops.append(loop + 1)
        body = self.block(pc + 1, loop)
        self.loops.pop()
        s = None if (isinstance(step, Const) and step.kind == "int" and step.val == 1) else step
        stmts.append(("fornum", var, start, stop, s, body))
        return loop + 1


def render(stmts, ind=0):
    out = []
    pad = "    "
    for si, st in enumerate(stmts):
        k = st[0]
        if k == "return" and si != len(stmts) - 1:

            inner = render([st])
            out.append("do " + inner[0])
            out.extend(inner[1:])
            out[-1] += " end"
            continue
        if k == "local":
            names, exprs = st[1], st[2]
            line = "local " + ", ".join(names)
            if exprs:
                line += " = " + ", ".join(e_str(e) for e in exprs)
            out.extend(multiline(line))
        elif k == "assign":
            tg, ex = st[1], st[2]
            if len(tg) == 1 and len(ex) == 1 and isinstance(ex[0], Func) and isinstance(tg[0], (Name, Index)):
                out.extend(funcdef(tg[0], ex[0]))
            else:
                out.extend(multiline(", ".join(t.s() for t in tg) + " = " +
                                     ", ".join(e_str(e) for e in ex)))
        elif k == "call":
            out.extend(multiline(st[1].s()))
        elif k == "do":
            out.append("do")
            out.extend("    " + l for l in render(st[1]))
            out.append("end")
        elif k == "return":
            out.extend(multiline("return" + (" " + ", ".join(e_str(e) for e in st[1]) if st[1] else "")))
        elif k == "break":
            out.append("break")
        elif k == "goto":
            out.append("goto L_%d" % st[1])
        elif k == "localfunc":
            f = st[2].s(name=st[1])
            out.extend(("local " + f).split("\n"))
        elif k == "if":
            out.extend(render_if(st))
        elif k == "while":
            out.append("while %s do" % fmt(st[1], 0))
            out.extend(pad + l for l in render(st[2]))
            out.append("end")
        elif k == "forin":
            out.append("for %s in %s do" % (", ".join(st[1]), ", ".join(e_str(e) for e in st[2])))
            out.extend(pad + l for l in render(st[3]))
            out.append("end")
        elif k == "repeat":
            out.append("repeat")
            out.extend(pad + l for l in render(st[1]))
            out.append("until %s" % fmt(st[2], 0))
        elif k == "label":
            out.append("::L_%d::" % st[1])
        elif k == "fornum":
            hdr = "for %s = %s, %s" % (st[1], fmt(st[2], 0), fmt(st[3], 0))
            if st[4] is not None:
                hdr += ", " + fmt(st[4], 0)
            out.append(hdr + " do")
            out.extend(pad + l for l in render(st[5]))
            out.append("end")
        else:
            out.append("-- unknown statement %r" % (k,))
    return out


def e_str(e):
    return fmt(e, 0)


def multiline(s):
    return s.split("\n")


def funcdef(target, fn):
    if isinstance(target, Name) and target.kind in ("global",):
        text = fn.s(name=target.n)
        return text.split("\n")
    if isinstance(target, Index) and isinstance(target.key, Const) and target.key.kind == "str":
        try:
            nm = target.key.val.decode("ascii")
        except UnicodeDecodeError:
            nm = None
        if nm and _IDENT.match(nm) and nm not in LUA_KEYWORDS:
            params = fn.dec.param_list()
            base = fmt(target.obj, 20, atom=True)
            if params and params[0] == "self":
                head = "function %s:%s(%s)" % (base, nm, ", ".join(params[1:]))
            else:
                head = "function %s.%s(%s)" % (base, nm, ", ".join(params))
            body = fn.dec.body_lines()
            if not body:
                return [head + " end"]
            return [head] + ["    " + l for l in body] + ["end"]
    return (target.s() + " = " + fn.s()).split("\n")


def render_if(st):
    out = []
    pad = "    "
    cond, then_b, else_b = st[1], st[2], st[3]
    out.append("if %s then" % fmt(cond, 0))
    out.extend(pad + l for l in render(then_b))
    while else_b is not None:
        if len(else_b) == 1 and else_b[0][0] == "if":
            inner = else_b[0]
            out.append("elseif %s then" % fmt(inner[1], 0))
            out.extend(pad + l for l in render(inner[2]))
            else_b = inner[3]
        else:
            out.append("else")
            out.extend(pad + l for l in render(else_b))
            else_b = None
    out.append("end")
    return out


def decompile_blob(blob: bytes):
    ch = parse_chunk(blob)
    game = ch.fmt == "game"
    d = FuncDec(ch.main, STRING_XOR_KEY, is_main=True, game=game)
    text = "\n".join(d.body_lines()) + "\n"
    text = _tidy_labels(text)

    def walk(x):
        yield x
        for c in x.subs:
            yield from walk(c)
    fns = list(walk(d))
    failed = sum(1 for x in fns if x._lines and x._lines[0].startswith("-- [decompile failed"))
    return text, len(fns), failed


def _tidy_labels(text: str) -> str:
    lines = text.split("\n")
    out = list(lines)
    for i, ln in enumerate(lines):
        m = re.fullmatch(r"(\s*)::(L_\d+)::", ln)
        if not m:
            continue
        nxt = next((l for l in lines[i + 1:] if l.strip()), "")
        if nxt.strip() in ("end", "until") or nxt.strip().startswith("until "):

            name = m.group(2)
            new = "continue"

            out[i] = m.group(1) + "::%s::" % new
            for j in range(i - 1, -1, -1):
                if re.match(r"\s*(for |while |repeat)", lines[j]) and len(lines[j]) - len(lines[j].lstrip()) < len(m.group(1)):
                    break
                out[j] = out[j].replace("goto " + name, "goto " + new) if re.match(r"\s*(if .*then\s*)?goto\b", out[j].strip()) or ("goto " + name) in out[j] else out[j]
    return "\n".join(out)


def check_lua_syntax(src: str):
    problems = []
    i, n, line = 0, len(src), 1
    toks = []
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1; i += 1
        elif c.isspace():
            i += 1
        elif src.startswith("--", i):
            m = re.match(r"--\[(=*)\[", src[i:])
            if m:
                close = "]" + m.group(1) + "]"
                j = src.find(close, i)
                j = n if j < 0 else j + len(close)
                line += src.count("\n", i, j); i = j
            else:
                j = src.find("\n", i)
                i = n if j < 0 else j
        elif c in "\"'":
            j = i + 1
            while j < n and src[j] != c:
                if src[j] == "\\":
                    j += 1
                if j < n and src[j] == "\n":
                    line += 1
                j += 1
            if j >= n:
                problems.append("line %d: unterminated string" % line)
            i = j + 1; toks.append(("str", "", line))
        elif c == "[" and re.match(r"\[=*\[", src[i:]):
            m = re.match(r"\[(=*)\[", src[i:])
            close = "]" + m.group(1) + "]"
            j = src.find(close, i)
            j = n if j < 0 else j + len(close)
            line += src.count("\n", i, j); i = j; toks.append(("str", "", line))
        elif c.isalpha() or c == "_":
            m = re.match(r"[A-Za-z_][A-Za-z_0-9]*", src[i:])
            toks.append(("id", m.group(0), line)); i += len(m.group(0))
        elif c.isdigit():
            m = re.match(r"0[xX][0-9a-fA-F.]+([pP][+-]?\d+)?|\d+\.?\d*([eE][+-]?\d+)?", src[i:])
            toks.append(("num", m.group(0), line)); i += len(m.group(0))
        else:
            two = src[i:i + 2]
            if two == "::":
                toks.append(("op", "::", line)); i += 2
            else:
                toks.append(("op", c, line)); i += 1

    stack = []
    closers = {"end", "until"}
    pending_do = 0
    scopes = [{"labels": {}, "gotos": []}]
    k = 0
    while k < len(toks):
        t, v, ln = toks[k]
        if t == "id":
            if v in ("function", "if"):
                stack.append((v, ln)); scopes.append({"labels": {}, "gotos": []})
            elif v in ("for", "while"):
                stack.append((v, ln)); pending_do += 1; scopes.append({"labels": {}, "gotos": []})
            elif v == "repeat":
                stack.append((v, ln)); scopes.append({"labels": {}, "gotos": []})
            elif v == "do":
                if pending_do:
                    pending_do -= 1
                else:
                    stack.append((v, ln)); scopes.append({"labels": {}, "gotos": []})
            elif v == "end":
                if not stack or stack[-1][0] == "repeat":
                    problems.append("line %d: unexpected 'end'" % ln)
                else:
                    stack.pop(); _close_scope(scopes, problems)
            elif v == "until":
                if not stack or stack[-1][0] != "repeat":
                    problems.append("line %d: unexpected 'until'" % ln)
                else:
                    stack.pop(); _close_scope(scopes, problems)
            elif v == "goto" and k + 1 < len(toks):
                scopes[-1]["gotos"].append((toks[k + 1][1], ln))
            elif v == "return":
                nx = toks[k + 1][1] if k + 1 < len(toks) else ""
                if nx not in ("end", "else", "elseif", "until", ""):

                    depth = 0; q = k + 1
                    while q < len(toks):
                        tv = toks[q][1] if toks[q][0] == "id" else ""
                        if tv in ("function", "if", "for", "while", "do", "repeat"):
                            if not (tv == "do" and q > 0 and toks[q - 1][1] in ("for", "while")) and tv in ("function", "if", "do", "repeat", "for", "while"):
                                depth += 1
                        elif tv in ("end", "until") and depth:
                            depth -= 1
                        elif tv in ("end", "else", "elseif", "until") and not depth:
                            break
                        q += 1
        elif t == "op" and v == "::" and k + 2 < len(toks) and toks[k + 2][1] == "::":
            scopes[-1]["labels"][toks[k + 1][1]] = ln; k += 2
        k += 1
    for kind, ln in stack:
        problems.append("line %d: '%s' never closed" % (ln, kind))
    _close_scope(scopes, problems, final=True)
    return problems


def _close_scope(scopes, problems, final=False):
    sc = scopes.pop() if len(scopes) > 1 or final else None
    if not sc:
        return
    for name, ln in sc["gotos"]:
        if name not in sc["labels"]:

            if scopes:
                scopes[-1]["gotos"].append((name, ln))
            else:
                problems.append("line %d: goto '%s' has no visible label" % (ln, name))


def coverage_check(blob: bytes, text: str):
    ch = parse_chunk(blob)
    game = ch.fmt == "game"
    d = FuncDec(ch.main, STRING_XOR_KEY, is_main=True, game=game)
    found = total = 0
    stack = [d]
    while stack:
        x = stack.pop()
        stack.extend(x.subs)
        for c in x.k:
            if c.kind == "str":
                total += 1
                sv = c.val.decode("latin-1") if isinstance(c.val, bytes) else c.val
                if sv in text or lua_quote(c.val) in text:
                    found += 1
    return found, total

def source_name_of(blob: bytes):
    try:
        ch = parse_chunk(blob)
        s = ch.main.source
        if s is None:
            return None
        if ch.fmt == "game":
            s = xor_string(s)
        return s.decode("latin-1")
    except Exception:
        return None


class LuaCompileError(Exception):
    pass


NO_JUMP = -1
NO_REG = 255
MAXARG_A, MAXARG_C, MAXARG_Bx = 255, 511, 262143
MAXARG_sBx, MAXARG_Ax = 131071, (1 << 26) - 1
BITRK = 256
MAXINDEXRK = 255
LFIELDS_PER_FLUSH = 50
LUA_MULTRET = -1
MAXVARS, MAXUPVAL, MAXREGS = 200, 255, 255

(VVOID, VNIL, VTRUE, VFALSE, VK, VKFLT, VKINT, VNONRELOC, VLOCAL, VUPVAL,
 VINDEXED, VJMP, VRELOCABLE, VCALL, VVARARG) = range(15)

(OPR_ADD, OPR_SUB, OPR_MUL, OPR_MOD, OPR_POW, OPR_DIV, OPR_IDIV, OPR_BAND, OPR_BOR,
 OPR_BXOR, OPR_SHL, OPR_SHR, OPR_CONCAT, OPR_EQ, OPR_LT, OPR_LE, OPR_NE, OPR_GT,
 OPR_GE, OPR_AND, OPR_OR, OPR_NOBINOPR) = range(22)
(OPR_MINUS, OPR_BNOT, OPR_NOT, OPR_LEN, OPR_NOUNOPR) = range(5)

_PRIORITY = [(10, 10), (10, 10), (11, 11), (11, 11), (14, 13), (11, 11), (11, 11),
             (6, 6), (4, 4), (5, 5), (7, 7), (7, 7), (9, 8), (3, 3), (3, 3), (3, 3),
             (3, 3), (3, 3), (3, 3), (2, 2), (1, 1)]
_UNARY_PRIORITY = 12

_BINOPR = {"+": OPR_ADD, "-": OPR_SUB, "*": OPR_MUL, "%": OPR_MOD, "^": OPR_POW,
           "/": OPR_DIV, "//": OPR_IDIV, "&": OPR_BAND, "|": OPR_BOR, "~": OPR_BXOR,
           "<<": OPR_SHL, ">>": OPR_SHR, "..": OPR_CONCAT, "~=": OPR_NE, "==": OPR_EQ,
           "<": OPR_LT, "<=": OPR_LE, ">": OPR_GT, ">=": OPR_GE, "and": OPR_AND,
           "or": OPR_OR}
_UNOPR = {"not": OPR_NOT, "-": OPR_MINUS, "~": OPR_BNOT, "#": OPR_LEN}

_RESERVED = frozenset(["and", "break", "do", "else", "elseif", "end", "false", "for",
                       "function", "goto", "if", "in", "local", "nil", "not", "or",
                       "repeat", "return", "then", "true", "until", "while"])
_RE_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _iABC(op, a, b, c):
    return op | (a << 6) | (c << 14) | (b << 23)


def _iABx(op, a, bx):
    return op | (a << 6) | (bx << 14)


def _iAsBx(op, a, sbx):
    return op | (a << 6) | ((sbx + MAXARG_sBx) << 14)


def _get_op(i): return i & 0x3F
def _get_A(i): return (i >> 6) & 0xFF
def _get_B(i): return (i >> 23) & 0x1FF
def _get_C(i): return (i >> 14) & 0x1FF
def _get_sBx(i): return (i >> 14) - MAXARG_sBx


def _set_op(i, op): return (i & ~0x3F) | op
def _set_A(i, v): return (i & ~(0xFF << 6)) | (v << 6)
def _set_B(i, v): return (i & ~(0x1FF << 23)) | (v << 23)
def _set_C(i, v): return (i & ~(0x1FF << 14)) | (v << 14)
def _set_sBx(i, v): return (i & 0x3FFF) | ((v + MAXARG_sBx) << 14)


def _test_tmode(op):
    return op in (EQ, LT, LE, TEST, TESTSET)


def _wrap64(x):
    x &= 0xFFFFFFFFFFFFFFFF
    return x - (1 << 64) if x >= (1 << 63) else x


def _int2fb(x):
    e = 0
    if x < 8:
        return x
    while x >= (8 << 4):
        x = (x + 0xF) >> 4
        e += 4
    while x >= (8 << 1):
        x = (x + 1) >> 1
        e += 1
    return ((e + 1) << 3) | (x - 8)


def _to_int_exact(v):
    if isinstance(v, int):
        return v
    if v != v or v in (float("inf"), float("-inf")):
        return None
    if v == int(v) and -(2.0 ** 63) <= v < 2.0 ** 63:
        return int(v)
    return None


def _arith(op, a, b):
    isint = isinstance(a, int) and isinstance(b, int)
    try:
        if op in (7, 8, 9, 10, 11, 13):
            x, y = _to_int_exact(a), _to_int_exact(b)
            if x is None or y is None:
                return None
            if op == 7:
                return _wrap64(x & y)
            if op == 8:
                return _wrap64(x | y)
            if op == 9:
                return _wrap64(x ^ y)
            if op == 13:
                return _wrap64(~x)

            def shl(v, n):
                if n <= -64 or n >= 64:
                    return 0
                if n >= 0:
                    return _wrap64(v << n)
                return _wrap64((v & 0xFFFFFFFFFFFFFFFF) >> (-n))
            return shl(x, y) if op == 10 else shl(x, -y)
        if op == 12:
            return _wrap64(-a) if isinstance(a, int) else -a
        if op in (0, 1, 2) and isint:
            return _wrap64(a + b if op == 0 else a - b if op == 1 else a * b)
        if op == 3:
            if isint:
                return _wrap64(a % b)
            a, b = float(a), float(b)
            m = math.fmod(a, b)
            if (m > 0 and b < 0) or (m < 0 and b != m and b > 0) or (m < 0 and b < 0 and False):
                m += b
            return m
        if op == 6:
            if isint:
                return _wrap64(a // b)
            return float(math.floor(float(a) / float(b)))
        a, b = float(a), float(b)
        if op == 0:
            return a + b
        if op == 1:
            return a - b
        if op == 2:
            return a * b
        if op == 4:
            return math.pow(a, b)
        if op == 5:
            return a / b
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    return None


class _Lex:
    def __init__(self, src, chunk):
        if src.startswith(b"\xef\xbb\xbf"):
            src = src[3:]
        self.s = src.decode("latin-1")
        self.n = len(self.s)
        self.p = 0
        self.linenumber = 1
        self.lastline = 1
        self.chunk = chunk
        if self.s.startswith("#"):
            j = self.s.find("\n")
            self.p = self.n if j < 0 else j
        self.t = ("EOS", None, "<eof>")
        self.la = None


    def error(self, msg, near=None, line=None):
        text = "%s:%d: %s" % (self.chunk, line or self.linenumber, msg)
        if near:
            text += " near " + near
        raise LuaCompileError(text)

    def tokstr(self, t):
        if t[0] == "EOS":
            return "<eof>"
        if t[0] in ("NAME", "STRING", "INT", "FLT"):
            return "'%s'" % t[2]
        return "'%s'" % t[0]


    def next(self):
        self.lastline = self.linenumber
        if self.la is not None:
            self.t, self.la = self.la, None
        else:
            self.t = self._llex()

    def lookahead(self):
        self.la = self._llex()
        return self.la[0]

    def _newline(self):
        old = self.s[self.p]
        self.p += 1
        if self.p < self.n and self.s[self.p] in "\n\r" and self.s[self.p] != old:
            self.p += 1
        self.linenumber += 1

    def _sep(self, p):
        s, n, ch = self.s, self.n, self.s[p]
        q, cnt = p + 1, 0
        while q < n and s[q] == "=":
            q += 1
            cnt += 1
        if q < n and s[q] == ch:
            return cnt + 2, q + 1
        return (1 if cnt == 0 else 0), q

    def _long(self, p, sep, is_comment, startline):
        s, n = self.s, self.n
        self.p = p
        if self.p < n and s[self.p] in "\n\r":
            self._newline()
        out = []
        close = "]" + "=" * (sep - 2) + "]"
        while True:
            if self.p >= n:
                self.error("unfinished long %s (starting at line %d)" %
                           ("comment" if is_comment else "string", startline), "<eof>")
            c = s[self.p]
            if c == "]" and s.startswith(close, self.p):
                self.p += len(close)
                break
            if c in "\n\r":
                self._newline()
                out.append("\n")
            else:
                out.append(c)
                self.p += 1
        return "".join(out)

    def _llex(self):
        s, n = self.s, self.n
        while True:
            if self.p >= n:
                return ("EOS", None, "<eof>")
            c = s[self.p]
            if c in "\n\r":
                self._newline()
                continue
            if c in " \f\t\v":
                self.p += 1
                continue
            start = self.p
            if c == "-":
                if s.startswith("--", self.p):
                    self.p += 2
                    if self.p < n and s[self.p] == "[":
                        sep, q = self._sep(self.p)
                        if sep >= 2:
                            self._long(q, sep, True, self.linenumber)
                            continue
                    while self.p < n and s[self.p] not in "\n\r":
                        self.p += 1
                    continue
                self.p += 1
                return ("-", None, "-")
            if c == "[":
                sep, q = self._sep(self.p)
                if sep >= 2:
                    line0 = self.linenumber
                    txt = self._long(q, sep, False, line0)
                    return ("STRING", txt.encode("latin-1"), s[start:self.p])
                if sep == 0:
                    self.error("invalid long string delimiter", "'['")
                self.p += 1
                return ("[", None, "[")
            if c in "=<>~:/.":
                nx = s[self.p + 1] if self.p + 1 < n else ""
                if c == "=" and nx == "=":
                    self.p += 2
                    return ("==", None, "==")
                if c == "<" and nx == "=":
                    self.p += 2
                    return ("<=", None, "<=")
                if c == "<" and nx == "<":
                    self.p += 2
                    return ("<<", None, "<<")
                if c == ">" and nx == "=":
                    self.p += 2
                    return (">=", None, ">=")
                if c == ">" and nx == ">":
                    self.p += 2
                    return (">>", None, ">>")
                if c == "~" and nx == "=":
                    self.p += 2
                    return ("~=", None, "~=")
                if c == ":" and nx == ":":
                    self.p += 2
                    return ("::", None, "::")
                if c == "/" and nx == "/":
                    self.p += 2
                    return ("//", None, "//")
                if c == ".":
                    if nx == ".":
                        if self.p + 2 < n and s[self.p + 2] == ".":
                            self.p += 3
                            return ("...", None, "...")
                        self.p += 2
                        return ("..", None, "..")
                    if nx.isdigit():
                        return self._number()
                self.p += 1
                return (c, None, c)
            if c in "\"'":
                return self._string(c)
            if c.isdigit():
                return self._number()
            if c.isalpha() and c.isascii() or c == "_":
                m = _RE_NAME.match(s, self.p)
                w = m.group(0)
                self.p = m.end()
                if w in _RESERVED:
                    return (w, None, w)
                return ("NAME", w.encode("latin-1"), w)
            self.p += 1
            return (c, None, c)

    def _number(self):
        s, n = self.s, self.n
        start = self.p
        expo = "Ee"
        first = s[self.p]
        self.p += 1
        if first == "0" and self.p < n and s[self.p] in "xX":
            expo = "Pp"
            self.p += 1
        while self.p < n:
            ch = s[self.p]
            if ch in expo:
                self.p += 1
                if self.p < n and s[self.p] in "+-":
                    self.p += 1
            elif ch in "0123456789abcdefABCDEF." :
                self.p += 1
            else:
                break
        if self.p < n and (s[self.p].isalpha() or s[self.p] == "_"):
            self.p += 1
        raw = s[start:self.p]
        v = _str2num(raw)
        if v is None:
            self.error("malformed number", "'%s'" % raw)
        return ("INT" if isinstance(v, int) else "FLT", v, raw)

    def _string(self, delim):
        s, n = self.s, self.n
        start = self.p
        self.p += 1
        out = []
        while True:
            if self.p >= n:
                self.error("unfinished string", "<eof>")
            c = s[self.p]
            if c == delim:
                self.p += 1
                break
            if c in "\n\r":
                self.error("unfinished string", "'%s'" % s[start:self.p])
            if c != "\\":
                out.append(c)
                self.p += 1
                continue
            self.p += 1
            if self.p >= n:
                self.error("unfinished string", "<eof>")
            e = s[self.p]
            simple = {"a": "\a", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t",
                      "v": "\v", "\\": "\\", '"': '"', "'": "'"}
            if e in simple:
                out.append(simple[e])
                self.p += 1
            elif e in "\n\r":
                self._newline()
                out.append("\n")
            elif e == "x":
                h = s[self.p + 1:self.p + 3]
                if len(h) < 2 or not all(ch in "0123456789abcdefABCDEF" for ch in h):
                    self.error("hexadecimal digit expected", "'%s'" % s[start:self.p + 3])
                out.append(chr(int(h, 16)))
                self.p += 3
            elif e == "z":
                self.p += 1
                while self.p < n and s[self.p] in " \f\t\v\n\r":
                    if s[self.p] in "\n\r":
                        self._newline()
                    else:
                        self.p += 1
            elif e.isdigit():
                q = self.p
                while q < n and q < self.p + 3 and s[q].isdigit():
                    q += 1
                v = int(s[self.p:q])
                if v > 255:
                    self.error("decimal escape too large", "'%s'" % s[start:q])
                out.append(chr(v))
                self.p = q
            elif e == "u":
                m = re.match(r"u\{([0-9a-fA-F]+)\}", s[self.p:self.p + 20])
                if not m:
                    self.error("missing '{' in \\u{xxxx}", "'%s'" % s[start:self.p + 2])
                cp = int(m.group(1), 16)
                if cp > 0x7FFFFFFF:
                    self.error("UTF-8 value too large", "'%s'" % s[start:self.p + 2])
                out.append(_utf8_bytes(cp).decode("latin-1"))
                self.p += m.end()
            else:
                self.error("invalid escape sequence", "'%s'" % s[start:self.p + 1])
        return ("STRING", "".join(out).encode("latin-1"), s[start:self.p])


def _utf8_bytes(x):
    if x < 0x80:
        return bytes([x])
    buf = []
    mfb = 0x3F
    while True:
        buf.append(0x80 | (x & 0x3F))
        x >>= 6
        mfb >>= 1
        if x <= mfb:
            break
    buf.append(((~mfb << 1) & 0xFF) | x)
    return bytes(reversed(buf))


def _str2num(raw):
    t = raw.strip()
    if not t:
        return None
    neg = False
    body = t
    low = body.lower()
    if low.startswith("0x"):
        h = body[2:]
        if re.fullmatch(r"[0-9a-fA-F]+", h):
            return _wrap64(int(h, 16))
        m = re.fullmatch(r"([0-9a-fA-F]*)(?:\.([0-9a-fA-F]*))?(?:[pP]([+-]?\d+))?", h)
        if not m or (not m.group(1) and not m.group(2)):
            return None
        try:
            return float.fromhex("0x" + (m.group(1) or "0") + "." + (m.group(2) or "0") +
                                 "p" + (m.group(3) or "0"))
        except (ValueError, OverflowError):
            return None
    if re.fullmatch(r"\d+", body):
        v = int(body)
        if v <= 0x7FFFFFFFFFFFFFFF:
            return v
        return float(body)
    if re.fullmatch(r"(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?", body):
        try:
            return float(body)
        except (ValueError, OverflowError):
            return None
    return None


class _Exp:
    __slots__ = ("k", "info", "ival", "nval", "ind_t", "ind_idx", "ind_vt", "t", "f")

    def __init__(self, k=VVOID):
        self.k, self.info, self.ival, self.nval = k, 0, 0, 0.0
        self.ind_t = self.ind_idx = self.ind_vt = 0
        self.t = self.f = NO_JUMP

    def assign(self, o):
        for a in _Exp.__slots__:
            setattr(self, a, getattr(o, a))


class _Label:
    __slots__ = ("name", "pc", "line", "nactvar")

    def __init__(self, name, line, nactvar, pc):
        self.name, self.line, self.nactvar, self.pc = name, line, nactvar, pc


class _Block:
    __slots__ = ("previous", "firstlabel", "firstgoto", "nactvar", "upval", "isloop")


class _FS:
    def __init__(self):
        self.f = LFunc()
        self.prev = None
        self.ls = None
        self.bl = None
        self.lasttarget = 0
        self.jpc = NO_JUMP
        self.freereg = 0
        self.nactvar = 0
        self.firstlocal = 0
        self.kcache = {}

    @property
    def pc(self):
        return len(self.f.code)


class _Compiler:

    def __init__(self, src, chunk):
        self.lx = _Lex(src, chunk)
        self.chunk = chunk
        self.fs = None
        self.actvar = []
        self.gt = []
        self.label = []
        self.envn = b"_ENV"
        self.h = {}


    def syntax_error(self, msg):
        self.lx.error(msg, self.lx.tokstr(self.lx.t))

    def sem_error(self, msg):
        self.lx.error(msg)

    def error_expected(self, tok):
        self.syntax_error("'%s' expected" % tok if tok not in ("NAME",) else "<name> expected")

    def testnext(self, tok):
        if self.lx.t[0] == tok:
            self.lx.next()
            return True
        return False

    def check(self, tok):
        if self.lx.t[0] != tok:
            self.error_expected(tok)

    def checknext(self, tok):
        self.check(tok)
        self.lx.next()

    def check_condition(self, cond, msg):
        if not cond:
            self.syntax_error(msg)

    def check_match(self, what, who, where):
        if not self.testnext(what):
            if where == self.lx.linenumber:
                self.error_expected(what)
            else:
                self.syntax_error("'%s' expected (to close '%s' at line %d)" % (what, who, where))

    def str_checkname(self):
        self.check("NAME")
        v = self.lx.t[1]
        self.lx.next()
        return v

    def checklimit(self, v, limit, what):
        if v > limit:
            self.sem_error("too many %s (limit is %d)" % (what, limit))


    def code(self, i):
        fs = self.fs
        self.dischargejpc()
        fs.f.code.append(i)
        fs.f.lineinfo.append(self.lx.lastline)
        return len(fs.f.code) - 1

    def codeABC(self, op, a, b, c):
        return self.code(_iABC(op, a, b, c))

    def codeABx(self, op, a, bx):
        return self.code(_iABx(op, a, bx))

    def codeAsBx(self, op, a, sbx):
        return self.code(_iAsBx(op, a, sbx))

    def codeextraarg(self, a):
        return self.code(EXTRAARG | (a << 6))

    def codek(self, reg, k):
        if k <= MAXARG_Bx:
            return self.codeABx(LOADK, reg, k)
        p = self.codeABx(LOADKX, reg, 0)
        self.codeextraarg(k)
        return p

    def fixline(self, line):
        self.fs.f.lineinfo[-1] = line

    def nil(self, frm, n):
        fs = self.fs
        l = frm + n - 1
        if fs.pc > fs.lasttarget:
            prev = fs.f.code[-1]
            if _get_op(prev) == LOADNIL:
                pfrom = _get_A(prev)
                pl = pfrom + _get_B(prev)
                if (pfrom <= frm <= pl + 1) or (frm <= pfrom <= l + 1):
                    if pfrom < frm:
                        frm = pfrom
                    if pl > l:
                        l = pl
                    prev = _set_A(prev, frm)
                    prev = _set_B(prev, l - frm)
                    fs.f.code[-1] = prev
                    return
        self.codeABC(LOADNIL, frm, n - 1, 0)

    def jump(self):
        fs = self.fs
        jpc = fs.jpc
        fs.jpc = NO_JUMP
        j = self.codeAsBx(JMP, 0, NO_JUMP)
        return self.concat(j, jpc)

    def ret(self, first, nret):
        self.codeABC(RETURN, first, nret + 1, 0)

    def condjump(self, op, a, b, c):
        self.codeABC(op, a, b, c)
        return self.jump()

    def fixjump(self, pc, dest):
        fs = self.fs
        offset = dest - (pc + 1)
        if abs(offset) > MAXARG_sBx:
            self.syntax_error("control structure too long")
        fs.f.code[pc] = _set_sBx(fs.f.code[pc], offset)

    def getlabel(self):
        self.fs.lasttarget = self.fs.pc
        return self.fs.pc

    def getjump(self, pc):
        offset = _get_sBx(self.fs.f.code[pc])
        if offset == NO_JUMP:
            return NO_JUMP
        return pc + 1 + offset

    def getjumpcontrol(self, pc):
        code = self.fs.f.code
        if pc >= 1 and _test_tmode(_get_op(code[pc - 1])):
            return pc - 1
        return pc

    def patchtestreg(self, node, reg):
        code = self.fs.f.code
        ip = self.getjumpcontrol(node)
        i = code[ip]
        if _get_op(i) != TESTSET:
            return False
        if reg != NO_REG and reg != _get_B(i):
            code[ip] = _set_A(i, reg)
        else:
            code[ip] = _iABC(TEST, _get_B(i), 0, _get_C(i))
        return True

    def removevalues(self, lst):
        while lst != NO_JUMP:
            self.patchtestreg(lst, NO_REG)
            lst = self.getjump(lst)

    def patchlistaux(self, lst, vtarget, reg, dtarget):
        while lst != NO_JUMP:
            nxt = self.getjump(lst)
            if self.patchtestreg(lst, reg):
                self.fixjump(lst, vtarget)
            else:
                self.fixjump(lst, dtarget)
            lst = nxt

    def dischargejpc(self):
        fs = self.fs
        self.patchlistaux(fs.jpc, fs.pc, NO_REG, fs.pc)
        fs.jpc = NO_JUMP

    def patchlist(self, lst, target):
        if target == self.fs.pc:
            self.patchtohere(lst)
        else:
            self.patchlistaux(lst, target, NO_REG, target)

    def patchclose(self, lst, level):
        level += 1
        code = self.fs.f.code
        while lst != NO_JUMP:
            nxt = self.getjump(lst)
            code[lst] = _set_A(code[lst], level)
            lst = nxt

    def patchtohere(self, lst):
        self.getlabel()
        self.fs.jpc = self.concat(self.fs.jpc, lst)

    def concat(self, l1, l2):
        if l2 == NO_JUMP:
            return l1
        if l1 == NO_JUMP:
            return l2
        lst = l1
        while True:
            nxt = self.getjump(lst)
            if nxt == NO_JUMP:
                break
            lst = nxt
        self.fixjump(lst, l2)
        return l1

    def checkstack(self, n):
        fs = self.fs
        newstack = fs.freereg + n
        if newstack > fs.f.maxstack:
            if newstack >= MAXREGS:
                self.syntax_error("function or expression needs too many registers")
            fs.f.maxstack = newstack

    def reserveregs(self, n):
        self.checkstack(n)
        self.fs.freereg += n

    def freereg(self, reg):
        fs = self.fs
        if not (reg & BITRK) and reg >= fs.nactvar:
            fs.freereg -= 1

    def freeexp(self, e):
        if e.k == VNONRELOC:
            self.freereg(e.info)

    def freeexps(self, e1, e2):
        r1 = e1.info if e1.k == VNONRELOC else -1
        r2 = e2.info if e2.k == VNONRELOC else -1
        if r1 > r2:
            self.freereg(r1)
            self.freereg(r2)
        else:
            self.freereg(r2)
            self.freereg(r1)

    @staticmethod
    def _kkey(tv):
        ty, v = tv
        if ty in (4, 0x14):
            return ("s", v)
        if ty == 0x13:
            return ("i", v)
        if ty == 3:
            return ("f", struct.pack("<d", v))
        if ty == 1:
            return ("b", bool(v))
        return ("n",)

    def addk(self, key, tv):


        fs = self.fs
        idx = self.h.get(key)
        if idx is not None and idx < len(fs.f.k) and self._kkey(fs.f.k[idx]) == key:
            return idx
        fs.f.k.append(tv)
        idx = len(fs.f.k) - 1
        self.h[key] = idx
        return idx

    def stringK(self, s):
        return self.addk(("s", s), (4 if len(s) <= 40 else 0x14, s))

    def intK(self, n):
        return self.addk(("i", n), (0x13, n))

    def numberK(self, r):
        return self.addk(("f", struct.pack("<d", r)), (3, r))

    def boolK(self, b):
        return self.addk(("b", bool(b)), (1, bool(b)))

    def nilK(self):
        return self.addk(("n",), (0, None))

    @staticmethod
    def hasjumps(e):
        return e.t != e.f

    def setreturns(self, e, nresults):
        code = self.fs.f.code
        if e.k == VCALL:
            code[e.info] = _set_C(code[e.info], nresults + 1)
        elif e.k == VVARARG:
            i = _set_B(code[e.info], nresults + 1)
            i = _set_A(i, self.fs.freereg)
            code[e.info] = i
            self.reserveregs(1)

    def setmultret(self, e):
        self.setreturns(e, LUA_MULTRET)

    def setoneret(self, e):
        code = self.fs.f.code
        if e.k == VCALL:
            e.k = VNONRELOC
            e.info = _get_A(code[e.info])
        elif e.k == VVARARG:
            code[e.info] = _set_B(code[e.info], 2)
            e.k = VRELOCABLE

    def dischargevars(self, e):
        k = e.k
        if k == VLOCAL:
            e.k = VNONRELOC
        elif k == VUPVAL:
            e.info = self.codeABC(GETUPVAL, 0, e.info, 0)
            e.k = VRELOCABLE
        elif k == VINDEXED:
            self.freereg(e.ind_idx)
            if e.ind_vt == VLOCAL:
                self.freereg(e.ind_t)
                op = GETTABLE
            else:
                op = GETTABUP
            e.info = self.codeABC(op, 0, e.ind_t, e.ind_idx)
            e.k = VRELOCABLE
        elif k in (VVARARG, VCALL):
            self.setoneret(e)

    def discharge2reg(self, e, reg):
        self.dischargevars(e)
        k = e.k
        if k == VNIL:
            self.nil(reg, 1)
        elif k in (VFALSE, VTRUE):
            self.codeABC(LOADBOOL, reg, 1 if k == VTRUE else 0, 0)
        elif k == VK:
            self.codek(reg, e.info)
        elif k == VKFLT:
            self.codek(reg, self.numberK(e.nval))
        elif k == VKINT:
            self.codek(reg, self.intK(e.ival))
        elif k == VRELOCABLE:
            code = self.fs.f.code
            code[e.info] = _set_A(code[e.info], reg)
        elif k == VNONRELOC:
            if reg != e.info:
                self.codeABC(MOVE, reg, e.info, 0)
        else:
            return
        e.info = reg
        e.k = VNONRELOC

    def discharge2anyreg(self, e):
        if e.k != VNONRELOC:
            self.reserveregs(1)
            self.discharge2reg(e, self.fs.freereg - 1)

    def code_loadbool(self, a, b, jmp):
        self.getlabel()
        return self.codeABC(LOADBOOL, a, b, jmp)

    def need_value(self, lst):
        code = self.fs.f.code
        while lst != NO_JUMP:
            if _get_op(code[self.getjumpcontrol(lst)]) != TESTSET:
                return True
            lst = self.getjump(lst)
        return False

    def exp2reg(self, e, reg):
        self.discharge2reg(e, reg)
        if e.k == VJMP:
            e.t = self.concat(e.t, e.info)
        if self.hasjumps(e):
            p_f = p_t = NO_JUMP
            if self.need_value(e.t) or self.need_value(e.f):
                fj = NO_JUMP if e.k == VJMP else self.jump()
                p_f = self.code_loadbool(reg, 0, 1)
                p_t = self.code_loadbool(reg, 1, 0)
                self.patchtohere(fj)
            final = self.getlabel()
            self.patchlistaux(e.f, final, reg, p_f)
            self.patchlistaux(e.t, final, reg, p_t)
        e.f = e.t = NO_JUMP
        e.info = reg
        e.k = VNONRELOC

    def exp2nextreg(self, e):
        self.dischargevars(e)
        self.freeexp(e)
        self.reserveregs(1)
        self.exp2reg(e, self.fs.freereg - 1)

    def exp2anyreg(self, e):
        self.dischargevars(e)
        if e.k == VNONRELOC:
            if not self.hasjumps(e):
                return e.info
            if e.info >= self.fs.nactvar:
                self.exp2reg(e, e.info)
                return e.info
        self.exp2nextreg(e)
        return e.info

    def exp2anyregup(self, e):
        if e.k != VUPVAL or self.hasjumps(e):
            self.exp2anyreg(e)

    def exp2val(self, e):
        if self.hasjumps(e):
            self.exp2anyreg(e)
        else:
            self.dischargevars(e)

    def exp2RK(self, e):
        self.exp2val(e)
        k = e.k
        if k == VTRUE:
            e.info = self.boolK(True)
        elif k == VFALSE:
            e.info = self.boolK(False)
        elif k == VNIL:
            e.info = self.nilK()
        elif k == VKINT:
            e.info = self.intK(e.ival)
        elif k == VKFLT:
            e.info = self.numberK(e.nval)
        elif k == VK:
            pass
        else:
            return self.exp2anyreg(e)
        e.k = VK
        if e.info <= MAXINDEXRK:
            return e.info | BITRK
        return self.exp2anyreg(e)

    def storevar(self, var, ex):
        k = var.k
        if k == VLOCAL:
            self.freeexp(ex)
            self.exp2reg(ex, var.info)
            return
        if k == VUPVAL:
            e = self.exp2anyreg(ex)
            self.codeABC(SETUPVAL, e, var.info, 0)
        elif k == VINDEXED:
            op = SETTABLE if var.ind_vt == VLOCAL else SETTABUP
            e = self.exp2RK(ex)
            self.codeABC(op, var.ind_t, var.ind_idx, e)
        self.freeexp(ex)

    def selfop(self, e, key):
        self.exp2anyreg(e)
        ereg = e.info
        self.freeexp(e)
        e.info = self.fs.freereg
        e.k = VNONRELOC
        self.reserveregs(2)
        self.codeABC(SELF, e.info, ereg, self.exp2RK(key))
        self.freeexp(key)

    def negatecondition(self, e):
        code = self.fs.f.code
        ip = self.getjumpcontrol(e.info)
        code[ip] = _set_A(code[ip], 0 if _get_A(code[ip]) else 1)

    def jumponcond(self, e, cond):
        fs = self.fs
        if e.k == VRELOCABLE:
            ie = fs.f.code[e.info]
            if _get_op(ie) == NOT:
                fs.f.code.pop()
                fs.f.lineinfo.pop()
                return self.condjump(TEST, _get_B(ie), 0, 0 if cond else 1)
        self.discharge2anyreg(e)
        self.freeexp(e)
        return self.condjump(TESTSET, NO_REG, e.info, 1 if cond else 0)

    def goiftrue(self, e):
        self.dischargevars(e)
        k = e.k
        if k == VJMP:
            self.negatecondition(e)
            pc = e.info
        elif k in (VK, VKFLT, VKINT, VTRUE):
            pc = NO_JUMP
        else:
            pc = self.jumponcond(e, 0)
        e.f = self.concat(e.f, pc)
        self.patchtohere(e.t)
        e.t = NO_JUMP

    def goiffalse(self, e):
        self.dischargevars(e)
        k = e.k
        if k == VJMP:
            pc = e.info
        elif k in (VNIL, VFALSE):
            pc = NO_JUMP
        else:
            pc = self.jumponcond(e, 1)
        e.t = self.concat(e.t, pc)
        self.patchtohere(e.f)
        e.f = NO_JUMP

    def codenot(self, e):
        self.dischargevars(e)
        k = e.k
        if k in (VNIL, VFALSE):
            e.k = VTRUE
        elif k in (VK, VKFLT, VKINT, VTRUE):
            e.k = VFALSE
        elif k == VJMP:
            self.negatecondition(e)
        elif k in (VRELOCABLE, VNONRELOC):
            self.discharge2anyreg(e)
            self.freeexp(e)
            e.info = self.codeABC(NOT, 0, e.info, 0)
            e.k = VRELOCABLE
        e.f, e.t = e.t, e.f
        self.removevalues(e.f)
        self.removevalues(e.t)

    def indexed(self, t, k):
        t.ind_t = t.info
        t.ind_idx = self.exp2RK(k)
        t.ind_vt = VUPVAL if t.k == VUPVAL else VLOCAL
        t.k = VINDEXED

    @staticmethod
    def tonumeral(e):
        if e.t != e.f:
            return None
        if e.k == VKINT:
            return e.ival
        if e.k == VKFLT:
            return e.nval
        return None

    def constfolding(self, op, e1, e2):
        v1 = self.tonumeral(e1)
        v2 = self.tonumeral(e2)
        if v1 is None or v2 is None:
            return False
        if op in (7, 8, 9, 10, 11, 13):
            if _to_int_exact(v1) is None or _to_int_exact(v2) is None:
                return False
        elif op in (5, 6, 3):
            if v2 == 0:
                return False
        res = _arith(op, v1, v2)
        if res is None:
            return False
        if isinstance(res, int):
            e1.k = VKINT
            e1.ival = res
        else:
            if res != res or res == 0:
                return False
            e1.k = VKFLT
            e1.nval = res
        return True

    def codeunexpval(self, op, e, line):
        r = self.exp2anyreg(e)
        self.freeexp(e)
        e.info = self.codeABC(op, 0, r, 0)
        e.k = VRELOCABLE
        self.fixline(line)

    def codebinexpval(self, op, e1, e2, line):
        rk2 = self.exp2RK(e2)
        rk1 = self.exp2RK(e1)
        self.freeexps(e1, e2)
        e1.info = self.codeABC(op, 0, rk1, rk2)
        e1.k = VRELOCABLE
        self.fixline(line)

    def codecomp(self, opr, e1, e2):
        rk1 = (e1.info | BITRK) if e1.k == VK else e1.info
        rk2 = self.exp2RK(e2)
        self.freeexps(e1, e2)
        if opr == OPR_NE:
            e1.info = self.condjump(EQ, 0, rk1, rk2)
        elif opr in (OPR_GT, OPR_GE):
            op = (opr - OPR_NE) + EQ
            e1.info = self.condjump(op, 1, rk2, rk1)
        else:
            op = (opr - OPR_EQ) + EQ
            e1.info = self.condjump(op, 1, rk1, rk2)
        e1.k = VJMP

    def prefix(self, op, e, line):
        if op in (OPR_MINUS, OPR_BNOT):
            ef = _Exp(VKINT)
            ef.ival = 0
            if self.constfolding(op + 12, e, ef):
                return
            self.codeunexpval(op + UNM, e, line)
        elif op == OPR_LEN:
            self.codeunexpval(op + UNM, e, line)
        elif op == OPR_NOT:
            self.codenot(e)

    def infix(self, op, v):
        if op == OPR_AND:
            self.goiftrue(v)
        elif op == OPR_OR:
            self.goiffalse(v)
        elif op == OPR_CONCAT:
            self.exp2nextreg(v)
        elif op <= OPR_SHR:
            if self.tonumeral(v) is None:
                self.exp2RK(v)
        else:
            self.exp2RK(v)

    def posfix(self, op, e1, e2, line):
        if op == OPR_AND:
            self.dischargevars(e2)
            e2.f = self.concat(e2.f, e1.f)
            e1.assign(e2)
        elif op == OPR_OR:
            self.dischargevars(e2)
            e2.t = self.concat(e2.t, e1.t)
            e1.assign(e2)
        elif op == OPR_CONCAT:
            self.exp2val(e2)
            code = self.fs.f.code
            if e2.k == VRELOCABLE and _get_op(code[e2.info]) == CONCAT:
                self.freeexp(e1)
                code[e2.info] = _set_B(code[e2.info], e1.info)
                e1.k = VRELOCABLE
                e1.info = e2.info
            else:
                self.exp2nextreg(e2)
                self.codebinexpval(CONCAT, e1, e2, line)
        elif op <= OPR_SHR:
            if not self.constfolding(op, e1, e2):
                self.codebinexpval(op + ADD, e1, e2, line)
        else:
            self.codecomp(op, e1, e2)

    def setlist(self, base, nelems, tostore):
        c = (nelems - 1) // LFIELDS_PER_FLUSH + 1
        b = 0 if tostore == LUA_MULTRET else tostore
        if c <= MAXARG_C:
            self.codeABC(SETLIST, base, b, c)
        elif c <= MAXARG_Ax:
            self.codeABC(SETLIST, base, b, 0)
            self.codeextraarg(c)
        else:
            self.syntax_error("constructor too long")
        self.fs.freereg = base + 1


    def init_exp(self, e, k, i):
        e.f = e.t = NO_JUMP
        e.k = k
        e.info = i

    def codestring(self, e, s):
        self.init_exp(e, VK, self.stringK(s))

    def checkname(self, e):
        self.codestring(e, self.str_checkname())

    def registerlocalvar(self, name):
        f = self.fs.f
        f.locvars.append([name, 0, 0])
        return len(f.locvars) - 1

    def new_localvar(self, name):
        fs = self.fs
        reg = self.registerlocalvar(name)
        self.checklimit(len(self.actvar) + 1 - fs.firstlocal, MAXVARS, "local variables")
        self.actvar.append(reg)

    def getlocvar(self, fs, i):
        return fs.f.locvars[self.actvar[fs.firstlocal + i]]

    def adjustlocalvars(self, nvars):
        fs = self.fs
        fs.nactvar += nvars
        for i in range(nvars, 0, -1):
            self.getlocvar(fs, fs.nactvar - i)[1] = fs.pc

    def removevars(self, tolevel):
        fs = self.fs
        cnt = fs.nactvar - tolevel
        base = fs.firstlocal + tolevel
        idxs = self.actvar[base:base + cnt]
        if cnt:
            del self.actvar[len(self.actvar) - cnt:]
        while fs.nactvar > tolevel:
            fs.nactvar -= 1
            fs.f.locvars[idxs[fs.nactvar - tolevel]][2] = fs.pc

    def searchupvalue(self, fs, name):
        for i, n in enumerate(fs.f.upnames):
            if n == name:
                return i
        return -1

    def newupvalue(self, fs, name, v):
        self.checklimit(len(fs.f.up) + 1, MAXUPVAL, "upvalues")
        fs.f.up.append((1 if v.k == VLOCAL else 0, v.info))
        fs.f.upnames.append(name)
        return len(fs.f.up) - 1

    def searchvar(self, fs, n):
        for i in range(fs.nactvar - 1, -1, -1):
            if n == self.getlocvar(fs, i)[0]:
                return i
        return -1

    def markupval(self, fs, level):
        bl = fs.bl
        while bl.nactvar > level:
            bl = bl.previous
        bl.upval = 1

    def singlevaraux(self, fs, n, var, base):
        if fs is None:
            return VVOID
        v = self.searchvar(fs, n)
        if v >= 0:
            self.init_exp(var, VLOCAL, v)
            if not base:
                self.markupval(fs, v)
            return VLOCAL
        idx = self.searchupvalue(fs, n)
        if idx < 0:
            if self.singlevaraux(fs.prev, n, var, 0) == VVOID:
                return VVOID
            idx = self.newupvalue(fs, n, var)
        self.init_exp(var, VUPVAL, idx)
        return VUPVAL

    def singlevar(self, var):
        name = self.str_checkname()
        fs = self.fs
        if self.singlevaraux(fs, name, var, 1) == VVOID:
            key = _Exp()
            self.singlevaraux(fs, self.envn, var, 1)
            self.codestring(key, name)
            self.indexed(var, key)

    def adjust_assign(self, nvars, nexps, e):
        fs = self.fs
        extra = nvars - nexps
        if e.k in (VCALL, VVARARG):
            extra += 1
            if extra < 0:
                extra = 0
            self.setreturns(e, extra)
            if extra > 1:
                self.reserveregs(extra - 1)
        else:
            if e.k != VVOID:
                self.exp2nextreg(e)
            if extra > 0:
                reg = fs.freereg
                self.reserveregs(extra)
                self.nil(reg, extra)
        if nexps > nvars:
            fs.freereg -= nexps - nvars


    def closegoto(self, g, label):
        fs = self.fs
        gt = self.gt[g]
        if gt.nactvar < label.nactvar:
            vname = self.getlocvar(fs, gt.nactvar)[0]
            self.sem_error("<goto %s> at line %d jumps into the scope of local '%s'" %
                           (gt.name.decode("latin-1"), gt.line, vname.decode("latin-1")))
        self.patchlist(gt.pc, label.pc)
        del self.gt[g]

    def findlabel(self, g):
        fs = self.fs
        bl = fs.bl
        gt = self.gt[g]
        for i in range(bl.firstlabel, len(self.label)):
            lb = self.label[i]
            if lb.name == gt.name:
                if gt.nactvar > lb.nactvar and (bl.upval or len(self.label) > bl.firstlabel):
                    self.patchclose(gt.pc, lb.nactvar)
                self.closegoto(g, lb)
                return True
        return False

    def newlabelentry(self, lst, name, line, pc):
        lst.append(_Label(name, line, self.fs.nactvar, pc))
        return len(lst) - 1

    def findgotos(self, lb):
        i = self.fs.bl.firstgoto
        while i < len(self.gt):
            if self.gt[i].name == lb.name:
                self.closegoto(i, lb)
            else:
                i += 1

    def movegotosout(self, bl):
        fs = self.fs
        i = bl.firstgoto
        while i < len(self.gt):
            gt = self.gt[i]
            if gt.nactvar > bl.nactvar:
                if bl.upval:
                    self.patchclose(gt.pc, bl.nactvar)
                gt.nactvar = bl.nactvar
            if not self.findlabel(i):
                i += 1

    def enterblock(self, bl, isloop):
        fs = self.fs
        bl.isloop = isloop
        bl.nactvar = fs.nactvar
        bl.firstlabel = len(self.label)
        bl.firstgoto = len(self.gt)
        bl.upval = 0
        bl.previous = fs.bl
        fs.bl = bl

    def breaklabel(self):
        l = self.newlabelentry(self.label, b"break", 0, self.fs.pc)
        self.findgotos(self.label[l])

    def undefgoto(self, gt):
        if gt.name == b"break":
            self.sem_error("<break> at line %d not inside a loop" % gt.line)
        self.sem_error("no visible label '%s' for <goto> at line %d" %
                       (gt.name.decode("latin-1"), gt.line))

    def leaveblock(self):
        fs = self.fs
        bl = fs.bl
        if bl.previous and bl.upval:
            j = self.jump()
            self.patchclose(j, bl.nactvar)
            self.patchtohere(j)
        if bl.isloop:
            self.breaklabel()
        fs.bl = bl.previous
        self.removevars(bl.nactvar)
        fs.freereg = fs.nactvar
        del self.label[bl.firstlabel:]
        if bl.previous:
            self.movegotosout(bl)
        elif bl.firstgoto < len(self.gt):
            self.undefgoto(self.gt[bl.firstgoto])

    def open_func(self, fs, bl):
        f = fs.f
        fs.prev = self.fs
        fs.ls = self
        self.fs = fs
        fs.firstlocal = len(self.actvar)
        fs.bl = None
        f.source = None
        f.maxstack = 2
        f.code, f.k, f.up, f.protos = [], [], [], []
        f.lineinfo, f.abslineinfo, f.locvars, f.upnames = [], [], [], []
        f.nparams, f.vararg, f.line, f.lastline = 0, 0, 0, 0
        self.enterblock(bl, 0)

    def close_func(self):
        fs = self.fs
        self.ret(0, 0)
        self.leaveblock()
        self.fs = fs.prev


    def block_follow(self, withuntil):
        t = self.lx.t[0]
        if t in ("else", "elseif", "end", "EOS"):
            return True
        if t == "until":
            return withuntil
        return False

    def statlist(self):
        while not self.block_follow(True):
            if self.lx.t[0] == "return":
                self.statement()
                return
            self.statement()

    def fieldsel(self, v):
        self.exp2anyregup(v)
        self.lx.next()
        key = _Exp()
        self.checkname(key)
        self.indexed(v, key)

    def yindex(self, v):
        self.lx.next()
        self.expr(v)
        self.exp2val(v)
        self.checknext("]")

    def recfield(self, cc):
        fs = self.fs
        reg = fs.freereg
        key, val = _Exp(), _Exp()
        if self.lx.t[0] == "NAME":
            self.checkname(key)
        else:
            self.yindex(key)
        cc["nh"] += 1
        self.checknext("=")
        rkkey = self.exp2RK(key)
        self.expr(val)
        self.codeABC(SETTABLE, cc["t"].info, rkkey, self.exp2RK(val))
        fs.freereg = reg

    def closelistfield(self, cc):
        if cc["v"].k == VVOID:
            return
        self.exp2nextreg(cc["v"])
        cc["v"].k = VVOID
        if cc["tostore"] == LFIELDS_PER_FLUSH:
            self.setlist(cc["t"].info, cc["na"], cc["tostore"])
            cc["tostore"] = 0

    def lastlistfield(self, cc):
        if cc["tostore"] == 0:
            return
        if cc["v"].k in (VCALL, VVARARG):
            self.setmultret(cc["v"])
            self.setlist(cc["t"].info, cc["na"], LUA_MULTRET)
            cc["na"] -= 1
        else:
            if cc["v"].k != VVOID:
                self.exp2nextreg(cc["v"])
            self.setlist(cc["t"].info, cc["na"], cc["tostore"])

    def listfield(self, cc):
        self.expr(cc["v"])
        cc["na"] += 1
        cc["tostore"] += 1

    def field(self, cc):
        t = self.lx.t[0]
        if t == "NAME":
            if self.lx.lookahead() != "=":
                self.listfield(cc)
            else:
                self.recfield(cc)
        elif t == "[":
            self.recfield(cc)
        else:
            self.listfield(cc)

    def constructor(self, t):
        fs = self.fs
        line = self.lx.linenumber
        pc = self.codeABC(NEWTABLE, 0, 0, 0)
        cc = {"na": 0, "nh": 0, "tostore": 0, "t": t, "v": _Exp()}
        self.init_exp(t, VRELOCABLE, pc)
        self.init_exp(cc["v"], VVOID, 0)
        self.exp2nextreg(t)
        self.checknext("{")
        while True:
            if self.lx.t[0] == "}":
                break
            self.closelistfield(cc)
            self.field(cc)
            if not (self.testnext(",") or self.testnext(";")):
                break
        self.check_match("}", "{", line)
        self.lastlistfield(cc)
        code = fs.f.code
        code[pc] = _set_B(code[pc], _int2fb(cc["na"]))
        code[pc] = _set_C(code[pc], _int2fb(cc["nh"]))

    def parlist(self):
        fs = self.fs
        f = fs.f
        nparams = 0
        f.vararg = 0
        if self.lx.t[0] != ")":
            while True:
                t = self.lx.t[0]
                if t == "NAME":
                    self.new_localvar(self.str_checkname())
                    nparams += 1
                elif t == "...":
                    self.lx.next()
                    f.vararg = 1
                else:
                    self.syntax_error("<name> or '...' expected")
                if f.vararg or not self.testnext(","):
                    break
        self.adjustlocalvars(nparams)
        f.nparams = fs.nactvar
        self.reserveregs(fs.nactvar)

    def body(self, e, ismethod, line):
        new_fs = _FS()
        bl = _Block()
        parent = self.fs
        parent.f.protos.append(new_fs.f)
        new_fs.f.line = line
        self.open_func(new_fs, bl)
        new_fs.f.line = line
        self.checknext("(")
        if ismethod:
            self.new_localvar(b"self")
            self.adjustlocalvars(1)
        self.parlist()
        self.checknext(")")
        self.statlist()
        new_fs.f.lastline = self.lx.linenumber
        self.check_match("end", "function", line)

        self.fs = parent
        self.init_exp(e, VRELOCABLE, self.codeABx(CLOSURE, 0, len(parent.f.protos) - 1))
        self.exp2nextreg(e)
        self.fs = new_fs
        self.close_func()

    def explist(self, v):
        n = 1
        self.expr(v)
        while self.testnext(","):
            self.exp2nextreg(v)
            self.expr(v)
            n += 1
        return n

    def funcargs(self, f, line):
        fs = self.fs
        args = _Exp()
        t = self.lx.t[0]
        if t == "(":
            self.lx.next()
            if self.lx.t[0] == ")":
                args.k = VVOID
            else:
                self.explist(args)
                self.setmultret(args)
            self.check_match(")", "(", line)
        elif t == "{":
            self.constructor(args)
        elif t == "STRING":
            self.codestring(args, self.lx.t[1])
            self.lx.next()
        else:
            self.syntax_error("function arguments expected")
        base = f.info
        if args.k in (VCALL, VVARARG):
            nparams = LUA_MULTRET
        else:
            if args.k != VVOID:
                self.exp2nextreg(args)
            nparams = fs.freereg - (base + 1)
        self.init_exp(f, VCALL, self.codeABC(CALL, base, nparams + 1, 2))
        self.fixline(line)
        fs.freereg = base + 1

    def primaryexp(self, v):
        t = self.lx.t[0]
        if t == "NAME":
            self.singlevar(v)
        elif t == "(":
            line = self.lx.linenumber
            self.lx.next()
            self.expr(v)
            self.check_match(")", "(", line)
            self.dischargevars(v)
        else:
            self.syntax_error("unexpected symbol")

    def suffixedexp(self, v):
        fs = self.fs
        line = self.lx.linenumber
        self.primaryexp(v)
        while True:
            t = self.lx.t[0]
            if t == ".":
                self.fieldsel(v)
            elif t == "[":
                key = _Exp()
                self.exp2anyregup(v)
                self.yindex(key)
                self.indexed(v, key)
            elif t == ":":
                key = _Exp()
                self.lx.next()
                self.checkname(key)
                self.selfop(v, key)
                self.funcargs(v, line)
            elif t in ("(", "STRING", "{"):
                self.exp2nextreg(v)
                self.funcargs(v, line)
            else:
                return

    def simpleexp(self, v):
        t = self.lx.t
        k = t[0]
        if k == "FLT":
            self.init_exp(v, VKFLT, 0)
            v.nval = t[1]
        elif k == "INT":
            self.init_exp(v, VKINT, 0)
            v.ival = t[1]
        elif k == "STRING":
            self.codestring(v, t[1])
        elif k == "nil":
            self.init_exp(v, VNIL, 0)
        elif k == "true":
            self.init_exp(v, VTRUE, 0)
        elif k == "false":
            self.init_exp(v, VFALSE, 0)
        elif k == "...":
            self.check_condition(self.fs.f.vararg, "cannot use '...' outside a vararg function")
            self.init_exp(v, VVARARG, self.codeABC(VARARG, 0, 1, 0))
        elif k == "{":
            self.constructor(v)
            return
        elif k == "function":
            self.lx.next()
            self.body(v, False, self.lx.linenumber)
            return
        else:
            self.suffixedexp(v)
            return
        self.lx.next()

    def subexpr(self, v, limit):
        uop = _UNOPR.get(self.lx.t[0], OPR_NOUNOPR)
        if uop != OPR_NOUNOPR:
            line = self.lx.linenumber
            self.lx.next()
            self.subexpr(v, _UNARY_PRIORITY)
            self.prefix(uop, v, line)
        else:
            self.simpleexp(v)
        op = _BINOPR.get(self.lx.t[0], OPR_NOBINOPR)
        while op != OPR_NOBINOPR and _PRIORITY[op][0] > limit:
            v2 = _Exp()
            line = self.lx.linenumber
            self.lx.next()
            self.infix(op, v)
            nextop = self.subexpr(v2, _PRIORITY[op][1])
            self.posfix(op, v, v2, line)
            op = nextop
        return op

    def expr(self, v):
        self.subexpr(v, 0)

    def block(self):
        bl = _Block()
        self.enterblock(bl, 0)
        self.statlist()
        self.leaveblock()

    def check_conflict(self, lh, v):
        fs = self.fs
        extra = fs.freereg
        conflict = False
        for h in lh:
            if h.k == VINDEXED:
                if h.ind_vt == v.k and h.ind_t == v.info:
                    conflict = True
                    h.ind_vt = VLOCAL
                    h.ind_t = extra
                if v.k == VLOCAL and h.ind_idx == v.info:
                    conflict = True
                    h.ind_idx = extra
        if conflict:
            op = MOVE if v.k == VLOCAL else GETUPVAL
            self.codeABC(op, extra, v.info, 0)
            self.reserveregs(1)

    def assignment(self, lh, nvars):
        e = _Exp()
        cur = lh[-1]
        self.check_condition(VLOCAL <= cur.k <= VINDEXED, "syntax error")
        if self.testnext(","):
            nv = _Exp()
            self.suffixedexp(nv)
            if nv.k != VINDEXED:
                self.check_conflict(lh, nv)
            self.assignment(lh + [nv], nvars + 1)
            return_after = True
        else:
            self.checknext("=")
            nexps = self.explist(e)
            if nexps != nvars:
                self.adjust_assign(nvars, nexps, e)
            else:
                self.setoneret(e)
                self.storevar(cur, e)
                return
        self.init_exp(e, VNONRELOC, self.fs.freereg - 1)
        self.storevar(cur, e)

    def cond(self):
        v = _Exp()
        self.expr(v)
        if v.k == VNIL:
            v.k = VFALSE
        self.goiftrue(v)
        return v.f

    def gotostat(self, pc):
        line = self.lx.linenumber
        if self.testnext("goto"):
            label = self.str_checkname()
        else:
            self.lx.next()
            label = b"break"
        g = self.newlabelentry(self.gt, label, line, pc)
        self.findlabel(g)

    def checkrepeated(self, name):
        for i in range(self.fs.bl.firstlabel, len(self.label)):
            if self.label[i].name == name:
                self.sem_error("label '%s' already defined on line %d" %
                               (name.decode("latin-1"), self.label[i].line))

    def skipnoopstat(self):
        while self.lx.t[0] in (";", "::"):
            self.statement()

    def labelstat(self, name, line):
        fs = self.fs
        self.checkrepeated(name)
        self.checknext("::")
        l = self.newlabelentry(self.label, name, line, self.getlabel())
        self.skipnoopstat()
        if self.block_follow(False):
            self.label[l].nactvar = fs.bl.nactvar
        self.findgotos(self.label[l])

    def whilestat(self, line):
        fs = self.fs
        self.lx.next()
        whileinit = self.getlabel()
        condexit = self.cond()
        bl = _Block()
        self.enterblock(bl, 1)
        self.checknext("do")
        self.block()
        self.patchlist(self.jump(), whileinit)
        self.check_match("end", "while", line)
        self.leaveblock()
        self.patchtohere(condexit)

    def repeatstat(self, line):
        fs = self.fs
        repeat_init = self.getlabel()
        bl1, bl2 = _Block(), _Block()
        self.enterblock(bl1, 1)
        self.enterblock(bl2, 0)
        self.lx.next()
        self.statlist()
        self.check_match("until", "repeat", line)
        condexit = self.cond()
        if bl2.upval:
            self.patchclose(condexit, bl2.nactvar)
        self.leaveblock()
        self.patchlist(condexit, repeat_init)
        self.leaveblock()

    def exp1(self):
        e = _Exp()
        self.expr(e)
        self.exp2nextreg(e)

    def forbody(self, base, line, nvars, isnum):
        fs = self.fs
        bl = _Block()
        self.adjustlocalvars(3)
        self.checknext("do")
        prep = self.codeAsBx(FORPREP, base, NO_JUMP) if isnum else self.jump()
        self.enterblock(bl, 0)
        self.adjustlocalvars(nvars)
        self.reserveregs(nvars)
        self.block()
        self.leaveblock()
        self.patchtohere(prep)
        if isnum:
            endfor = self.codeAsBx(FORLOOP, base, NO_JUMP)
        else:
            self.codeABC(TFORCALL, base, 0, nvars)
            self.fixline(line)
            endfor = self.codeAsBx(TFORLOOP, base + 2, NO_JUMP)
        self.patchlist(endfor, prep + 1)
        self.fixline(line)

    def fornum(self, varname, line):
        fs = self.fs
        base = fs.freereg
        self.new_localvar(b"(for index)")
        self.new_localvar(b"(for limit)")
        self.new_localvar(b"(for step)")
        self.new_localvar(varname)
        self.checknext("=")
        self.exp1()
        self.checknext(",")
        self.exp1()
        if self.testnext(","):
            self.exp1()
        else:
            self.codek(fs.freereg, self.intK(1))
            self.reserveregs(1)
        self.forbody(base, line, 1, True)

    def forlist(self, indexname):
        fs = self.fs
        e = _Exp()
        nvars = 4
        base = fs.freereg
        self.new_localvar(b"(for generator)")
        self.new_localvar(b"(for state)")
        self.new_localvar(b"(for control)")
        self.new_localvar(indexname)
        while self.testnext(","):
            self.new_localvar(self.str_checkname())
            nvars += 1
        self.checknext("in")
        line = self.lx.linenumber
        self.adjust_assign(3, self.explist(e), e)
        self.checkstack(3)
        self.forbody(base, line, nvars - 3, False)

    def forstat(self, line):
        fs = self.fs
        bl = _Block()
        self.enterblock(bl, 1)
        self.lx.next()
        varname = self.str_checkname()
        t = self.lx.t[0]
        if t == "=":
            self.fornum(varname, line)
        elif t in (",", "in"):
            self.forlist(varname)
        else:
            self.syntax_error("'=' or 'in' expected")
        self.check_match("end", "for", line)
        self.leaveblock()

    def test_then_block(self, escapelist):
        fs = self.fs
        bl = _Block()
        v = _Exp()
        self.lx.next()
        self.expr(v)
        self.checknext("then")
        if self.lx.t[0] in ("goto", "break"):
            self.goiffalse(v)
            self.enterblock(bl, 0)
            self.gotostat(v.t)
            while self.testnext(";"):
                pass
            if self.block_follow(False):
                self.leaveblock()
                return escapelist
            jf = self.jump()
        else:
            self.goiftrue(v)
            self.enterblock(bl, 0)
            jf = v.f
        self.statlist()
        self.leaveblock()
        if self.lx.t[0] in ("else", "elseif"):
            escapelist = self.concat(escapelist, self.jump())
        self.patchtohere(jf)
        return escapelist

    def ifstat(self, line):
        escapelist = NO_JUMP
        escapelist = self.test_then_block(escapelist)
        while self.lx.t[0] == "elseif":
            escapelist = self.test_then_block(escapelist)
        if self.testnext("else"):
            self.block()
        self.check_match("end", "if", line)
        self.patchtohere(escapelist)

    def localfunc(self):
        b = _Exp()
        fs = self.fs
        self.new_localvar(self.str_checkname())
        self.adjustlocalvars(1)
        self.body(b, False, self.lx.linenumber)
        self.getlocvar(fs, b.info)[1] = fs.pc

    def localstat(self):
        nvars = 0
        e = _Exp()
        while True:
            self.new_localvar(self.str_checkname())
            nvars += 1
            if not self.testnext(","):
                break
        if self.testnext("="):
            nexps = self.explist(e)
        else:
            e.k = VVOID
            nexps = 0
        self.adjust_assign(nvars, nexps, e)
        self.adjustlocalvars(nvars)

    def funcname(self, v):
        ismethod = False
        self.singlevar(v)
        while self.lx.t[0] == ".":
            self.fieldsel(v)
        if self.lx.t[0] == ":":
            ismethod = True
            self.fieldsel(v)
        return ismethod

    def funcstat(self, line):
        v, b = _Exp(), _Exp()
        self.lx.next()
        ismethod = self.funcname(v)
        self.body(b, ismethod, line)
        self.storevar(v, b)
        self.fixline(line)

    def exprstat(self):
        fs = self.fs
        v = _Exp()
        self.suffixedexp(v)
        if self.lx.t[0] in ("=", ","):
            self.assignment([v], 1)
        else:
            self.check_condition(v.k == VCALL, "syntax error")
            code = fs.f.code
            code[v.info] = _set_C(code[v.info], 1)

    def retstat(self):
        fs = self.fs
        e = _Exp()
        if self.block_follow(True) or self.lx.t[0] == ";":
            first = nret = 0
        else:
            nret = self.explist(e)
            if e.k in (VCALL, VVARARG):
                self.setmultret(e)
                if e.k == VCALL and nret == 1:
                    code = fs.f.code
                    code[e.info] = _set_op(code[e.info], TAILCALL)
                first = fs.nactvar
                nret = LUA_MULTRET
            else:
                if nret == 1:
                    first = self.exp2anyreg(e)
                else:
                    self.exp2nextreg(e)
                    first = fs.nactvar
        self.ret(first, nret)
        self.testnext(";")

    def statement(self):
        line = self.lx.linenumber
        fs = self.fs
        t = self.lx.t[0]
        if t == ";":
            self.lx.next()
        elif t == "if":
            self.ifstat(line)
        elif t == "while":
            self.whilestat(line)
        elif t == "do":
            self.lx.next()
            self.block()
            self.check_match("end", "do", line)
        elif t == "for":
            self.forstat(line)
        elif t == "repeat":
            self.repeatstat(line)
        elif t == "function":
            self.funcstat(line)
        elif t == "local":
            self.lx.next()
            if self.testnext("function"):
                self.localfunc()
            else:
                self.localstat()
        elif t == "::":
            self.lx.next()
            self.labelstat(self.str_checkname(), line)
        elif t == "return":
            self.lx.next()
            self.retstat()
        elif t in ("break", "goto"):
            self.gotostat(self.jump())
        else:
            self.exprstat()
        self.fs.freereg = self.fs.nactvar

    def mainfunc(self):
        fs = _FS()
        bl = _Block()
        self.open_func(fs, bl)
        fs.f.vararg = 1
        v = _Exp()
        self.init_exp(v, VLOCAL, 0)
        self.newupvalue(fs, self.envn, v)
        self.lx.next()
        self.statlist()
        self.check("EOS")
        self.close_func()
        return fs.f


def compile_lua(source: bytes, chunkname: str = "?") -> bytes:
    c = _Compiler(source, chunkname)
    main = c.mainfunc()

    def fin(f, is_main):
        f.locvars = [(n, a, b) for n, a, b in f.locvars]
        f.source = (b"@" + chunkname.encode("utf-8", "replace")) if is_main else None
        for p in f.protos:
            fin(p, False)
    fin(main, True)
    ch = Chunk()
    ch.fmt, ch.size_t, ch.nup_main, ch.main = "std", STD_SIZE_T, 1, main
    return write_chunk(ch)


BASE = Path(os.environ.get("LUAC_TOOL_BASEDIR", "/storage/emulated/0/luac_tool/"))
D_LUA = BASE / "Lua"
D_INJECT = BASE / "INJECT"
D_REPACK = BASE / "REPACK"
D_SOURCE = BASE / "SOURCE"


_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(code, s):
    return "\033[%sm%s\033[0m" % (code, s) if _COLOR else s


def cyan(s): return _c("1;36", s)
def green(s): return _c("1;32", s)
def red(s): return _c("1;31", s)
def yellow(s): return _c("1;33", s)
def dim(s): return _c("2", s)
def bold(s): return _c("1", s)


def status(tag, rel, note=""):
    mark = {"ok": green("  ✓ "), "fail": red("  ✗ "), "keep": yellow("  ~ "), "skip": dim("  - ")}[tag]
    print(mark + rel + ((" " + dim(note)) if note else ""))


def is_luac(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"\x1bLua"
    except OSError:
        return False


def collect(src: Path):
    src = Path(src)
    if src.is_file():
        return [(src, Path(src.name))]
    if not src.is_dir():
        return []
    out = []
    for p in sorted(src.rglob("*")):
        if p.is_file() and is_luac(p):
            out.append((p, p.relative_to(src)))
    return out


def _write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        path.write_text(data, encoding="utf-8")
    else:
        path.write_bytes(data)


def verify_encoded(std_blob: bytes, game_blob: bytes) -> bool:
    a = parse_chunk(std_blob, "std")
    b = parse_chunk(decode_blob(game_blob), "std")
    a.size_t = b.size_t = STD_SIZE_T
    a.main.source = b.main.source
    return write_chunk(a) == write_chunk(b)


def do_decode(src, dst, protect_edits=True):
    ok = kept = fail = 0
    files = collect(src)
    for f, rel in files:
        try:
            blob = f.read_bytes()
            try:
                if parse_chunk(blob).fmt == "std":
                    status("skip", rel.as_posix(), "already standard format")
                    continue
            except BadChunk:
                pass
            std = decode_blob(blob)
            exact = encode_blob(std, blob) == blob
            out = Path(dst) / rel
            if protect_edits and out.exists() and out.read_bytes() != std:
                kept += 1
                status("keep", rel.as_posix(), "exists and differs - your edited file was kept")
                continue
            _write(out, std)
            ok += 1
            tl = len(parse_chunk(blob, "game").tail)
            notes = []
            if tl:
                notes.append("%d trailing bytes after the chunk were kept" % tl)
            if not exact:
                notes.append("round-trip differs!")
            status("ok" if exact else "keep", rel.as_posix(), "(" + "; ".join(notes) + ")" if notes else "")
        except Exception as ex:
            fail += 1
            status("fail", rel.as_posix(), str(ex))
    return ok, kept, fail


def do_encode(src, dst, ref=None):
    ok = skip = fail = 0
    for f, rel in collect(src):
        try:
            blob = f.read_bytes()
            try:
                if parse_chunk(blob).fmt == "game":
                    skip += 1
                    status("skip", rel.as_posix(), "already game format")
                    continue
            except BadChunk:
                pass
            reference = None
            if ref:
                rp = Path(ref) / rel if Path(ref).is_dir() else Path(ref)
                if rp.is_file():
                    reference = rp.read_bytes()
            out = encode_blob(blob, reference)
            parse_chunk(out, "game")
            good = verify_encoded(blob, out)
            _write(Path(dst) / rel, out)
            ok += 1
            notes = []
            if reference is None:
                notes.append("no original in Lua/: path+lines taken from this file")
            if not good:
                notes.append("WARNING: re-decode check differs")
            status("ok", rel.as_posix(), "(" + "; ".join(notes) + ")" if notes else "")
        except Exception as ex:
            fail += 1
            status("fail", rel.as_posix(), str(ex))
    return ok, skip, fail


MANIFEST = ".luac_manifest.json"


def do_decompile(src, dst):
    tf = tn = tb = verified = 0
    man = _load_manifest(dst) if Path(dst).is_dir() else {}
    for f, rel in collect(src):
        try:
            blob = f.read_bytes()
            text, n, bad = decompile_blob(blob)
            head = "-- decompiled from luac bytecode (Lua 5.3)\n"
            nm = source_name_of(blob)
            if nm:
                head += "-- original path: %s\n" % nm.lstrip("@")
            notes = []
            if bad:
                head += "-- %d of %d functions could not be rebuilt; see the disassembly comments\n" % (bad, n)
                notes.append("%d function(s) left as disassembly" % bad)
            probs = check_lua_syntax(text)
            cf, ct = coverage_check(blob, text)
            if cf != ct:
                head += "-- WARNING: %d of %d string constants missing from the output\n" % (ct - cf, ct)
                notes.append("%d string(s) missing" % (ct - cf))
            if probs:
                head += "-- WARNING: syntax self-check found %d problem(s): %s\n" % (len(probs), "; ".join(probs[:3]))
                notes.append("%d syntax warning(s)" % len(probs))
            same, total, err = verify_source(blob, text)
            if err:
                head += "-- WARNING: this source does not compile back: %s\n" % err
                notes.append("does not compile back")
            elif same != total:
                head += ("-- NOTE: %d of %d functions rebuild to different bytecode than the original "
                         "(check them before relying on the result)\n" % (total - same, total))
                notes.append("%d/%d functions differ after rebuild" % (total - same, total))
            else:
                head += "-- verified: all %d functions rebuild to the original bytecode\n" % total
                verified += 1
            out = Path(dst) / rel
            if out.suffix.lower() != ".lua":
                out = out.with_name(out.name + ".lua")
            body = (head + text).encode("utf-8")
            _write(out, body)
            man[out.relative_to(dst).as_posix()] = hashlib.sha1(body).hexdigest()
            tf += 1
            tn += n
            tb += bad
            ok_all = not notes
            status("ok" if ok_all else "keep", rel.as_posix(),
                   "(%d functions%s)" % (n, ", verified" if ok_all else "; " + "; ".join(notes)))
        except Exception as ex:
            status("fail", rel.as_posix(), str(ex))
    if tf:
        try:
            _write(Path(dst) / MANIFEST, json.dumps(man, indent=1))
        except OSError:
            pass
    print("Decompiled %d file(s), %d/%d functions -> %s" % (tf, tn - tb, tn, dst))
    return tf, verified


def _count_funcs(f):
    return 1 + sum(_count_funcs(p) for p in f.protos)


def _same_func(a, b):
    return (a.code == b.code and a.k == b.k and a.nparams == b.nparams and
            a.vararg == b.vararg and a.up == b.up and a.maxstack == b.maxstack)


def verify_source(blob: bytes, text: str):
    orig = parse_chunk(decode_blob(blob), "std").main
    total = _count_funcs(orig)
    try:
        new = parse_chunk(compile_lua(text.encode("utf-8"), "verify"), "std").main
    except LuaCompileError as ex:
        return 0, total, str(ex)
    same = 0
    stack = [(orig, new)]
    while stack:
        a, b = stack.pop()
        if _same_func(a, b):
            same += 1
        if len(a.protos) == len(b.protos):
            stack.extend(zip(a.protos, b.protos))
    return same, total, None


def collect_sources(src):
    src = Path(src)
    if src.is_file():
        return [(src, Path(src.name))]
    out = []
    if src.is_dir():
        for p in sorted(src.rglob("*.lua")):
            if p.is_file() and not is_luac(p):
                out.append((p, p.relative_to(src)))
    return out


def _load_manifest(d):
    try:
        return json.loads((Path(d) / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _find_reference(ref_dir, rel: Path):
    if not ref_dir:
        return None
    ref_dir = Path(ref_dir)
    names = [rel]
    if rel.suffix.lower() == ".lua" and rel.with_suffix("").suffix:
        names.append(rel.with_suffix(""))
    for n in names:
        p = ref_dir / n
        if p.is_file() and is_luac(p):
            return p, n
    return None


def do_rebuild(src, dst, ref_dir=None):
    ok = same = fail = 0
    man = _load_manifest(src) if Path(src).is_dir() else {}
    for f, rel in collect_sources(src):
        try:
            data = f.read_bytes()
            ref = _find_reference(ref_dir, rel)
            ref_blob = ref[0].read_bytes() if ref else None
            out = Path(dst) / (ref[1] if ref else rel)
            if ref_blob is not None and man.get(rel.as_posix()) == hashlib.sha1(data).hexdigest():
                _write(out, ref_blob)
                same += 1
                status("ok", rel.as_posix(), "(unchanged - original file kept byte-exact)")
                continue
            std = compile_lua(data, rel.as_posix())
            game = encode_blob(std, ref_blob)
            if not verify_encoded(std, game):
                raise BadChunk("self-check failed (round trip differs)")
            nf = _count_funcs(parse_chunk(std, "std").main)
            _write(out, game)
            ok += 1
            status("ok", rel.as_posix(), "(rebuilt, %d functions)" % nf)
        except LuaCompileError as ex:
            fail += 1
            status("fail", rel.as_posix(), str(ex))
        except Exception as ex:
            fail += 1
            status("fail", rel.as_posix(), "%s: %s" % (type(ex).__name__, ex))
    return ok, same, fail


def do_info(path):
    for f, rel in collect(path):
        blob = f.read_bytes()
        try:
            ch = parse_chunk(blob)
        except BadChunk as ex:
            print("%s: %s" % (rel.as_posix(), ex))
            continue

        def cnt(x):
            return 1 + sum(cnt(c) for c in x.protos)
        print("%s: format=%s size_t=%d functions=%d source=%s" %
              (rel.as_posix(), "game" if ch.fmt == "game" else "standard 5.3", ch.size_t,
               cnt(ch.main), source_name_of(blob)) +
              ("  trailing_bytes=%d" % len(ch.tail) if ch.tail else ""))


W = 46


def _count(d: Path) -> int:
    return len(collect(d))


def _count_src(d: Path) -> int:
    return len(collect_sources(d))


def draw_header():
    line = "═" * W
    print(cyan("╔" + line + "╗"))
    print(cyan("║") + bold("LUAC TOOL  ·  Termux".center(W)) + cyan("║"))
    print(cyan("╠" + line + "╣"))
    print(cyan("║") + (" " + str(BASE)).ljust(W)[:W] + cyan("║"))
    print(cyan("╚" + line + "╝"))
    rows = [("Lua", "game files", _count(D_LUA)), ("SOURCE", "readable / edit", _count_src(D_SOURCE)),
            ("REPACK", "rebuilt (final)", _count(D_REPACK))]
    for name, what, n in rows:
        print("  %s %s %s" % (bold(name.ljust(7)), dim(what.ljust(19)),
                              (green if n else dim)("%d file(s)" % n)))
    print()


def draw_menu():
    print("  " + bold("[1]") + "  DECOMPILE  " + dim("Lua    ->  SOURCE  (readable .lua)"))
    print("  " + bold("[2]") + "  REBUILD    " + dim("SOURCE ->  REPACK  (game luac)"))
    print("  " + bold("[0]") + "  Exit")
    print()


def _pause():
    try:
        input(dim("\nPress Enter to go back..."))
    except (EOFError, KeyboardInterrupt):
        raise SystemExit(0)


def action_decompile():
    print(bold("\nDECOMPILE") + dim("   %s  ->  %s\n" % (D_LUA, D_SOURCE)))
    if not collect(D_LUA):
        print(yellow("No luac files found in Lua/."))
        print("Put the game's .lua/.luac bytecode files in:\n  " + str(D_LUA))
        return
    tf, verified = do_decompile(D_LUA, D_SOURCE)
    if tf:
        print("\n" + green("%d file(s) written" % tf) +
              (", " + green("%d verified" % verified) if verified else "") +
              (", " + yellow("%d need a look" % (tf - verified)) if tf - verified else ""))
        print("Readable files are in: " + str(D_SOURCE))
        print(dim("Edit them, then run option 2 to rebuild."))


def action_rebuild():
    print(bold("\nREBUILD") + dim("   %s  ->  %s\n" % (D_SOURCE, D_REPACK)))
    if not collect_sources(D_SOURCE):
        print(yellow("No .lua files found in SOURCE/."))
        print("Run option 1 first:\n  " + str(D_SOURCE))
        return
    ok, same, fail = do_rebuild(D_SOURCE, D_REPACK, D_LUA)
    print("\n" + green("%d rebuilt" % ok) +
          (", " + dim("%d unchanged" % same) if same else "") +
          (", " + red("%d failed" % fail) if fail else ""))
    if ok or same:
        print("Finished files: " + str(D_REPACK))
        print(dim("Copy them back into the game / pak tool (same names as the originals)."))


def ui():
    for d in (D_LUA, D_SOURCE, D_REPACK):
        try:
            d.mkdir(parents=True, exist_ok=True)
        except OSError as ex:
            print(red("Cannot create %s: %s" % (d, ex)))
            print("Run  termux-setup-storage  once, then start the tool again.")
            return
    while True:
        os.system("clear" if os.name != "nt" else "cls")
        draw_header()
        draw_menu()
        try:
            c = input(bold("Choose: ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if c == "1":
            action_decompile()
            _pause()
        elif c == "2":
            action_rebuild()
            _pause()
        elif c in ("0", "q", "Q"):
            return
        else:
            print(red("Invalid choice."))
            _pause()


USAGE = """luac_tool.py  -  single-file Lua bytecode tool

  python luac_tool.py                      Termux menu (1 = decompile, 2 = rebuild)
  python luac_tool.py rebuild    IN [OUT] [--ref ORIGINALS]    readable .lua -> game luac
  python luac_tool.py decode     IN [OUT]                      game luac -> standard luac
  python luac_tool.py encode     IN [OUT] [--ref ORIGINAL]     standard luac -> game luac
  python luac_tool.py decompile  IN [OUT]                      luac -> readable .lua
  python luac_tool.py info       IN

IN / OUT / ORIGINAL can be a single file or a folder.
"""


def main(argv):
    if len(argv) < 2:
        return ui()
    cmd, args = argv[1].lower(), argv[2:]
    ref = None
    if "--ref" in args:
        i = args.index("--ref")
        ref = args[i + 1]
        del args[i:i + 2]
    if cmd in ("-h", "--help", "help") or not args:
        print(USAGE)
        return
    if cmd == "decode":
        r = do_decode(args[0], args[1] if len(args) > 1 else D_INJECT)
        print("decoded %d, kept %d, failed %d" % r)
    elif cmd == "encode":
        r = do_encode(args[0], args[1] if len(args) > 1 else D_REPACK, ref)
        print("encoded %d, skipped %d, failed %d" % r)
    elif cmd == "decompile":
        do_decompile(args[0], args[1] if len(args) > 1 else D_SOURCE)
    elif cmd == "rebuild":
        r = do_rebuild(args[0], args[1] if len(args) > 1 else D_REPACK, ref or D_LUA)
        print("rebuilt %d, unchanged %d, failed %d" % r)
    elif cmd == "info":
        do_info(args[0])
    else:
        print(USAGE)


def _run():
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":

    for size in (512, 256, 128, 64):
        try:
            threading.stack_size(size * 1024 * 1024)
            break
        except (ValueError, RuntimeError):
            continue
    t = threading.Thread(target=_run)
    t.start()
    t.join()
