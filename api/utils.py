from fastapi.responses import ORJSONResponse


class DefaultORJSONResponse(ORJSONResponse):
    def render(self, content):
        return super().render({"status": "success", **content})
