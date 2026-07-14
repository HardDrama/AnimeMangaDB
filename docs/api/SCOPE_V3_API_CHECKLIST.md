# Scope v3 API Checklist

## Planning

- [x] API goals defined
- [x] Endpoints identified
- [x] Response format defined
- [x] Compatibility requirements documented

---

## Implementation

- [ ] Response models
- [ ] Repository integration
- [ ] Chapter endpoints
- [ ] Search endpoints
- [ ] API tests

## Response Models

- [x] Chapter metadata response model
- [x] Required certified metadata fields
- [x] Nullable manga-arc behavior
- [x] SQLAlchemy object serialization
- [x] ISO 8601 datetime serialization
- [x] Existing API schemas preserved
- [ ] Chapter-list endpoint
- [ ] Individual chapter endpoint

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
- [ ] Individual chapter endpoint

---

## Validation

- [ ] One Piece validation
- [ ] Naruto validation
- [ ] Regression testing

---

## Certification

- [ ] Final validation
- [ ] API certified