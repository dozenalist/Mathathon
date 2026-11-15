"""Create the human-readable PDF for the independent zeta(7) audit."""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
OUT.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Cambria','C:/Windows/Fonts/cambria.ttc',subfontIndex=0))
pdfmetrics.registerFont(TTFont('Cambria-Bold','C:/Windows/Fonts/cambriab.ttf'))
pdfmetrics.registerFont(TTFont('Cambria-Italic','C:/Windows/Fonts/cambriai.ttf'))
pdfmetrics.registerFontFamily('Cambria',normal='Cambria',bold='Cambria-Bold',italic='Cambria-Italic',boldItalic='Cambria-Bold')
NAVY=colors.HexColor('#15354a'); TEAL=colors.HexColor('#096b69'); RED=colors.HexColor('#9d3f32')
GREY=colors.HexColor('#52616a'); LIGHT=colors.HexColor('#edf3f5')
styles={
 'title':ParagraphStyle('title',fontName='Cambria-Bold',fontSize=25,leading=29,textColor=NAVY,spaceAfter=14),
 'head':ParagraphStyle('head',fontName='Cambria-Bold',fontSize=17,leading=21,textColor=NAVY,spaceAfter=12),
 'sub':ParagraphStyle('sub',fontName='Cambria-Bold',fontSize=12,leading=15,textColor=TEAL,spaceBefore=11,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='Cambria',fontSize=11.2,leading=15.3,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Cambria',fontSize=9.2,leading=12.2,textColor=GREY,spaceAfter=6),
 'eq':ParagraphStyle('eq',fontName='Cambria',fontSize=11.4,leading=17,leftIndent=13,rightIndent=6,spaceBefore=5,spaceAfter=10),
 'cell':ParagraphStyle('cell',fontName='Cambria',fontSize=10.1,leading=13.1),
 'cellsmall':ParagraphStyle('cellsmall',fontName='Cambria',fontSize=9.1,leading=11.6),
 'th':ParagraphStyle('th',fontName='Cambria-Bold',fontSize=10.1,leading=13.1,textColor=colors.white),
}
story=[]
plain=[]
def P(t,style='body'):
    story.append(Paragraph(t,styles[style])); plain.append(re.sub('<[^>]+>','',t))
def H(t): P(t,'head')
def S(t): P(t,'sub')
def E(t): P(t,'eq')
def page(title): story.append(PageBreak()); H(title)
def table(rows,widths,small=False):
    data=[[Paragraph(str(c),styles['th' if i==0 else ('cellsmall' if small else 'cell')]) for c in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),
      ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
      ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
      ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),
      ('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#c7d3d9'))]))
    story.extend([t,Spacer(1,10)]); plain.extend([' | '.join(map(str,r)) for r in rows])

P('Why the ζ(5) argument<br/>does not directly prove ζ(7)','title')
P('Independent exploration of Aabir Fauzan’s September 2026 construction<br/>14 November 2026','small')
P('<b>The positive determinant survives. The arithmetic estimate does not.</b> A faithful ζ(7) version still gives rational polynomials, the expected degree, and a positive value at ζ(7). It even retains the same leading real-decay estimate. What changes is the cost of making every coefficient integral.')
P('There are two separate findings. First, an unchanged local denominator bound is demonstrably false: a concrete coefficient needs 22 more powers of 29 than that bound permits. Second, after repairing the estimates, the final upper bound has the wrong sign to finish the irrationality argument.')
S('The comparison that decides the proof')
P('Write F for the rational determinant after the paper’s factorial scaling, and multiply it by a positive rational number m to obtain an integer polynomial Q. The proof needs the decay of F to outweigh the growth of m:')
E('log Q(ζ(s)) = log m + log F(ζ(s)) ≤ (A + U)K<super>2</super> + o(K<super>2</super>).')
table([
 ['At the paper’s cutoff M = 200','ζ(5)','Transferred ζ(7)'],
 ['Real-decay coefficient U','−1.3669955000','−1.3669955000'],
 ['Normalization bound A','1.3495876977','2.3274522811'],
 ['Sum A + U','−0.0174078023','+0.9604567811'],
], [230,125,125])
P('A negative sum proves that the positive integer-polynomial values tend to zero fast enough. A positive <i>upper</i> bound proves no such decay. It also does <b>not</b> prove that the actual values grow.')
S('What “the same argument” means here')
P('The main audit keeps K = 40n, N = 3n, h = 37n, the numerator D<sub>N</sub><super>6</super>, and the paper’s factorial scaling. It replaces the entire ζ(5) functional by its correct ζ(7) analogue. A separate experiment tests D<sub>N</sub><super>8</super>. The conclusion concerns these specific transfers; it is not an impossibility theorem for all Hankel-determinant approaches.')
P('Reading route: pages 2–4 follow the opening equations in order; pages 5–8 locate and quantify the failure; pages 9–10 explain the real bound and the attempted repair; page 11 records sources and verification.','small')

