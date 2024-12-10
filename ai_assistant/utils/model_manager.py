import importlib

class ModelManager:
    def __init__(self):
        self.models = {}

    def load_model(self, model_name, model_class):
        """Dynamically load and initialize a model."""
        module = importlib.import_module(f"models.{model_name}")
        model_class = getattr(module, model_class)
        self.models[model_name] = model_class()

    def get_model(self, model_name):
        """Retrieve a model instance."""
        return self.models.get(model_name, None)

    def list_models(self):
        """List available models."""
        return list(self.models.keys())
