from logging import Logger


class MasterPipeline:
    def __init__(self, logger: Logger, historical_pipeline, preprocessing_pipeline):
        self.logger = logger
        self.historical_pipeline = historical_pipeline
        self.preprocessing_pipeline = preprocessing_pipeline

    async def run(self) -> None:

        await self.historical_pipeline.run()

        self.preprocessing_pipeline.run()
