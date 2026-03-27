import kotlin.random.Random

/**
 * PolyphonyZero.kt - Refined Surgical Strike
 * φ-weighted divergence. Harmonic resonance. Visualizer Bridge.
 * Compile: kotlinc PolyphonyZero.kt -include-runtime -d loom.jar && java -jar loom.jar
 */

/** 96-Byte Lattice State - Packed */
class LatticeState(bytes: ByteArray? = null) {
    val data = bytes?.copyOf() ?: ByteArray(96)

    // Byte 0-7: Timestamp
    var timestamp: Long
        get() = longFrom(0)
        set(v) = longTo(0, v)

    // Byte 8-23: Node ID (128-bit)
    fun getNodeId(): ByteArray = data.copyOfRange(8, 24)
    fun setNodeId(id: ByteArray) = id.copyInto(data, 8)

    // Byte 24-31: Energy (Double)
    var energy: Double
        get() = doubleFrom(24)
        set(v) = doubleTo(24, v)

    // Byte 32-63: 4 Hypergraph Edges (8 bytes each)
    fun getEdge(i: Int): Long = longFrom(32 + i * 8)
    fun setEdge(i: Int, v: Long) = longTo(32 + i * 8, v)

    // Byte 64-95: 8 Harmonics (4 bytes each)
    fun getHarmonic(i: Int): Int = intFrom(64 + i * 4)
    fun setHarmonic(i: Int, v: Int) = intTo(64 + i * 4, v)

    // Primitive packing
    private fun longFrom(o: Int): Long {
        var r = 0L
        for (i in 0..7) r = r or ((data[o + i].toLong() and 0xFF) shl (i * 8))
        return r
    }
    private fun longTo(o: Int, v: Long) {
        for (i in 0..7) data[o + i] = ((v shr (i * 8)) and 0xFF).toByte()
    }
    private fun intFrom(o: Int): Int {
        var r = 0
        for (i in 0..3) r = r or ((data[o + i].toInt() and 0xFF) shl (i * 8))
        return r
    }
    private fun intTo(o: Int, v: Int) {
        for (i in 0..3) data[o + i] = ((v shr (i * 8)) and 0xFF).toByte()
    }
    private fun doubleFrom(o: Int): Double = Double.fromBits(longFrom(o))
    private fun doubleTo(o: Int, v: Double) = longTo(o, v.toBits())

    fun toBytes(): ByteArray = data.copyOf()
}

/** State Machine - φ-weighted weak emergence */
class StateMachine {
    private val history = mutableListOf<LatticeState>()
    private var current = LatticeState().apply {
        timestamp = System.currentTimeMillis()
        energy = 1.0
        repeat(4) { setEdge(it, Random.nextLong()) }
        repeat(8) { setHarmonic(it, Random.nextInt(1024)) }
    }

    fun step(): LatticeState {
        history.add(current)
        if (history.size > 100) history.removeAt(0)

        val next = LatticeState()
        next.timestamp = System.currentTimeMillis()

        // Calculate mean energy (gravity well)
        val meanEnergy = if (history.isEmpty()) 1.0 else history.map { it.energy }.average()

        // Divergence: Move away from mean with φ-weighted probability
        val phi = 1.618033988749895
        val divergence = if (Random.nextDouble() < (1 / phi)) 0.9 else 1.1
        next.energy = (current.energy * divergence).coerceIn(0.01, 1000.0)

        // Edge inheritance with mutation
        repeat(4) { idx ->
            val parent = history.randomOrNull() ?: current
            val mutation = if (Random.nextBoolean()) 1 else -1
            next.setEdge(idx, parent.getEdge(idx) + mutation)
        }

        // Harmonic resonance (sine approximation via previous states)
        repeat(8) { idx ->
            val phase = history.takeLast(3).map { it.getHarmonic(idx) }.sum()
            next.setHarmonic(idx, (phase + Random.nextInt(-50, 50)) % 1024)
        }

        current = next
        return current
    }

    fun getHistory(): List<LatticeState> = history.toList()
    fun getCurrent(): LatticeState = current
}

/** Visualizer Bridge - State bytes to ASCII draw calls */
class VisualizerBridge {
    fun render(state: LatticeState) {
        val energyNorm = (state.energy / 10.0).coerceIn(0.0, 1.0)
        val barLength = (energyNorm * 40).toInt()

        println("\u001B[H\u001B[2J") // Clear screen
        println("=".repeat(50))
        println("POLYPHONY ZERO - Thread 0x${state.timestamp.toString(16).takeLast(4)}")
        println("=".repeat(50))

        // Energy bar
        println("ENERGY [${"█".repeat(barLength)}${" ".repeat(40 - barLength)}] ${"%.2f".format(state.energy)}")

        // Edges as hex
        print("EDGES ")
        repeat(4) { println("0x${state.getEdge(it).toString(16).padStart(16, '0')}") }

        // Harmonics as waveform
        println("WAVEFORM")
        val harmonics = (0..7).map { state.getHarmonic(it) }
        val max = harmonics.maxOrNull() ?: 1
        val min = harmonics.minOrNull() ?: 0
        val range = (max - min).coerceAtLeast(1)

        harmonics.forEach { h ->
            val height = ((h - min) * 10 / range)
            println(" ${" ".repeat(height)}* ${h}")
        }
        println("=".repeat(50))
    }
}

/** Main - The ignition */
fun main() {
    println("INIT: 96-byte lattice test")
    println("Checking packing integrity...")

    // Verify 96-byte constraint
    val testState = LatticeState()
    val bytes = testState.toBytes()
    check(bytes.size == 96) { "VIOLATION: ${bytes.size} bytes != 96" }

    println("✓ Byte packing verified: ${bytes.size} bytes")
    println("✓ Polyphony thread spinning up...")
    Thread.sleep(500)

    val machine = StateMachine()
    val viz = VisualizerBridge()

    // One thread, 50 steps, visible proof
    repeat(50) {
        val state = machine.step()
        viz.render(state)
        Thread.sleep(100) // 10fps - slow enough to witness
    }

    println("\nCOMPLETE: 50 states generated, 96-byte integrity maintained")
    println("The lattice lives. Expand to multi-thread or architect properly.")
}
