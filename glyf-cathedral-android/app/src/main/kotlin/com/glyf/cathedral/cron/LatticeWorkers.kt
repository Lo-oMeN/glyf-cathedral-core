package com.glyf.cathedral.cron

import android.content.Context
import androidx.work.*
import com.glyf.cathedral.core.PhiConstants
import com.glyf.cathedral.data.LatticeRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.concurrent.TimeUnit

/**
 * WorkManager cron worker for φ⁷ lattice persistence
 * Fibonacci-timed execution with voltage threshold checks
 */
class LatticeCronWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    
    companion object {
        const val WORK_NAME = "glyf_lattice_cron"
        const val KEY_INTERVAL_INDEX = "interval_index"
        const val KEY_FIRE_COUNT = "fire_count"
        
        /**
         * Schedule the cron worker with Fibonacci intervals
         */
        fun schedule(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiresBatteryNotLow(true)
                .build()
            
            // Initial trigger after 13 minutes (default Fibonacci interval)
            val initialDelay = PhiConstants.FIB_MOD_89[13] * 60L
            
            val workRequest = PeriodicWorkRequestBuilder<LatticeCronWorker>(
                initialDelay, TimeUnit.SECONDS
            )
                .setConstraints(constraints)
                .setBackoffCriteria(
                    BackoffPolicy.EXPONENTIAL,
                    WorkRequest.MIN_BACKOFF_MILLIS,
                    TimeUnit.MILLISECONDS
                )
                .addTag(WORK_NAME)
                .build()
            
            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                WORK_NAME,
                ExistingPeriodicWorkPolicy.KEEP,
                workRequest
            )
        }
        
        /**
         * Cancel scheduled work
         */
        fun cancel(context: Context) {
            WorkManager.getInstance(context).cancelUniqueWork(WORK_NAME)
        }
    }
    
    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        try {
            val repository = LatticeRepository(applicationContext)
            val fired = repository.processCrons()
            
            if (fired > 0) {
                // Trigger CBOR emission if crons fired
                // TODO: Integrate with Rosetta bridge
                emitRosettaInquiry()
            }
            
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
    
    private fun emitRosettaInquiry() {
        // Placeholder for CBOR emission
        // Will be implemented when Rosetta bridge is ready
    }
}

/**
 * One-time worker for immediate lattice operations
 */
class LatticeImmediateWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    
    companion object {
        const val KEY_OPERATION = "operation"
        const val OP_EVICT = "evict"
        const val OP_SCALE_VOLTAGE = "scale_voltage"
        const val KEY_PARAM = "param"
        
        fun enqueueEvict(context: Context, count: Int) {
            val workRequest = OneTimeWorkRequestBuilder<LatticeImmediateWorker>()
                .setInputData(workDataOf(
                    KEY_OPERATION to OP_EVICT,
                    KEY_PARAM to count
                ))
                .build()
            
            WorkManager.getInstance(context).enqueue(workRequest)
        }
        
        fun enqueueScaleVoltage(context: Context, k: Int) {
            val workRequest = OneTimeWorkRequestBuilder<LatticeImmediateWorker>()
                .setInputData(workDataOf(
                    KEY_OPERATION to OP_SCALE_VOLTAGE,
                    KEY_PARAM to k
                ))
                .build()
            
            WorkManager.getInstance(context).enqueue(workRequest)
        }
    }
    
    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val repository = LatticeRepository(applicationContext)
        val operation = inputData.getString(KEY_OPERATION)
        
        when (operation) {
            OP_EVICT -> {
                val count = inputData.getInt(KEY_PARAM, 1)
                repository.evictOutermost(count)
            }
            OP_SCALE_VOLTAGE -> {
                val k = inputData.getInt(KEY_PARAM, 0)
                val state = repository.getLatticeState()
                val newState = state.scaleVoltage(k)
                repository.saveLatticeState(newState)
            }
        }
        
        Result.success()
    }
}

/**
 * Worker for 72-hour stress test simulation
 */
class LatticeStressTestWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    
    companion object {
        const val WORK_NAME = "glyf_stress_test"
        
        fun start(context: Context) {
            val workRequest = OneTimeWorkRequestBuilder<LatticeStressTestWorker>()
                .setInitialDelay(0, TimeUnit.SECONDS)
                .build()
            
            WorkManager.getInstance(context).enqueueUniqueWork(
                WORK_NAME,
                ExistingWorkPolicy.REPLACE,
                workRequest
            )
        }
    }
    
    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val repository = LatticeRepository(applicationContext)
        val random = java.util.Random()
        
        // Run for 72 hours of simulation (or until stopped)
        val iterations = 72 * 60 * 60 // 72 hours in seconds
        
        repeat(iterations) { i ->
            // Random mutation: insert or evict
            if (random.nextBoolean()) {
                val q = random.nextInt(20) - 10
                val r = random.nextInt(20) - 10
                val tile = HexTile(
                    coord = AxialCoord.fromQr(q, r),
                    spin = TernarySpin.values()[random.nextInt(3)],
                    phiMag = random.nextFloat() * PhiConstants.PHI_7.toFloat()
                )
                repository.insertWithEviction(tile)
            } else {
                repository.evictOutermost(1)
            }
            
            // Every 13 iterations, process crons
            if (i % 13 == 0) {
                repository.processCrons()
            }
            
            // Report progress every hour
            if (i % 3600 == 0) {
                val hours = i / 3600
                setProgress(workDataOf("hours" to hours))
            }
            
            // Small delay to not overwhelm the system
            kotlinx.coroutines.delay(1000) // 1 second per iteration
        }
        
        Result.success()
    }
}
