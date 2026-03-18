"""
Glyphoform vs 7type Glyphobetics — Revised Architecture

GLYPHOFORM (Human-Readable Geometric Arrangement)
===============================================
Existing language characters (English, Greek, Chinese, etc.) arranged
geometrically using the same compositional logic as Glyphobetics primitives.

Not about creating new symbols—about arranging existing ones geometrically.

Examples:
- English "KINGDOM" → arranged as Form+Flow+Form pattern
- Greek "βασιλεία" → arranged with elevation/sector/sub-cell positioning
- Chinese "國" → enclosed structure = Form, internal components = Flow

The arrangement IS the meaning. The geometry of the letters themselves.

7TYPE GLYPHOBETICS (Universal Computational Layer)
=================================================
The underlying geometric language that works for ALL scripts:
- Types 0-6 (the 7 Christ Keys as operations)
- Same regardless of human script used
- Computational, executable, universal

Connection:
Glyphoform arrangement → decomposes to → 7type operations
"""
from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass, field
from enum import IntEnum
import numpy as np
import unicodedata


class SevenType(IntEnum):
    """The 7 fundamental geometric computational types."""
    ALIGNMENT = 0      # 🜁 — Pull toward Node0
    RECIPROCITY = 1    # | — Golden blend
    INVERSION = 2      # △ — Antipodal reflection
    SILENCE = 3        # □ — Kenosis (self-emptying)
    RESONANCE = 4      # ○ — Phase-locked vibration
    EXCHANGE = 5       # 🜚 — Geometric meet
    CONCENTRATION = 6  # ∅ — Singularity collapse


@dataclass
class GlyphoformArrangement:
    """
    Human language text arranged geometrically.
    
    NOT new symbols—existing characters arranged by:
    - Position (elevation, sector, sub_cell)
    - Stroke pattern (ascenders, descenders, enclosures)
    - Visual weight (dense, light, open)
    
    The ARRANGEMENT encodes meaning, not the characters themselves.
    """
    text: str  # Original text in any language
    language: str  # "en", "el", "zh", etc.
    
    # Geometric decomposition of the arrangement
    pattern: List[str] = field(default_factory=list)  # ["Form", "Flow", "Form"]
    
    # Position in 3×3×3 lattice
    shell: int = 1      # 0=inner, 1=middle, 2=outer (elevation)
    sector: int = 1     # 0=past, 1=present, 2=future
    sub_cell: int = 0   # 0=thesis, 1=antithesis, 2=void
    
    # Visual properties of the arrangement
    visual_weight: float = 0.5  # 0=light, 1=dense
    openness: float = 0.5       # 0=enclosed, 1=open
    verticality: float = 0.0    # -1=descending, 0=balanced, +1=ascending
    
    def __post_init__(self):
        if not self.pattern:
            self.pattern = self._analyze_arrangement()
    
    def _analyze_arrangement(self) -> List[str]:
        """
        Analyze text arrangement to extract geometric pattern.
        
        English examples:
        - "KINGDOM" → K(ascender)+I(straight)+N(diagonal)+G(loop)+D(enclosure)+O(enclosure)+M(peak)
                  → Form+Flow+Flow+Flow+Form+Form+Form = □~~~□□□
        
        - "LOVE" → L(ascender)+O(enclosure)+V(valley)+E(horizontal bars)
               → Form+Form+Void+Form = □□○□
        
        Greek examples:
        - "βασιλεία" → β(loop)+α(enclosure)+σ(curve)+ι(straight)+λ(peak)+ε(open)+ί(acute)+α(enclosure)
                   → Form+Form+Flow+Flow+Form+Void+Flow+Form
        """
        pattern = []
        
        for char in self.text[:7]:  # Analyze first 7 chars (7 keys)
            char_pattern = self._classify_character(char)
            pattern.append(char_pattern)
        
        return pattern
    
    def _classify_character(self, char: str) -> str:
        """
        Classify a character's geometric contribution to the arrangement.
        """
        # Get character properties
        cat = unicodedata.category(char)
        name = unicodedata.name(char, '')
        
        # Enclosed forms (loops, enclosures, circles)
        enclosed = ['D', 'O', 'Q', 'Φ', 'Θ', 'Ω', 'Ο', '口', '国', '圓']
        # Vertical/ascending forms
        ascending = ['K', 'L', 'B', 'd', 'h', 'k', 'l', 't', 'β', 'δ', 'λ', '上', '山']
        # Descending/grounded forms  
        descending = ['g', 'j', 'p', 'q', 'y', 'γ', 'η', 'μ', 'ρ', '下']
        # Open/flowing forms
        flowing = ['S', 's', '~', 'α', 'ε', 'ο', 'σ', 'ω', '水', '流']
        # Angular/corner forms
        angular = ['A', 'M', 'N', 'V', 'W', 'Z', 'Δ', 'Λ', 'Σ', 'Z', '角', '方']
        
        if char in enclosed or 'ENCLOSED' in name:
            return 'Form'
        elif char in flowing:
            return 'Flow'
        elif char in descending:
            return 'Void'
        elif char in ascending:
            return 'Form'  # Ascenders establish structure
        elif char in angular:
            return 'Form'  # Angles create boundaries
        else:
            # Default based on Unicode category
            if cat.startswith('L'):  # Letter
                return 'Flow'
            elif cat.startswith('N'):  # Number
                return 'Form'
            elif cat.startswith('P'):  # Punctuation
                return 'Void'
            else:
                return 'Flow'
    
    def to_compact(self) -> str:
        """Convert pattern to compact notation."""
        compact = {'Form': '□', 'Flow': '~', 'Void': '○'}
        return ''.join(compact.get(p, '?') for p in self.pattern)