page('The opening equations, in order')
P('References such as (2.2) refer to Fauzan’s original 32-page PDF [F]. The statements about ζ(7) below are derived in this exploration.')
S('1. Parameters and elementary factors — (2.1), page 3')
E('K = 40n,  N = 3n,  h = K − N = 37n,<br/>α = N/K = 3/40,  λ = h/K = 37/40,<br/>D<sub>m</sub>(t) = ∏<sub>j=1</sub><super>m</super>(t + j<super>2</super>),  H<sub>j</sub><super>(s)</super> = ∑<sub>v=1</sub><super>j</super> v<super>−s</super>.')
P('<b>Works:</b> retain the parameters and D<sub>m</sub>. Replace H<super>(5)</super> by H<super>(7)</super>. These choices define a concrete test, although the original numerical optimization need not be optimal for ζ(7).')
S('2. Polynomial moments — (2.2), page 3')
E('μ<sub>5</sub>(t<super>e</super>) = (−1)<super>e</super>B<sub>2e+2</sub>(2e+3)(2e+4)(2e+5)/24,<br/>μ<sub>7</sub>(t<super>e</super>) = (−1)<super>e</super>B<sub>2e+2</sub>∏<sub>r=3</sub><super>7</super>(2e+r)/720.')
P('<b>Requires a real change:</b> merely replacing the symbol ζ(5) by ζ(7) is insufficient. The moments change too. They remain rational. Here B<sub>m</sub> denotes a Bernoulli number, with B<sub>1</sub> = −1/2.')
table([['Moment','μ₅','μ₇'],['1','5/12','7/12'],['t','7/24','7/10'],['t²','1/2','11/6']],[240,120,120])
S('3. Simple poles — (2.3), page 3')
E('μ<sub>5,X</sub>(1/(t+j<super>2</super>)) = j<super>4</super>(X−H<sub>j</sub><super>(5)</super>) − 1/4 + 1/(2j),<br/>μ<sub>7,X</sub>(1/(t+j<super>2</super>)) = j<super>6</super>(X−H<sub>j</sub><super>(7)</super>) − 1/6 + 1/(2j).')
P('<b>Works after correction:</b> polynomial division and simple partial fractions still define the functional uniquely. It is affine in X. There are no extra unknown ζ(3) or ζ(5) terms.')
P('The formulas are justified by the positive integral on the next page, using Euler’s even-zeta formula and the same integration-by-parts/Hermite mechanism as [F, Proposition 2.2]. See [D1–D2].','small')

