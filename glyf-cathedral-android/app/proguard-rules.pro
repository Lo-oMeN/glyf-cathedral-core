# ProGuard rules for L∞M∆N Cathedral

# Keep the 96-byte LatticeState structure
-keep class com.glyf.cathedral.visualizer.LatticeState { *; }

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep ViewModel constructors
-keepclassmembers class * extends androidx.lifecycle.ViewModel {
    <init>(...);
}

# Keep Compose-related classes
-keep class androidx.compose.** { *; }
-keep class com.glyf.cathedral.ui.theme.** { *; }

# Optimization rules
-optimizationpasses 5
-dontusemixedcaseclassnames
-dontskipnonpubliclibraryclasses
-dontpreverify
-verbose

# Preserve annotations
-keepattributes *Annotation*
-keepattributes Signature
-keepattributes Exceptions
-keepattributes InnerClasses
-keepattributes EnclosingMethod

# Remove logging in release
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
    public static *** w(...);
    public static *** e(...);
}
