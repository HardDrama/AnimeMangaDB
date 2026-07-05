# 📋 AnimeMangaDB v0.29.0 Changelog

## 🌐 Website Backend Foundation

### ✨ Added
• FastAPI backend project
• API application skeleton
• Root API endpoint
• Health endpoint
• Version endpoint
• Anime endpoint
• Episodes endpoint
• Backend API test suite

### 🔄 Improved
• Connected Anime endpoint to the repository layer
• Connected Episodes endpoint to the repository layer
• Repository now supports listing anime
• Repository now supports listing episodes
• Backend now serves live data from the AnimeMangaDB database

### 🏛️ Architecture
• Introduced dedicated backend package
• Backend communicates through the repository layer rather than directly accessing the database
• Continued separation between scraper, repository, and API layers
• Established foundation for REST API development

### 🧪 Testing
• Added API endpoint tests
• Added root endpoint validation
• Added health endpoint validation
• Added version endpoint validation
• Added anime endpoint validation
• Added episodes endpoint validation
• Increased automated test coverage from 28 to 33 tests
• All automated tests continue to pass

### ✅ Validation
• FastAPI application launches successfully
• Interactive Swagger documentation available
• Anime endpoint returns live database records
• Episodes endpoint returns live database records
• Backend successfully integrates with repository layer
• Final test result: 33 automated tests passing