example (h : (2:ℕ) = 1) : (3:ℝ) < 0 := absurd h (by norm_num)
example (h : (2:ℝ) = 1) : (3:ℝ) < 0 := absurd h (by norm_num)
example (h : (2:ℕ) = 1) : (3:ℝ) < 0 := absurd h (by decide)
