# Unreleased Update Info
## Version 0.1.0
- Repository Created
## Version 0.2.0
- Python environment
## Version 0.3.0
- Data models
## Version 0.4.0
- Base extractor
## Version 0.5.0 
- Browser Client
## Version 0.6.0
- HTML parser
## Version 0.7.0
- Provider configuration

# Day 2 AM Updates

## Version 0.8.0
### Added
- BaseProvider
- FandomProvider
- Provider configuration model
- Config loader
- One Piece provider configuration
- URL generation abstraction
### Improved
- Separated provider logic from parser logic
- Continued building a modular scraping architecture

## Version 0.9.0
### Added
- Configurable selector engine
### Improved
- Testing of minor changes

## Version 0.10.0
### Added
- FandomExtractor
- Generic parsing pipeline
- Required field extraction helper
- HTML fixture parsing
- End-to-end creation of EpisodeData
### Improved
- Successfully parsed a real Fandom HTML page into a validated model
- Established the foundation for extracting manga chapters, arcs, and additional metadata

# Day 2 PM Updates
## Version 0.11.0
### Added
- HTML inspection workflow
- Chapter selector
- Text parsing helper
- Chapter number extraction
- End-to-end chapter mapping
### Improved
- **FandomExtractor** now returns real chapter data instead of placeholders

# Day 3 AM Updates

## Version 0.12.0

### Added
- **extract_all_numbers()** utility
- Unit tests for chapter parsing
- Support for extracting multiple chapter numbers from text

### Improved
- Text parsing utilities are now ready to handle more complex episode-to-manga mappings

## Version 0.13.0

### Improved
- Fandom Extracter
- Chapter numbers

## Version 0.13.1

### Improved
- Text Parser
- Fandom Extractor

## Version 0.14.0

### Added
- Added **adapted_chapters** to the **EpisodeData** model
- Updated **FandomExtractor** to populate the **adapted_chapters** field
- Began storing both complete chapter lists and summary chapter information

### Changed
- Improved the episode data model to better represent episodes that adapt multiple manga chapters
- Continued shifting the project from a proof-of-concept scraper toward a structured data pipeline
- Refined the parser architecture in preparation for persistent database storage

### Fixed
- Fixed chapter parsing logic to avoid incorrectly treating page numbers as manga chapter numbers
- Corrected variable naming inconsistencies during chapter extraction

### Developer Notes
- Decided to evolve AnimeMangaDB into a feature-rich lookup website over time, beginning with simple episode-to-manga lookup tool
- Established a versioned development workflow using feature branches, semantic versioning, and changelog entries
- Continued following an incremental, test-first development process

## Version 0.15.0

### Added
- Implemented SQLite database using SQLAlchemy ORM
- Created database engine and session management
- Introduced delarative base class for ORM
- Added **Anime** database model with: Unique title constraint, Provider metadata (fandom, etc.), and Base URL Storage
- Added **Episode** database model with: Foreign key relationship to **Anime**, and Episode metadata (number, title, arc, source URL, timestamp)
- Implemented repository layer
- Added full database initialization script
- Established relational schema: One-to-many relationship: Anime -> Episodes

### Changed
- Updated scraper pipeline to use repository pattern instead of direct DB access
- Refractored data flow to use **EpisodeData** (Pydantic) as intermediate representation
- Switched HTTP fetching to Playwright-based browser clients for anti-bot resilience

### Improved Architecture
- Clear seperation of concerns
  - Provider -> URL generation
  - HTTP/Browser Client -> fetching HTML
  - Extractor -> parsing structured data
  - Repository -> persistence Layer
- Introduced structured pipeline:
  - Fetch -> Extract -> Transform -> Persist

### Verified
- Successfully scraped One Piece episode page
- Successfully inserted:
  - 1 Anime record
  - 1 Episode Record
- Verified no duplicate anime entries on repeated runs
- Confirmed SQLite persistence works correctly

### Fixed
- Fixed 403 Forbidden issue by routing scraping through Playwright browser client
- Fixed repository structure and method scoping issues
- Fixed SQLAlchemy model initialization and relationship setup

# Version 0.16.0

## Release Date: June 30,2026

### New Features
- Added normalized **episode_chapters** database table
- Implemented **EpisodeChapter** SQLAlchemy model
- Added repository support for storing adapted manga chapters
- Linked episodes to individual chapter records
- Extended the scraping pipeline to persist chapter relationships automatically