page('The matrix, its degree, and positivity')
S('4. The matrix and scaling — (2.4)–(2.6), page 4')
E('G<sub>7,K</sub>(X)<sub>ij</sub> = μ<sub>7,X</sub>(D<sub>N</sub>(t)<super>6</super>t<super>i+j</super>/D<sub>K</sub>(t)),  0 ≤ i,j &lt; h,<br/>Δ<sub>7,K</sub>(X) = det G<sub>7,K</sub>(X),  F<sub>7,K</sub> = S<sub>K</sub>Δ<sub>7,K</sub>,<br/>S<sub>K</sub> = (K!)<super>2h</super>4<super>h−1</super> / [(N!)<super>12h</super>∏<sub>i=1</sub><super>h−1</super>((2i)!)<super>2</super>].')
P('<b>Works:</b> use the same matrix shape and scalar. The prime-dependent normalization m must be rebuilt; its original values are not automatically valid.')
S('5. Exact degree — (2.9), page 4')
P('After cancellation there are exactly h possible poles, at −j² for N &lt; j ≤ K. Their X-coefficients change from j⁴ to j⁶. The same Vandermonde calculation gives')
E('[X<super>h</super>]Δ<sub>7,K</sub> = (−1)<super>h(h−1)/2</super>∏<sub>j=N+1</sub><super>K</super>j<super>6</super>D<sub>N</sub>(−j<super>2</super>)<super>5</super> ≠ 0.')
P('<b>Works:</b> the degree is still h. The exponent 5 on D<sub>N</sub> comes from cancellation of D<sub>N</sub><super>6</super>/D<sub>K</sub>; it does not become 7 just because the zeta argument changes.')
S('6. Positive integral — Proposition 2.2, page 5')
E('w<sub>7</sub>(y) = [(2π)<super>6</super>/360] y<super>7</super>∑<sub>ℓ≥1</sub>ℓ<super>6</super>e<super>−2πℓy</super> &gt; 0,<br/>μ<sub>7,ζ(7)</sub>(R) = ∫<sub>0</sub><super>∞</super>R(y<super>2</super>)w<sub>7</sub>(y) dy.')
P('For monomials, integrate the exponential series term by term. The result is (2e+7)! ζ(2e+2)/[360(2π)<super>2e+2</super>], which is exactly the rational moment on page 2. For poles, six integrations by parts give a<super>6</super>ζ(7,a) − 1/(2a) − 1/6; at a = j this is the displayed pole formula. The boundary terms vanish: at zero each is O(y), and at infinity they decay exponentially.')
P('For any nonzero polynomial q of degree less than h, the integral of D<sub>N</sub>(y²)<super>6</super>q(y²)<super>2</super>w<sub>7</sub>(y)/D<sub>K</sub>(y²) is strictly positive. Thus G<sub>7,K</sub>(ζ(7)) is positive definite and Δ<sub>7,K</sub>(ζ(7)) &gt; 0. Nonvanishing is not the obstruction.')

page('A small successful example, then the first cost')
S('A determinant small enough to inspect')
P('Set K = 2, N = 0, h = 2 just to see the construction. Direct partial fractions give the symmetric matrix with entries')
E('G<sub>00</sub> = −21X + 85/4,<br/>G<sub>01</sub> = G<sub>10</sub> = 85X − 257/3,<br/>G<sub>11</sub> = −341X + 4127/12.')
P('Its determinant and one integer normalization are')
E('Δ(X) = −64X<super>2</super> + (569/6)X − 4399/144,<br/>144Δ(X) = −9216X<super>2</super> + 13656X − 4399.')
P('The positive-integral argument proves Δ(ζ(7)) &gt; 0. This example shows that the transfer is not empty. A single positive integer-polynomial value, however, supplies no irrationality proof. We need a whole sequence with sufficiently rapid decay. These small parameters are illustrative, outside the paper’s global asymptotic setup.')
S('7. Pullback to integer poles — (3.1)–(3.3), pages 5–6')
P('The substitution t = −x² turns poles at negative squares into integer poles. Let L(x<super>k</super>) = B<sub>k</sub>. The original functional uses three derivatives; ζ(7) needs five:')
E('τ<sub>5</sub>(P) = L(P<super>(3)</super>)/24,  τ<sub>7</sub>(P) = L(P<super>(5)</super>)/720,<br/>μ<sub>7,X</sub>(R) = τ<sub>7,X</sub>(x<super>7</super>R(−x<super>2</super>)).')
P('On a simple pole, set τ<sub>7,X</sub>(1/(x−r)) = H<sub>d(r)</sub><super>(7)</super>−X, where d(r) = r for r ≥ 0 and d(r) = −r−1 otherwise. Reflection still changes the sign. The translation difference becomes g<super>(6)</super>(0)/720 instead of g<super>(4)</super>(0)/24.')
S('8. Distribution among residue classes — (3.7), page 7')
E('τ<sub>5,X</sub>(g) = p<super>−4</super>∑<sub>a=0</sub><super>p−1</super>τ<sub>5,Y</sub><super>ext</super>(g(a+px)),<br/>τ<sub>7,X</sub>(g) = p<super>−6</super>∑<sub>a=0</sub><super>p−1</super>τ<sub>7,Y</sub><super>ext</super>(g(a+px)).')
P('In the s-th formula, Y = p<super>s</super>X + C<sub>p,s</sub>; the constant C<sub>p,s</sub> makes the identity hold at g(x) = 1/x.','small')
P('<b>This is the first consequential arithmetic change:</b> two extra derivatives require two extra powers of p in the denominator. At nonzero residue classes x<super>7</super> is a p-adic unit, so it cannot pay back this loss. At the zero class its two extra powers of p do pay it back.')