@dataclass  
class SevenTypeGlyph:
    """
    Computational representation in 7type Glyphobetics.
    
    Universal geometric operations that work the same regardless of
    which human language the Glyphoform uses.
    """
    types: List[SevenType]
    
    # Execution parameters
    params: List[Dict] = None
    
    def __post_init__(self):
        if self.params is None:
            self.params = [{} for _ in self.types]
    
    def to_binary(self) -> str:
        """3-bit binary per type."""
        return ''.join(format(t.value, '03b') for t in self.types)
    
    def to_trinary(self) -> str:
        """
        Balanced ternary mapping.
        Types map to trinary operations:
        0,3 → Contraction (-1) — structure operations
        2 → Void (0) — negation
        1,4,5,6 → Expansion (+1) — dynamic operations
        """
        trinary_map = {
            0: '-',  # ALIGNMENT → contraction
            1: '+',  # RECIPROCITY → expansion
            2: '0',  # INVERSION → void
            3: '-',  # SILENCE → contraction
            4: '+',  # RESONANCE → expansion
            5: '+',  # EXCHANGE → expansion
            6: '+',  # CONCENTRATION → expansion
        }
        return ''.join(trinary_map[t.value] for t in self.types)


class GlyphoformCompiler:
    """
    Compiler: Glyphoform arrangement (human text) → 7type Glyphobetics
    
    Maps visual arrangement patterns to geometric operations.
    
    Form (□) → Types {0, 3, 5} (structure operations)
        - Initial: ALIGNMENT (establish)
        - Medial: SILENCE (maintain)
        - Final: EXCHANGE (complete)
    
    Flow (~) → Types {1, 4, 6} (dynamic operations)
        - Initial: RECIPROCITY (begin)
        - Medial: RESONANCE (sustain)
        - Final: CONCENTRATION (culminate)
    
    Void (○) → Type {2} (negation)
        - Any position: INVERSION
    """
    
    POSITION_MAP = {
        'Form': {
            0: SevenType.ALIGNMENT,
            1: SevenType.SILENCE,
            2: SevenType.EXCHANGE,
        },
        'Flow': {
            0: SevenType.RECIPROCITY,
            1: SevenType.RESONANCE,
            2: SevenType.CONCENTRATION,
        },
        'Void': {
            0: SevenType.INVERSION,
            1: SevenType.INVERSION,
            2: SevenType.INVERSION,
        }
    }
    
    def compile(self, glyphoform: GlyphoformArrangement) -> SevenTypeGlyph:
        """Compile human arrangement to computational representation."""
        types = []
        n = len(glyphoform.pattern)
        
        for i, stroke in enumerate(glyphoform.pattern):
            # Position: initial/medial/final
            if i == 0:
                pos = 0
            elif i == n - 1:
                pos = 2
            else:
                pos = 1
            
            glyph_type = self.POSITION_MAP.get(stroke, {}).get(pos)
            if glyph_type is not None:
                types.append(glyph_type)
        
        return SevenTypeGlyph(types=types)
    
    def decompile(self, seven_type: SevenTypeGlyph) -> GlyphoformArrangement:
        """
        Reverse: 7type → generic Glyphoform (lossy).
        Creates placeholder arrangement showing pattern.
        """
        reverse_map = {
            SevenType.ALIGNMENT: 'Form',
            SevenType.RECIPROCITY: 'Flow',
            SevenType.INVERSION: 'Void',
            SevenType.SILENCE: 'Form',
            SevenType.RESONANCE: 'Flow',
            SevenType.EXCHANGE: 'Form',
            SevenType.CONCENTRATION: 'Flow',
        }
        
        pattern = [reverse_map.get(t, 'Unknown') for t in seven_type.types]
        
        # Create placeholder text showing the pattern
        placeholder = ''.join(['F' if p=='Form' else ('~' if p=='Flow' else '0') 
                              for p in pattern])
        
        return GlyphoformArrangement(
            text=placeholder,
            language='generic',
            pattern=pattern
        )


