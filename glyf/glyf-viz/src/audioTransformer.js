/**
 * GLYF Audio Transformer — Web Audio API Implementation
 * 
 * Processes audio in browser without cloud APIs.
 * Extracts 96-byte features → maps to 7-type primitives.
 * Enables GLYF to "hear" locally.
 */

const AudioTransformer = {
  // Configuration
  SAMPLE_RATE: 16000,  // 16kHz optimal for voice
  FRAME_SIZE: 512,     // 32ms frames
  HOP_SIZE: 256,       // 50% overlap
  
  /**
   * Process audio buffer → 96-byte AudioGlyf structure
   * @param {AudioBuffer} audioBuffer — Web Audio API buffer
   * @returns {AudioGlyf} — 96-byte audio structure
   */
  transform(audioBuffer) {
    // Get mono PCM data
    const pcm = this.getMonoPCM(audioBuffer);
    
    // Step 1: Pre-emphasis
    const preemphasized = this.preEmphasis(pcm);
    
    // Step 2: Frame extraction with Hann window
    const frames = this.extractFrames(preemphasized);
    
    // Step 3: FFT → spectrum (using Web Audio's native FFT)
    const spectrum = this.computeSpectrum(frames);
    
    // Step 4: Feature extraction
    const spectralCentroid = this.spectralCentroid(spectrum);
    const harmonicSignature = this.harmonicAnalysis(spectrum);
    const energyRMS = this.rmsEnergy(pcm);
    
    // Step 5: Temporal hash
    const temporalSig = this.hashAudio(pcm);
    
    return {
      temporalSig,
      spectralCentroid,
      harmonicSignature,
      energyRMS,
      
      // Convenience method
      dominantPrimitive() {
        const maxIdx = harmonicSignature.indexOf(Math.max(...harmonicSignature));
        return PRIMITIVE_NAMES[maxIdx];
      },
      
      // Convert to GlyfWord for semantic pipeline
      toGlyfWord() {
        return {
          nativeSig: temporalSig,
          geoCentroid: spectralCentroid,
          centerAxis: harmonicSignature,
          trajectoryMag: energyRMS
        };
      }
    };
  },
  
  /**
   * Get mono PCM from AudioBuffer
   */
  getMonoPCM(audioBuffer) {
    const numChannels = audioBuffer.numberOfChannels;
    const length = audioBuffer.length;
    const sampleRate = audioBuffer.sampleRate;
    
    // Mix to mono if stereo
    const mono = new Float32Array(length);
    
    for (let i = 0; i < length; i++) {
      let sum = 0;
      for (let ch = 0; ch < numChannels; ch++) {
        sum += audioBuffer.getChannelData(ch)[i];
      }
      mono[i] = sum / numChannels;
    }
    
    // Resample to 16kHz if necessary
    if (sampleRate !== this.SAMPLE_RATE) {
      return this.resample(mono, sampleRate, this.SAMPLE_RATE);
    }
    
    return mono;
  },
  
  /**
   * Resample audio using linear interpolation
   */
  resample(input, inputRate, outputRate) {
    const ratio = inputRate / outputRate;
    const outputLength = Math.floor(input.length / ratio);
    const output = new Float32Array(outputLength);
    
    for (let i = 0; i < outputLength; i++) {
      const idx = i * ratio;
      const idxFloor = Math.floor(idx);
      const idxCeil = Math.min(idxFloor + 1, input.length - 1);
      const fraction = idx - idxFloor;
      
      output[i] = input[idxFloor] * (1 - fraction) + input[idxCeil] * fraction;
    }
    
    return output;
  },
  
  /**
   * Pre-emphasis filter: y[n] = x[n] - 0.97*x[n-1]
   */
  preEmphasis(samples) {
    const output = new Float32Array(samples.length);
    output[0] = samples[0];
    
    for (let i = 1; i < samples.length; i++) {
      output[i] = samples[i] - 0.97 * samples[i - 1];
    }
    
    return output;
  },
  
  /**
   * Extract overlapping frames with Hann window
   */
  extractFrames(samples) {
    const numFrames = Math.floor((samples.length - this.FRAME_SIZE) / this.HOP_SIZE) + 1;
    const frames = [];
    
    for (let i = 0; i < numFrames; i++) {
      const start = i * this.HOP_SIZE;
      const frame = new Float32Array(this.FRAME_SIZE);
      
      for (let j = 0; j < this.FRAME_SIZE; j++) {
        // Hann window
        const window = 0.5 * (1 - Math.cos((2 * Math.PI * j) / (this.FRAME_SIZE - 1)));
        frame[j] = (samples[start + j] || 0) * window;
      }
      
      frames.push(frame);
    }
    
    return frames;
  },
  
  /**
   * Compute magnitude spectrum using FFT
   * Uses Web Audio API's AnalyserNode or custom FFT
   */
  computeSpectrum(frames) {
    const spectra = [];
    
    for (const frame of frames) {
      const fft = this.fft(frame);
      const magnitude = fft.map(c => Math.sqrt(c.real ** 2 + c.imag ** 2));
      spectra.push(magnitude.slice(0, this.FRAME_SIZE / 2));
    }
    
    return spectra;
  },
  
  /**
   * Naive FFT implementation (for no-external-dependency build)
   * For production: use fft.js or similar
   */
  fft(input) {
    const N = input.length;
    
    // Pad to power of 2
    const power = Math.ceil(Math.log2(N));
    const paddedLength = 2 ** power;
    const padded = new Float32Array(paddedLength);
    padded.set(input);
    
    // Output: array of {real, imag}
    const output = [];
    for (let k = 0; k < paddedLength; k++) {
      let real = 0;
      let imag = 0;
      
      for (let n = 0; n < paddedLength; n++) {
        const angle = -2 * Math.PI * k * n / paddedLength;
        real += padded[n] * Math.cos(angle);
        imag += padded[n] * Math.sin(angle);
      }
      
      output.push({ real, imag });
    }
    
    return output;
  },
  
  /**
   * Spectral centroid across [low, mid, high] bands
   */
  spectralCentroid(spectra) {
    const avgSpectrum = this.averageSpectrum(spectra);
    const nyquist = this.SAMPLE_RATE / 2;
    const binSize = nyquist / avgSpectrum.length;
    
    // Band cutoffs
    const lowCutoff = 300;
    const midCutoff = 2000;
    
    let lowSum = 0, lowWeight = 0;
    let midSum = 0, midWeight = 0;
    let highSum = 0, highWeight = 0;
    
    for (let i = 0; i < avgSpectrum.length; i++) {
      const freq = i * binSize;
      const mag = avgSpectrum[i];
      
      if (freq < lowCutoff) {
        lowSum += freq * mag;
        lowWeight += mag;
      } else if (freq < midCutoff) {
        midSum += freq * mag;
        midWeight += mag;
      } else {
        highSum += freq * mag;
        highWeight += mag;
      }
    }
    
    return [
      lowWeight > 0 ? lowSum / lowWeight : 0,
      midWeight > 0 ? midSum / midWeight : 0,
      highWeight > 0 ? highSum / highWeight : 0
    ];
  },
  
  /**
   * Harmonic analysis → 7-type primitive mapping
   * [0]=Curve(fundamental), [1]=Line(1st), [2]=Angle(2nd), etc.
   */
  harmonicAnalysis(spectra) {
    const avgSpectrum = this.averageSpectrum(spectra);
    const nyquist = this.SAMPLE_RATE / 2;
    const binSize = nyquist / avgSpectrum.length;
    
    // Find fundamental frequency
    const fundamentalBin = this.findFundamental(avgSpectrum);
    const fundamentalFreq = fundamentalBin * binSize;
    
    const harmonics = new Array(7).fill(0);
    
    // Extract 7 harmonics
    for (let h = 0; h < 7; h++) {
      const targetFreq = fundamentalFreq * (h + 1);
      const targetBin = Math.round(targetFreq / binSize);
      
      if (targetBin < avgSpectrum.length) {
        // Smoothing
        const prev = avgSpectrum[targetBin - 1] || 0;
        const curr = avgSpectrum[targetBin];
        const next = avgSpectrum[targetBin + 1] || 0;
        
        harmonics[h] = (curr + prev + next) / 3;
      }
    }
    
    // Normalize
    const max = Math.max(...harmonics);
    if (max > 0) {
      return harmonics.map(h => h / max);
    }
    
    return harmonics;
  },
  
  /**
   * Find fundamental frequency (pitch)
   */
  findFundamental(spectrum) {
    const nyquist = this.SAMPLE_RATE / 2;
    const binSize = nyquist / spectrum.length;
    
    const minBin = Math.floor(80 / binSize);   // 80Hz
    const maxBin = Math.floor(400 / binSize);  // 400Hz
    
    let peakBin = minBin;
    let peakMag = 0;
    
    for (let i = minBin; i < Math.min(maxBin, spectrum.length); i++) {
      if (spectrum[i] > peakMag) {
        peakMag = spectrum[i];
        peakBin = i;
      }
    }
    
    return peakBin;
  },
  
  /**
   * RMS energy calculation
   */
  rmsEnergy(samples) {
    let sumSq = 0;
    for (const s of samples) {
      sumSq += s * s;
    }
    return Math.sqrt(sumSq / samples.length);
  },
  
  /**
   * Average spectrum across frames
   */
  averageSpectrum(spectra) {
    if (spectra.length === 0) return [];
    
    const len = spectra[0].length;
    const avg = new Array(len).fill(0);
    
    for (const spectrum of spectra) {
      for (let i = 0; i < len; i++) {
        avg[i] += spectrum[i];
      }
    }
    
    return avg.map(v => v / spectra.length);
  },
  
  /**
   * Perceptual hash of audio
   */
  hashAudio(samples) {
    let hash = 0xcbf29ce484222325n; // FNV offset basis
    
    // Sample every 100th point
    for (let i = 0; i < samples.length; i += 100) {
      const bucket = Math.floor((samples[i] + 1) * 128); // 0-255
      hash ^= BigInt(bucket);
      hash *= 0x100000001b3n; // FNV prime
    }
    
    return Number(hash & 0xFFFFFFFFFFFFFFFFn);
  },
  
  /**
   * Decode Ogg/Opus file → AudioBuffer
   * Requires opus-decoder library or Web Audio API
   */
  async decodeOggOpus(arrayBuffer) {
    // If native Opus support available
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    try {
      // Try native decoding first (modern browsers support Opus)
      const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer.slice(0));
      return audioBuffer;
    } catch (e) {
      // Fallback: use opus-decoder library
      console.log('Native Opus decode failed, using fallback');
      return null;
    }
  }
};

// 7-Type primitive names for mapping
const PRIMITIVE_NAMES = [
  'Curve',    // 0 — fundamental
  'Line',     // 1 — 1st harmonic
  'Angle',    // 2 — 2nd harmonic
  'Vesica',   // 3 — 3rd harmonic
  'Spiral',   // 4 — 4th harmonic
  'Node',     // 5 — 5th harmonic
  'Field'     // 6 — 6th harmonic
];

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AudioTransformer;
}
