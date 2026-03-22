# ProGuard rules for GLYF Cathedral

# Keep model classes for serialization
-keep class com.glyf.cathedral.core.** { *; }
-keep class com.glyf.cathedral.data.** { *; }
-keep class com.glyf.cathedral.rosetta.** { *; }

# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-dontwarn androidx.room.paging.**

# Ktor
-keep class io.ktor.** { *; }
-dontwarn io.ktor.**

# Kotlin serialization
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt
-keepclassmembers class kotlinx.serialization.json.** { *; }

# WorkManager
-keep class * extends androidx.work.Worker
-keep class * extends androidx.work.CoroutineWorker

# General
-keepattributes Signature
-keepattributes Exceptions
-keepattributes LineNumberTable
-keepattributes SourceFile
