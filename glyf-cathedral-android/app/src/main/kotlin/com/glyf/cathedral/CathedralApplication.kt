package com.glyf.cathedral

import android.app.Application
import androidx.work.Configuration
import com.glyf.cathedral.cron.LatticeWorkerFactory

/**
 * Application class for GLYF Cathedral
 */
class CathedralApplication : Application(), Configuration.Provider {
    
    override fun getWorkManagerConfiguration(): Configuration {
        return Configuration.Builder()
            .setWorkerFactory(LatticeWorkerFactory())
            .build()
    }
}
