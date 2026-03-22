package com.glyf.cathedral.data

import androidx.room.*
import com.glyf.cathedral.core.*

/**
 * Room Entity for HexTile
 */
@Entity(tableName = "hex_tiles")
data class HexTileEntity(
    @PrimaryKey
    val id: String, // "q,r,s" format
    
    val q: Int,
    val r: Int,
    val s: Int,
    
    val spinValue: Byte,
    val phiMag: Float,
    val chiralHash: Long,
    val timestamp: Long,
    val evictionPriority: Byte,
    val priorityTiebreaker: Byte
) {
    companion object {
        fun fromTile(tile: HexTile): HexTileEntity {
            val coord = tile.coord
            return HexTileEntity(
                id = "${coord.q},${coord.r},${coord.s}",
                q = coord.q,
                r = coord.r,
                s = coord.s,
                spinValue = tile.spin.value,
                phiMag = tile.phiMag,
                chiralHash = tile.chiralHash,
                timestamp = tile.timestamp,
                evictionPriority = tile.evictionPriority,
                priorityTiebreaker = tile.priorityTiebreaker
            )
        }
    }
    
    fun toTile(): HexTile = HexTile(
        coord = AxialCoord(q, r, s),
        spin = TernarySpin.fromValue(spinValue),
        phiMag = phiMag,
        chiralHash = chiralHash,
        timestamp = timestamp,
        evictionPriority = evictionPriority,
        priorityTiebreaker = priorityTiebreaker
    )
}

/**
 * Room Entity for CronTile
 */
@Entity(tableName = "cron_tiles")
data class CronTileEntity(
    @PrimaryKey
    val id: String, // "q,r,s" anchor format
    
    val intervalFib: Byte,
    val lastTick: Long,
    val voltageThreshold: Float,
    
    val anchorQ: Int,
    val anchorR: Int,
    val anchorS: Int
) {
    companion object {
        fun fromTile(tile: CronTile): CronTileEntity {
            val coord = tile.anchorCoord
            return CronTileEntity(
                id = "${coord.q},${coord.r},${coord.s}",
                intervalFib = tile.intervalFib,
                lastTick = tile.lastTick,
                voltageThreshold = tile.voltageThreshold,
                anchorQ = coord.q,
                anchorR = coord.r,
                anchorS = coord.s
            )
        }
    }
    
    fun toTile(): CronTile = CronTile(
        intervalFib = intervalFib,
        lastTick = lastTick,
        voltageThreshold = voltageThreshold,
        anchorCoord = AxialCoord(anchorQ, anchorR, anchorS)
    )
}

/**
 * Room Entity for lattice metadata
 */
@Entity(tableName = "lattice_meta")
data class LatticeMetaEntity(
    @PrimaryKey
    val id: Int = 1, // Singleton
    
    val version: Int,
    val explorerVoltage: Float,
    val junctionThreshold: Byte,
    val radialRadius: Short,
    val cronFibBase: Byte,
    val lastUpdated: Long
)

@Dao
interface HexTileDao {
    @Query("SELECT * FROM hex_tiles ORDER BY evictionPriority DESC, priorityTiebreaker DESC")
    suspend fun getAllOrdered(): List<HexTileEntity>
    
    @Query("SELECT * FROM hex_tiles WHERE q = :q AND r = :r AND s = :s")
    suspend fun getByCoord(q: Int, r: Int, s: Int): HexTileEntity?
    
    @Query("SELECT * FROM hex_tiles WHERE evictionPriority >= :minPriority")
    suspend fun getByMinPriority(minPriority: Byte): List<HexTileEntity>
    
    @Query("SELECT COUNT(*) FROM hex_tiles")
    suspend fun count(): Int
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(tile: HexTileEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(tiles: List<HexTileEntity>)
    
    @Delete
    suspend fun delete(tile: HexTileEntity)
    
    @Query("DELETE FROM hex_tiles WHERE id = :id")
    suspend fun deleteById(id: String)
    
    @Query("DELETE FROM hex_tiles ORDER BY evictionPriority DESC, priorityTiebreaker DESC LIMIT :count")
    suspend fun deleteOutermost(count: Int)
    
    @Query("DELETE FROM hex_tiles")
    suspend fun deleteAll()
}

@Dao
interface CronTileDao {
    @Query("SELECT * FROM cron_tiles")
    suspend fun getAll(): List<CronTileEntity>
    
    @Query("SELECT * FROM cron_tiles WHERE anchorQ = :q AND anchorR = :r AND anchorS = :s")
    suspend fun getByAnchor(q: Int, r: Int, s: Int): CronTileEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(tile: CronTileEntity)
    
    @Delete
    suspend fun delete(tile: CronTileEntity)
    
    @Query("DELETE FROM cron_tiles WHERE id = :id")
    suspend fun deleteById(id: String)
}

@Dao
interface LatticeMetaDao {
    @Query("SELECT * FROM lattice_meta WHERE id = 1")
    suspend fun get(): LatticeMetaEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun set(meta: LatticeMetaEntity)
}

@Database(
    entities = [HexTileEntity::class, CronTileEntity::class, LatticeMetaEntity::class],
    version = 1,
    exportSchema = false
)
abstract class LatticeDatabase : RoomDatabase() {
    abstract fun hexTileDao(): HexTileDao
    abstract fun cronTileDao(): CronTileDao
    abstract fun latticeMetaDao(): LatticeMetaDao
}
