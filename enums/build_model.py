from enum import Enum


class BuildStatus(Enum):
    BUILD_SUCCESS = "SUCCESS"
    BUILD_FAILURE = "FAILURE"
    BUILD_UNKNOWN = "UNKNOWN"


class BuildState(Enum):
    BUILD_QUEUED = "queued"
    BUILD_RUNNING = "running"
    BUILD_FINISHED = "finished"
