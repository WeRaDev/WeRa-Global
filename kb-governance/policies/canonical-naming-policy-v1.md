# Canonical Naming and Alias Handling Policy v1
version: 1.0
status: active-draft
source_of_truth: Reusable artifact `21-KB-Controlled-Vocabulary-and-Entity-Standards-v1`

## Purpose
Enforce terminology consistency across all split KB repositories and prevent naming drift.

## Canonical product names
| Canonical | Alias (deprecated or variant) | Rule |
|---|---|---|
| `WeRaSolar` | Solar business line | Use canonical in active docs |
| `SolarSeed` | Solar Seed, SolarSeat | Use canonical in active docs |
| `WERA Cloud` | WeRaCloud, Vera Cloud | Use canonical in active docs |
| `City of Light` | CityLight | Use only as conceptual or roadmap layer |

## Usage rules
1. Canonical names are mandatory in:
   - standards, policy, operational, and customer-facing KB records.
2. Aliases are allowed only when:
   - quoting historical source text, or
   - documenting deprecation mapping.
3. Alias usage must include explicit label:
   - `alias/deprecated`.

## CI enforcement rules
- Reject new or modified lines containing non-labeled deprecated aliases in active docs.
- Permit aliases only when one of the following markers appears in the same section:
  - `alias/deprecated`
  - `historical quote`
  - `legacy naming context`

## Governance gate
Any change to canonical name set or alias policy requires three-entity approval:
- WeRa Capital
- WeRa STAK
- WeRa Association

## Migration guidance
- During artifact migration, preserve original wording in source capture blocks.
- Normalize active operational language to canonical naming during destination rewrite.
