package com.loom.app

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import kotlin.math.*

/**
 * ChristKeyVoiceTransformer — Sacred geometry voice synthesis
 * No ElevenLabs. No cloud. Just φ-weighted harmonics from the 96-byte lattice.
 */
class ChristKeyVoiceTransformer {
    
    companion object {
        const val SAMPLE_RATE = 22050
        const val BUFFER_SIZE = 1024
        val PHI = 1.618033988749895
    }
    
    private var audioTrack: AudioTrack? = null
    private var isSpeaking = false
    
    /**
     * Synthesize speech from text using Christ-key harmonics
     * Maps phonemes to geometric waveforms modulated by lattice state
     */
    fun speak(text: String, state: LatticeState) {
        if (isSpeaking) return
        
        val phonemes = textToPhonemes(text)
        val samples = synthesize(phonemes, state)
        play(samples)
    }
    
    /**
     * Text → Phoneme stream (simplified mapping)
     */
    private fun textToPhonemes(text: String): List<Phoneme> {
        return text.lowercase().map { char ->
            when (char) {
                'a', 'e' -> Phoneme.VOWEL_OPEN      // Root chakra
                'i' -> Phoneme.VOWEL_CLOSE        // Crown chakra  
                'o', 'u' -> Phoneme.VOWEL_ROUND    // Heart chakra
                'm', 'n' -> Phoneme.NASAL         // Vesica hum
                's', 'f' -> Phoneme.FRICATIVE      // Wind spiral
                'k', 't' -> Phoneme.PLOSIVE        // Crystal strike
                'l', 'r' -> Phoneme.LIQUID         // Wave flow
                else -> Phoneme.SILENCE
            }
        }
    }
    
    /**
     * Phoneme synthesis using 8 lattice harmonics as formant filter
     */
    private fun synthesize(phonemes: List<Phoneme>, state: LatticeState): ShortArray {
        val totalSamples = phonemes.size * SAMPLE_RATE / 10  // 100ms per phoneme
        val samples = ShortArray(totalSamples)
        
        // Extract 8 harmonics from lattice (bytes 64-95)
        val harmonics = (0..7).map { state.getHarmonic(it) }
        
        // φ-weighted fundamental frequency
        val baseFreq = 110.0 * PHI * state.energy
        
        var sampleIndex = 0
        
        phonemes.forEach { phoneme ->
            val phonemeSamples = SAMPLE_RATE / 10
            val formants = phoneme.formants.map { f -> f * baseFreq }
            
            for (i in 0 until phonemeSamples) {
                if (sampleIndex >= totalSamples) break
                
                val t = i.toDouble() / SAMPLE_RATE
                
                // Carrier: golden ratio detuned saw
                var sample = 0.0
                for (h in 1..8) {
                    val detune = 1.0 + (harmonics[h-1] % 100) / 10000.0
                    val freq = baseFreq * h * detune
                    val phase = 2 * PI * freq * t
                    sample += saw(phase) / h  // Harmonic decay
                }
                
                // Formant filter using lattice harmonics as resonators
                var filtered = 0.0
                formants.forEachIndexed { idx, f ->
                    val resonance = harmonics[idx % 8] / 1024.0
                    filtered += sample * resonator(t, f, resonance)
                }
                
                // φ-envelope for sacred attack/decay
                val envelope = phiEnvelope(i, phonemeSamples)
                
                // Final sample
                val final = (filtered * envelope * 32767 * 0.3).toInt()
                samples[sampleIndex++] = final.toShort()
            }
        }
        
        return samples
    }
    
    /**
     * Sawtooth wave with Christ-key modulation
     */
    private fun saw(phase: Double): Double {
        val normalized = (phase % (2 * PI)) / (2 * PI)
        return 2 * normalized - 1
    }
    
    /**
     * Resonator filter: 1 / (1 + (f/f0)^2)
     */
    private fun resonator(t: Double, freq: Double, resonance: Double): Double {
        return resonance * sin(2 * PI * freq * t)
    }
    
    /**
     * φ-weighted envelope: attack and decay by golden ratio
     */
    private fun phiEnvelope(position: Int, total: Int): Double {
        val t = position.toDouble() / total
        val phiInv = 1 / PHI
        
        // Attack: fast (φ^-2), Decay: slow (φ^-1)
        return when {
            t < phiInv * phiInv -> t / (phiInv * phiInv)  // Sharp attack
            else -> exp(-(t - phiInv * phiInv) * PHI * 3)  // Sacred decay
        }
    }
    
    /**
     * Play PCM samples through AudioTrack
     */
    private fun play(samples: ShortArray) {
        val minBuffer = AudioTrack.getMinBufferSize(
            SAMPLE_RATE,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT
        )
        
        audioTrack = AudioTrack.Builder()
            .setAudioAttributes(AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                .build())
            .setAudioFormat(AudioFormat.Builder()
                .setSampleRate(SAMPLE_RATE)
                .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                .build())
            .setBufferSizeInBytes(minBuffer.coerceAtLeast(samples.size * 2))
            .build()
        
        audioTrack?.apply {
            play()
            write(samples, 0, samples.size)
            stop()
            release()
        }
        
        audioTrack = null
    }
    
    fun stop() {
        isSpeaking = false
        audioTrack?.stop()
        audioTrack?.release()
        audioTrack = null
    }
    
    /**
     * Phoneme types with formant frequencies (Hz)
     */
    enum class Phoneme(val formants: List<Double>) {
        VOWEL_OPEN(listOf(1.0, 1.6, 2.4)),      // "ah" — root
        VOWEL_CLOSE(listOf(2.8, 3.4, 4.0)),     // "ee" — crown  
        VOWEL_ROUND(listOf(0.8, 1.2, 2.2)),     // "oh" — heart
        NASAL(listOf(1.0, 1.4, 2.8)),           // "mm" — vesica
        FRICATIVE(listOf(4.0, 6.0, 8.0)),       // "ss" — wind
        PLOSIVE(listOf(0.5, 1.0, 1.5)),         // "kk" — crystal
        LIQUID(listOf(1.2, 1.8, 2.6)),          // "ll" — flow
        SILENCE(listOf(0.0, 0.0, 0.0))          // rest
    }
}

/**
 * Extension: Integrate with MainActivity
 * Usage: voice.speak("The cathedral breathes", stateMachine.current)
 */