### Improvements
- Refractored chapter extraction to use dedicated parsing logic
- Improved separation between:
  - HTML parsing
  - Data extraction
  - Repository/database persistence
- Updated **EpisodeData** model to better represent chapter information
- Simplified **main.py** into cleaner ingestion pipeline

### Bug Fixes
- Fixed chapter extraction returning page numbers instead of chapter numbers
- Fixed multiple paeser inconsistencies caused by duplicated parsing functions
- Resolved model/schema mismatches between
  - Extractor
  - Pydantic models
  - Repository layer
- Fixed several Python scope/import issues encountered during development
- Corrected chapter persistence so adapted chapters are now written to the database successfully

### Database
New table:
- **episode_chapters**
Relationships: Anime -> Episodes -> EpisodeChapters

### Verification
Successfully verified end-to-end pipeline:
- HTML download
- HTML parsing
- Episode extraction
- Chapter extraction
- Episode insertion
- Chapter insertion
- Database persistence

# Version 0.17.0

## Added
- Repository methods for retrieving existing episodes
- Duplicate detection for episode creation
- Duplicate detection for chapter mapping
- Database uniqueness constraints for Anime, Episode, and EpisodeChapter
- SQLAlchemy 2.0 typed model for EpisodeChapter

## Changed
- Repository now reuses existing episodes instead of inserting duplicates
- Chapter insertion is now idempotent
- Database schema now enforces data integrity
- EpisodeChapter model now follows the same SQLAlchemy style as the rest of the project

## Fixed
- Duplicate episode insertion on repeated scraper runs
- Duplicate episode-chapter relationships
- Potential database inconsistency caused by repeated imports

# v0.18.0 — Changelog
## Added
- Added FandomEpisodeIndexCrawler for discovering episode numbers from the One Piece Fandom Episode Guide.
- Added crawler-driven scraping flow in main.py.
- Added development crawl limit to avoid long full-dataset runs during testing.
## Changed
- Refactored main.py so episode discovery is handled by a crawler instead of hardcoded episode numbers.
- Restored FandomProvider to a clean URL-building responsibility.
- Separated crawler, provider, extractor, and repository responsibilities more clearly.
## Improved
- Full episode discovery now works across saga pages.
- Verified full crawl successfully indexed the One Piece episode set.
- Reduced console noise by removing temporary crawler debug output.
- Development runs now process only the first 5 discovered episodes for faster testing.
## Fixed
- Fixed broken episode guide assumptions caused by treating the hub page as a flat episode index.
- Fixed provider/crawler responsibility confusion.
- Fixed missing chapter output display for episodes without manga mappings.
## Developer Notes
- Full crawl took about 1.8 hours during validation.
- Current development limit is intentionally hardcoded:
> episode_numbers = episode_numbers[:5]
- This should later become configurable through CLI flags or config settings.

# v0.19.0 Changelog
## Release Summary
Version 0.19.0 transforms the scraper from a fixed prototype into a configurable application. Scraper behavior is now controlled through configuration rather than source code, making development, testing, and future expansion significantly easier.
## Added
### Configurable Scraper Settings
Added a dedicated scraper configuration section to provider configuration files.
Supported options:
- max_episodes
- start_episode
- end_episode
- full_crawl
These options allow scraper behavior to be changed without modifying Python code.
### Scraper Configuration Model
Added **ScraperConfig** to the configuration model.
Configuration is now strongly validated through Pydantic alongside existing provider settings.
### Episode Range Filtering
Added optional episode range support.
Examples:
- Scrape only Episode 1–20
- Scrape only Episode 500–550
- Scrape newest episodes only
### Full Crawl Mode
Added support for production crawling.
When enabled:
- ignores development limits
- crawls every discovered episode
- requires no code modifications
## Changed
### main.py
Refactored scraper execution to read crawl behavior from configuration.
Removed hardcoded development settings.
### Configuration System
Expanded provider configuration to support scraper execution settings while remaining backward compatible with the overall configuration structure.
## Improved
### Development Workflow
Development testing is significantly faster.
Examples:
- scrape first 5 episodes
- scrape a small episode range
- perform full production crawl
All controlled through JSON configuration.
## Maintainability
Scraper behavior is now data-driven rather than code-driven.
This greatly reduces the need to edit Python files during normal testing.
## Validation
Successfully validated:
- Development crawl
- Episode range crawl
- Full crawl mode
Full crawl successfully progressed through the discovered episode list without requiring code changes.

