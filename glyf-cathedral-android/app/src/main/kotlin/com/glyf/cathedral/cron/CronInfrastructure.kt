package com.glyf.cathedral.cron

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.work.*

/**
 * Boot receiver to reschedule cron work after reboot
 */
class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            // Reschedule cron work
            LatticeCronWorker.schedule(context)
        }
    }
}

/**
 * Custom worker factory for dependency injection
 */
class LatticeWorkerFactory : WorkerFactory() {
    override fun createWorker(
        context: Context,
        workerClassName: String,
        workerParameters: WorkerParameters
    ): ListenableWorker? {
        return when (workerClassName) {
            LatticeCronWorker::class.java.name ->
                LatticeCronWorker(context, workerParameters)
            LatticeImmediateWorker::class.java.name ->
                LatticeImmediateWorker(context, workerParameters)
            LatticeStressTestWorker::class.java.name ->
                LatticeStressTestWorker(context, workerParameters)
            else -> null
        }
    }
}
