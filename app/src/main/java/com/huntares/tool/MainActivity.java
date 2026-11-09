package com.huntares.tool;

import android.app.*;
import android.os.*;
import android.content.*;
import android.net.Uri;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.*;
import android.widget.*;
import androidx.documentfile.provider.DocumentFile;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import java.io.*;
import java.util.*;

public class MainActivity extends Activity {
    DocumentFile root;
    LinearLayout body;
    TextView status;
    String mode = "full";
    static final int PICK_TREE = 10;
    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        if (!Python.isStarted()) Python.start(new AndroidPlatform(this));
        String uri = getPreferences(0).getString("tree", null);
        if (uri != null) root = DocumentFile.fromTreeUri(this, Uri.parse(uri));
        showHome();
    }
    int white = Color.WHITE;
    int muted = 0xffadb0b8;
    GradientDrawable panel(boolean glow) {
        GradientDrawable d = new GradientDrawable(GradientDrawable.Orientation.TL_BR,
            new int[]{0xff1b1d21, 0xff050506, 0xff111216});
        d.setCornerRadius(22);
        d.setStroke(glow ? 2 : 1, glow ? 0xffe3e3e3 : 0xff55565a);
        return d;
    }
    TextView label(String value, int size, int color) {
        TextView t = new TextView(this); t.setText(value); t.setTextSize(size);
        t.setTextColor(color); t.setGravity(Gravity.CENTER_VERTICAL);
        return t;
    }
    void init(String title) {
        ScrollView scroll = new ScrollView(this);
        body = new LinearLayout(this); body.setOrientation(1); body.setPadding(22,28,22,28);
        body.setBackground(new GradientDrawable(GradientDrawable.Orientation.TL_BR,
            new int[]{0xff030304,0xff17181b,0xff030304}));
        scroll.setFillViewport(true); scroll.addView(body); setContentView(scroll);
        LinearLayout header = new LinearLayout(this); header.setGravity(Gravity.CENTER_VERTICAL);
        TextView back = label("‹", 36, white); back.setPadding(4,0,18,0);
        if (!title.equals("HUNTARES TOOL")) {
            header.addView(back); back.setOnClickListener(v -> showHome());
        }
        TextView h = label(title, 25, white); h.setTypeface(null,Typeface.BOLD);
        header.addView(h, new LinearLayout.LayoutParams(0,70,1));
        TextView help = label("ⓘ", 30, white); help.setGravity(Gravity.CENTER);
        help.setBackground(panel(true));
        header.addView(help, new LinearLayout.LayoutParams(62,62));
        help.setOnClickListener(v -> showHelp(title));
        body.addView(header);
        TextView logo = label("♛\nHUNTARES", 34, white);
        logo.setGravity(Gravity.CENTER); logo.setTypeface(null,Typeface.BOLD);
        logo.setPadding(0,38,0,28); body.addView(logo);
        status = label("", 13, muted); status.setPadding(8,8,8,20); body.addView(status);
        footer();
    }
    void footer() {
        TextView foot = label("♛  H U N T A R E S", 17, white);
        foot.setGravity(Gravity.CENTER); foot.setPadding(10,38,10,24);
        foot.setOnClickListener(v -> {
            Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse("https://t.me/TDM9993"));
            try { startActivity(i); } catch (Exception e) { msg("Не удалось открыть Telegram"); }
        });
        body.addView(foot);
    }
    void button(String name, Runnable action) {
        TextView b = label(name + "    ›", 19, white);
        b.setTypeface(null, Typeface.BOLD); b.setPadding(24,24,20,24);
        b.setBackground(panel(true));
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1,-2);
        lp.setMargins(0,8,0,12); body.addView(b,lp);
        b.setOnClickListener(v -> action.run());
    }
    void showHelp(String context) {
        final String pak = "1. Открой PAK TOOL/ОРИГИНАЛ ПАК и положи туда исходный .pak.\n\n"
            + "2. В PAK UNPACK выбери архив и режим: полный, только Lua или .uasset + .uexp.\n\n"
            + "3. Изменяй файлы в PAK TOOL/PAK UNPACK/имя_патча, сохраняя пути.\n\n"
            + "4. Нажми PAK REPACK. Результат появится в PAK TOOL/PAK REPACK.\n\n"
            + "Оригинальный архив сохраняй отдельно. Некоторые зашифрованные PAK могут не поддерживаться.";
        final String lua = "1. Положи исходный Lua 5.3 в LUA TOOL/ОРИГИНАЛ ЛУА.\n\n"
            + "2. Нажми «Расшифровать» и выбери файл.\n\n"
            + "3. Открой LUA TOOL/lua_unpak и отредактируй результат.\n\n"
            + "4. Нажми «Собрать обратно с изменениями». Файл появится в LUA TOOL/result_lua.\n\n"
            + "Проверяй результат: не любой бинарный Lua поддерживается.";
        String message = context.contains("LUA") ? lua : context.contains("PAK") ? pak :
            "PAK TOOL — работа с .pak, .uasset, .uexp и Lua внутри архивов.\n\n"
            + "LUA TOOL — отдельная обработка Lua 5.3.\n\n" + pak + "\n\nLUA TOOL\n" + lua;
        new AlertDialog.Builder(this).setTitle("ⓘ  Помощь и обучение")
            .setMessage(message).setPositiveButton("Понятно",(d,w)->{}).show();
    }
    void msg(String s) { runOnUiThread(() -> status.setText(s)); }
    DocumentFile dir(DocumentFile base, String name) {
        DocumentFile f = base.findFile(name);
        if (f == null) f = base.createDirectory(name);
        if (f == null || !f.isDirectory()) throw new IllegalStateException("Нет доступа к папке " + name);
        return f;
    }
    DocumentFile path(String... names) {
        if (root == null) throw new IllegalStateException("Выберите рабочую папку");
        DocumentFile d = dir(root, "HUNTARES TOOL");
        for (String name : names) d = dir(d, name);
        return d;
    }
    void setup() {
        path("PAK TOOL", "ОРИГИНАЛ ПАК"); path("PAK TOOL", "PAK UNPACK"); path("PAK TOOL", "PAK REPACK");
        path("LUA TOOL", "ОРИГИНАЛ ЛУА"); path("LUA TOOL", "lua_unpak"); path("LUA TOOL", "result_lua");
    }
    void showHome() {
        init("HUNTARES TOOL");
        msg(root == null ? "Сначала выберите рабочую папку (например, Documents)." : "Рабочая папка выбрана");
        button("Разрешить доступ / выбрать папку", () -> {
            Intent i = new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE);
            i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
            startActivityForResult(i, PICK_TREE);
        });
        button("LUA TOOL", () -> showLua()); button("PAK TOOL", () -> showPak());
        button("Открыть рабочую папку", () -> { if (root != null) {
            Intent i = new Intent(Intent.ACTION_VIEW); i.setDataAndType(root.getUri(), "vnd.android.document/directory");
            i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            try { startActivity(i); } catch(Exception e) { msg("Откройте выбранную папку в файловом менеджере"); }
        }});
        TextView t = new TextView(this); t.setText("Алгоритм Lua: @VoidPAK. Только поддерживаемые форматы Lua 5.3 и PAK. Результаты требуют проверки."); t.setTextColor(0xffaaaaaa); body.addView(t);
    }
    @Override protected void onActivityResult(int req, int result, Intent data) {
        super.onActivityResult(req, result, data);
        if (req == PICK_TREE && result == RESULT_OK && data != null) {
            Uri u = data.getData();
            getContentResolver().takePersistableUriPermission(u, Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            root = DocumentFile.fromTreeUri(this, u);
            try { setup(); showHome(); msg("Созданы папки HUNTARES TOOL в выбранном каталоге"); }
            catch(Exception e) { msg("Ошибка: " + e.getMessage()); }
        }
    }
    void showLua() {
        init("LUA TOOL"); button("← Главная", () -> showHome());
        button("Расшифровать", () -> chooseFile(new String[]{"LUA TOOL","ОРИГИНАЛ ЛУА"}, ".lua,.luac", file -> {
            String name = file.getName(); String outName = name.replaceAll("\\.luac$", ".lua");
            DocumentFile dest = path("LUA TOOL", "lua_unpak");
            process("lua_unpack", new DocumentFile[]{file}, dest, outName, "text/plain");
        }));
        button("Собрать обратно с изменениями", () -> chooseFile(new String[]{"LUA TOOL","lua_unpak"}, ".lua", file -> {
            DocumentFile origDir = path("LUA TOOL", "ОРИГИНАЛ ЛУА");
            DocumentFile orig = origDir.findFile(file.getName());
            if (orig == null) orig = origDir.findFile(file.getName().replaceAll("\\.lua$", ".luac"));
            if (orig == null) { msg("Не найден оригинальный Lua с таким именем"); return; }
            process("lua_repack", new DocumentFile[]{file, orig}, path("LUA TOOL", "result_lua"), file.getName(), "application/octet-stream");
        }));
    }
    void showPak() {
        init("PAK TOOL"); button("← Главная", () -> showHome());
        final String[] labels = {"Полный PAK + Lua (извлечение)", "Только Lua", "Только .uasset и .uexp"};
        Spinner spinner = new Spinner(this); ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, labels);
        spinner.setAdapter(adapter); body.addView(spinner);
        button("PAK UNPACK", () -> chooseFile(new String[]{"PAK TOOL","ОРИГИНАЛ ПАК"}, ".pak", file -> {
            String stem = file.getName().replaceAll("(?i)\\.pak$", "");
            DocumentFile dest = path("PAK TOOL", "PAK UNPACK");
            DocumentFile folder = dir(dest, stem);
            processPakUnpack(file, folder, new String[]{"full", "lua", "assets"}[spinner.getSelectedItemPosition()]);
        }));
        button("PAK REPACK", () -> chooseFile(new String[]{"PAK TOOL","ОРИГИНАЛ ПАК"}, ".pak", file -> {
            String stem = file.getName().replaceAll("(?i)\\.pak$", "");
            DocumentFile edits = path("PAK TOOL", "PAK UNPACK").findFile(stem);
            if (edits == null || !edits.isDirectory()) { msg("Нет папки распаковки: " + stem); return; }
            processPakRepack(file, edits, path("PAK TOOL", "PAK REPACK"), file.getName());
        }));
    }
    interface FileChoice { void selected(DocumentFile f); }
    void chooseFile(String[] folders, String extensions, FileChoice callback) {
        try {
            DocumentFile d = path(folders); ArrayList<DocumentFile> files = new ArrayList<>();
            for (DocumentFile f : d.listFiles()) if (f.isFile() && extensions.contains("." + f.getName().toLowerCase(Locale.ROOT).replaceAll("^.*\\.", ""))) files.add(f);
            if (files.isEmpty()) { msg("Нет файлов в папке: " + folders[folders.length-1]); return; }
            String[] names = new String[files.size()]; for(int i=0;i<files.size();i++) names[i]=files.get(i).getName();
            new AlertDialog.Builder(this).setTitle("Выберите файл").setItems(names, (dlg, which) -> callback.selected(files.get(which))).show();
        } catch(Exception e) { msg(e.getMessage()); }
    }
    File copyToTemp(DocumentFile doc) throws Exception {
        File f = File.createTempFile("huntares_", ".bin", getCacheDir());
        try(InputStream in = getContentResolver().openInputStream(doc.getUri()); OutputStream out = new FileOutputStream(f)) { byte[] b=new byte[65536]; int n; while((n=in.read(b))!=-1) out.write(b,0,n); }
        return f;
    }
    void copyBack(File file, DocumentFile dir, String name, String mime) throws Exception {
        if (dir.findFile(name) != null) throw new IOException("Результат уже существует: " + name);
        DocumentFile target = dir.createFile(mime, name);
        if (target == null) throw new IOException("Не удалось создать файл");
        try(InputStream in=new FileInputStream(file); OutputStream out=getContentResolver().openOutputStream(target.getUri(),"w")) { byte[] b=new byte[65536]; int n; while((n=in.read(b))!=-1) out.write(b,0,n); }
    }
    void process(String action, DocumentFile[] inputs, DocumentFile dest, String name, String mime) {
        msg("Обработка..."); new Thread(() -> {
            ArrayList<File> temps=new ArrayList<>();
            try {
                ArrayList<Object> args=new ArrayList<>();
                for(DocumentFile doc:inputs) { File f=copyToTemp(doc); temps.add(f); args.add(f.getAbsolutePath()); }
                File output=File.createTempFile("huntares_result_", ".bin", getCacheDir()); temps.add(output); args.add(output.getAbsolutePath());
                String report=Python.getInstance().getModule("bridge").callAttr(action, args.toArray()).toString();
                copyBack(output,dest,name,mime); msg(report + "\nФайл: " + name);
            } catch(Exception e) { msg("Ошибка: " + e.getMessage()); }
            finally { for(File f:temps) f.delete(); }
        }).start();
    }
    void processPakUnpack(DocumentFile pak, DocumentFile dest, String mode) {
        msg("Распаковка PAK..."); new Thread(() -> {
            File original=null; File folder=new File(getCacheDir(),"pak_"+System.nanoTime()); folder.mkdirs();
            try { original=copyToTemp(pak);
                String report=Python.getInstance().getModule("bridge").callAttr("pak_unpack",original.getAbsolutePath(),folder.getAbsolutePath(),mode).toString();
                uploadTree(folder,dest); msg(report);
            } catch(Exception e) { msg("PAK ошибка: " + e.getMessage()); }
            finally { if(original!=null) original.delete(); deleteTree(folder); }
        }).start();
    }
    void processPakRepack(DocumentFile pak, DocumentFile edits, DocumentFile dest, String name) {
        msg("Сборка PAK..."); new Thread(() -> {
            File original=null; File folder=new File(getCacheDir(),"edit_"+System.nanoTime()); folder.mkdirs();
            File output=new File(getCacheDir(),"result_"+System.nanoTime()+".pak");
            try { original=copyToTemp(pak); downloadTree(edits,folder);
                String report=Python.getInstance().getModule("bridge").callAttr("pak_repack",original.getAbsolutePath(),folder.getAbsolutePath(),output.getAbsolutePath()).toString();
                copyBack(output,dest,name,"application/octet-stream"); msg(report);
            } catch(Exception e) { msg("PAK ошибка: " + e.getMessage()); }
            finally { if(original!=null) original.delete(); output.delete(); deleteTree(folder); }
        }).start();
    }
    void uploadTree(File src, DocumentFile dst) throws Exception {
        File[] files=src.listFiles(); if(files==null)return;
        for(File f:files) if(f.isDirectory()) uploadTree(f,dir(dst,f.getName())); else copyBack(f,dst,f.getName(),"application/octet-stream");
    }
    void downloadTree(DocumentFile src, File dst) throws Exception {
        for(DocumentFile f:src.listFiles()) { File local=new File(dst,f.getName());
            if(f.isDirectory()) { local.mkdirs(); downloadTree(f,local); }
            else try(InputStream in=getContentResolver().openInputStream(f.getUri());OutputStream out=new FileOutputStream(local)) {byte[] b=new byte[65536];int n;while((n=in.read(b))!=-1)out.write(b,0,n);}
        }
    }
    void deleteTree(File f) {if(f.isDirectory()){File[] a=f.listFiles();if(a!=null)for(File x:a)deleteTree(x);}f.delete();}
}