# :clipboard: AnimeMangaDB v0.20.0 Changelog
## :rocket: Performance & Developer Experience
### :sparkles: Added
- Crawl progress reporting ([1/5], [2/5], etc.)
- Crawl elapsed time reporting
- Crawl summary statistics
- Per-episode error handling
- Failed episode reporting
### :arrows_counterclockwise: Improved
- Cleaner crawl summary output
- More readable console logs during long scraping sessions
- Scraper now continues when an individual episode fails instead of stopping the entire crawl
### :tools: Development
- Attempted browser session reuse for improved performance
- Reverted browser reuse after discovering Cloudflare compatibility issues
- Preserved stable and reliable scraping behavior
### :white_check_mark: Validation
- Verified progress reporting
- Verified elapsed time reporting
- Verified crawl summary statistics
- Verified error handling logic
- Successfully completed multiple validation crawls

# :clipboard: AnimeMangaDB v0.21.0 Changelog

## :test_tube: Automated Testing Foundation

### :sparkles: Added
• Organized test suite into dedicated modules
• Repository unit tests
• Provider unit tests
• Provider configuration tests
• Extractor fixture tests
• Chapter relationship tests

### :arrows_counterclockwise: Improved
• Better test organization for future growth
• Isolated in-memory database testing
• Increased confidence when refactoring scraper code

### :tools: Testing Coverage
• Text parser validation
• Episode URL generation
• Provider configuration loading
• Anime repository operations
• Episode repository operations
• Episode ↔ Chapter relationship handling
• Duplicate prevention
• Extractor validation using saved HTML fixtures

### :white_check_mark: Validation
• Test suite reorganized without breaking functionality
• Repository tests isolated from production database
• All automated tests passing

Final Result:
• 16 automated tests passing

# :clipboard: AnimeMangaDB v0.22.0 Changelog

## :arrows_counterclockwise: Update & Synchronization

### :sparkles: Added
• Episode update detection
• Existing episode record updates
• Chapter mapping comparison
• Chapter mapping replacement
• Tests for update detection
• Tests for chapter replacement logic

### :arrows_counterclockwise: Improved
• Existing episodes can now be refreshed when source data changes
• Chapter mappings can now be compared against newly scraped data
• Changed chapter mappings can now be replaced automatically
• Scraper is now closer to a true sync pipeline instead of only an importer

### :test_tube: Testing
• Added episode update detection tests
• Added episode update behavior tests
• Added chapter mapping comparison tests
• Added chapter replacement tests

### :white_check_mark: Validation
• Repository update logic verified
• Chapter mapping sync logic verified
• Scraper integration verified
• Final test result: 22 tests passing

# :clipboard: AnimeMangaDB v0.23.0 Changelog

## :globe_with_meridians: Multi-Series Configuration Support

### :sparkles: Added
• Initial multi-series configuration support
• Naruto provider configuration placeholder
• Config path metadata
• Multi-series configuration loading tests
• Runtime configuration path argument support

### :arrows_counterclockwise: Improved
• Scraper can now load different provider configuration files
• Active series and configuration are displayed at startup
• Configuration system prepared for multiple anime series
• Reduced hardcoded One Piece dependencies

### :test_tube: Testing
• Added Naruto configuration loading test
• Verified multiple provider configurations load successfully
• Verified runtime configuration selection
• All existing tests continue to pass

### :white_check_mark: Validation
• Successfully loaded One Piece configuration
• Successfully loaded Naruto configuration
• Verified runtime configuration switching
• Final test result: 23 automated tests passing

# :clipboard: AnimeMangaDB v0.24.0 Changelog

## :computer: Command Line Interface

### :sparkles: Added
• Command line interface using argparse
• Runtime configuration selection (`--config`)
• Runtime full crawl override (`--full-crawl`)
• Runtime episode range overrides (`--start-episode`, `--end-episode`)
• Runtime maximum episode override (`--max-episodes`)
• Dry run mode (`--dry-run`)

### :arrows_counterclockwise: Improved
• Configuration can now be overridden without editing JSON files
• Development and testing workflow is significantly faster
• Automatic CLI help menu (`--help`)
• Scraper startup now clearly displays the active series and configuration

