package com.glyf.cathedral

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class GlyfApplication : Application() {
    
    override fun onCreate() {
        super.onCreate()
        // Initialize cathedral state
    }
}
