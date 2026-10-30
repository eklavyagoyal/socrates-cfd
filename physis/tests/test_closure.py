import numpy as np
import torch

from physis.surrogates.closure import MLPEnsemble


def test_constant_and_nearly_constant_features_keep_unit_scale():
    x = np.array([[0.4, 0.0, 1.0], [0.6, 0.0, 1.0 + 1e-7]])
    model = MLPEnsemble(members=1, epochs=1).fit(x, np.array([-4.0, -3.0]))
    np.testing.assert_allclose(model.sd, [0.1, 1.0, 1.0])

    # An unseen family's flag must enter the net as 1, rather than 1e9.
    unseen = np.array([[0.5, 1.0, 1.0]])
    seen_inputs = []
    handle = model.models[0].register_forward_pre_hook(
        lambda _module, args: seen_inputs.append(args[0].clone()))
    try:
        mean, spread = model.predict(unseen)
    finally:
        handle.remove()
    torch.testing.assert_close(seen_inputs[0][0, 1], torch.tensor(1.0))
    assert np.isfinite(mean).all() and np.isfinite(spread).all()
