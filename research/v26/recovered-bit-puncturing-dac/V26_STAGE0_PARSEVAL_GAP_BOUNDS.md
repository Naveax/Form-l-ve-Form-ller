# V26 Stage0 Parseval Gap Bounds

## Purpose

The admitted Stage0 result reports exact signed single-column marginals **within the frozen local cap**. This note asks a different mathematical question: how far can those capped marginal vectors still be from the corresponding full exact double-round Walsh marginals?

The answer has a source-independent Parseval lower bound, provided the capped coefficient vectors use the same normalized Walsh coefficient space as the full transform. The missing canonical core is still required to turn that compatibility assumption into implementation-level authority.

## 1. Full double-round marginal norm

A ChaCha double-round is a bijection on the 512-bit state. Let `P` be that permutation and let

`C_P(alpha,beta)`

be its normalized Walsh correlation matrix. For any fixed output mask `beta`, and for any subset S of the 512 input-mask coordinates, define the coefficient marginal

`m_S(alpha_S) = sum_{alpha_barS} C_P((alpha_S,alpha_barS),beta)`.

By the general subset-marginal identity, `m_S` is the normalized Walsh spectrum of the Boolean phase obtained by restricting all input coordinates outside S to zero. Parseval therefore gives

`||m_S||_2^2 = 1`.

This applies in particular when S is any complete next-column interface of four 32-bit words. Therefore the four **full exact** next-column marginals for q138 each have squared norm exactly one.

They cannot be identically zero.

## 2. Admitted cap4 Stage0 energies

The admitted cap4 Stage0 reports signed marginal energies

- C0: `0`,
- C1: `0.5193693190813065`,
- C2: `0.5347073078155518`,
- C3: `0`.

These are exact energies of the capped signed marginal vectors, not claims about the full exact double-round marginal energy.

Their l2 norms are

- C0: `0`,
- C1: `0.7206728238814798`,
- C2: `0.7312368342852757`,
- C3: `0`.

## 3. Reverse-triangle lower bounds

Let `m_c` be the corresponding full exact column marginal and `m_{c,K}` the cap4 marginal in the same normalized coefficient space. Since

`||m_c||_2 = 1`,

the reverse triangle inequality gives

`||m_c - m_{c,K}||_2 >= 1 - ||m_{c,K}||_2`.

Therefore the cap4-to-full l2 residual is bounded below by

- C0: `>= 1`, hence exactly `1` if `m_{0,K}=0`;
- C1: `>= 0.2793271761185202`;
- C2: `>= 0.26876316571472425`;
- C3: `>= 1`, hence exactly `1` if `m_{3,K}=0`.

These are **lower bounds**, not upper error certificates. They say that cap4 is necessarily still a substantial distance from the full exact marginal if the coefficient-space compatibility assumption holds.

## 4. What this proves and what it does not

The mathematical point is sharp:

- Stage0 can simultaneously be `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0` **within the bounded trail family**;
- and still be far from the full exact Walsh marginal.

There is no contradiction. The first statement concerns representation efficiency of a frozen truncated family. The second concerns approximation completeness relative to the full permutation spectrum.

In particular, the zero C0/C3 capped marginals are not merely ambiguous about hidden cross-column correlation. They are guaranteed not to equal the corresponding full exact single-column marginals.

## 5. Consequence for the next mathematical objective

Support size and memory compression alone cannot establish that the capped separator captures the mathematically important part of the full exact object.

A useful full-exact bridge needs an **upper** residual certificate

`||m_c - m_{c,K}||_2 <= epsilon_c(K)`

or an analogous tensor-level certificate.

The Parseval gap above provides a necessary sanity check for any proposed upper bound. For example, no cap4 certificate can claim

- `epsilon_0 < 1`,
- `epsilon_1 < 0.2793271761185202`,
- `epsilon_2 < 0.26876316571472425`,
- `epsilon_3 < 1`

for these particular capped vectors under compatible normalization.

If a future derivation produces such a smaller upper bound, either its assumptions, normalization, or identification of the capped vector must be wrong.

## 6. Epsilon-rank implication

Because C0/C3 have residual floor one at cap4, no low-rank structure observed solely in those zero capped marginals can yield a nontrivial full-exact epsilon-rank statement at tolerance below one.

For C1/C2, the best possible future full-exact epsilon-rank bridge at cap4 must tolerate at least the Parseval floors above, unless additional trail classes are incorporated and the capped vector changes.

Thus the correct progression is:

`increase/understand cap -> certify residual -> then interpret capped rank/singular structure`.

Doing rank first and silently assuming the tail is small reverses the logical order.

## 7. Compatibility caveat

The inequality itself is pure Walsh analysis. Applying the numerical bounds to the recovered cap4 implementation requires confirmation that its signed marginal coefficients are normalized in the same coefficient space as the full correlation column and represent a compatible partial/truncated expansion. Historical authority strongly motivates that interpretation, but the canonical core bytes are still missing, so the implementation-level identification remains explicitly conditional.

## 8. Claims not admitted

This note does not prove an upper cap4 error bound, convergence in K, low full-exact epsilon-rank, full second-layer contraction, ranking gain, alpha<1, or full-round relevance.