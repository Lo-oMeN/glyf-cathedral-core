package com.glyf.cathedral.core

import kotlin.math.abs
import kotlin.math.pow

/**
 * φ⁷ Geometric Constants
 */
object PhiConstants {
    const val PHI = 1.618033988749895
    const val PHI_INV = 0.6180339887498948
    const val PHI_2 = 2.618033988749895
    const val PHI_3 = 4.23606797749979
    const val PHI_4 = 6.854101966249685
    const val PHI_7 = 29.034441853748633
    const val GOLDEN_ANGLE_DEG = 137.50776405003785
    const val GOLDEN_ANGLE_RAD = 2.39996322972865332
    
    // Fibonacci sequence mod 89 for cron intervals
    val FIB_MOD_89 = listOf(0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 % 89, 144 % 89, 233 % 89)
    
    /**
     * Compute φ^k with saturation
     */
    fun phiPow(k: Int): Double = when (k) {
        0 -> 1.0
        1 -> PHI
        2 -> PHI_2
        3 -> PHI_3
        4 -> PHI_4
        7 -> PHI_7
        -1 -> PHI_INV
        else -> PHI.pow(k)
    }
}

/**
 * Axial coordinates for hexagonal grid
 * Constraint: q + r + s = 0
 */
data class AxialCoord(
    val q: Int,
    val r: Int,
    val s: Int
) {
    init {
        require(q + r + s == 0) { "Axial coordinates must sum to zero: ($q, $r, $s)" }
    }
    
    companion object {
        val ORIGIN = AxialCoord(0, 0, 0)
        
        fun fromQr(q: Int, r: Int) = AxialCoord(q, r, -q - r)
    }
    
    /**
     * Hex distance from origin
     */
    fun distance(): Int = (abs(q) + abs(r) + abs(s)) / 2
    
    /**
     * Hex distance to another coordinate
     */
    fun distanceTo(other: AxialCoord): Int {
        val dq = q - other.q
        val dr = r - other.r
        val ds = s - other.s
        return (abs(dq) + abs(dr) + abs(ds)) / 2
    }
    
    /**
     * Convert to pixel coordinates (pointy-topped hex)
     */
    fun toPixel(size: Float): Pair<Float, Float> {
        val x = size * (sqrt3 * q + sqrt3 / 2 * r)
        val y = size * (3.0 / 2 * r)
        return Pair(x.toFloat(), y.toFloat())
    }
    
    /**
     * Neighbors in hex grid (6 directions)
     */
    fun neighbors(): List<AxialCoord> = listOf(
        AxialCoord(q + 1, r, s - 1),
        AxialCoord(q + 1, r - 1, s),
        AxialCoord(q, r - 1, s + 1),
        AxialCoord(q - 1, r, s + 1),
        AxialCoord(q - 1, r + 1, s),
        AxialCoord(q, r + 1, s - 1)
    )
    
    private val sqrt3 = 1.7320508075688772
}

/**
 * Ternary spin states
 */
enum class TernarySpin(val value: Byte) {
    NEGATIVE(-1),
    ZERO(0),
    POSITIVE(1);
    
    companion object {
        fun fromValue(v: Byte): TernarySpin = when (v) {
            (-1).toByte() -> NEGATIVE
            0.toByte() -> ZERO
            1.toByte() -> POSITIVE
            else -> ZERO
        }
    }
}

/**
 * HexTile — persistence tile for φ⁷ lattice
 * Android adaptation (64-byte alignment not required)
 */
data class HexTile(
    val coord: AxialCoord,
    val spin: TernarySpin = TernarySpin.ZERO,
    val phiMag: Float = 0.0f,
    val chiralHash: Long = 0L,
    val timestamp: Long = System.nanoTime(),
    val evictionPriority: Byte = 128,
    val priorityTiebreaker: Byte = 0
) {
    companion object {
        const val MAX_PRIORITY: Byte = 255
        const val MIN_PRIORITY: Byte = 0
    }
    
    /**
     * Compute distance from origin
     */
    fun distance(): Int = coord.distance()
    
    /**
     * Scale phiMag by φ^k with saturation
     */
    fun scalePhi(k: Int): HexTile {
        val newMag = (phiMag * PhiConstants.phiPow(k)).toFloat()
        val saturated = when {
            newMag < 1.17549435e-38f -> 0.0f // f32 min normal
            newMag > PhiConstants.PHI_7.toFloat() -> PhiConstants.PHI_7.toFloat()
            else -> newMag
        }
        return copy(phiMag = saturated)
    }
    
    /**
     * Encode chiral hash from 3 spin populations
     */
    fun withChiralHash(spinNeg: Int, spinZero: Int, spinPos: Int): HexTile {
        val mask0 = (spinNeg and 0x1FFFFF).toLong()
        val mask1 = ((spinZero and 0x1FFFFF).toLong() shl 21)
        val mask2 = ((spinPos and 0x3FFFFF).toLong() shl 42)
        return copy(chiralHash = mask0 or mask1 or mask2)
    }
    
    /**
     * Decode chiral hash to 3 spin populations
     */
    fun decodeChiral(): Triple<Int, Int, Int> {
        val spinNeg = (chiralHash and 0x1FFFFF).toInt()
        val spinZero = ((chiralHash shr 21) and 0x1FFFFF).toInt()
        val spinPos = ((chiralHash shr 42) and 0x3FFFFF).toInt()
        return Triple(spinNeg, spinZero, spinPos)
    }
    
    /**
     * Update eviction priority based on distance
     */
    fun withPriority(maxRadius: Int): HexTile {
        val dist = distance()
        val maxR = maxRadius.coerceAtLeast(1)
        val priority = ((dist * 255) / maxR).coerceIn(0, 255).toByte()
        val tiebreaker = ((timestamp shr 32).toInt() xor dist).toByte()
        return copy(
            evictionPriority = priority,
            priorityTiebreaker = tiebreaker
        )
    }
    
    /**
     * Check if this tile should be evicted before other
     */
    fun shouldEvictBefore(other: HexTile): Boolean {
        return if (evictionPriority != other.evictionPriority) {
            evictionPriority > other.evictionPriority // Higher = evict first
        } else {
            priorityTiebreaker > other.priorityTiebreaker
        }
    }
}

