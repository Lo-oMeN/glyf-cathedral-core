"""
Cultural Atlas Drift: Lexicon-Lattice Bridge
Connects the 729-slot trinary-PGA atlas to the geometry.glyph_id lexicon.

βασιλεία at [inner-present-thesis] becomes the first rotor-populated cell,
testing meet/join invariants against sense.metaphors.
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import IntEnum

from atlas_lattice import TrinaryPGALattice, LatticeAddress, PGAMultivector16D


@dataclass
class LexiconEntry:
    """
    A lexicon entry with geometry.glyph_id and sense.metaphors.
    
    From the 2025-10-26 dataset, now repositioned in the 3×3×3 lattice.
    """
    greek: str
    english: str
    glyph_id: str  # geometry.glyph_id: Form, Flow, Void strokes
    fractal_level: int  # geometry.fractal_level: 0=primitive, 1=operator, 2=emergence
    shell: int  # 0=inner, 1=middle, 2=outer
    sector: int  # 0=past, 1=present, 2=future
    sub_cell: int  # 0=thesis, 1=antithesis, 2=void
    
    # sense.metaphors column
    metaphors: List[str] = field(default_factory=list)
    
    # Semantic coordinates
    elevation: float = 0.0  # Vertical position in lattice
    forward: float = 0.0    # Temporal position
    lateral: float = 0.0    # Force direction
    
    # Rotor encoding
    rotor_angle: float = 0.0
    rotor_plane: Tuple[int, int] = field(default_factory=lambda: (1, 2))  # e₁₂ plane default


class CulturalAtlas:
    """
    The 14 core Greek lexemes positioned as high-elevation landmarks
    in the 729-slot trinary-PGA lattice.
    
    Each lexeme carries:
    - Rotor encoding (φ-scaled, quasiperiodic)
    - Metaphor connections (sense.metaphors)
    - Meet/join invariants with neighboring cells
    """
    
    CORE_LEXEMES = {
        'βασιλεία': {
            'english': 'kingdom/sovereignty',
            'glyph_id': 'Form+Flow+Form',  # Enclosure with flow
            'fractal_level': 2,  # emergence
            'shell': 0,  # inner (foundational)
            'sector': 1,  # present
            'sub_cell': 0,  # thesis (+1)
            'metaphors': [
                'royal_power', 'divine_reign', 'eschatological_hope',
                'mustard_seed', 'yeast', 'hidden_treasure', 'pearl'
            ],
            'rotor_angle': np.pi / 3,  # 60° - stability
        },
        'ἐχθρός': {
            'english': 'enemy/opposition',
            'glyph_id': 'Form+Form+Void',  # Opposition with absence
            'fractal_level': 1,
            'shell': 0,
            'sector': 0,  # past
            'sub_cell': 1,  # antithesis (-1)
            'metaphors': [
                'adversary', 'persecutor', 'last_enemy_death',
                'weeds_among_wheat', 'wolf_among_sheep'
            ],
            'rotor_angle': -np.pi / 4,  # -45° - opposition
        },
        'ἀφίημι': {
            'english': 'release/forgive/let_go',
            'glyph_id': 'Flow+Flow+Void',  # Double flow into void
            'fractal_level': 1,
            'shell': 0,
            'sector': 2,  # future
            'sub_cell': 2,  # void (0)
            'metaphors': [
                'forgiveness', 'divorce', 'leave_behind', 'abandon',
                'send_away', 'remit_debt', 'release_captive'
            ],
            'rotor_angle': 0,  # 0° - void horizon
        },
        'ταπεινόω': {
            'english': 'humble/lower/exalt',
            'glyph_id': 'Form+Void+Flow',  # Descent then ascent
            'fractal_level': 1,
            'shell': 1,  # middle (relational)
            'sector': 1,  # present
            'sub_cell': 0,  # thesis
            'metaphors': [
                'humility', 'self_abasement', 'God_opposes_proud',
                'exaltation_follows', 'Christ_emptied_himself'
            ],
            'rotor_angle': -np.pi / 6,  # -30° - descent
        },
        'μεριμνάω': {
            'english': 'anxious/worry/care',
            'glyph_id': 'Form+Form+Form',  # Triple enclosure (trapped)
            'fractal_level': 1,
            'shell': 1,
            'sector': 1,
            'sub_cell': 1,  # antithesis
            'metaphors': [
                'divided_mind', 'anxiety', 'cares_of_world',
                'thorns_choking_seed', 'martha_distracted'
            ],
            'rotor_angle': np.pi / 2,  # 90° - maximum stress
        },
        'καρδία': {
            'english': 'heart/center/will',
            'glyph_id': 'Flow+Form+Flow',  # Flow through center
            'fractal_level': 0,  # primitive
            'shell': 1,
            'sector': 1,
            'sub_cell': 2,  # void
            'metaphors': [
                'inner_person', 'seat_of_emotions', 'treasure_store',
                'hard_heart', 'pure_heart', 'circumcised_heart'
            ],
            'rotor_angle': 0,
        },
        'ἀγάπη': {
            'english': 'love/charity',
            'glyph_id': 'Flow+Flow+Flow',  # Triple flow
            'fractal_level': 2,
            'shell': 1,
            'sector': 2,  # future
            'sub_cell': 0,
            'metaphors': [
                'sacrificial_love', 'God_is_love', 'love_enemy',
                'lay_down_life', 'never_fails', 'greatest_virtue'
            ],
            'rotor_angle': np.pi / 4,  # 45° - expansion
        },
        'εἰρήνη': {
            'english': 'peace/wholeness',
            'glyph_id': 'Void+Flow+Void',  # Flow between voids
            'fractal_level': 1,
            'shell': 1,
            'sector': 0,  # past
            'sub_cell': 2,
            'metaphors': [
                'shalom', 'peace_maker', 'peace_that_passes',
                'not_as_world_gives', 'wholeness', 'reconciliation'
            ],
            'rotor_angle': np.pi / 6,
        },
        'σῶμα': {
            'english': 'body/corpse/substance',
            'glyph_id': 'Form+Form+Flow',  # Form with internal flow
            'fractal_level': 0,
            'shell': 2,  # outer (emergence)
            'sector': 1,
            'sub_cell': 0,
            'metaphors': [
                'physical_body', 'body_of_Christ', 'temple_of_Spirit',
                'resurrection_body', 'one_body_many_members'
            ],
            'rotor_angle': np.pi / 5,
        },
        'ἀνάστασις': {
            'english': 'resurrection/rising',
            'glyph_id': 'Void+Flow+Form',  # Emergence from void
            'fractal_level': 2,
            'shell': 2,
            'sector': 2,
            'sub_cell': 1,
            'metaphors': [
                'Christ_raised', 'firstfruits', 'general_resurrection',
                'new_life', 'upward_call', 'hope_of_glory'
            ],
            'rotor_angle': np.pi / 3,  # Rising angle
        },
        'δοῦλος': {
            'english': 'servant/slave',
            'glyph_id': 'Form+Void+Form',  # Enclosed service
            'fractal_level': 1,
            'shell': 2,
            'sector': 0,
            'sub_cell': 2,
            'metaphors': [
                'bondservant', 'slave_of_Christ', 'willing_service',
                'foot_washing', 'greatest_is_least', 'ransom_many'
            ],
            'rotor_angle': -np.pi / 8,
        },
    }
    
    def __init__(self, lattice: Optional[TrinaryPGALattice] = None):
        self.lattice = lattice or TrinaryPGALattice()
        self.lexicon: Dict[str, LexiconEntry] = {}
        self._populate_lexicon()
        self._encode_rotors()
    
    def _populate_lexicon(self):
        """Populate lexicon entries from core definitions."""
        for greek, data in self.CORE_LEXEMES.items():
            entry = LexiconEntry(
                greek=greek,
                english=data['english'],
                glyph_id=data['glyph_id'],
                fractal_level=data['fractal_level'],
                shell=data['shell'],
                sector=data['sector'],
                sub_cell=data['sub_cell'],
                metaphors=data['metaphors'],
                rotor_angle=data['rotor_angle']
            )
            
            # Compute semantic coordinates
            entry.elevation = data['shell'] - 1  # -1, 0, +1
            entry.forward = data['sector'] - 1   # -1, 0, +1
            entry.lateral = {0: 1, 1: -1, 2: 0}[data['sub_cell']]  # +1, -1, 0
            
            self.lexicon[greek] = entry
            
            # Link to lattice cell
            addr = LatticeAddress(
                data['shell'], data['sector'], data['sub_cell'], 0, 0
            )
            cell = self.lattice.cells[addr.linear_index]
            cell.bigram = greek  # Override with Greek lexeme
            cell.kenosis_fruit_score = 0.9 if data['sub_cell'] == 0 else 0.5
    
    def _encode_rotors(self):
        """Encode each lexeme as φ-scaled rotor in its cell's multivector."""
        for greek, entry in self.lexicon.items():
            addr = LatticeAddress(
                entry.shell, entry.sector, entry.sub_cell, 0, 0
            )
            cell = self.lattice.cells[addr.linear_index]
            
            # Create φ-scaled rotor
            phi_scale = (1.618 ** (entry.shell + 1))
            angle = entry.rotor_angle * phi_scale
            
            # Rotor in e₁₂ plane: R = cos(θ/2) + sin(θ/2)e₁₂
            mv = PGAMultivector16D()
            mv.values[0] = np.cos(angle / 2)  # scalar
            mv.values[8] = np.sin(angle / 2)  # e₁₂ bivector
            
            # Add elevation encoding (e₀ component)
            mv.values[1] = entry.elevation * 0.3  # e₀ degenerate
            
            # Add forward motion (e₁ + e₂ components)
            mv.values[2] = entry.forward * 0.2 * np.cos(angle)
            mv.values[3] = entry.forward * 0.2 * np.sin(angle)
            
            cell.multivector = mv
    
    def get_cell(self, greek: str) -> Optional[object]:
        """Get lattice cell by Greek lexeme."""
        if greek not in self.lexicon:
            return None
        entry = self.lexicon[greek]
        addr = LatticeAddress(
            entry.shell, entry.sector, entry.sub_cell, 0, 0
        )
        return self.lattice.cells[addr.linear_index]
    
    def meet_invariant(self, lex1: str, lex2: str) -> Tuple[PGAMultivector16D, float]:
        """
        Test meet (∧) invariant between two lexemes.
        
        Returns: (meet_result, coherence_of_meet)
        """
        cell1 = self.get_cell(lex1)
        cell2 = self.get_cell(lex2)
        
        if not cell1 or not cell2:
            return PGAMultivector16D(), 0.0
        
        meet_mv = cell1.multivector.meet(cell2.multivector)
        coherence = meet_mv.coherence
        
        return meet_mv, coherence
    
    def join_invariant(self, lex1: str, lex2: str) -> Tuple[PGAMultivector16D, float]:
        """
        Test join (∨) invariant between two lexemes.
        
        Returns: (join_result, coherence_of_join)
        """
        cell1 = self.get_cell(lex1)
        cell2 = self.get_cell(lex2)
        
        if not cell1 or not cell2:
            return PGAMultivector16D(), 0.0
        
        join_mv = cell1.multivector.join(cell2.multivector)
        coherence = join_mv.coherence
        
        return join_mv, coherence
    
    def metaphor_proximity(self, lex1: str, lex2: str) -> float:
        """
        Compute semantic proximity via shared metaphors.
        Returns 0-1 score based on metaphor overlap.
        """
        if lex1 not in self.lexicon or lex2 not in self.lexicon:
            return 0.0
        
        m1 = set(self.lexicon[lex1].metaphors)
        m2 = set(self.lexicon[lex2].metaphors)
        
        if not m1 or not m2:
            return 0.0
        
        intersection = len(m1 & m2)
        union = len(m1 | m2)
        
        return intersection / union if union > 0 else 0.0
    
    def test_betaisia_invariants(self):
        """
        Test βασιλεία (kingdom) meet/join invariants against all other lexemes.
        """
        print("=== βασιλεία (Kingdom) Invariants ===\n")
        
        basileia = 'βασιλεία'
        other_lexemes = [k for k in self.lexicon.keys() if k != basileia]
        
        print(f"Position: {self.lexicon[basileia].shell}-{self.lexicon[basileia].sector}-{self.lexicon[basileia].sub_cell}")
        print(f"Glyph ID: {self.lexicon[basileia].glyph_id}")
        print(f"Coherence κ: {self.get_cell(basileia).multivector.coherence:.4f}")
        print()
        
        print("Meet (∧) and Join (∨) with other lexemes:")
        print(f"{'Lexeme':<15} {'Meet κ':<10} {'Join κ':<10} {'Metaphor Sim':<15}")
        print("-" * 55)
        
        results = []
        for other in other_lexemes:
            meet_mv, meet_k = self.meet_invariant(basileia, other)
            join_mv, join_k = self.join_invariant(basileia, other)
            metaphor_sim = self.metaphor_proximity(basileia, other)
            
            results.append({
                'lexeme': other,
                'meet_k': meet_k,
                'join_k': join_k,
                'metaphor_sim': metaphor_sim
            })
            
            print(f"{other:<15} {meet_k:<10.4f} {join_k:<10.4f} {metaphor_sim:<15.4f}")
        
        # Find strongest connections
        print("\nStrongest metaphor connections:")
        top_metaphors = sorted(results, key=lambda x: x['metaphor_sim'], reverse=True)[:3]
        for r in top_metaphors:
            print(f"  {r['lexeme']}: {r['metaphor_sim']:.4f}")
        
        print("\nHighest meet coherence (intersection):")
        top_meet = sorted(results, key=lambda x: x['meet_k'], reverse=True)[:3]
        for r in top_meet:
            print(f"  {r['lexeme']}: κ={r['meet_k']:.4f}")
        
        print("\nHighest join coherence (union):")
        top_join = sorted(results, key=lambda x: x['join_k'], reverse=True)[:3]
        for r in top_join:
            print(f"  {r['lexeme']}: κ={r['join_k']:.4f}")
    
    def atlas_summary(self):
        """Print complete atlas summary."""
        print("=== CULTURAL ATLAS SUMMARY ===\n")
        
        print(f"Total lexemes: {len(self.lexicon)}")
        print(f"Lattice integration: {len([c for c in self.lattice.cells.values() if c.bigram in self.lexicon])} cells")
        print()
        
        # By shell
        print("By Shell (elevation):")
        for shell, name in [(0, 'Inner'), (1, 'Middle'), (2, 'Outer')]:
            lexemes = [k for k, v in self.lexicon.items() if v.shell == shell]
            print(f"  {name}: {lexemes}")
        print()
        
        # By sub_cell (trinary state)
        print("By Trinary State:")
        for sub, name in [(0, 'Thesis (+1)'), (1, 'Antithesis (−1)'), (2, 'Void (0)')]:
            lexemes = [k for k, v in self.lexicon.items() if v.sub_cell == sub]
            print(f"  {name}: {lexemes}")
        print()
        
        # By fractal level
        print("By Fractal Level:")
        for level, name in [(0, 'Primitive'), (1, 'Operator'), (2, 'Emergence')]:
            lexemes = [(k, v.glyph_id) for k, v in self.lexicon.items() if v.fractal_level == level]
            print(f"  {name}:")
            for g, gid in lexemes:
                print(f"    {g}: {gid}")


def test_cultural_atlas():
    """Test the cultural atlas drift."""
    print("=== CULTURAL ATLAS DRIFT ===\n")
    
    atlas = CulturalAtlas()
    atlas.atlas_summary()
    print()
    
    # Test βασιλεία invariants
    atlas.test_betaisia_invariants()
    
    print("\n=== ATLAS DRIFT COMPLETE ===")


if __name__ == "__main__":
    test_cultural_atlas()
