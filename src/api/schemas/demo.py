from pydantic import BaseModel, ConfigDict, Field


class DemoProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    projectId: str = Field(alias="project_id")
    workflowId: str = Field(alias="workflow_id")