### :test_tube: Testing
• Verified default configuration loading
• Verified runtime configuration switching
• Verified full crawl override
• Verified runtime episode filtering
• Verified runtime max episode override
• Verified dry run mode
• All automated tests continue to pass

### :white_check_mark: Validation
• CLI successfully controls scraper behavior
• Configuration overrides work correctly
• Dry run performs no scraping or database writes
• Final test result: 23 automated tests passing

# :clipboard: AnimeMangaDB v0.25.0 Changelog

## :fish_cake: Naruto Support Foundation

### :sparkles: Added
• Fandom page inspection tool
• Saved inspection output for offline analysis
• URL argument support for the inspection tool
• Table preview support for Fandom inspection
• Naruto episode page analysis workflow
• Naruto episode index crawler
• Naruto title-based episode URL support
• Naruto chapter parsing support
• Naruto crawler smoke test

### :arrows_counterclockwise: Improved
• Scraper now supports both numeric and title-based episode URLs
• FandomExtractor now uses provider-configured selectors instead of hardcoded chapter selectors
• Chapter parser now supports formats such as "Naruto Chapter #1"
• Scraper architecture expanded to support multiple Fandom wiki structures

### :test_tube: Testing
• Added Naruto episode crawler smoke test
• Added Naruto chapter parsing test
• Verified Naruto episode discovery
• Verified title-based URL scraping
• Verified chapter extraction for Naruto Episode 1
• All automated tests continue to pass

### :white_check_mark: Validation
• Successfully discovered Naruto episode URLs from List of Animated Media
• Successfully scraped Naruto Episode 1
• Successfully mapped Naruto Episode 1 → Manga Chapter 1
• Final test result: 25 automated tests passing

# :clipboard: AnimeMangaDB v0.26.0 Changelog

## :construction_site: Generic Provider Framework

### :sparkles: Added
• EpisodeReference model for standardized episode discovery
• BaseEpisodeIndexCrawler abstract interface
• Episode crawler factory for provider selection
• Unified crawler architecture across supported series

### :arrows_counterclockwise: Improved
• One Piece crawler now returns EpisodeReference objects
• Naruto crawler now returns EpisodeReference objects
• Main scraper now works with a unified EpisodeReference model
• Removed series-specific crawler logic from main.py
• Simplified crawler selection through a centralized factory

### :test_tube: Testing
• Updated Naruto crawler tests for EpisodeReference
• Verified One Piece dry-run with new architecture
• Verified Naruto dry-run with new architecture
• Confirmed EpisodeReference integration across all crawlers
• All automated tests continue to pass

### :classical_building: Architecture
• Established a common interface for all episode index crawlers
• Standardized crawler output regardless of provider implementation
• Reduced coupling between the application core and provider-specific code
• Prepared the framework for adding future anime series with minimal core changes

### :white_check_mark: Validation
• One Piece crawler successfully returns EpisodeReference objects
• Naruto crawler successfully returns EpisodeReference objects
• Factory correctly selects the appropriate crawler
• Main scraper successfully processes multiple providers through a shared interface
• Final test result: 25 automated tests passing

# :clipboard: AnimeMangaDB v0.27.0 Changelog

## :jigsaw: Provider Plugin Architecture

### :sparkles: Added
• Provider factory for centralized provider creation
• Extractor factory for centralized extractor creation
• Repository factory for centralized repository creation
• ScraperServices container for dependency management
• Dedicated services package for scraper components

### :arrows_counterclockwise: Improved
• main.py now initializes scraper components through ScraperServices
• Centralized dependency creation across the scraper pipeline
• Reduced coupling between application startup and implementation details
• Simplified dependency management for future providers and services

### :classical_building: Architecture
• Provider creation abstracted behind a factory
• Extractor creation abstracted behind a factory
• Repository creation abstracted behind a factory
• Scraper dependencies grouped into a reusable service container
• Continued separation of application orchestration from implementation

### :test_tube: Testing
• Verified provider factory integration
• Verified extractor factory integration
• Verified repository factory integration
• Verified ScraperServices integration
• Verified One Piece dry-run
• Verified Naruto dry-run
• All automated tests continue to pass

### :white_check_mark: Validation
• One Piece scraper continues to function correctly
• Naruto scraper continues to function correctly
• Scraper startup now relies on shared service initialization
• Final test result: 25 automated tests passing