page('An unchanged local lemma is actually false')
P('Here is a finite check that distinguishes a false transferred claim from a bound we merely failed to prove. For a rational number r, v<sub>p</sub>(r) counts numerator powers of p minus denominator powers. Thus v<sub>29</sub>(r) = −82 means that its reduced denominator contains exactly 29<super>82</super>. For a polynomial, v<sub>p</sub><super>G</super> is the minimum over its coefficients.')
S('The local test')
E('K = 40,  N = 3,  h = 37,  p = 29.')
P('All hypotheses of the original outer-range lemma (4.9) hold: p ≥ 7, p ≤ K &lt; 3p, p² &gt; 2K, 2N &lt; p, and 5N ≤ 2p−2. The old formula (4.14) gives')
E('γ<sub>29</sub><super>out</super> = −7(40−29) + 6·3 − 1 = −60.')
P('If that bound carried over unchanged, every coefficient of Δ<sub>7,40</sub> would have 29-adic valuation at least −60. But exact arithmetic gives')
E('<b>v<sub>29</sub>(Δ<sub>5,40</sub>(0)) = −60,<br/>v<sub>29</sub>(Δ<sub>7,40</sub>(0)) = −82.</b>')
P('Evaluation at X = 0 extracts the constant coefficient. Consequently v<sub>29</sub><super>G</super>(Δ<sub>7,40</sub>) ≤ −82 &lt; −60. The copied local estimate is false. This conclusion does not require guessing any asymptotic behavior.')
table([['Prime p','Old bound','vₚ(Δ₅(0))','vₚ(Δ₇(0))'],
 ['23','−110','−110','−136'],['29','−60','−60','−82'],['31','−46','−46','−64'],['37','−4','−4','−10']],[100,125,125,130])
P('The scaling does not repair this: v<sub>29</sub>(S<sub>K</sub>) = 14, so the old prescription supplies 29<super>46</super> while the new F constant coefficient needs 29<super>68</super>. Reusing that local prescription leaves 22 denominator powers of 29.')
S('How the check was verified')
P('The supplied script constructs each entry as an exact rational number using Bernoulli moments and partial fractions. It then computes the full rational determinant by Gaussian elimination and separately computes its valuation by modular elimination with tracked precision. The two algorithms agree for both functionals and all six primes.')
P('K = 40 is below the later global requirement K ≥ 200M². That does not invalidate this local counterexample: the tested lemma has the separate hypotheses (4.9), all checked above. No asymptotic claim is inferred from the example.','small')

