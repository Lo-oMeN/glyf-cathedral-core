package glyf.core.parser

/**
 * AST Node for GLYF 7-segment glyphoform composition.
 * 
 * Primitives: C, L, A, V, S, N, F represent individual segments
 * Combinators: | (juxtapose), / (superpose), () (contain), - (connect)
 */
sealed class GlyfNode {
    abstract fun toNotation(): String
}

/**
 * Primitive 7-segment component.
 * C=Center, L=Left, A=Above, V=Below, S=Super, N=Near, F=Far
 */
enum class PrimitiveType {
    C, L, A, V, S, N, F
}

/**
 * A primitive glyph component.
 */
data class Primitive(val type: PrimitiveType) : GlyfNode() {
    override fun toNotation(): String = type.name
}

/**
 * Base class for compound expressions (contain, connect, juxtapose, superpose).
 */
sealed class Compound : GlyfNode()

/**
 * Juxtaposition: A|B places A beside B horizontally.
 */
data class Juxtapose(val left: GlyfNode, val right: GlyfNode) : Compound() {
    override fun toNotation(): String = "${left.toNotation()}|${right.toNotation()}"
}

/**
 * Superposition: A/B overlays B on A.
 */
data class Superpose(val bottom: GlyfNode, val top: GlyfNode) : Compound() {
    override fun toNotation(): String = "${bottom.toNotation()}/${top.toNotation()}"
}

/**
 * Containment: (A) wraps/containes A.
 */
data class Contain(val inner: GlyfNode) : Compound() {
    override fun toNotation(): String = "(${inner.toNotation()})"
}

/**
 * Connection: A-B connects A to B.
 */
data class Connect(val from: GlyfNode, val to: GlyfNode) : Compound() {
    override fun toNotation(): String = "${from.toNotation()}-${to.toNotation()}"
}

/**
 * A complete bracket-wrapped glyph expression [expr].
 * This is the top-level container for GLYF notation.
 */
data class BracketExpr(val inner: GlyfNode) : GlyfNode() {
    override fun toNotation(): String = "[${inner.toNotation()}]"
}
