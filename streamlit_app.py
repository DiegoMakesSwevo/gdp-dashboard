import math
import random
from dataclasses import dataclass
from typing import Callable, Dict, List

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Riemann Sum Practice Studio',
    page_icon='📐',
    layout='wide',
)

# ----------------------------------------------------------------------------
# Data models and helpers

Function = Callable[[float], float]


def round4(value: float) -> float:
    """Round to four decimal places for consistent display."""
    return round(value, 4)


def riemann_summaries(fn: Function, a: float, b: float, n: int) -> Dict[str, float]:
    """Compute several Riemann-style approximations over [a, b]."""
    if n <= 0:
        raise ValueError('n must be positive')

    dx = (b - a) / n
    points = [a + i * dx for i in range(n + 1)]
    left_x = points[:-1]
    right_x = points[1:]

    left_values = [fn(x) for x in left_x]
    right_values = [fn(x) for x in right_x]

    upper_rectangles = [max(l, r) for l, r in zip(left_values, right_values)]
    lower_rectangles = [min(l, r) for l, r in zip(left_values, right_values)]
    trapezoids = [0.5 * (l + r) for l, r in zip(left_values, right_values)]
    midpoints = [fn((x0 + x1) / 2) for x0, x1 in zip(left_x, right_x)]

    return {
        'upper_sum': round4(sum(upper_rectangles) * dx),
        'lower_sum': round4(sum(lower_rectangles) * dx),
        'trapezoidal': round4(sum(trapezoids) * dx),
        'midpoint': round4(sum(midpoints) * dx),
        'dx': round4(dx),
        'left_values': left_values,
        'right_values': right_values,
        'points': points,
    }


@dataclass
class PracticeProblem:
    title: str
    description: str
    fn_label: str
    a: float
    b: float
    n: int

    def render(self, fn: Function):
        st.markdown(f'#### {self.title}')
        st.write(self.description)
        sums = riemann_summaries(fn, self.a, self.b, self.n)
        cols = st.columns(4)
        cols[0].metric('Upper sum', f"{sums['upper_sum']:.4f}")
        cols[1].metric('Lower sum', f"{sums['lower_sum']:.4f}")
        cols[2].metric('Trapezoidal', f"{sums['trapezoidal']:.4f}")
        cols[3].metric('Midpoint', f"{sums['midpoint']:.4f}")
        with st.expander('Show interval grid and function values'):
            table = pd.DataFrame(
                {
                    'x_left': sums['points'][:-1],
                    'x_right': sums['points'][1:],
                    'f(left)': [round4(x) for x in sums['left_values']],
                    'f(right)': [round4(x) for x in sums['right_values']],
                }
            )
            st.dataframe(table, hide_index=True, use_container_width=True)


# ----------------------------------------------------------------------------
# Predefined functions

FUNCTION_BANK: Dict[str, Function] = {
    '14/(x^2 + 1)': lambda x: 14 / (x**2 + 1),
    '3x - x^2': lambda x: 3 * x - x**2,
    '√x + 1': lambda x: math.sqrt(max(x, 0)) + 1,
    '2sin(x) + 4': lambda x: 2 * math.sin(x) + 4,
    'e^{-x/2}': lambda x: math.exp(-x / 2),
}


PREMADE_PROBLEMS: List[PracticeProblem] = [
    PracticeProblem(
        title='Classic rational peak',
        description='Use upper and lower sums on y = 14/(x² + 1) over [0, 2] with 4 equal pieces.',
        fn_label='14/(x^2 + 1)',
        a=0,
        b=2,
        n=4,
    ),
    PracticeProblem(
        title='Concave parabola snapshot',
        description='Estimate ∫ (3x − x²) from 0 to 3 with 6 subintervals.',
        fn_label='3x - x^2',
        a=0,
        b=3,
        n=6,
    ),
    PracticeProblem(
        title='Non-negative radical bump',
        description='Approximate the area under √x + 1 on [1, 5] with 8 subintervals.',
        fn_label='√x + 1',
        a=1,
        b=5,
        n=8,
    ),
]

# ----------------------------------------------------------------------------
# Page content