page('Repairing the small and intermediate primes')
S('9. Completion and small primes — pages 6–9')
P('The analytic completion still works for large primes. Its coefficients lose at most one power of p, and the original degree restrictions remain sufficient. There is one small exception worth recording: the analogue of C<sub>p</sub> ∈ p<super>5</super>ℤ<sub>p</sub> is C<sub>p,7</sub> ∈ p<super>7</super>ℤ<sub>p</sub> for p ≥ 11, but v<sub>7</sub>(C<sub>7,7</sub>) = 6. Treating 7 among the small primes handles this without an asymptotic cost.')
P('The integer-valued basis survives. Five derivatives and seventh-order harmonic denominators change the coarse bound (3.12) to')
E('v<sub>p</sub><super>G</super>(F<sub>7,K</sub>) ≥ −8h⌊log<sub>p</sub>(5K)⌋ − h v<sub>p</sub>(720),')
P('in place of −6h⌊log<sub>p</sub>(5K)⌋ − h v<sub>p</sub>(24). The leading normalization cost over p ≤ K/M therefore changes from 6λ/M to 8λ/M. Fixed primes and higher prime powers contribute only o(K²).')
P('A simple pole already shows the mechanism. At j = p+1, H<sub>j</sub><super>(s)</super> contains the term 1/p<super>s</super> and j is a p-unit, so the pole’s constant coefficient has valuation −s. The change −5 to −7 is real. At j = p, the factor j<super>s−1</super> cancels all but one denominator power, independently of s.','small')
S('10. Intermediate primes — (4.2)–(4.8), pages 10–11')
P('For K/M &lt; p ≤ K/3, retain the paper’s basis, which prescribes zeros at residue classes. Let ℓ<sub>A</sub>(a) count j ≤ A with j ≡ ±a (mod p), and ν<sub>i</sub>(a) be the order of vanishing of row i at t = −a². The ordinary-source entry bound changes as follows:')
E('ζ(5): ν<sub>i</sub> + ν<sub>j</sub> + 6ℓ<sub>N</sub> − ℓ<sub>K</sub> − 4,<br/>ζ(7): ν<sub>i</sub> + ν<sub>j</sub> + 6ℓ<sub>N</sub> − ℓ<sub>K</sub> − 6.')
P('The basis is still unimodular: changing basis introduces no p-denominator. Its ordinary row weights each decrease by 1, so the determinant bound decreases by 2 per ordinary row. The reserved zero block has only O<sub>M</sub>(1) rows, while the full matrix has h = λK rows.')
E('γ<sub>7,p</sub><super>in</super> = γ<sub>5,p</sub><super>in</super> − 2h + O<sub>M</sub>(1),<br/>Γ<sub>7</sub>(x) = Γ<sub>5</sub>(x) − 2λx,  x = K/p.')
P('This gives an additional normalization coefficient 2λ(1/3−1/M). The small-prime increase contributes 2λ/M, so their sum is <b>2λ/3 = 37/60</b>. Moving the cutoff does not remove this combined loss.')
P('The formula concerns the explicit bounds produced by this basis. It is not a claim that the determinant’s true coefficient content has exactly that size.','small')

page('The outer primes include a genuine improvement')
S('11. Polynomial moments — (4.10), pages 11–12')
P('The higher-order functional has five consecutive factors in its polynomial moment, rather than three. These cancel more Bernoulli denominators. For p ≥ 11, the guaranteed p-integral range improves from e &lt; 2p−3 to e &lt; 3p−4.')
P('Why: if 2e+2 = m(p−1), with 1 ≤ m ≤ 5, one of 2e+3, …, 2e+7 is a multiple of p. It cancels the possible denominator supplied by B<sub>2e+2</sub>. This is the von Staudt–Clausen mechanism [D4].')
E('r<sub>5,p</sub> = max(0, K+4N−2p+2),<br/>r<sub>7,p</sub> = max(0, K+4N−3p+3).')
P('These are rank bounds for the nonintegral polynomial correction. The smaller ζ(7) rank helps. Any explanation that counts only worse harmonic denominators misses this compensation.')
S('12. Pole-class weights — (4.11)–(4.14), pages 12–13')
P('Let ℓ count the original poles in an ordinary class before cancellation, and δ = 1 if a pole was removed by D<sub>N</sub>, otherwise 0. There are ℓ−δ remaining poles. For the low-index rows i &lt; ℓ−2, the repaired weights are')
E('w<sub>7,a,i</sub> = min(0, i+3δ−(ℓ+6)/2).')
P('The higher-index rows retain weight 0. Their cancellation still works because seventh powers have the same odd-exponent reflection congruence as fifth powers. For a removed class, the total denominator cost becomes:')
table([['Number of poles ℓ','2','3','4','5','6'],['ζ(5) cost','0','1','2','4','6'],['ζ(7) cost','0','3','6','9','12'],['ζ(7) zero weights','1','1','1','1','2']],[180,60,60,60,60,60])
P('An unremoved class costs 9(ℓ−2), in place of 7(ℓ−2). The zero-class costs remain 1 or 4. Using the unchanged rank lemma 4.2 with the improved r<sub>7,p</sub> accounts for both effects.')
P('Exact piecewise integration of the resulting outer-prime cost gives an increase of <b>1387/3840 = 0.3611979167</b>. The scalar S<sub>K</sub> is unchanged, so its contribution cancels in this comparison. The formulas and rational integration are supplied in arithmetic_notes.txt and arithmetic_costs.py.')

