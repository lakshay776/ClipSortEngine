from PreProcessing.TranscriptStrategy.FreeStrategy import free_strategy
from PreProcessing.TranscriptStrategy.ProStrategy import ProStrategy

def TranscriptionService(videos,Subscription):
    if Subscription=="Free":
        return free_strategy(videos)
    elif Subscription=="Pro":
        return ProStrategy(videos)
