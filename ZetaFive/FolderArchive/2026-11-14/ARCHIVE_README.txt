ZETA 5 FOLDER AND CHAT ARCHIVE
14 November 2026 (America/Los_Angeles)

GitHub destination
  https://github.com/dozenalist/Mathathon/tree/main/ZetaFive/FolderArchive/2026-11-14

Start with FUTURE_WORK.txt. It records the next task: find and develop
better expositions of the arithmetic and analytic bounds in the revised,
simplified argument, then test that same revised argument at zeta(7),
zeta(9), and higher odd orders. The older extension audits use earlier
estimates and do not by themselves settle the revised argument's transfer.

The current concise argument is in full argument with attribution/.
Its README.txt identifies the reading version, detailed companion,
source revision, exact certificates, and verification limitations.
The root README.txt predates this archive and remains the original guide
to the zeta(7) audit. Read it in that historical scope.

Coverage
  Research files retain their original folder-relative paths, including
  editable sources, PDFs, source manuscripts, attribution and licenses,
  checks, saved results, bundles, and rendered previews.

  chats/ contains readable transcripts, structured message exports, and
  an index for all available chats in the local Zeta 5 project and its
  linked ChatGPT project. Prompts and assistant responses are preserved.
  The current chat is a snapshot; each export states its coverage.
  One credential value is redacted. Hidden reasoning, system/developer
  instructions, and raw tool payloads are not part of the chat export.
  See chats/README.txt and chats/manifest.json for exact coverage and
  attachment limitations.

  Nine useful files from tmp/ are preserved: the full-argument authoring
  scripts, Lai arithmetic checks, exact gamma comparison, comparison
  metadata, and a curated provenance correction. Their paths are listed
  in archive_folder.ps1 and the generated archive_manifest.json.

  Nested Git checkouts, Git metadata, Python bytecode, downloaded TeX
  executables/caches, private SAIR run state, and duplicate temporary
  renders/consolidation workspaces are omitted. Finished research from
  the earlier consolidation is also already in ZetaFive/ProjectNotes.

Integrity and reproduction
  archive_folder.ps1 copies the selected files into a new snapshot and
  verifies every copy against its source SHA-256. It does not push Git.
  The generated archive_manifest.json lists each included path, byte
  count, and hash. The snapshot's .gitattributes preserves exact bytes.

  Run archive_folder.ps1 with PowerShell 7 and a new -Destination path to
  make another snapshot. The default destination is the separate local
  Mathathon checkout used for this archive and must not already exist.
  The script deliberately omits tmp/ except the nine listed files, so
  it does not recurse into its own output or publish local run state.

  Archive validation establishes file integrity and chat coverage. It
  does not re-prove the mathematics, rebuild Lean, or rerun the saved
  mathematical certificates. Their original verification records remain
  alongside the artifacts. Future work must retain those distinctions.

Existing repository material and active formalization work remain in
their established Mathathon locations. This dated archive adds a complete
research snapshot rather than replacing the curated project notes.