page('The final inequality loses its negative sign')
P('The prime number theorem converts local valuation costs into K²-scale coefficients, just as in [F, Section 5]. The repaired estimates give the following additional cost:')
table([['Prime range','Added coefficient'],['Small: p ≤ K/M','2λ/M'],['Intermediate: K/M &lt; p ≤ K/3','2λ(1/3−1/M)'],['Outer: p &gt; K/3','1387/3840'],['Total','751/768 = 0.9778645833']],[340,140])
E('A<sub>7,M</sub> = A<sub>5,M</sub> + 751/768.')
P('Here A<sub>5,M</sub> is the paper’s explicit upper bound, not the unknown minimal normalization cost. Its exact formula is')
E('A<sub>5,M</sub> = A<sub>*</sub> + 7λ/M − (2923/240−1/4)/M<super>2</super> + 32/M<super>3</super>,<br/>A<sub>*</sub> = 9928298118277006344769 / 7535670527041937280000,<br/>U = −2733991/2000000.')
P('For M = 200 the original proof has A<sub>5,200</sub> + U = −0.0174078022583. Our repaired transfer has')
E('<b>A<sub>7,200</sub> + U = +0.9604567810750.</b>')
P('Even the formal limit M → ∞ leaves A<sub>*</sub> + U + 751/768 = +0.9283760102417. The displayed formula has A<sub>5,M</sub> &gt; A<sub>*</sub> for every allowed M ≥ 40. Thus changing the fixed cutoff alone cannot rescue this certificate. This compares explicit constants; it does not interchange the K and M limits.')
S('Why that sign matters')
P('If ζ(7) = a/b and Q<sub>K</sub> has integer coefficients and degree h, then b<super>h</super>Q<sub>K</sub>(a/b) is an integer. Positivity makes it nonzero. To obtain a contradiction, the proof needs its value to tend to zero:')
E('0 &lt; b<super>h</super>Q<sub>K</sub>(a/b) ≤ exp[h log b − cK<super>2</super> + o(K<super>2</super>)] → 0.')
P('The linear term h log b cannot compete with negative quadratic decay. But the transferred estimate supplies no c &gt; 0. The final integer contradiction therefore cannot be drawn.')
P('<b>Logical boundary:</b> a positive upper bound is inconclusive. It does not show that Q<sub>K</sub>(ζ(7)) fails to decay, and it does not rule out stronger bounds or a different construction.')

page('Why the real-decay estimate still works')
P('This part is useful because it identifies what does <i>not</i> break. With the same D<sub>N</sub><super>6</super>/D<sub>K</sub>, Andréief’s identity still expresses the determinant as a positive multiple integral:')
E('Δ<sub>7,K</sub>(ζ(7)) = (1/h!) ∫ ∏<sub>i&lt;j</sub>(y<sub>i</sub><super>2</super>−y<sub>j</sub><super>2</super>)<super>2</super><br/>         × ∏<sub>i</sub>[D<sub>N</sub>(y<sub>i</sub><super>2</super>)<super>6</super>/D<sub>K</sub>(y<sub>i</sub><super>2</super>)]w<sub>7</sub>(y<sub>i</sub>) dy<sub>i</sub>.')
P('The only new ingredient is the weight. Its exponential tail is still e<super>−2πy</super>; the power of y changes from 5 to 7. An explicit bound is')
E('w<sub>7</sub>(y) ≤ 2<super>19</super>(1+y)<super>7</super>e<super>−2πy</super>.')
P('For example, this follows from ∑ℓ<super>6</super>q<super>ℓ</super> = q(1+57q+302q²+302q³+57q⁴+q⁵)/(1−q)<super>7</super>, together with 1−e<super>−u</super> ≥ u/(1+u).')
S('The leading field is unchanged')
P('After y<sub>i</sub> = K√t<sub>i</sub>, the same K²-scale logarithmic-energy problem appears:')
E('V(t) = 2π√t + ∫<sub>0</sub><super>1</super>log(t+u²) du − 6∫<sub>0</sub><super>α</super>log(t+u²) du.')
P('The squared Vandermonde rewards separation between the t-points, while V penalizes their locations. A comparison measure ρ bounds this competition. Its potential is U<sub>ρ</sub>(t) = ∫log|t−u| dρ(u), and its energy is I(ρ) = ∫U<sub>ρ</sub>(t) dρ(t).')
P('The additional polynomial weight contributes only O(K log K), below the K² scale. The original comparison measure and energy inequality therefore apply without changing V or U. Keeping the constants explicit, the ζ(7) version gives')
E('0 &lt; F<sub>7,K</sub>(ζ(7)),<br/>log F<sub>7,K</sub>(ζ(7)) ≤ UK<super>2</super> + 26K log K + 200K.')
P('The original bound (6.16) has 24K log K instead of 26K log K. One can check the remaining integral directly: ∫<sub>0</sub><super>∞</super>t<super>−1/2</super>(1+√t)<super>7</super>e<super>−√t</super>dt = 27400.')
P('Thus the analytic part supplies essentially the same amount of decay, while the arithmetic part asks it to cover a substantially larger cost. The underlying issue is the mismatch between these two changes.')
P('The original rigorous comparison-measure certificate in [F, Lemma 6.1 and Appendix A] is used as an established input here. This audit does not claim to have independently rechecked all 684 interval enclosures in that appendix.','small')
P('A separate rational interval check sharpens the diagnosis: even exact finite integration of the same local cost and a perfect potential bound for this same measure leave the final certificate coefficient above 0.9. Thus the failure cannot be repaired merely by tightening the old numerical enclosures. See experiments/main_measure_certificate.py.','small')

