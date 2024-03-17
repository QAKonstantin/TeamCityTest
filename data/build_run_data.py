from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class BuildRunDataModel(BaseModel):
    buildType: dict


class BuildRunData:

    @staticmethod
    def build_run_data(build_conf_id) -> BuildRunDataModel:
        return BuildRunDataModel(
            buildType={
                "id": build_conf_id
            }
        )


class BuildTypeModel(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str


class UserModel(BaseModel):
    username: str
    id: int
    href: str


class TriggeredModel(BaseModel):
    type: str
    date: str
    user: UserModel


class HrefModel(BaseModel):
    href: str


class RevisionsModel(BaseModel):
    count: int


class BuildRunResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: int
    buildTypeId: str
    state: str
    href: str
    webUrl: str
    buildType: BuildTypeModel
    waitReason: str
    queuedDate: str
    triggered: TriggeredModel
    changes: Optional[HrefModel] = None
    revisions: Optional[RevisionsModel] = None
    compatibleAgents: Optional[HrefModel] = None
    artifacts: Optional[HrefModel] = None
    vcsLabels: list
    customization: dict


class GetBuildModel(BaseModel):
    id: int
    buildTypeId: str
    state: str
    href: str
    webUrl: str


class BuildGetResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow")
    count: int
    href: str
    build: List[GetBuildModel]
