## Linear classifiers and learned representations

1. Start from a familiar binary classification problem.
2. Build the perceptron and soften its output.
3. Use XOR to expose the limit of one linear boundary.
4. Compose perceptrons into a multi-layer perceptron.
5. Relate nonlinear activations to expressivity.

## Build the argument progressively

\SlideTransition[duration=0.6,direction=0]{wipe}

::: incremental

- Observe the training examples.
- Construct a decision boundary.
- Evaluate the predictions.

:::

## From a score to a prediction

\SlideTransition[duration=0.8]{dissolve}

The linear score combines the input features:

$$z = \mathbf{w}^{\mathsf{T}}\mathbf{x} + b.$$

\pause

A nonlinear activation turns the score into a prediction:

$$\hat{y} = \sigma(z) = \frac{1}{1 + e^{-z}}.$$

## Choose precisely what appears

\transpush<1>[direction=0,duration=0.4]

\begin{overprint}
\onslide<1|handout:0>
\begin{block}{First view}
A single perceptron learns one linear decision boundary.
\end{block}
\onslide<2|handout:1>
\begin{block}{Second view}
Multiple layers compose features into richer representations.
\end{block}
\end{overprint}

## Tables stay readable

The XOR truth table cannot be separated by one linear boundary.

| Input $x_1$ | Input $x_2$ | Target $y$ |
|:-----------:|:-----------:|:----------:|
| 0           | 0           | 0          |
| 0           | 1           | 1          |
| 1           | 0           | 1          |
| 1           | 1           | 0          |

## Source code

```python
def predict(features, weights, bias):
    score = sum(x * w for x, w in zip(features, weights))
    return int(score + bias >= 0)
```

The Beamer writer automatically makes this a fragile frame.

## Diagrams and columns

:::: columns

::: {.column width="48%"}

\begin{tikzpicture}[x=1.3cm,y=1.3cm]
  \draw[->,color=SlidesMuted] (-0.3,0) -- (3,0) node[right] {$x_1$};
  \draw[->,color=SlidesMuted] (0,-0.3) -- (0,2.7) node[above] {$x_2$};
  \draw[thick,color=SlidesPrimary] (0,2.2) -- (2.6,0.2);
  \foreach \x/\y in {0.4/0.4,1.0/0.5,1.6/0.3}
    \fill[color=SlidesAccent] (\x,\y) circle (2pt);
  \foreach \x/\y in {0.8/2.2,1.6/1.7,2.3/1.5}
    \draw[thick,color=SlidesHeading] (\x,\y) circle (2pt);
\end{tikzpicture}

:::

::: {.column width="48%"}

- Use vector diagrams for sharp figures.
- Keep each frame focused on one idea.
- All overlays of a frame share its footer number.

:::

::::
