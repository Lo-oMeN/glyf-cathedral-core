/** ============================================================================
 * PHASE 0: Pybind11 Bindings for GaugeNode128
 * Pragmatic Geometric AI - Proof of Concept
 * ============================================================================ */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/operators.h>
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>

namespace py = pybind11;

/* Include the C header (wrapped in extern "C") */
extern "C" {
    #include "../core/gauge_node.h"
}

/* ============================================================================
 * Python Wrapper Class for GaugeNode128
 * ============================================================================ */

class PyGaugeNode128 {
public:
    GaugeNode128 node;
    
    PyGaugeNode128() {
        std::memset(&node, 0, sizeof(GaugeNode128));
    }
    
    PyGaugeNode128(uint32_t id, uint8_t glyph_type, float x, float y, float z) {
        gauge_node_init(&node, id, static_cast<GlyfPrimitive>(glyph_type), x, y, z);
    }
    
    void init(uint32_t id, uint8_t glyph_type, float x, float y, float z) {
        gauge_node_init(&node, id, static_cast<GlyfPrimitive>(glyph_type), x, y, z);
    }
    
    /* Getters */
    uint32_t get_node_id() const { return node.node_id; }
    float get_x() const { return node.coordinates[0]; }
    float get_y() const { return node.coordinates[1]; }
    float get_z() const { return node.coordinates[2]; }
    uint8_t get_glyph_type() const { return node.glyph_type; }
    uint8_t get_chirality() const { return node.chirality; }
    uint16_t get_bond_count() const { return node.bond_count; }
    float get_holonomy_phase() const { return node.holonomy_phase; }
    
    /* Setters */
    void set_node_id(uint32_t id) { node.node_id = id; }
    void set_coordinates(float x, float y, float z) {
        node.coordinates[0] = x;
        node.coordinates[1] = y;
        node.coordinates[2] = z;
    }
    void set_glyph_type(uint8_t type) { node.glyph_type = type; }
    void set_chirality(uint8_t c) { node.chirality = c; }
    void set_holonomy_phase(float phase) { node.holonomy_phase = phase; }
    
    std::vector<uint32_t> get_bonds() const {
        std::vector<uint32_t> result;
        for (uint16_t i = 0; i < node.bond_count; i++) {
            result.push_back(node.bonds[i]);
        }
        return result;
    }
    
    py::array_t<uint8_t> get_payload() const {
        return py::array_t<uint8_t>(72, node.payload);
    }
    
    void set_payload(const std::vector<uint8_t>& data) {
        size_t len = std::min(data.size(), size_t(72));
        std::memcpy(node.payload, data.data(), len);
    }
    
    /* Direct struct access for C operations */
    GaugeNode128* ptr() { return &node; }
};

/* ============================================================================
 * Module Bindings
 * ============================================================================ */

