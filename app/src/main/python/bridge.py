"""Local-only file processing. Original code by @VoidPAK in luac_tool.py."""
from pathlib import Path
import luac_tool as lt

def lua_unpack(src, dest):
    raw = Path(src).read_bytes()
    if not raw.startswith(b'\x1bLua\x53'):
        raise ValueError('Поддерживается бинарный Lua 5.3')
    ch = lt.parse_chunk(raw)
    standard = lt.decode_blob(raw) if ch.fmt == 'game' else raw
    text, total, bad = lt.decompile_blob(standard)
    if not text.strip():
        raise ValueError('Декомпилятор не создал исходник')
    Path(dest).write_text('-- Декомпиляция Lua 5.3; алгоритм @VoidPAK\n' + text, encoding='utf-8')
    return f'Готово: функций {total}, с ошибками {bad}. Проверьте код перед сборкой.'

def lua_repack(src, original, dest):
    source = Path(src).read_bytes()
    ref = Path(original).read_bytes()
    ch = lt.parse_chunk(ref)
    compiled = lt.compile_lua(source, Path(src).name)
    packed = lt.encode_blob(compiled, reference=ref) if ch.fmt == 'game' else compiled
    lt.parse_chunk(packed, ch.fmt)
    Path(dest).write_bytes(packed)
    return 'Lua собран; совместимость с игрой не гарантирована.'

def pak_unpack(src, dest, mode):
    import UltimateEngineTool as ue
    pak = ue.TencentPakFile(Path(src))
    if not pak._index:
        raise ValueError('Индекс PAK не прочитан')
    pak.dump(Path(dest))
    root = Path(dest)
    if mode != 'full':
        exts = ('.lua', '.luac') if mode == 'lua' else ('.uasset', '.uexp')
        for f in root.rglob('*'):
            if f.is_file() and f.suffix.lower() not in exts:
                f.unlink()
    return 'Распаковка завершена. Поддержка данного PAK не гарантирована.'

def pak_repack(original, edits, dest):
    import UltimateEngineTool as ue
    pak = ue.TencentPakFile(Path(original))
    if not pak._index:
        raise ValueError('Индекс PAK не прочитан')
    count = ue.repack_pak_file_full(pak, Path(edits), Path(dest))
    if not Path(dest).exists():
        raise ValueError('PAK не создан')
    return f'Обработано: {count}. Проверьте результат.'