# :clipboard: AnimeMangaDB v0.28.0 Changelog

## :arrows_counterclockwise: Scraper Pipeline Refactor

### :sparkles: Added
• ScraperPipeline service for episode scraping workflow
• Dedicated pipeline service module
• Initial ScraperPipeline unit test suite
• Fake dependency test framework for isolated pipeline testing

### :arrows_counterclockwise: Improved
• Moved episode scraping workflow out of main.py
• main.py now focuses on application orchestration only
• Centralized scraping logic into a reusable service
• Improved separation of concerns between orchestration and business logic

### :classical_building: Architecture
• ScraperPipeline now coordinates provider, client, extractor, and repository interactions
• Reduced responsibilities of main.py
• Improved service-oriented architecture
• Established foundation for future pipeline extensions (parallel scraping, retries, progress callbacks, etc.)

### :test_tube: Testing
• Added ScraperPipeline construction test
• Added successful episode scrape test using fake dependencies
• Added no-chapter episode scrape test
• Increased automated test coverage from 25 to 28 tests
• All automated tests continue to pass

### :white_check_mark: Validation
• One Piece scraping continues to function correctly
• Naruto scraping continues to function correctly
• Dry-run behavior unchanged
• Pipeline successfully handles episodes with and without chapter mappings
• Final test result: 28 automated tests passing

# :clipboard: AnimeMangaDB v0.29.0 Changelog

## :globe_with_meridians: Website Backend Foundation

### :sparkles: Added
• FastAPI backend project
• API application skeleton
• Root API endpoint
• Health endpoint
• Version endpoint
• Anime endpoint
• Episodes endpoint
• Backend API test suite

### :arrows_counterclockwise: Improved
• Connected Anime endpoint to the repository layer
• Connected Episodes endpoint to the repository layer
• Repository now supports listing anime
• Repository now supports listing episodes
• Backend now serves live data from the AnimeMangaDB database

### :classical_building: Architecture
• Introduced dedicated backend package
• Backend communicates through the repository layer rather than directly accessing the database
• Continued separation between scraper, repository, and API layers
• Established foundation for REST API development

### :test_tube: Testing
• Added API endpoint tests
• Added root endpoint validation
• Added health endpoint validation
• Added version endpoint validation
• Added anime endpoint validation
• Added episodes endpoint validation
• Increased automated test coverage from 28 to 33 tests
• All automated tests continue to pass

### :white_check_mark: Validation
• FastAPI application launches successfully
• Interactive Swagger documentation available
• Anime endpoint returns live database records
• Episodes endpoint returns live database records
• Backend successfully integrates with repository layer
• Final test result: 33 automated tests passing

# :clipboard: AnimeMangaDB v0.30.0 Changelog

## :rocket: API Expansion

### :sparkles: Added
• Pydantic API response models
• Anime detail endpoint
• Episode detail endpoint
• Episode lookup by anime and episode number
• Episode chapters endpoint
• Episode chapter response model

### :arrows_counterclockwise: Improved
• Anime list endpoint now uses typed response models
• Episodes list endpoint now uses typed response models
• Repository expanded with API-focused query methods
• API responses are now validated and documented automatically by FastAPI

### :classical_building: Architecture
• Introduced backend response model package
• Continued separation between database models and API models
• Expanded repository layer to support REST API queries
• Improved API consistency through typed responses

### :test_tube: Testing
• Added anime detail endpoint test
• Added episode detail endpoint test
• Added episode lookup endpoint test
• Added episode chapters endpoint test
• Increased automated test coverage from 33 to 37 tests
• All automated tests continue to pass

### :white_check_mark: Validation
• Anime endpoint returns typed responses
• Episodes endpoint returns typed responses
• Anime detail endpoint handles existing and missing records
• Episode detail endpoint handles existing and missing records
• Episode lookup endpoint successfully queries by anime and episode number
• Episode chapters endpoint returns chapter mappings
• Final test result: 37 automated tests passing

# 📋 AnimeMangaDB v0.31.0 Changelog

## 🖥️ Frontend Foundation

### ✨ Added
• React frontend project powered by Vite
• Frontend API client module
• Anime list page
• Basic dark-themed user interface
• Anime cards displaying provider and episode count
• Styled loading and error states
• Backend CORS configuration for frontend integration

