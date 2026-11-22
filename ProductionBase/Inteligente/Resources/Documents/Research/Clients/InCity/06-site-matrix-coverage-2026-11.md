# InCity site vs Content Matrix coverage

**Date:** 2026-11-18

## Live public routes (HTTP 200)
| URL | In website.menu | In matrix before fix | Notes |
|-----|-----------------|----------------------|-------|
| `/` | yes | yes | Home |
| `/tours-from-lisbon` | yes | **no** | Core commercial |
| `/tours-from-sintra` | yes | **no** | Core commercial |
| `/intv` | yes | **no** | Video/stories |
| `/reviews` | yes | **no** | Trust |
| `/vasco-da-lama` | yes | **no** | About/Goodfoot |
| `/contactus` | no (form still live) | yes | Contact |
| `/privacy` | no | yes | Thin policy page |

404 examples (not product pages): `/about`, `/blog`, `/tours`, `/goodfoot`, `/contact`.

## Root cause
Seed `incity_matrix_v1.json` only included Home + Contact + Privacy (P1 pilot minimum). Menu routes for tours/about/reviews were never seeded.

## Fix
Import `incity_matrix_v2_extra_pages.json` (upsert by url/anchor) — adds five pages + analysis sections without wiping Home finals.

## Follow-up content workflow
1. Import extra pages
2. Operator sessions per page (or batch accept suggestions where safe)
3. Verify run scoped to new URLs
4. Apply checklist for approved rows