PYBIND11_MODULE(py_gauge, m) {
    m.doc() = "Pybind11 bindings for GaugeNode128 - Pragmatic Geometric AI";
    
    /* =========================================================================
     * GlyfPrimitive Enum
     * ========================================================================= */
    py::enum_<GlyfPrimitive>(m, "GlyfPrimitive")
        .value("VOID", GLYPH_VOID, "NULL pointer, zero tensor, attention mask 0")
        .value("DOT", GLYPH_DOT, "Scalar vertex, 1D embedding anchor")
        .value("CURVE", GLYPH_CURVE, "Bézier control points (quadratic, 3 floats)")
        .value("LINE", GLYPH_LINE, "Vector edge, difference of dot coordinates")
        .value("ANGLE", GLYPH_ANGLE, "Cosine similarity threshold, attention gating")
        .value("CIRCLE", GLYPH_CIRCLE, "L2 norm boundary, clustering radius")
        .value("VESICA", GLYPH_VESICA, "Intersection volume, attention overlap region")
        .export_values();
    
    /* =========================================================================
     * GaugeNode128 Class
     * ========================================================================= */
    py::class_<PyGaugeNode128>(m, "GaugeNode128")
        .def(py::init<>(), "Create empty GaugeNode128")
        .def(py::init<uint32_t, uint8_t, float, float, float>(),
             py::arg("id"), py::arg("glyph_type"), py::arg("x"), py::arg("y"), py::arg("z"),
             "Initialize node with id, glyph type, and coordinates")
        .def("init", &PyGaugeNode128::init,
             py::arg("id"), py::arg("glyph_type"), py::arg("x"), py::arg("y"), py::arg("z"),
             "Initialize node with id, glyph type, and coordinates")
        
        /* Properties */
        .def_property("node_id", &PyGaugeNode128::get_node_id, &PyGaugeNode128::set_node_id,
                      "Unique node identifier")
        .def_property("glyph_type", &PyGaugeNode128::get_glyph_type, &PyGaugeNode128::set_glyph_type,
                      "Sevenfold primitive type")
        .def_property("chirality", &PyGaugeNode128::get_chirality, &PyGaugeNode128::set_chirality,
                      "Handedness flag (0 or 1)")
        .def_property("bond_count", &PyGaugeNode128::get_bond_count, nullptr,
                      "Number of connected bonds")
        .def_property("holonomy_phase", &PyGaugeNode128::get_holonomy_phase, &PyGaugeNode128::set_holonomy_phase,
                      "Accumulated rotation phase")
        
        /* Coordinates */
        .def_property_readonly("x", &PyGaugeNode128::get_x, "X coordinate")
        .def_property_readonly("y", &PyGaugeNode128::get_y, "Y coordinate")
        .def_property_readonly("z", &PyGaugeNode128::get_z, "Z coordinate")
        .def("set_coordinates", &PyGaugeNode128::set_coordinates,
             py::arg("x"), py::arg("y"), py::arg("z"),
             "Set spatial coordinates")
        
        /* Bonds and Payload */
        .def("get_bonds", &PyGaugeNode128::get_bonds, "Get list of connected node IDs")
        .def("get_payload", &PyGaugeNode128::get_payload, "Get 72-byte payload as numpy array")
        .def("set_payload", &PyGaugeNode128::set_payload, py::arg("data"), "Set payload from byte array")
        
        /* Direct pointer access */
        .def("_ptr", &PyGaugeNode128::ptr, py::return_value_policy::reference_internal,
             "Internal: Get raw pointer to C struct")
        
        /* String representation */
        .def("__repr__", [](const PyGaugeNode128& n) {
            return "<GaugeNode128 id=" + std::to_string(n.get_node_id()) + 
                   " glyph=" + std::to_string(n.get_glyph_type()) +
                   " bonds=" + std::to_string(n.get_bond_count()) + ">";
        });
    
    /* =========================================================================
     * Core Operations
     * ========================================================================= */
    m.def("gauge_node_connect", [](PyGaugeNode128& a, PyGaugeNode128& b) {
        return gauge_node_connect(&a.node, &b.node);
    }, py::arg("a"), py::arg("b"), 
    "Connect two nodes bidirectionally. Returns True if successful.");
    
    m.def("gauge_node_distance", [](const PyGaugeNode128& a, const PyGaugeNode128& b) {
        return gauge_node_distance(&a.node, &b.node);
    }, py::arg("a"), py::arg("b"),
    "Calculate L2 distance between two nodes.");
    
    m.def("gauge_node_vesica_overlap", [](const PyGaugeNode128& a, const PyGaugeNode128& b) {
        return gauge_node_vesica_overlap(&a.node, &b.node);
    }, py::arg("a"), py::arg("b"),
    "Calculate Vesica intersection volume between two nodes.");
    
    m.def("gauge_node_init", [](PyGaugeNode128& node, uint32_t id, uint8_t glyph_type,
                                 float x, float y, float z) {
        gauge_node_init(&node.node, id, static_cast<GlyfPrimitive>(glyph_type), x, y, z);
    }, py::arg("node"), py::arg("id"), py::arg("glyph_type"), 
       py::arg("x"), py::arg("y"), py::arg("z"),
    "Initialize a node with given glyph type and coordinates.");
    
    /* =========================================================================
     * Holonomy Operations
     * ========================================================================= */
    m.def("holonomy_verify_graph", [](const std::vector<PyGaugeNode128>& nodes) {
        if (nodes.empty()) return true;
        
        /* Create temporary array for C function */
        std::vector<GaugeNode128> raw_nodes;
        raw_nodes.reserve(nodes.size());
        for (const auto& n : nodes) {
            raw_nodes.push_back(n.node);
        }
        
        return holonomy_verify_graph(raw_nodes.data(), static_cast<uint32_t>(nodes.size()));
    }, py::arg("nodes"),
    "Verify holonomy invariants for all cycles in the graph.");
    
    m.def("holonomy_compute_parity", [](const std::vector<PyGaugeNode128>& nodes,
                                         const std::vector<uint32_t>& cycle) {
        if (nodes.empty() || cycle.empty()) return uint8_t(0);
        
        std::vector<GaugeNode128> raw_nodes;
        raw_nodes.reserve(nodes.size());
        for (const auto& n : nodes) {
            raw_nodes.push_back(n.node);
        }
        
        return holonomy_compute_parity(raw_nodes.data(), 
                                       const_cast<uint32_t*>(cycle.data()), 
                                       static_cast<uint32_t>(cycle.size()));
    }, py::arg("nodes"), py::arg("cycle"),
    "Compute XOR of chirality bits along a cycle.");
    
    /* =========================================================================
     * Serialization
     * ========================================================================= */
    m.def("gauge_graph_write", [](const std::string& filename, 
                                   const std::vector<PyGaugeNode128>& nodes) {
        if (nodes.empty()) return -1;
        
        std::vector<GaugeNode128> raw_nodes;
        raw_nodes.reserve(nodes.size());
        for (const auto& n : nodes) {
            raw_nodes.push_back(n.node);
        }
        
        return gauge_graph_write(filename.c_str(), 
                                 raw_nodes.data(), 
                                 static_cast<uint32_t>(nodes.size()));
    }, py::arg("filename"), py::arg("nodes"),
    "Write graph to binary file. Returns 0 on success.");
    
    m.def("gauge_graph_read", [](const std::string& filename) {
        uint32_t num_nodes = 0;
        GaugeNode128* raw_nodes = gauge_graph_read(filename.c_str(), &num_nodes);
        
        if (!raw_nodes) {
            throw std::runtime_error("Failed to read graph from " + filename);
        }
        
        std::vector<PyGaugeNode128> result;
        result.reserve(num_nodes);
        for (uint32_t i = 0; i < num_nodes; i++) {
            PyGaugeNode128 py_node;
            py_node.node = raw_nodes[i];
            result.push_back(py_node);
        }
        
        free(raw_nodes);
        return result;
    }, py::arg("filename"),
    "Read graph from binary file. Returns list of GaugeNode128.");
    
    /* =========================================================================
     * Constants
     * ========================================================================= */
    m.attr("GLYPH_COUNT") = GLYPH_COUNT;
    m.attr("GAUGE_NODE_MAGIC") = GAUGE_NODE_MAGIC;
    m.attr("GAUGE_NODE_VERSION") = GAUGE_NODE_VERSION;
    m.attr("PHI") = PHI;
    m.attr("PHI_INV") = PHI_INV;
    m.attr("PHI_SQUARED") = PHI_SQUARED;
    m.attr("GOLDEN_ANGLE") = GOLDEN_ANGLE;
    
    /* Size check */
    m.attr("GAUGE_NODE_SIZE") = sizeof(GaugeNode128);
}
