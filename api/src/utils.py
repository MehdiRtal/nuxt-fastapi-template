from fastapi.responses import ORJSONResponse


class DefaultORJSONResponse(ORJSONResponse):
    def render(self, content):
        if isinstance(content, dict):
            return super().render({"status": "success", **content})
        else:
            return super().render({"status": "success", "data": content})