### 🔄 Improved
• Frontend now retrieves live data from the FastAPI backend
• Anime endpoint expanded with episode count information
• Repository now supports episode counting by anime
• API response model updated to include episode counts

### 🏛️ Architecture
• Introduced dedicated frontend project
• Separated API communication into a reusable client module
• Established browser → API → repository → database workflow
• Continued separation between presentation, API, and data layers

### 🧪 Testing
• Backend test suite remains fully passing
• Verified frontend communicates successfully with FastAPI
• Verified anime list rendering
• Verified episode count display
• Verified loading and error state behavior
• Final test result: 37 automated tests passing

### ✅ Validation
• React development server launches successfully
• FastAPI backend serves frontend requests
• Anime list displays live database records
• Episode counts display correctly
• Frontend gracefully handles loading and backend connection errors
• Complete end-to-end data flow successfully demonstrated

# 📋 AnimeMangaDB v0.32.0 Changelog

## 🔎 Search & Episode Browser

### ✨ Added
• Anime selection in the frontend
• Episode list loading for selected anime
• Scrollable episode list
• Selected episode details section
• Episode chapter mapping display
• Episode search/filtering by number or title

### 🔄 Improved
• Anime cards are now interactive
• Frontend now supports the full Anime → Episode → Chapter Mapping flow
• Episode lists are easier to browse
• Search makes large anime lists like One Piece more usable
• Improved spacing and pluralization in the UI

### ✅ Validation
• Anime selection works
• Episode lists load from the API
• Episode search/filtering works
• Chapter mappings display correctly
• Selected episode details display correctly
• Full frontend/backend flow verified

# 📋 AnimeMangaDB v0.33.0 Changelog

## 🔎 Lookup Experience

### ✨ Added
• Manga chapter lookup API
• Frontend chapter lookup client
• Chapter lookup interface
• Clickable chapter lookup results
• Automatic navigation from lookup results to selected anime/episode
• Anime titles displayed in chapter lookup results

### 🔄 Improved
• Connected the two main lookup workflows
• Users can now search by manga chapter and jump directly to matching episodes
• Chapter lookup results are easier to understand
• Frontend now supports both Anime → Episode → Chapter and Chapter → Episode flows

### ✅ Validation
• Chapter lookup API returns matching episodes
• Frontend chapter search works
• Missing chapters show no-result state
• Lookup result clicks select the correct anime and episode
• Chapter mapping display updates correctly

# 📋 AnimeMangaDB v0.34.0 Changelog

## 🎨 UI Polish

### ✨ Added
• Sticky site header with navigation links
• Reusable AnimeCard component
• Reusable EpisodeCard component
• ChapterLookup component
• AnimeBrowser component
• EpisodeBrowser component
• SelectedEpisode component
• ChapterMapping component

### 🔄 Improved
• Refactored App.jsx into reusable React components
• Simplified component hierarchy
• Improved frontend maintainability
• Navigation links now jump directly to major sections
• Continued improvement of the browsing experience

### 🏛️ Architecture
• Introduced a dedicated frontend component architecture
• Reduced responsibility of App.jsx to application orchestration
• Established reusable UI building blocks
• Improved separation of presentation and application logic

### 🧪 Testing
• Verified all extracted components function identically to their original implementations
• Validated anime browsing
• Validated episode browsing
• Validated chapter lookup
• Validated chapter mapping display
• Backend test suite remains fully passing (39 tests)

### ✅ Validation
• Header navigation functions correctly
• Anime browser remains fully operational
• Episode browser remains fully operational
• Chapter lookup remains fully operational
• Selected episode display works correctly
• Chapter mapping display works correctly
• All frontend functionality preserved after component refactoring

# 📋 AnimeMangaDB v0.35.0 Changelog

## 📊 Data Quality & Metadata

### ✨ Added
• Database quality inspection tool
• Missing chapter mapping detection
• Generic episode title detection
• Missing arc detection
• Sample issue reporting
• Percentage-based quality metrics
• Automatic quality threshold warnings

### 🔄 Improved
• Database inspection now provides actionable quality metrics
• Reports include sample records for faster debugging
• Percentage reporting makes quality trends easier to understand
• Automatic warnings highlight significant data quality issues

### 🏛️ Architecture
• Introduced dedicated data quality tooling
• Established a repeatable database inspection workflow
• Laid the foundation for future metadata validation and cleanup tools