/**
 * Cron tile for scheduled persistence
 */
data class CronTile(
    val intervalFib: Byte, // τ mod 89
    val lastTick: Long = 0, // Unix seconds
    val voltageThreshold: Float = PhiConstants.PHI_INV.toFloat(),
    val anchorCoord: AxialCoord
) {
    companion object {
        const val DEFAULT_INTERVAL: Byte = 13
    }
    
    /**
     * Get interval in seconds
     */
    fun intervalSeconds(): Long {
        val fib = PhiConstants.FIB_MOD_89.getOrElse(intervalFib.toInt()) { 13 }
        return fib * 60L
    }
    
    /**
     * Check if cron should fire
     */
    fun shouldFire(nowSecs: Long, currentVoltage: Float): Boolean {
        val elapsed = nowSecs - lastTick
        return elapsed >= intervalSeconds() && currentVoltage >= voltageThreshold
    }
    
    /**
     * Record a tick
     */
    fun tick(nowSecs: Long): CronTile = copy(lastTick = nowSecs)
    
    /**
     * Time until next fire (saturating)
     */
    fun timeUntilFire(nowSecs: Long): Long {
        val interval = intervalSeconds()
        val elapsed = nowSecs - lastTick
        return (interval - elapsed).coerceAtLeast(0)
    }
}

/**
 * Lattice state container
 */
data class LatticeState(
    val version: Int = 0x00000702,
    val hotTiles: List<HexTile> = emptyList(),
    val cronTiles: List<CronTile> = emptyList(),
    val explorerVoltage: Float = PhiConstants.PHI_7.toFloat(),
    val junctionThreshold: Byte = (-3).toByte(),
    val radialRadius: Short = 21,
    val cronFibBase: Byte = 13
) {
    companion object {
        const val MAX_HOT_TILES = 1024
        const val MAX_CRON_TILES = 64
    }
    
    val hotCount: Int get() = hotTiles.size
    val cronCount: Int get() = cronTiles.size
    val loadFactor: Float get() = hotCount.toFloat() / MAX_HOT_TILES
    
    /**
     * Insert tile, evicting if necessary
     */
    fun insertTile(tile: HexTile): Pair<LatticeState, HexTile?> {
        return if (hotCount >= MAX_HOT_TILES) {
            // Evict outermost
            val sorted = hotTiles.sortedWith(compareByDescending { it.evictionPriority })
            val evicted = sorted.firstOrNull()
            val remaining = sorted.drop(1).take(MAX_HOT_TILES - 1)
            val newTiles = remaining + tile.withPriority(radialRadius.toInt())
            Pair(copy(hotTiles = newTiles), evicted)
        } else {
            val newTiles = hotTiles + tile.withPriority(radialRadius.toInt())
            Pair(copy(hotTiles = newTiles), null)
        }
    }
    
    /**
     * Find tile by coordinate
     */
    fun findTile(coord: AxialCoord): HexTile? = hotTiles.find { it.coord == coord }
    
    /**
     * Query tiles within radial distance
     */
    fun queryRadial(center: AxialCoord, radius: Int): List<HexTile> {
        return hotTiles.filter { it.coord.distanceTo(center) <= radius }
    }
    
    /**
     * Process cron ticks
     */
    fun processCrons(nowSecs: Long): Pair<LatticeState, Int> {
        var fired = 0
        val updatedCrons = cronTiles.map { cron ->
            if (cron.shouldFire(nowSecs, explorerVoltage)) {
                fired++
                cron.tick(nowSecs)
            } else {
                cron
            }
        }
        return Pair(copy(cronTiles = updatedCrons), fired)
    }
    
    /**
     * Scale explorer voltage by φ^k
     */
    fun scaleVoltage(k: Int): LatticeState {
        val newVoltage = (explorerVoltage * PhiConstants.phiPow(k)).toFloat()
        val saturated = when {
            newVoltage < 1.17549435e-38f -> 0.0f
            newVoltage > PhiConstants.PHI_7.toFloat() -> PhiConstants.PHI_7.toFloat()
            else -> newVoltage
        }
        return copy(explorerVoltage = saturated)
    }
}