page('A further attempted repair and its limits')
S('Adding two more numerator factors')
P('A natural response to the extra denominator loss is to replace D<sub>N</sub><super>6</super> by D<sub>N</sub><super>8</super>. I tested this separately, keeping α = 3/40 and λ = 37/40. It changes the construction, so the previous real bound cannot simply be copied.')
P('This repair helps the arithmetic. At a removed pole class, the additional zeros restore the original ζ(5) row-weight table. But unremoved classes still cost more, and the scalar normalization changes from (N!)<super>12h</super> to (N!)<super>16h</super> in the denominator.')
E('V<sub>8</sub>(t) = V<sub>6</sub>(t) − 2∫<sub>0</sub><super>α</super>log(t+u²) du,<br/>C<sub>8</sub> − C<sub>6</sub> = 4αλ(1−log α) ≈ 0.9962991384.')
P('The new arithmetic coefficient at M = 200 is A<sub>8,200</sub> = 1.723096570942415… . This is an exact rational integral, evaluated over 1,508 intervals. A numerical potential search suggested failure with the old comparison measure ρ. A subsequent interval calculation certifies that limited conclusion using just one point.')
S('One point is enough to reject this measure and cost')
P('Any valid potential upper bound M<sub>8</sub> for the original measure must satisfy M<sub>8</sub> ≥ 2U<sub>ρ</sub>(3/4) − V<sub>8</sub>(3/4). Substituting this lower requirement into the final coefficient gives')
E('A<sub>8,200</sub> + λM<sub>8</sub> − I(ρ) + C<sub>8</sub><br/>≥ A<sub>8,200</sub> + λ[2U<sub>ρ</sub>(3/4)−V<sub>8</sub>(3/4)] − I(ρ) + C<sub>8</sub><br/>&gt; <b>1.3</b>.')
P('The value on the second line is enclosed between 1.305909182511730956 and 1.305909182511731277. The supplied certificate uses rational intervals, integer square roots, and logarithm/arctangent series with explicit remainders. Thus improving the potential search alone cannot make this particular measure-and-arithmetic certificate succeed.')
P('There is also an exact tradeoff: passing from D<sub>N</sub><super>6</super> to D<sub>N</sub><super>8</super> multiplies the normalized positive integrand by ∏<sub>i</sub>[D<sub>N</sub>(y<sub>i</sub>²)/(N!)²]<super>2</super> &gt; 1. Thus F itself becomes larger, even before estimating it. More numerator zeros help divisibility while increasing the real value.')
P('This rules out the specified D<sub>N</sub><super>8</super> certificate with the old measure, not every D<sub>N</sub><super>8</super> construction. Other measures, parameters, or stronger arithmetic bounds remain untested.')

