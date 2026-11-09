package com.huntares.tool;

import android.app.*;
import android.os.*;
import android.content.*;
import android.net.Uri;
import android.graphics.Color;
import android.content.SharedPreferences;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.*;
import android.widget.*;
import androidx.documentfile.provider.DocumentFile;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import java.io.*;
import java.util.*;
import org.json.*;
import java.net.*;
import java.security.SecureRandom;

public class MainActivity extends Activity {
    DocumentFile root;
    LinearLayout body;
    TextView status;
    String mode = "full";
    boolean admin = false;
    String sessionKey = "";
    // OFFLINE DEMO: local admin authorization is not tamper-proof.
    // The signing private key is still embedded and extractable; not for commercial security.
    // SHA-256 verifier: the literal admin passphrase is not included in the APK.
    // This only obscures the secret; local authorization can still be patched.
    private static final String ACCESS_DIGEST = "52f4853d1f97d4c81dc04df1f430ed6f991b9bc75495c4d87c8a8dd897e83a4b";
    private boolean checkLocalAccess(String supplied) {
        try {
            java.security.MessageDigest sha = java.security.MessageDigest.getInstance("SHA-256");
            byte[] digest = sha.digest(supplied.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            byte[] expected = new byte[ACCESS_DIGEST.length() / 2];
            for (int i = 0; i < expected.length; i++)
                expected[i] = (byte) Integer.parseInt(ACCESS_DIGEST.substring(i*2, i*2+2), 16);
            return java.security.MessageDigest.isEqual(digest, expected);
        } catch (Exception ignored) { return false; }
    }
    static final String SIGNING_PRIVATE = "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDP0OW7L9B3jp3zstSIckvejFA5AFsYqLtEdU4WLMcW0DDB9Ps9L+BuxtV7hFNOrKKBF5wd3rAxtwT8S5TMbX80aAm1bDAr3DgDohHhkHtIhkriEUciPPk2yjok1x7ewi5icWtUrv+OpRhEgLKBUdbMnBkvjisO8XtoYxNAA2dTqavjD5qoN4JwehQ2rXonoSrNluM3hjuPb60dIAdcrNu4YbNiLhRAc+hW5orKOXbrUqAkopD63P7C4kf4fzZy6piP+bfBGoZQgQxBBMXokKudvT/Xbw/Ub48frmZvBwsWISufWTguW/muqIiJEnQZhf2VsptbcU1Coq0X2then5mNAgMBAAECggEATbOVsf+Wup0ggdYDkWDq7TMZa7auWPH90wLpR3FGn0kIcfzfU2lrSQAfIie/3lK+D/Z78M8qoewEeTDpWeY3AalEuAjTmhKk/vbCKMyUy/EqXoyHRE34AHxscQneCPwhy70MnIUyGGuyPyq/k4q9/ZL/97/4aYXw1n7026JqJ+VETO647qrn8MbUo2GNoHgL1Fjxr49fod6e6KNsGs1bsSZtkQFuxjSD5K9QT23AhoRgo5FLGviXFqSC3hWbD5K9nRXxDSEpnS5IUUWBKVq+8z5PqS4oBkIjGjVtRQnJaZ35FH5L7ihgwFJ1XganCb7lnKoDX4lboz2/lpV7GQBLIQKBgQDsuwYVpHv3sJZosZ8pOnGPXoD6Q+Uqk3vXAMNocfvx8Pw+BWcEX0OOEbsDw6MuLoXhuzFJLz4oZPrvnH/AbwTbZhexufbePJt+NBFU3jDEdK938Fej304/UnfIvMpWZ1Ghl7jt/Sg9Y7jxzAg70u0lxS+OScKfKxSqzSN5YLejBwKBgQDgu1qc3JPwwpOhDKN+HwXbU0mqWKoEhJ7/EmRCqjyr8lVXXR9SqZM0JWB2vbojwFeo2WrGdJOzMDt+HA4+DBxtrrwunWPGLuS+yAWNeBJsPOP2IHLtX8DZKKRxdSa9rHoYFkJCikBeAltC/O9sAaqm4lFnvDdMFx9SZejqVSBVywKBgEmXNiQCNvtfrNIs7VJutaCg+y1Rb+sVX/kNZrGQRYcHqBJLsaOdTa3beyyHY7HWio4KmB6tDgCWq59TIi+bE4J0sUbxjXm2k4ve+chNLhHUSDvbvhLWN0feBhij/65ufeTi+n0ZJqo21uZry991CX2lV8w+x76dMNaL4Mw5sbx/AoGALtrhKZNTxP7MiOd5rvII5pGW6k1SJV8BR20uOjgELlV4NZ7UyQdSCa1BT4B/LrULkcjC2l2z7chAnyp6TbV4t+WWlqF6C/f6+Uv63GQMc0S+wrJBQ/yS2LQAlSc3zJQJYLxDVFw+z1rubCkQQhSW3/SPxHEZlmO7xBI7XaAh/cECgYBYU2yuAY0th0CVH81agJFtUxuxtZjOZx0NdioyXti82v8oNYye7cB3GgipUlL3rN+Mymxg9nZT089tL0B7xev3iushpXH7tn8447FDLsxfvjj0IjjTAE3Wm/uXtfo9ukyqVnRKH8K+OXWE2uE9BMyXIv2SgP2dZ2+JGb57HPvnng==";
    static final String SIGNING_PUBLIC = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz9Dluy/Qd46d87LUiHJL3oxQOQBbGKi7RHVOFizHFtAwwfT7PS/gbsbVe4RTTqyigRecHd6wMbcE/EuUzG1/NGgJtWwwK9w4A6IR4ZB7SIZK4hFHIjz5Nso6JNce3sIuYnFrVK7/jqUYRICygVHWzJwZL44rDvF7aGMTQANnU6mr4w+aqDeCcHoUNq16J6EqzZbjN4Y7j2+tHSAHXKzbuGGzYi4UQHPoVuaKyjl261KgJKKQ+tz+wuJH+H82cuqYj/m3wRqGUIEMQQTF6JCrnb0/128P1G+PH65mbwcLFiErn1k4Llv5rqiIiRJ0GYX9lbKbW3FNQqKtF9rYXp+ZjQIDAQAB";
    final String STORE = "offline_licenses";
    String b64(byte[] b) { return android.util.Base64.encodeToString(b, android.util.Base64.URL_SAFE | android.util.Base64.NO_WRAP | android.util.Base64.NO_PADDING); }
    byte[] un64(String s) { return android.util.Base64.decode(s, android.util.Base64.URL_SAFE | android.util.Base64.NO_WRAP | android.util.Base64.NO_PADDING); }
    String sign(String payload) throws Exception {
        java.security.KeyFactory factory=java.security.KeyFactory.getInstance("RSA");
        java.security.PrivateKey pk=factory.generatePrivate(new java.security.spec.PKCS8EncodedKeySpec(android.util.Base64.decode(SIGNING_PRIVATE,android.util.Base64.DEFAULT)));
        java.security.Signature sig=java.security.Signature.getInstance("SHA256withRSA");sig.initSign(pk);sig.update(payload.getBytes("UTF-8"));return b64(sig.sign());
    }
    JSONObject decodeLicense(String token) throws Exception {
        String[] parts=token.split("\\.");
        if(parts.length!=3 || !parts[0].equals("HT1"))throw new Exception("Неверный формат ключа");
        java.security.KeyFactory factory=java.security.KeyFactory.getInstance("RSA");
        java.security.PublicKey pk=factory.generatePublic(new java.security.spec.X509EncodedKeySpec(android.util.Base64.decode(SIGNING_PUBLIC,android.util.Base64.DEFAULT)));
        java.security.Signature sig=java.security.Signature.getInstance("SHA256withRSA");sig.initVerify(pk);sig.update(parts[1].getBytes("UTF-8"));
        if(!sig.verify(un64(parts[2])))throw new Exception("Неверная подпись ключа");
        JSONObject data=new JSONObject(new String(un64(parts[1]),"UTF-8"));
        if(data.optLong("exp",0)>0 && System.currentTimeMillis()>data.optLong("exp"))throw new Exception("Срок ключа истёк");
        if(data.optString("type").equals("hwid") && !deviceId().equals(data.optString("device")))throw new Exception("Ключ привязан к другому устройству");
        return data;
    }
    void copyText(String text) {
        ((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE)).setPrimaryClip(android.content.ClipData.newPlainText("HUNTARES key",text));
        msg("Скопировано в буфер обмена");
    }
    JSONObject obj(String... fields) { JSONObject j=new JSONObject(); try {for(int i=0;i<fields.length;i+=2)j.put(fields[i],fields[i+1]);}catch(Exception e){}return j; }
    String deviceId() {
        SharedPreferences pref=getPreferences(0);
        String id=pref.getString("device_id",null);
        if(id==null){byte[] b=new byte[16];new SecureRandom().nextBytes(b);StringBuilder x=new StringBuilder();for(byte v:b)x.append(String.format(java.util.Locale.US,"%02x",v&255));id=x.toString();pref.edit().putString("device_id",id).apply();}
        return id;
    }
    void activate(String key) {
        if(checkLocalAccess(key)){admin=true;sessionKey=key;showHome();return;}
        try {decodeLicense(key);admin=false;sessionKey=key;showHome();}
        catch(Exception e){msg("Активация отклонена: "+e.getMessage());}
    }
    void showActivation(){
        init("Активация доступа");
        TextView t=label("Введите лицензионный ключ, чтобы открыть HUNTARES TOOL",16,white);t.setPadding(dp(6),dp(22),0,dp(14));body.addView(t);
        EditText key=new EditText(this);key.setSingleLine(false);key.setMinLines(2);key.setMaxLines(5);key.setHint("Ключ доступа");key.setTextColor(white);key.setHintTextColor(muted);key.setBackground(panel(false));key.setPadding(dp(15),dp(12),dp(15),dp(12));body.addView(key);
        button("Активировать",()->activate(key.getText().toString().trim()));
        TextView code=label("Код устройства: "+deviceId(),12,muted);code.setPadding(dp(8),dp(18),dp(8),dp(10));body.addView(code);
        button("Скопировать код устройства",()->copyText(deviceId()));
        TextView contact=label("Получить ключ и купить обучение по созданию CFG: @haunter_extaze",14,white);
        contact.setPadding(dp(8),dp(22),dp(8),dp(22));body.addView(contact);
        contact.setOnClickListener(v->startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://t.me/haunter_extaze"))));
        footer();
    }

    static final int PICK_TREE = 10;
    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        if (!Python.isStarted()) Python.start(new AndroidPlatform(this));
        String uri = getPreferences(0).getString("tree", null);
        if (uri != null) root = DocumentFile.fromTreeUri(this, Uri.parse(uri));
        showActivation();
    }
    int white = Color.WHITE;
    int accent() { return Color.WHITE; }

    int muted = 0xffadb0b8;
    GradientDrawable panel(boolean glow) {
        GradientDrawable d = new GradientDrawable(GradientDrawable.Orientation.TL_BR,
            new int[]{0xff1b1d21, 0xff050506, 0xff111216});
        d.setCornerRadius(22);
        d.setStroke(glow ? 2 : 1, glow ? accent() : 0xff55565a);
        return d;
    }
    TextView label(String value, int size, int color) {
        TextView t = new TextView(this); t.setText(value); t.setTextSize(size);
        t.setTextColor(color); t.setGravity(Gravity.CENTER_VERTICAL);
        return t;
    }
    int dp(float n) { return (int)(getResources().getDisplayMetrics().density*n+0.5f); }
    GradientDrawable bg(int color, int stroke, int radius) {
        GradientDrawable d=new GradientDrawable(); d.setColor(color); d.setCornerRadius(dp(radius));
        if(stroke!=0) d.setStroke(dp(1),stroke); return d;
    }
    void init(String title) {
        ScrollView scroll=new ScrollView(this); scroll.setFillViewport(true); scroll.setBackgroundColor(0xff050506);
        body=new LinearLayout(this); body.setOrientation(1); body.setPadding(dp(18),dp(22),dp(18),dp(28));
        scroll.addView(body); setContentView(scroll);
        LinearLayout header=new LinearLayout(this); header.setGravity(Gravity.CENTER_VERTICAL);
        if(!title.equals("HUNTARES TOOL")) {
            TextView back=label("‹",32,Color.WHITE); back.setPadding(0,0,dp(16),0);
            header.addView(back); back.setOnClickListener(v->showHome());
        }
        TextView h=label(title,22,Color.WHITE); h.setTypeface(null,Typeface.BOLD);
        header.addView(h,new LinearLayout.LayoutParams(0,dp(52),1));
        TextView gear=label("⚙",25,accent()); gear.setGravity(Gravity.CENTER);
        gear.setBackground(bg(0xff18181b,0xff343438,12)); header.addView(gear,new LinearLayout.LayoutParams(dp(45),dp(45)));
        gear.setOnClickListener(v->showSettings()); body.addView(header);
        if(title.equals("HUNTARES TOOL")) {
            ImageView avatar=new ImageView(this); avatar.setImageResource(R.mipmap.ic_launcher);
            avatar.setScaleType(ImageView.ScaleType.FIT_CENTER);
            LinearLayout.LayoutParams ip=new LinearLayout.LayoutParams(dp(174),dp(174));
            ip.gravity=Gravity.CENTER_HORIZONTAL; ip.setMargins(0,dp(16),0,dp(5)); body.addView(avatar,ip);
            TextView tag=label("HUNTARES TOOL",25,Color.WHITE);tag.setGravity(Gravity.CENTER);tag.setTypeface(null,Typeface.BOLD);body.addView(tag);
            TextView subtitle=label("Профессиональный PAK / LUA инструмент",12,muted);subtitle.setGravity(Gravity.CENTER);
            subtitle.setPadding(0,dp(5),0,dp(14));body.addView(subtitle);
        }
        status=label("",13,muted);status.setPadding(dp(8),dp(12),dp(8),dp(12));body.addView(status);
    }
    void footer() {
        TextView f=label("♛  HUNTARES TOOL",16,Color.WHITE);f.setGravity(Gravity.CENTER);
        f.setPadding(0,dp(28),0,dp(16));body.addView(f);
    }
    void button(String name, Runnable action) {
        LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);
        card.setPadding(dp(17),dp(15),dp(15),dp(15));card.setBackground(panel(false));
        String icon="◇";String labelText=name;
        if(name.contains("PAK")) icon="⬡";
        else if(name.contains("LUA")||name.contains("Lua")) icon="{ }";
        else if(name.contains("Настрой")) icon="⚙";
        else if(name.contains("Лиценз")||name.contains("Админ")) icon="♛";
        else if(name.contains("папк")||name.contains("доступ")) icon="▣";
        TextView symbol=label(icon,21,accent());symbol.setGravity(Gravity.CENTER);
        card.addView(symbol,new LinearLayout.LayoutParams(dp(43),dp(43)));
        TextView text=label(labelText,16,Color.WHITE);text.setTypeface(null,Typeface.BOLD);
        text.setPadding(dp(8),0,0,0);card.addView(text,new LinearLayout.LayoutParams(0,-2,1));
        TextView arrow=label("›",26,0xffbbbbbb);card.addView(arrow);
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,dp(5),0,dp(6));body.addView(card,lp);
        card.setOnClickListener(v->action.run());
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
        if(sessionKey.isEmpty()){showActivation();return;}
        init("HUNTARES TOOL");
        if(root==null) {
            msg("Для работы выберите папку, например Documents");
            button("Разрешить доступ / выбрать папку", ()->pickFolder());
        } else {
            status.setText("●  Рабочая папка подключена");status.setTextColor(0xff65dca1);
        }
        section("ИНСТРУМЕНТЫ");
        LinearLayout grid=new LinearLayout(this);grid.setOrientation(1);grid.setPadding(dp(8),dp(8),dp(8),dp(8));grid.setBackground(panel(true));body.addView(grid);
        String[][] names={{"PAK UNPACK","PAK REPACK"},{"LUA UNPACK","LUA REPACK"}};
        for(int row=0;row<2;row++){
            LinearLayout line=new LinearLayout(this);grid.addView(line);
            for(int col=0;col<2;col++){
                final int r=row,c=col;
                TextView tile=label(names[row][col],14,white);tile.setGravity(Gravity.CENTER);tile.setTypeface(null,Typeface.BOLD);tile.setBackground(bg(0xff17181b,0xff5b5b61,14));
                LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,dp(105),1);lp.setMargins(dp(4),dp(4),dp(4),dp(4));line.addView(tile,lp);
                tile.setOnClickListener(v->{if(r==0)showPak();else showLua();});
            }
        }
        section("ПРИЛОЖЕНИЕ");
        button("Настройки",()->showSettings());
        if(admin)button("♛  Админ-панель",()->showAdmin());
        button("Открыть рабочую папку",()->{if(root==null)pickFolder();else {
            Intent i=new Intent(Intent.ACTION_VIEW);i.setDataAndType(root.getUri(),"vnd.android.document/directory");
            i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            try{startActivity(i);}catch(Exception e){msg("Откройте папку через файловый менеджер");}
        }});
        footer();
    }
    void pickFolder() {
        Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE);
        i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION|Intent.FLAG_GRANT_WRITE_URI_PERMISSION|Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        startActivityForResult(i,PICK_TREE);
    }
    void section(String text) {
        TextView v=label(text,12,muted);v.setTypeface(null,Typeface.BOLD);
        v.setPadding(dp(7),dp(19),0,dp(7));body.addView(v);
    }
    void showSettings() {
        init("Настройки");status.setText("Оформление: чёрно-белое, фиксированное");
        section("ОБЩИЕ");
        settingToggle("Показывать полное время","full_time",true);
        settingToggle("Сохранять последнюю директорию","last_dir",true);
        settingToggle("Звук действий","sounds",false);
        button("Выход из аккаунта",()->{sessionKey="";admin=false;showActivation();});
        button("О приложении",()->new AlertDialog.Builder(this).setTitle("HUNTARES TOOL")
            .setMessage("PAK / LUA инструмент. Поддержка файлов зависит от формата.")
            .setPositiveButton("Закрыть",null).show());
        footer();
    }
    void settingToggle(String name,String key,boolean def) {
        Switch sw=new Switch(this);sw.setText(name);sw.setTextSize(15);sw.setTextColor(Color.WHITE);
        sw.setChecked(getPreferences(0).getBoolean(key,def));sw.setPadding(dp(12),dp(15),dp(12),dp(15));
        sw.setBackground(panel(false));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,dp(4),0,dp(5));body.addView(sw,lp);
        sw.setOnCheckedChangeListener((v,checked)->getPreferences(0).edit().putBoolean(key,checked).apply());
    }
    void showAdmin() {
        if(!admin){showHome();return;}
        init("Админ-панель");status.setText("Офлайн-ключи • без сервера");
        button("Создать HWID-ключ",()->showCreateKey("hwid"));
        button("Создать универсальный ключ",()->showCreateKey("universal"));
        button("Информация о ключах",()->showKeys());footer();
    }
    void showCreateKey(String type) {
        if(!admin){showActivation();return;}
        init(type.equals("hwid")?"Создать HWID-ключ":"Создать универсальный ключ");
        section("НАЗВАНИЕ КЛЮЧА");
        EditText name=new EditText(this);name.setSingleLine(true);name.setHint("HUNTARES-VIP");name.setTextColor(white);name.setHintTextColor(muted);body.addView(name);
        EditText device=new EditText(this);
        if(type.equals("hwid")){
            section("КОД УСТРОЙСТВА ПОЛЬЗОВАТЕЛЯ");
            device.setSingleLine(true);device.setHint("Пользователь копирует код на экране входа");device.setTextColor(white);device.setHintTextColor(muted);body.addView(device);
        }
        Switch unlimited=new Switch(this);unlimited.setText("Бессрочно");unlimited.setTextColor(white);unlimited.setChecked(true);body.addView(unlimited);
        section("СРОК В ДНЯХ");
        EditText days=new EditText(this);days.setInputType(2);days.setText("7");days.setTextColor(white);days.setVisibility(View.GONE);body.addView(days);
        unlimited.setOnCheckedChangeListener((v,on)->days.setVisibility(on?View.GONE:View.VISIBLE));
        button("Создать и скопировать ключ",()->{
            try {
                String title=name.getText().toString().trim();if(title.isEmpty())throw new Exception("Введите название");
                String id=device.getText().toString().trim();if(type.equals("hwid") && !id.matches("[a-fA-F0-9]{32}"))throw new Exception("Нужен 32-значный код устройства");
                long exp=0;
                if(!unlimited.isChecked()){
                    long d=Long.parseLong(days.getText().toString().trim());
                    if(d<1 || d>36500)throw new Exception("Срок: 1–36500 дней");
                    exp=System.currentTimeMillis()+d*86400000L;
                }
                JSONObject data=new JSONObject();data.put("name",title);data.put("type",type);data.put("device",id);data.put("exp",exp);data.put("created",System.currentTimeMillis());
                String encoded=b64(data.toString().getBytes("UTF-8"));
                String token="HT1."+encoded+"."+sign(encoded);
                org.json.JSONArray all=storedKeys();all.put(new JSONObject().put("token",token).put("name",title).put("type",type).put("device",id).put("exp",exp));
                getPreferences(0).edit().putString(STORE,all.toString()).apply();
                copyText(token);
                new AlertDialog.Builder(this).setTitle("Ключ создан").setMessage("Ключ скопирован. Передайте его пользователю.\n\n"+title+"\n"+token).setPositiveButton("Готово",null).show();
            }catch(Exception e){msg("Ошибка: "+e.getMessage());}
        });footer();
    }
    JSONArray storedKeys(){try{return new JSONArray(getPreferences(0).getString(STORE,"[]"));}catch(Exception e){return new JSONArray();}}
    void showKeys(){
        if(!admin){showActivation();return;}
        init("Информация о ключах");
        msg("Список хранится только на этом телефоне. Удалённые активации недоступны.");
        JSONArray all=storedKeys();
        for(int i=0;i<all.length();i++){
            JSONObject item=all.optJSONObject(i);if(item==null)continue;
            String token=item.optString("token");
            button(item.optString("name")+" • "+item.optString("type"),()->showKeyDetails(token));
        }
        if(all.length()==0)section("КЛЮЧЕЙ ПОКА НЕТ");
        footer();
    }
    void showKeyDetails(String token){
        if(!admin){showActivation();return;}
        init("Данные ключа");
        try {
            JSONObject data=decodeLicense(token);
            section("НАЗВАНИЕ: "+data.optString("name"));
            section("ТИП: "+data.optString("type"));
            section("УСТРОЙСТВО (ЕСЛИ HWID): "+data.optString("device"));
            long exp=data.optLong("exp");section("СРОК: "+(exp==0?"Бессрочно":new java.text.SimpleDateFormat("dd.MM.yyyy",java.util.Locale.getDefault()).format(new Date(exp))));
        }catch(Exception e){section("Состояние: "+e.getMessage());}
        button("Скопировать ключ",()->copyText(token));
        section("Без сервера нельзя узнать модель телефона пользователя или отозвать уже выданный ключ.");
        footer();
    }
    @Override protected void onActivityResult(int req, int result, Intent data) {
        super.onActivityResult(req, result, data);
        if (req == PICK_TREE && result == RESULT_OK && data != null) {
            Uri u = data.getData();
            getContentResolver().takePersistableUriPermission(u, Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            root = DocumentFile.fromTreeUri(this, u);
            getPreferences(0).edit().putString("tree", u.toString()).apply();
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
