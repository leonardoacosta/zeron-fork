# Scoped skills viewer specification

## ADDED Requirements

### Requirement: Host-bound skill inventory
The system MUST provide a read-only inventory of skills discovered for an explicitly selected host and harness. The inventory MUST identify global/user or project scope, provenance, and whether each entry is effective or shadowed. The viewer MUST NOT infer provenance or scope from a display path. It MUST preserve existing completion and delivery behavior.

#### Scenario: View global inventory without project context
- **WHEN** a user selects a supported host and the global scope
- **AND** no project directory is active
- **THEN** the viewer lists discovered global/user skills with their provenance and effective/shadowed status
- **AND** it does not require or invent a project directory.

#### Scenario: View project inventory
- **WHEN** a user selects project scope with an explicit active project
- **THEN** the viewer displays that project context and lists skills discovered for it
- **AND** it distinguishes project entries from global entries and indicates shadowing under the established precedence rules.

#### Scenario: Project scope has no context
- **WHEN** a user selects project scope without an active project
- **THEN** the viewer explains that project context is unavailable
- **AND** it does not scan an arbitrary current directory.

#### Scenario: Shadowed entries remain inspectable
- **WHEN** a skill is shadowed by a higher-precedence entry
- **THEN** the inventory still shows it as shadowed with its own provenance
- **AND** the completion catalog continues to use its existing effective-entry behavior.

#### Scenario: Discovery is partial or fails
- **WHEN** one discovery source fails while another succeeds
- **THEN** the viewer reports the failed source and retains successful entries
- **AND** an entirely unavailable result is distinct from a valid empty inventory.

### Requirement: Safe bounded content inspection
The system MUST allow content inspection only for an inventory entry bound to the selected host and its authorized content-read boundary. Remote content reads MAY be performed through the selected host's RPC. The system MUST NOT open a remote host path through the local filesystem. For local reads, it MUST enforce canonical path containment and a documented symlink policy. It MUST enforce limits on traversal, bytes read, and returned content. Unsupported or unavailable content MUST have an explicit status. Content MUST render as inert, escaped text.

#### Scenario: Read available local skill
- **WHEN** a user opens an entry with locally readable content under an approved root
- **THEN** the viewer displays its bounded content as inert text
- **AND** associates the result with the selected host and inventory entry.

#### Scenario: Remote skill content read through selected host
- **WHEN** a selected remote host advertises a skill and supports an authorized content-read RPC
- **THEN** the viewer reads content through that selected host's RPC and displays bounded content as inert text
- **AND** never opens the host path using local filesystem APIs.

#### Scenario: Remote/native entry has no supported content reader
- **WHEN** a selected host advertises a skill without a supported content-read boundary
- **THEN** the viewer shows its metadata and reports content as unavailable or unsupported
- **AND** does not attempt a local read using the host-provided path.

#### Scenario: Unsafe path or escaping symlink
- **WHEN** the entry resolves outside approved roots or through a disallowed symlink
- **THEN** the system refuses the read and reports unsafe/unavailable content
- **AND** returns no file content.

#### Scenario: Permission denied or file absent
- **WHEN** an eligible file cannot be read because access is denied or it disappeared
- **THEN** the viewer reports permission denied or stale/missing content distinctly
- **AND** keeps the inventory available.

#### Scenario: File changes between discovery and read
- **WHEN** the inventory identity or file metadata no longer matches at read time
- **THEN** the system returns a stale-entry result and requests refresh
- **AND** does not display unverified content.

#### Scenario: Read or scan limit reached
- **WHEN** traversal, file-size, read, or response limits are exceeded
- **THEN** the system returns a limit-exceeded status without presenting truncated content as complete.

### Requirement: Desktop and mobile accessible viewer
The system MUST provide the viewer on desktop and mobile in the initial delivery. Both layouts MUST expose host/harness, scope, project context when relevant, skill identity, provenance, shadowing, and content availability. Controls and status MUST be keyboard and screen-reader accessible. Mobile MUST provide a clear path between the list and selected skill details.

#### Scenario: Desktop selection and details
- **WHEN** a user selects a skill on desktop
- **THEN** the viewer presents its metadata and content or unavailability reason
- **AND** selection and status are announced accessibly with predictable focus.

#### Scenario: Mobile list and detail
- **WHEN** a user selects a skill on mobile
- **THEN** the viewer presents details and provides an accessible return path to the list
- **AND** retains the selected host and scope context.

#### Scenario: Loading, empty, or error state
- **WHEN** discovery or content is loading, empty, partially failed, or unavailable
- **THEN** the UI presents a distinct accessible state rather than a blank or ambiguous panel.

### Requirement: Optional Jcode host integration
The viewer MUST support existing host integrations without requiring Jcode. It MAY expose Jcode-specific discovery only after the host's discovery capability and behavior are verified. Jcode absence or unsupported discovery MUST NOT break baseline viewer use.

#### Scenario: Jcode unavailable
- **WHEN** Jcode is not installed, not selected, or lacks verified skill discovery
- **THEN** the viewer remains usable with other supported hosts
- **AND** does not fail startup, build, or baseline tests because of Jcode.

#### Scenario: Jcode discovery verified
- **WHEN** Jcode capability and its scope/provenance semantics have been verified
- **THEN** its discovered skills appear only for the selected Jcode host with the same explicit scope and safe-content rules.

### Requirement: Completion compatibility
The viewer MUST NOT alter existing skill or command completion behavior.

#### Scenario: Existing completion remains independent
- **WHEN** skill discovery is unavailable or partially fails while command discovery succeeds, or vice versa
- **THEN** the existing composer retains the independently available completion rows and delivery behavior.
