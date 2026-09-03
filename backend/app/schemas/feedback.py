from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ALLOWED_ACTIONS = {"CONFIRM", "REJECT", "RECLASSIFY"}


class FeedbackCreate(BaseModel):
    detection_id: str = Field(min_length=1)
    action: str
    expert_label: str | None = Field(None, max_length=128)
    comment: str | None = Field(None, max_length=2000)

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        v_up = v.upper().strip()
        if v_up not in ALLOWED_ACTIONS:
            raise ValueError(f"action must be one of {sorted(ALLOWED_ACTIONS)}")
        return v_up

    @field_validator("expert_label")
    @classmethod
    def strip_label(cls, v: str | None) -> str | None:
        return v.strip() if v else v

    @model_validator(mode="after")
    def require_label_for_reclassify(self) -> "FeedbackCreate":
        # A per-field validator on expert_label would NOT reliably catch the case
        # where the client omits expert_label entirely: pydantic v2 only runs
        # field validators against an explicitly-provided value by default (it
        # skips validation when a field falls back to its default), so a request
        # body that simply leaves expert_label out would slip through. A
        # model-level validator always runs after construction, regardless of
        # which fields were supplied, so it catches both the omitted-field case
        # and the empty-string case.
        if self.action == "RECLASSIFY" and not (self.expert_label and self.expert_label.strip()):
            raise ValueError("expert_label is required when action is RECLASSIFY")
        return self


class FeedbackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    detection_id: str
    ai_label: str
    expert_label: str | None
    action: str
    comment: str | None