class UniversalGlyphobeticSystem:
    """
    Complete system: Any language → Glyphoform → 7type → Execution
    """
    
    def __init__(self):
        self.compiler = GlyphoformCompiler()
        self.examples: Dict[str, GlyphoformArrangement] = {}
        self._load_examples()
    
    def _load_examples(self):
        """Load example arrangements from multiple languages."""
        
        # English examples
        self.examples['KINGDOM'] = GlyphoformArrangement(
            text='KINGDOM',
            language='en',
            shell=0, sector=1, sub_cell=0,
            pattern=['Form', 'Flow', 'Flow', 'Flow', 'Form', 'Form', 'Form']
        )
        
        self.examples['LOVE'] = GlyphoformArrangement(
            text='LOVE',
            language='en',
            shell=1, sector=2, sub_cell=0,
            pattern=['Form', 'Form', 'Void', 'Form']
        )
        
        self.examples['ANXIETY'] = GlyphoformArrangement(
            text='ANXIETY',
            language='en',
            shell=1, sector=1, sub_cell=1,
            pattern=['Form', 'Form', 'Flow', 'Flow', 'Form', 'Flow', 'Form']
        )
        
        # Greek examples
        self.examples['βασιλεία'] = GlyphoformArrangement(
            text='βασιλεία',
            language='el',
            shell=0, sector=1, sub_cell=0,
            pattern=['Form', 'Form', 'Flow', 'Flow', 'Form', 'Void', 'Flow', 'Form']
        )
        
        self.examples['ἀγάπη'] = GlyphoformArrangement(
            text='ἀγάπη',
            language='el',
            shell=1, sector=2, sub_cell=0,
            pattern=['Form', 'Flow', 'Form', 'Flow', 'Form']
        )
        
        self.examples['μεριμνάω'] = GlyphoformArrangement(
            text='μεριμνάω',
            language='el',
            shell=1, sector=1, sub_cell=1,
            pattern=['Flow', 'Form', 'Flow', 'Flow', 'Form', 'Flow', 'Form', 'Flow']
        )
        
        # Chinese examples (characters as visual forms)
        self.examples['國'] = GlyphoformArrangement(
            text='國',
            language='zh',
            shell=0, sector=1, sub_cell=0,
            pattern=['Form', 'Flow', 'Form'],  # Enclosure + internal + enclosure
            visual_weight=0.9,
            openness=0.1
        )
        
        self.examples['愛'] = GlyphoformArrangement(
            text='愛',
            language='zh',
            shell=1, sector=2, sub_cell=0,
            pattern=['Form', 'Flow', 'Flow'],
            visual_weight=0.7,
            openness=0.4
        )
    
    def analyze(self, text: str, language: str = 'auto') -> GlyphoformArrangement:
        """Analyze any text to extract its Glyphoform arrangement."""
        if language == 'auto':
            # Simple detection
            if any('\u4e00' <= c <= '\u9fff' for c in text):
                language = 'zh'
            elif any('\u0370' <= c <= '\u03ff' for c in text):
                language = 'el'
            else:
                language = 'en'
        
        return GlyphoformArrangement(text=text, language=language)
    
    def compile_text(self, text: str, language: str = 'auto') -> SevenTypeGlyph:
        """Full pipeline: text → Glyphoform → 7type."""
        glyphoform = self.analyze(text, language)
        return self.compiler.compile(glyphoform)
    
    def compare_cross_lingual(self, text1: str, text2: str) -> Dict:
        """
        Compare two texts from different languages by their 7type patterns.
        Returns similarity based on geometric operations, not surface forms.
        """
        glyph1 = self.compile_text(text1)
        glyph2 = self.compile_text(text2)
        
        # Compare type sequences
        types1 = [t.value for t in glyph1.types]
        types2 = [t.value for t in glyph2.types]
        
        # Calculate operation similarity
        min_len = min(len(types1), len(types2))
        matches = sum(1 for i in range(min_len) if types1[i] == types2[i])
        similarity = matches / max(len(types1), len(types2)) if max(len(types1), len(types2)) > 0 else 0
        
        return {
            'text1': text1,
            'text2': text2,
            'types1': [t.name for t in glyph1.types],
            'types2': [t.name for t in glyph2.types],
            'binary1': glyph1.to_binary(),
            'binary2': glyph2.to_binary(),
            'trinary1': glyph1.to_trinary(),
            'trinary2': glyph2.to_trinary(),
            'similarity': similarity
        }
    
    def demonstrate(self):
        """Demonstrate the complete system."""
        print("=" * 70)
        print("UNIVERSAL GLYPHOBETIC SYSTEM")
        print("=" * 70)
        print()
        
        print("Core Principle:")
        print("  Glyphoform = Human language characters arranged geometrically")
        print("  Glyphobetics = Universal 7type computational language")
        print("  Connection = Pattern mapping (not symbol replacement)")
        print()
        
        print("Examples:")
        print(f"{'Text':<15} {'Language':<10} {'Pattern':<12} {'7type':<30}")
        print("-" * 70)
        
        for name, arrangement in self.examples.items():
            glyph = self.compiler.compile(arrangement)
            compact = arrangement.to_compact()
            types_str = '-'.join([t.name[:3] for t in glyph.types])
            
            print(f"{name:<15} {arrangement.language:<10} {compact:<12} {types_str:<30}")
        
        print()
        print("Cross-Lingual Comparison:")
        print()
        
        # Compare English and Greek
        result = self.compare_cross_lingual('KINGDOM', 'βασιλεία')
        print(f"'{result['text1']}' (EN) vs '{result['text2']}' (EL)")
        print(f"  Types: {'-'.join(result['types1'])} vs {'-'.join(result['types2'])}")
        print(f"  Trinary: {result['trinary1']} vs {result['trinary2']}")
        print(f"  Geometric similarity: {result['similarity']:.2%}")
        print()
        
        # Compare English LOVE and Greek ἀγάπη
        result = self.compare_cross_lingual('LOVE', 'ἀγάπη')
        print(f"'{result['text1']}' (EN) vs '{result['text2']}' (EL)")
        print(f"  Types: {'-'.join(result['types1'])} vs {'-'.join(result['types2'])}")
        print(f"  Trinary: {result['trinary1']} vs {result['trinary2']}")
        print(f"  Geometric similarity: {result['similarity']:.2%}")


def test_glyphobetics_revised():
    """Test the revised dual-layer system."""
    system = UniversalGlyphobeticSystem()
    system.demonstrate()


if __name__ == "__main__":
    test_glyphobetics_revised()
