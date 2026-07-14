# Scope v3 API Checklist

## Planning

- [x] API goals defined
- [x] Endpoints identified
- [x] Response format defined
- [x] Compatibility requirements documented

---

## Implementation

- [x] Response models
- [x] Repository integration
- [x] Chapter endpoints
- [x] Search endpoints
- [ ] API tests

## Response Models

- [x] Chapter metadata response model
- [x] Required certified metadata fields
- [x] Nullable manga-arc behavior
- [x] SQLAlchemy object serialization
- [x] ISO 8601 datetime serialization
- [x] Existing API schemas preserved
- [x] Chapter-list endpoint
- [x] Individual chapter endpoint

## Chapter List Endpoint

- [x] Series chapter-list route added
- [x] Repository-backed chapter retrieval
- [x] Ascending chapter ordering
- [x] One Piece Chapters 1–1188 returned
- [x] Naruto Chapters 1–700 returned
- [x] Nullable manga arc preserved
- [x] Empty valid dataset returns an empty list
- [x] Unknown anime returns 404
- [x] Scope v2 anime endpoints remain compatible
- [x] Individual chapter endpoint

## Individual Chapter Endpoint

- [x] Individual chapter route added
- [x] Anime-scoped chapter lookup
- [x] Shared chapter response model
- [x] One Piece chapter detail validated
- [x] Naruto chapter detail validated
- [x] Nullable manga arc preserved
- [x] Unknown anime returns 404
- [x] Missing chapter returns 404
- [x] Invalid chapter number returns 422
- [x] List and detail contracts are consistent

## Chapter Metadata Search

- [x] Search response includes chapter metadata
- [x] Existing chapter-mapping search preserved
- [x] Chapter-title search implemented
- [x] Manga-arc search implemented
- [x] Exact numeric chapter search implemented
- [x] Multi-series results supported
- [x] Nullable manga arc preserved
- [x] Empty metadata search returns an empty list
- [x] Existing search response fields preserved

---

## Validation

- [ ] One Piece validation
- [ ] Naruto validation
- [ ] Regression testing

---

## Certification

- [ ] Final validation
- [ ] API certified