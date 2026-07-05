# 📋 AnimeMangaDB v0.30.0 Changelog

## 🚀 API Expansion

### ✨ Added
• Pydantic API response models
• Anime detail endpoint
• Episode detail endpoint
• Episode lookup by anime and episode number
• Episode chapters endpoint
• Episode chapter response model

### 🔄 Improved
• Anime list endpoint now uses typed response models
• Episodes list endpoint now uses typed response models
• Repository expanded with API-focused query methods
• API responses are now validated and documented automatically by FastAPI

### 🏛️ Architecture
• Introduced backend response model package
• Continued separation between database models and API models
• Expanded repository layer to support REST API queries
• Improved API consistency through typed responses

### 🧪 Testing
• Added anime detail endpoint test
• Added episode detail endpoint test
• Added episode lookup endpoint test
• Added episode chapters endpoint test
• Increased automated test coverage from 33 to 37 tests
• All automated tests continue to pass

### ✅ Validation
• Anime endpoint returns typed responses
• Episodes endpoint returns typed responses
• Anime detail endpoint handles existing and missing records
• Episode detail endpoint handles existing and missing records
• Episode lookup endpoint successfully queries by anime and episode number
• Episode chapters endpoint returns chapter mappings
• Final test result: 37 automated tests passing