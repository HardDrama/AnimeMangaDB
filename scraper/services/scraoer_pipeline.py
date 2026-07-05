class ScraperPipeline:
    def __init__(
        self,
        config,
        provider,
        client,
        extractor,
        repo,
    ):
        self.config = config
        self.provider = provider
        self.client = client
        self.extractor = extractor
        self.repo = repo