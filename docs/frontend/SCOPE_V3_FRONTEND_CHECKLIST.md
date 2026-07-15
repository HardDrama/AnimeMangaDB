# Scope v3 Frontend Checklist

## Planning

- [x] Frontend responsibilities defined
- [x] Backend responsibilities defined
- [x] Certified API inputs documented
- [x] Supported series documented
- [x] Nullable metadata behavior documented
- [x] Compatibility requirements documented
- [x] Responsive requirements documented
- [x] Accessibility requirements documented

---

## API Client

- [x] Chapter metadata JSDoc contract added
- [x] Series chapter-list request added
- [x] Chapter-detail request added
- [x] Search response contract extended
- [x] Nullable manga-arc typing documented
- [x] Existing API field names preserved
- [x] Existing client error-handling convention preserved
- [x] No UI behavior changed

## Future API-Dependent Enhancements

- [ ] Add anime identity to chapter metadata search results
- [ ] Link global chapter search results to chapter detail pages
- [ ] Add anime-scoped chapter-to-episode endpoint
- [ ] Display episode mappings on chapter detail pages

---

## Series Chapter List

- [x] Reusable chapter metadata card added
- [x] Reusable chapter metadata list added
- [x] Anime detail page loads chapter metadata
- [x] Existing episode list preserved
- [x] Numerical API ordering preserved
- [x] Chapter-number filtering added
- [x] Chapter-title filtering added
- [x] Manga-arc filtering added
- [x] Loading state added
- [x] Error state added
- [x] Empty state added
- [x] No-match state added
- [x] Null manga arc displayed as not applicable
- [x] Responsive chapter grid added

---

## Chapter Detail

- [x] Chapter-detail route added
- [x] Chapter-detail page added
- [x] Chapter cards link to details
- [x] Anime title displayed
- [x] Chapter number displayed
- [x] Chapter title displayed
- [x] Manga arc displayed
- [x] Null manga arc displayed as not applicable
- [x] Canonical source link added
- [x] Last-updated timestamp displayed
- [x] Breadcrumb navigation added
- [x] Back-to-anime navigation added
- [x] Loading state added
- [x] Error state added
- [x] Direct URL navigation validated
- [x] Responsive detail layout validated

---

## Search

- [x] Chapter Metadata section added
- [x] Scope v2 chapter mappings preserved
- [x] Search result types clearly distinguished
- [x] Chapter numbers displayed
- [x] Chapter titles displayed
- [x] Manga arcs displayed
- [x] Null manga arc displayed as not applicable
- [x] Canonical source links added
- [x] Empty chapter metadata results handled
- [x] Multi-series numeric search validated
- [x] Search identity limitation documented
- [ ] Internal chapter-detail links from search

---

## Certified Dataset Validation

- [x] One Piece chapter-list validation
- [x] One Piece chapter-detail validation
- [x] One Piece search validation
- [ ] Naruto chapter-list validation
- [ ] Naruto chapter-detail validation
- [ ] Naruto Chapter 700 validation
- [ ] Naruto search validation

## One Piece Frontend Validation

- [x] Anime detail page validated
- [x] All 1188 chapter records represented
- [x] Chapter range 1–1188 validated
- [x] Chapter-list rendering validated
- [x] Chapter-number filtering validated
- [x] Chapter-title filtering validated
- [x] Manga-arc filtering validated
- [x] Empty filter state validated
- [x] Chapter detail navigation validated
- [x] Representative chapter details validated
- [x] Canonical source links validated
- [x] Chapter metadata search validated
- [x] Existing episode behavior preserved
- [x] Scope v2 mappings preserved
- [x] Desktop behavior validated
- [x] Tablet behavior validated
- [x] Mobile behavior validated
- [x] Accessibility review completed

---

## Compatibility

- [ ] Existing anime views preserved
- [ ] Existing episode views preserved
- [ ] Existing episode mappings preserved
- [ ] Existing search behavior preserved

---

## Validation

- [ ] Frontend tests pass
- [ ] Production build passes
- [ ] Frontend lint passes
- [ ] Backend regression suite passes
- [ ] Desktop validation completed
- [ ] Tablet validation completed
- [ ] Mobile validation completed
- [ ] Accessibility review completed
- [ ] Final frontend validation completed

---

## Certification

- [ ] Scope v3 frontend integration certified