package com.glyf.cathedral.ui

import android.app.Application
import androidx.lifecycle.*
import com.glyf.cathedral.core.*
import com.glyf.cathedral.cron.LatticeCronWorker
import com.glyf.cathedral.data.LatticeRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

/**
 * ViewModel for lattice operations
 * Bridges UI with repository and cron workers
 */
class LatticeViewModel(application: Application) : AndroidViewModel(application) {
    
    private val repository = LatticeRepository(application)
    
    // ═══════════════════════════════════════════════════════════════════════
    // State Flows
    // ═══════════════════════════════════════════════════════════════════════
    
    private val _tiles = MutableStateFlow<List<HexTile>>(emptyList())
    val tiles: StateFlow<List<HexTile>> = _tiles.asStateFlow()
    
    private val _explorerVoltage = MutableStateFlow(PhiConstants.PHI_7.toFloat())
    val explorerVoltage: StateFlow<Float> = _explorerVoltage.asStateFlow()
    
    private val _selectedCoord = MutableStateFlow<AxialCoord?>(null)
    val selectedCoord: StateFlow<AxialCoord?> = _selectedCoord.asStateFlow()
    
    private val _radialRadius = MutableStateFlow(21)
    val radialRadius: StateFlow<Int> = _radialRadius.asStateFlow()
    
    private val _cronEnabled = MutableStateFlow(false)
    val cronEnabled: StateFlow<Boolean> = _cronEnabled.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    // ═══════════════════════════════════════════════════════════════════════
    // Initialization
    // ═══════════════════════════════════════════════════════════════════════
    
    init {
        viewModelScope.launch {
            loadLattice()
        }
        
        // Auto-refresh tiles every second
        viewModelScope.launch {
            while (true) {
 kotlinx.coroutines.delay(1000)
                if (!_isLoading.value) {
                    refreshTiles()
                }
            }
        }
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // Public Operations
    // ═══════════════════════════════════════════════════════════════════════
    
    fun selectCoord(coord: AxialCoord) {
        _selectedCoord.value = coord
    }
    
    fun addTileAt(coord: AxialCoord, spin: TernarySpin = TernarySpin.ZERO) {
        viewModelScope.launch {
            _isLoading.value = true
            
            val tile = HexTile(
                coord = coord,
                spin = spin,
                phiMag = _explorerVoltage.value * 0.5f
            ).withPriority(_radialRadius.value)
            
            val evicted = repository.insertWithEviction(tile)
            evicted?.let {
                // Handle evicted tile (log, sync, etc.)
            }
            
            refreshTiles()
            _isLoading.value = false
        }
    }
    
    fun evictOutermost() {
        viewModelScope.launch {
            _isLoading.value = true
            repository.evictOutermost(1)
            refreshTiles()
            _isLoading.value = false
        }
    }
    
    fun scaleVoltage(k: Int) {
        viewModelScope.launch {
            _isLoading.value = true
            
            val currentState = repository.getLatticeState()
            val newState = currentState.scaleVoltage(k)
            repository.saveLatticeState(newState)
            
            _explorerVoltage.value = newState.explorerVoltage
            refreshTiles()
            _isLoading.value = false
        }
    }
    
    fun processCrons() {
        viewModelScope.launch {
            _isLoading.value = true
            val fired = repository.processCrons()
            if (fired > 0) {
                // Show notification or update UI
            }
            refreshTiles()
            _isLoading.value = false
        }
    }
    
    fun updateRadialRadius(radius: Int) {
        _radialRadius.value = radius
        viewModelScope.launch {
            // Update all tile priorities
            val state = repository.getLatticeState()
            val updatedTiles = state.hotTiles.map { 
                it.withPriority(radius) 
            }
            
            // Clear and re-insert with new priorities
            repository.clearAll()
            updatedTiles.forEach { repository.insertTile(it) }
            
            refreshTiles()
        }
    }
    
    fun setCronEnabled(enabled: Boolean) {
        _cronEnabled.value = enabled
        
        if (enabled) {
            LatticeCronWorker.schedule(getApplication())
        } else {
            LatticeCronWorker.cancel(getApplication())
        }
    }
    
    fun queryRadial(center: AxialCoord, radius: Int = _radialRadius.value) {
        viewModelScope.launch {
            _isLoading.value = true
            val results = repository.queryRadial(center, radius)
            // Could emit these to a separate flow for display
            _isLoading.value = false
        }
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // Private Helpers
    // ═══════════════════════════════════════════════════════════════════════
    
    private suspend fun loadLattice() {
        _isLoading.value = true
        
        val state = repository.getLatticeState()
        _explorerVoltage.value = state.explorerVoltage
        _radialRadius.value = state.radialRadius.toInt()
        
        refreshTiles()
        _isLoading.value = false
    }
    
    private suspend fun refreshTiles() {
        val tiles = repository.getAllTiles()
        _tiles.value = tiles
    }
}

/**
 * Factory for creating ViewModel with Application context
 */
class LatticeViewModelFactory(
    private val application: Application
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(LatticeViewModel::class.java)) {
            return LatticeViewModel(application) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
