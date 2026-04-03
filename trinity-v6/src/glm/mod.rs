//! GLM (Geometric Language Model) Module
//! 
//! Persistent state management for distributed model shards
//! with Reed-Solomon protection and zero-allocation design.

#![no_std]

pub mod state;

// Re-export primary types for convenience
pub use state::{
    GLMState, 
    GLMMetadata, 
    Cryogen, 
    Fellowship as GLMFellowship,
    RSEncoder,
    PersistenceError,
    FellowshipError,
    CheckpointPool,
    CheckpointHandle,
    SyncStatus,
    ConsensusState,
};
