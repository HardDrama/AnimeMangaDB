# Runtime Composition Architecture

## Diagram

                FastAPI

                   │

          API Service Factory

                   │

         Repository Factory

                   │

            Model Factory

                   │

         Runtime Providers

          ┌──────────────┐

          ▼              ▼

    Production      Shared Manga

        Runtime         Runtime