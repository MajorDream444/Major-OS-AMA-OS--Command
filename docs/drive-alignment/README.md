# GitHub and three-Drive alignment

The index records the initial public-safe operating-document set. Account-specific mirror manifests and original IDs stay inside each private Drive mirror folder. No private contacts or client data are copied into this public repository.

GitHub holds the canonical operating instructions and code. ArtMobAGI, MajorNFTs and Hanzo each have an intentional Drive mirror. Mirrored files keep their exact source bytes; taxonomy tags live in the associated manifest, not injected into the original text. This avoids changing hashes just to add metadata. Each record has fourteen meaningful namespace tags.

The duplicate is a tracked mirror, not an unmanaged copy. Match by stable mirror_id and provider file ID, never title alone. Record repo path, commit/snapshot, source SHA256, Drive file ID, account, source timestamp, mirror timestamp and verification status. Later updates replace the same Drive file ID after fetching its current metadata. Do not repeatedly create new copies.

Before a future sync: compare GitHub hash, stored last-synced hash and current Drive bytes. If only GitHub changed, update the Drive mirror. If Drive changed independently, preserve both versions and raise a conflict; do not overwrite. If both changed, require explicit reconciliation. Never merge documents by newest timestamp alone. Google-native exports have a different byte format; compare a defined normalized-text representation and record the export format separately.

Drive-native original assets remain original sources and need separate provenance records and classification before a repo copy. Public-safe derivatives may be committed after content review; private originals need a private repository or restricted storage. Authorization to align storage is not authorization to publish private material.

This initial copy is not a continuous sync daemon. Do not report future synchronization as enabled until a scheduled runner, credentials, conflict handling and end-to-end verification are working. The current Yawdie worker is not a Drive adapter.
