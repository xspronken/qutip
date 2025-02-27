import numpy as np
import pytest

from qutip.bloch import Bloch
from qutip import ket, ket2dm

try:
    import matplotlib.pyplot as plt
    from matplotlib.testing.decorators import check_figures_equal
except ImportError:
    def check_figures_equal(*args, **kw):
        def _error(*args, **kw):
            raise RuntimeError("matplotlib is not installed")
    plt = None


check_pngs_equal = check_figures_equal(extensions=["png"])


class TestBloch:
    def plot_arc_test(self, fig, *args, **kw):
        b = Bloch(fig=fig)
        b.add_arc(*args, **kw)
        b.render()

    def plot_arc_ref(self, fig, start, end, **kw):
        fmt = kw.pop("fmt", "b")
        steps = kw.pop("steps", None)
        start = np.array(start)
        end = np.array(end)
        if steps is None:
            steps = int(np.linalg.norm(start - end) * 100)
            steps = max(2, steps)

        t = np.linspace(0, 1, steps)
        line = start[:, np.newaxis] * t + end[:, np.newaxis] * (1 - t)
        arc = line * np.linalg.norm(start) / np.linalg.norm(line, axis=0)

        b = Bloch(fig=fig)
        b.render()
        b.axes.plot(arc[1, :], -arc[0, :], arc[2, :], fmt, **kw)

    @pytest.mark.parametrize([
        "start_test", "start_ref", "end_test", "end_ref", "kwargs",
    ], [
        pytest.param(
            (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), {}, id="arrays"),
        pytest.param(
            (0.1, 0, 0), (0.1, 0, 0), (0, 0.1, 0), (0, 0.1, 0), {},
            id="small-radius"),
        pytest.param(
            (1e-5, 0, 0), (1e-5, 0, 0), (0, 1e-5, 0), (0, 1e-5, 0), {},
            id="tiny-radius"),
        pytest.param(
            (1.2, 0, 0), (1.2, 0, 0), (0, 1.2, 0), (0, 1.2, 0), {},
            id="large-radius"),
        pytest.param(
            (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0),
            {"fmt": "r", "linestyle": "-"}, id="fmt-and-kwargs",
        ),
        pytest.param(
            ket("0"), (0, 0, 1),
            (ket("0") + ket("1")).unit(), (1, 0, 0),
            {}, id="kets",
        ),
        pytest.param(
            ket2dm(ket("0")), (0, 0, 1),
            ket2dm(ket("0") + ket("1")).unit(), (1, 0, 0),
            {}, id="dms",
        ),
        pytest.param(
            ket2dm(ket("0")) * 0.5, (0, 0, 0.5),
            ket2dm(ket("0") + ket("1")).unit() * 0.5, (0.5, 0, 0),
            {}, id="non-unit-dms",
        ),
    ])
    @check_pngs_equal
    def test_arc(
        self, start_test, start_ref, end_test, end_ref, kwargs,
        fig_test, fig_ref,
    ):
        self.plot_arc_test(fig_test, start_test, end_test, **kwargs)
        self.plot_arc_ref(fig_ref, start_ref, end_ref, **kwargs)

    @pytest.mark.parametrize([
        "start", "end", "err_msg",
    ], [
        pytest.param(
            (0, 0, 0), (0, 1, 0),
            "Polar and azimuthal angles undefined at origin.",
            id="start-origin",
        ),
        pytest.param(
            (1, 0, 0), (0, 0, 0),
            "Polar and azimuthal angles undefined at origin.",
            id="end-origin",
        ),
        pytest.param(
            (0.9, 0, 0), (0, 1, 0), "Points not on the same sphere.",
            id="different-spheres",
        ),
        pytest.param(
            (1, 0, 0), (1, 0, 0),
            "Start and end represent the same point. No arc can be formed.",
            id="same-points",
        ),
        pytest.param(
            (1, 0, 0), (-1, 0, 0),
            "Start and end are diagonally opposite, no unique arc is"
            " possible.",
            id="opposite-points",
        ),
    ])
    def test_arc_errors(self, start, end, err_msg):
        b = Bloch()
        with pytest.raises(ValueError) as err:
            b.add_arc(start, end)
        assert str(err.value) == err_msg

    def plot_line_test(self, fig, *args, **kw):
        b = Bloch(fig=fig)
        b.add_line(*args, **kw)
        b.render()

    def plot_line_ref(self, fig, start, end, **kw):
        fmt = kw.pop("fmt", "k")

        x = [start[1], end[1]]
        y = [-start[0], -end[0]]
        z = [start[2], end[2]]

        b = Bloch(fig=fig)
        b.render()
        b.axes.plot(x, y, z, fmt, **kw)

    @pytest.mark.parametrize([
        "start_test", "start_ref", "end_test", "end_ref", "kwargs",
    ], [
        pytest.param(
            (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), {}, id="arrays"),
        pytest.param(
            (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0),
            {"fmt": "r", "linestyle": "-"}, id="fmt-and-kwargs",
        ),
        pytest.param(
            ket("0"), (0, 0, 1),
            (ket("0") + ket("1")).unit(), (1, 0, 0),
            {}, id="kets",
        ),
        pytest.param(
            ket2dm(ket("0")), (0, 0, 1),
            ket2dm(ket("0") + ket("1")).unit(), (1, 0, 0),
            {}, id="dms",
        ),
        pytest.param(
            ket2dm(ket("0")) * 0.5, (0, 0, 0.5),
            ket2dm(ket("0") + ket("1")).unit() * 0.5, (0.5, 0, 0),
            {}, id="non-unit-dms",
        ),
    ])
    @check_pngs_equal
    def test_line(
        self, start_test, start_ref, end_test, end_ref, kwargs,
        fig_test, fig_ref,
    ):
        self.plot_line_test(fig_test, start_test, end_test, **kwargs)
        self.plot_line_ref(fig_ref, start_ref, end_ref, **kwargs)

    def plot_vector_test(self, fig, vectors):
        b = Bloch(fig=fig)
        b.add_vectors(vectors)
        b.render()

    def plot_vector_ref(self, fig, vectors):
        from qutip.bloch import Arrow3D
        b = Bloch(fig=fig)
        b.render()
        colors = ['g', '#CC6600', 'b', 'r']

        if not isinstance(vectors[0], (list, tuple, np.ndarray)):
            vectors = [vectors]

        for i, v in enumerate(vectors):
            color = colors[i % len(colors)]
            xs3d = v[1] * np.array([0, 1])
            ys3d = -v[0] * np.array([0, 1])
            zs3d = v[2] * np.array([0, 1])
            a = Arrow3D(
                xs3d, ys3d, zs3d,
                mutation_scale=20, lw=3, arrowstyle="-|>", color=color)
            b.axes.add_artist(a)

    @pytest.mark.parametrize([
        "vectors",
    ], [
        pytest.param(
            (0, 0, 1), id="single-vector-tuple"),
        pytest.param(
            [0, 0, 1], id="single-vector-list"),
       pytest.param(
            np.array([0, 0, 1]), id="single-vector-numpy"),
        pytest.param(
            [(0, 0, 1), (0, 1, 0)], id="list-vectors-tuple"),
        pytest.param(
            [[0, 0, 1]], id="list-vectors-list"),
        pytest.param(
            [np.array([0, 0, 1])], id="list-vectors-numpy"),
    ])
    @check_pngs_equal
    def test_vector(self, vectors, fig_test, fig_ref):
        self.plot_vector_test(fig_test, vectors)
        self.plot_vector_ref(fig_ref, vectors)
