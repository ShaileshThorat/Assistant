class Model1:
    def __init__(self):
        # Initialize model (e.g., load weights, etc.)
        print("Model1 Initialized")

    def predict(self, input_text):
        # Example logic: Convert input to uppercase
        print(f"Model1 predicting: {input_text}")  # Debugging line
        return input_text.upper()
