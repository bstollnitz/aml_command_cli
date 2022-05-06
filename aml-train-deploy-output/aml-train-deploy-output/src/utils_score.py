"""Utilities used when scoring."""

import numpy as np
import torch


def predict(model: torch.nn.Module, x: np.ndarray, device: str) -> np.ndarray:
    """
    Makes a prediction for input x.
    """
    model.to(device)
    model.eval()

    x = torch.from_numpy(x).float().to(device)
    with torch.no_grad():
        y_prime = model(x)
        _, predicted_indices = torch.max(y_prime, dim=1)
    return predicted_indices.cpu().numpy()