### 🧪 Testing
• Backend test suite remains fully passing
• Database quality inspection validated against current dataset
• Verified missing chapter reporting
• Verified generic title reporting
• Verified missing arc reporting
• Verified percentage calculations
• Verified warning thresholds
• Final test result: 39 automated tests passing

### ✅ Validation
• Quality report generates successfully
• Sample issue reporting works correctly
• Percentage metrics display correctly
• Warning thresholds trigger appropriately
• Existing scraper and API functionality remain unaffected

# 📋 AnimeMangaDB v0.36.0 Changelog

## 🧭 Navigation & Routing

### ✨ Added
• React Router integration
• BrowserRouter application wrapper
• Route definitions for the frontend
• Dedicated Not Found (404) route
• Router-based home navigation
• Dedicated Chapter Lookup route (/lookup)
• Anime detail route placeholder (/anime/:animeId)
• Episode detail route placeholder (/episodes/:episodeId)

### 🔄 Improved
• Transitioned from a single-page layout toward a route-based application
• Header navigation now leverages React Router
• Unknown URLs now display a friendly 404 page instead of a blank screen
• Established the foundation for bookmarkable and shareable URLs

### 🏛️ Architecture
• Introduced route-based application structure
• Prepared the frontend for dedicated Anime and Episode pages
• Improved navigation scalability for future features
• Established a clean routing foundation for continued frontend growth

### 🧪 Testing
• Backend test suite remains fully passing
• Verified BrowserRouter integration
• Verified application routing
• Verified lookup route
• Verified anime placeholder route
• Verified episode placeholder route
• Verified Not Found route
• Final test result: 39 automated tests passing

### ✅ Validation
• Home page loads correctly
• Chapter Lookup route functions correctly
• Unknown routes display the 404 page
• Anime detail placeholder route loads
• Episode detail placeholder route loads
• Existing frontend functionality remains unaffected by routing changes

# 📋 AnimeMangaDB v0.37.0 Changelog

## 📄 Dedicated Detail Pages

### ✨ Added
• Anime Detail page
• Episode Detail page
• Frontend Anime Detail API client
• Frontend Episode Detail API client
• Breadcrumb navigation
• Full page-based navigation between anime and episodes

### 🔄 Improved
• Anime cards now navigate directly to dedicated detail pages
• Episode cards now navigate directly to dedicated detail pages
• Breadcrumbs provide clear navigation context
• Navigation now follows URL-based routing instead of relying solely on application state
• Users can directly access anime and episode pages through bookmarkable URLs

### 🏛️ Architecture
• Introduced dedicated page components
• Separated page-level concerns from reusable UI components
• Expanded React Router usage throughout the application
• Established a scalable page architecture for future growth

### 🧪 Testing
• Backend test suite remains fully passing
• Verified Anime Detail page
• Verified Episode Detail page
• Verified Anime card navigation
• Verified Episode card navigation
• Verified breadcrumb navigation
• Verified route handling
• Final test result: 39 automated tests passing

### ✅ Validation
• Anime detail pages load correctly
• Episode detail pages load correctly
• Breadcrumb navigation functions correctly
• Anime cards navigate to detail pages
• Episode cards navigate to detail pages
• Existing application functionality remains intact

# 📋 AnimeMangaDB v0.38.0 Changelog

## 🔍 Search & Discovery

### ✨ Added
• Global Search interface
• Reusable GlobalSearch component
• Anime title filtering
• Search status indicator
• Search empty-state messaging
• Clear Search button

### 🔄 Improved
• Introduced a unified search entry point on the Home page
• Anime browser now updates dynamically while typing
• Clear visual feedback when filters are active
• Improved user experience for discovering anime

### 🏛️ Architecture
• Introduced dedicated GlobalSearch component
• Continued separation of presentation and application logic
• Extended component-based frontend architecture
• Prepared the application for future multi-category search

### 🧪 Testing
• Backend test suite remains fully passing
• Verified Global Search input
• Verified anime filtering
• Verified empty search state
• Verified search status display
• Verified Clear Search functionality
• Final test result: 39 automated tests passing

### ✅ Validation
• Global Search loads correctly
• Anime list filters in real time
• Clearing search restores the full anime list
• Empty searches display an appropriate message
• Existing browsing and routing functionality remain unaffected