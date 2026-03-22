package com.glyf.cathedral.data

import android.content.Context
import androidx.room.Room
import com.glyf.cathedral.core.*
import kotlinx.coroutines.flow.*

/**
 * Repository for lattice operations
 * Bridges core models with Room persistence
 */
class LatticeRepository(context: Context) {
    
    private val db = Room.databaseBuilder(
        context,
        LatticeDatabase::class.java,
        "glyf_lattice"
    ).build()
    
    private val hexDao = db.hexTileDao()
    private val cronDao = db.cronTileDao()
    private val metaDao = db.latticeMetaDao()
    
    // ═══════════════════════════════════════════════════════════════════════
    // HexTile Operations
    // ═══════════════════════════════════════════════════════════════════════
    
    suspend fun getAllTiles(): List<HexTile> {
        return hexDao.getAllOrdered().map { it.toTile() }
    }
    
    suspend fun getTile(coord: AxialCoord): HexTile? {
        return hexDao.getByCoord(coord.q, coord.r, coord.s)?.toTile()
    }
    
    suspend fun insertTile(tile: HexTile) {
        hexDao.insert(HexTileEntity.fromTile(tile))
    }
    
    suspend fun insertTiles(tiles: List<HexTile>) {
        hexDao.insertAll(tiles.map { HexTileEntity.fromTile(it) })
    }
    
    suspend fun deleteTile(coord: AxialCoord) {
        hexDao.deleteById("${coord.q},${coord.r},${coord.s}")
    }
    
    suspend fun evictOutermost(count: Int) {
        hexDao.deleteOutermost(count)
    }
    
    suspend fun getTileCount(): Int = hexDao.count()
    
    fun getTilesFlow(): Flow<List<HexTile>> = flow {
        while (true) {
            emit(getAllTiles())
            kotlinx.coroutines.delay(1000) // Refresh every second
        }
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // CronTile Operations
    // ═══════════════════════════════════════════════════════════════════════
    
    suspend fun getAllCrons(): List<CronTile> {
        return cronDao.getAll().map { it.toTile() }
    }
    
    suspend fun getCron(anchor: AxialCoord): CronTile? {
        return cronDao.getByAnchor(anchor.q, anchor.r, anchor.s)?.toTile()
    }
    
    suspend fun insertCron(cron: CronTile) {
        cronDao.insert(CronTileEntity.fromTile(cron))
    }
    
    suspend fun deleteCron(anchor: AxialCoord) {
        cronDao.deleteById("${anchor.q},${anchor.r},${anchor.s}")
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // Lattice State Operations
    // ═══════════════════════════════════════════════════════════════════════
    
    suspend fun getLatticeState(): LatticeState {
        val meta = metaDao.get()
        val tiles = getAllTiles()
        val crons = getAllCrons()
        
        return if (meta != null) {
            LatticeState(
                version = meta.version,
                hotTiles = tiles,
                cronTiles = crons,
                explorerVoltage = meta.explorerVoltage,
                junctionThreshold = meta.junctionThreshold,
                radialRadius = meta.radialRadius,
                cronFibBase = meta.cronFibBase
            )
        } else {
            LatticeState() // Default
        }
    }
    
    suspend fun saveLatticeState(state: LatticeState) {
        // Save metadata
        metaDao.set(
            LatticeMetaEntity(
                version = state.version,
                explorerVoltage = state.explorerVoltage,
                junctionThreshold = state.junctionThreshold,
                radialRadius = state.radialRadius,
                cronFibBase = state.cronFibBase,
                lastUpdated = System.currentTimeMillis()
            )
        )
        
        // Note: Tiles and crons are saved individually to avoid full wipe
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // High-Level Operations
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * Insert tile with auto-eviction if at capacity
     */
    suspend fun insertWithEviction(tile: HexTile, maxTiles: Int = 1024): HexTile? {
        val currentCount = getTileCount()
        
        return if (currentCount >= maxTiles) {
            // Evict outermost tile
            val allTiles = getAllTiles()
            if (allTiles.isNotEmpty()) {
                val toEvict = allTiles.maxByOrNull { it.evictionPriority.toInt() }
                toEvict?.let {
                    deleteTile(it.coord)
                    insertTile(tile)
                    it // Return evicted tile
                }
            } else {
                insertTile(tile)
                null
            }
        } else {
            insertTile(tile)
            null
        }
    }
    
    /**
     * Query tiles within radial distance
     */
    suspend fun queryRadial(center: AxialCoord, radius: Int): List<HexTile> {
        val allTiles = getAllTiles()
        return allTiles.filter { it.coord.distanceTo(center) <= radius }
    }
    
    /**
     * Process all cron triggers
     */
    suspend fun processCrons(nowSecs: Long = System.currentTimeMillis() / 1000): Int {
        val state = getLatticeState()
        val (newState, fired) = state.processCrons(nowSecs)
        
        // Save updated crons
        newState.cronTiles.forEach { insertCron(it) }
        
        return fired
    }
    
    /**
     * Clear all data
     */
    suspend fun clearAll() {
        hexDao.deleteAll()
        // Crons and meta are preserved? Or clear them too?
        // For now, keep crons as they're scheduled tasks
    }
}
