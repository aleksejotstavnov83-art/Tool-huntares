# Keep Android entrypoint and Chaquopy integration intact.
-keep class com.huntares.tool.MainActivity { *; }
-keep class com.chaquo.python.** { *; }
-dontwarn com.chaquo.python.**