page('Sources, reproducibility, and scope')
P('Source equation numbers and page numbers throughout refer to the version listed below. No previous chat analysis was used. The source paper was identified from the task context because the workspace initially contained no manuscript.')
S('Primary mathematical sources')
P('[F] Aabir Fauzan, <i>ζ(5) is irrational</i>, 17 September 2026, version 1, 32 pages. <link href="https://zenodo.org/records/22826419" color="#096b69">Zenodo record and PDF</link>. Main audit: Sections 2–7; Appendix A supplies the existing energy certificate; Appendix B supplies exact constants. Appendix C concerns the additional irrationality-exponent result and is not needed here.','small')
P('[D1] NIST DLMF, <link href="https://dlmf.nist.gov/25.6.E2" color="#096b69">25.6.2</link>, Euler’s formula for even zeta values. [D2] <link href="https://dlmf.nist.gov/25.11.E29" color="#096b69">25.11.29</link>, Hermite’s integral for Hurwitz zeta. These explain the rational moments and the simple-pole integral.','small')
P('[D3] NIST DLMF, <link href="https://dlmf.nist.gov/24.4" color="#096b69">24.4.1, 24.4.3, and 24.4.18</link>, Bernoulli difference, reflection, and multiplication identities. [D4] <link href="https://dlmf.nist.gov/24.10.i" color="#096b69">24.10(i)</link>, von Staudt–Clausen. These support the local distribution and denominator arguments.','small')
S('Background sources consulted')
P('The <link href="https://github.com/domino14/zeta5" color="#096b69">domino14 Lean formalization</link> (README and definition/functional files) and the <link href="https://isa-afp.org/entries/Zeta_5_Irrational.html" color="#096b69">Archive of Formal Proofs entry</link> helped identify and cross-check the construction. Their reported verification status is not a substitute for the ζ(7) derivations. No Lean or Isabelle build was run. Web sources were accessed 14 November 2026.','small')
S('Files accompanying the report')
table([['File','Purpose'],['sources/Fauzan_2026_zeta5.pdf','Primary manuscript; hash and URLs in source_ledger.json.'],['experiments/exact_checks.py<br/>and .json','Exact matrices and two-method determinant checks.'],['arithmetic_notes.txt;<br/>algebra_notes.txt','Detailed derivations and source equation references.'],['arithmetic_costs.py;<br/>arithmetic_exact_inner.py','Exact outer and inner cost integrals.'],['arithmetic_variant_notes.txt<br/>and arithmetic_variant_results.json','D⁸ arithmetic derivation and exact constants.'],['experiments/single_point_certificate.py;<br/>experiments/main_measure_certificate.py','Rational interval checks for the specified D⁸ and D⁶ certificates.']],[220,260],small=True)
P('Run <b>python experiments/exact_checks.py</b> for the finite counterexample, <b>python arithmetic_costs.py</b> for the main cost comparison, and <b>python arithmetic_exact_inner.py</b> followed by <b>python experiments/single_point_certificate.py</b> for the D⁸ check. These use standard-library Python. The PDF source is build_report.py.','small')
S('Verification record')
P('Identities were checked on exact examples; outer weights on 1,975 parameter pairs. The determinant used two exact methods. Exact integration reproduces [F, (5.18)]. The initial potential search is exploratory; the final single-point D⁸ rejection uses rigorous rational intervals.','small')

def footer(canvas,doc):
    canvas.setTitle('Why the zeta(5) argument does not directly prove zeta(7)')
    canvas.setAuthor('Independent mathematical exploration')
    canvas.setStrokeColor(colors.HexColor('#d7e0e4'));canvas.setLineWidth(.5)
    canvas.line(54,42,558,42)
    canvas.setFont('Cambria',8.5);canvas.setFillColor(GREY)
    canvas.drawString(54,29,'ζ(5) to ζ(7)  |  Scope: the specified transfer and its estimates')
    canvas.drawRightString(558,29,str(doc.page))

doc=SimpleDocTemplate(str(OUT/'zeta7_argument_audit.pdf'),pagesize=(612,792),
                     rightMargin=66,leftMargin=66,topMargin=49,bottomMargin=58)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(OUT/'report_text_for_review.txt').write_text('\n\n'.join(plain),encoding='utf-8')
print(OUT/'zeta7_argument_audit.pdf')