st.title('📐 Riemann Sum Practice Studio')

st.markdown(
    """
This page is a compact practice lab for upper sums, lower sums, trapezoids, and midpoint rules.
Each card below computes everything for you, rounded to four decimal places, and shows the grid
used in the calculation so you can double-check by hand.
    """
)

# Hero example
with st.expander('See the fully-worked template for any interval'):
    st.markdown(
        """
1. Choose a function (e.g., 14/(x²+1)), an interval [a,b], and the number of subintervals *n*.
2. Compute the width Δx = (b − a) / n.
3. Form left and right endpoints, then take max(left,right) for the upper sum and min(left,right) for the lower sum on each slice.
4. Multiply each max/min by Δx and add them up. The trapezoidal rule uses the average of the two heights; the midpoint rule samples the center.
        """
    )
    st.caption('All results below follow that blueprint and round to four decimals.')

# Showcase premade practice
st.header('Ready-to-use practice problems', divider='gray')

for problem in PREMADE_PROBLEMS:
    fn = FUNCTION_BANK[problem.fn_label]
    problem.render(fn)
    st.divider()

# Custom sandbox
st.header('Build your own problem', divider='gray')

col1, col2 = st.columns([2, 1])

with col1:
    fn_label = st.selectbox('Choose a function', list(FUNCTION_BANK.keys()), index=0)
    a = st.number_input('Interval start (a)', value=0.0, format='%0.2f')
    b = st.number_input('Interval end (b)', value=2.0, format='%0.2f')
    n = st.slider('Number of equal subintervals (n)', min_value=1, max_value=50, value=6)

with col2:
    st.markdown('**Quick tips**')
    st.markdown('- Keep *n* large to see upper/lower sums converge.\n- Try intervals that cross zero to see symmetry effects.\n- Midpoint and trapezoidal rules are often close to the true integral.')

if b == a:
    st.error('Choose an interval with nonzero width.')
elif n <= 0:
    st.error('Choose a positive number of subintervals.')
else:
    chosen_fn = FUNCTION_BANK[fn_label]
    summary = riemann_summaries(chosen_fn, a, b, n)
    st.subheader(f'Summary for {fn_label} on [{a}, {b}] with n = {n}')
    cols = st.columns(4)
    cols[0].metric('Upper sum', f"{summary['upper_sum']:.4f}")
    cols[1].metric('Lower sum', f"{summary['lower_sum']:.4f}")
    cols[2].metric('Trapezoidal', f"{summary['trapezoidal']:.4f}")
    cols[3].metric('Midpoint', f"{summary['midpoint']:.4f}")

    with st.expander('Show calculation grid'):
        grid = pd.DataFrame(
            {
                'x_i': summary['points'][:-1],
                'x_{i+1}': summary['points'][1:],
                'f(x_i)': [round4(x) for x in summary['left_values']],
                'f(x_{i+1})': [round4(x) for x in summary['right_values']],
            }
        )
        dx_value = summary['dx']
        st.write(f'Δx = {dx_value:.4f}')
        st.dataframe(grid, hide_index=True, use_container_width=True)

# Randomized drills
st.header('Randomized drills', divider='gray')

num_drills = st.slider('How many drills would you like?', min_value=1, max_value=5, value=3)
seed = st.number_input('Set a seed for repeatable drills (optional)', value=0, step=1)
if seed:
    random.seed(seed)

st.caption('Each drill chooses a function, interval, and n so you can check your manual work against the computed sums.')

for i in range(num_drills):
    fn_label = random.choice(list(FUNCTION_BANK.keys()))
    a = random.randint(-3, 1)
    b = a + random.randint(2, 6)
    n = random.choice([4, 5, 6, 8, 10, 12])
    drill = PracticeProblem(
        title=f'Drill {i + 1}',
        description=f'Compute upper/lower sums for {fn_label} on [{a}, {b}] with n = {n}.',
        fn_label=fn_label,
        a=a,
        b=b,
        n=n,
    )
    drill.render(FUNCTION_BANK[fn_label])
    st.divider()

st.success('Practice as many times as you like—the calculations update immediately!')
