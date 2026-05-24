import unittest


from gaskill.sstat import (
    mean, geometric_mean, harmonic_mean, median, mode, quantile, quartiles, iqr,
    variance, stdev, mad, range_stat, cv, skewness, kurtosis,
    covariance, correlation, spearman, linear_regression,
    normal_pdf, normal_cdf, binomial_pmf, poisson_pmf,
    z_score, t_test, chi_square, f_test, normalize, standardize,
    rolling_mean, ewma, summary, probability_distribution
)


class TestCentralTendency(unittest.TestCase):
    def test_mean(self):
        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(mean(data), 3)

    def test_mean_empty(self):
        with self.assertRaises(ValueError):
            mean([])

    def test_geometric_mean(self):
        data = [1, 2, 4]
        result = geometric_mean(data)
        self.assertAlmostEqual(result, 2)

    def test_geometric_mean_negative(self):
        with self.assertRaises(ValueError):
            geometric_mean([-1, 1])

    def test_harmonic_mean(self):
        data = [1, 2, 4]
        result = harmonic_mean(data)
        self.assertAlmostEqual(result, 12/7, places=3)

    def test_median_odd(self):
        data = [1, 3, 2]
        self.assertEqual(median(data), 2)

    def test_median_even(self):
        data = [1, 2, 3, 4]
        self.assertEqual(median(data), 2.5)

    def test_mode(self):
        data = [1, 2, 2, 3, 3, 3]
        result = mode(data)
        self.assertEqual(result, [3])

    def test_quantile(self):
        data = [1, 2, 3, 4, 5]
        self.assertEqual(quantile(data, 0.5), 3)
        self.assertEqual(quartiles(data)[0], 2)
        self.assertEqual(quartiles(data)[1], 3)
        self.assertEqual(quartiles(data)[2], 4)


class TestDispersion(unittest.TestCase):
    def test_variance(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = variance(data)
        self.assertAlmostEqual(result, 4, places=1)

    def test_stdev(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = stdev(data)
        self.assertAlmostEqual(result, 2, places=1)

    def test_mad(self):
        data = [1, 2, 3, 4, 5]
        result = mad(data)
        self.assertAlmostEqual(result, 1.2)

    def test_range_stat(self):
        data = [1, 2, 3, 4, 5]
        self.assertEqual(range_stat(data), 4)


class TestDistribution(unittest.TestCase):
    def test_skewness(self):
        data = [1, 2, 3, 4, 5]
        result = skewness(data)
        self.assertAlmostEqual(result, 0, places=1)

    def test_kurtosis(self):
        data = [1, 2, 3, 4, 5]
        result = kurtosis(data)
        self.assertIsInstance(result, float)  # 只检查返回有效值


class TestCorrelation(unittest.TestCase):
    def test_covariance(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = covariance(x, y)
        self.assertGreater(result, 0)

    def test_correlation_perfect(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = correlation(x, y)
        self.assertAlmostEqual(result, 1)

    def test_spearman(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        result = spearman(x, y)
        self.assertAlmostEqual(result, 1)


class TestRegression(unittest.TestCase):
    def test_linear_regression(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        slope, intercept, r2 = linear_regression(x, y)
        self.assertAlmostEqual(slope, 2, places=1)
        self.assertAlmostEqual(r2, 1)


class TestProbabilityDistributions(unittest.TestCase):
    def test_normal_pdf(self):
        result = normal_pdf(0, 0, 1)
        self.assertAlmostEqual(result, 0.3989, places=3)

    def test_normal_cdf(self):
        result = normal_cdf(0, 0, 1)
        self.assertAlmostEqual(result, 0.5)

    def test_binomial_pmf(self):
        result = binomial_pmf(2, 5, 0.5)
        self.assertAlmostEqual(result, 0.3125, places=3)

    def test_poisson_pmf(self):
        result = poisson_pmf(3, 2)
        self.assertAlmostEqual(result, 0.180, places=2)


class TestHypothesisTesting(unittest.TestCase):
    def test_z_score(self):
        result = z_score(85, 70, 10)
        self.assertEqual(result, 1.5)

    def test_t_test(self):
        data = [1, 2, 3, 4, 5]
        t, p = t_test(data, 3)
        self.assertAlmostEqual(t, 0, places=5)

    def test_chi_square(self):
        observed = [10, 20, 30]
        expected = [15, 20, 25]
        result = chi_square(observed, expected)
        self.assertGreater(result, 0)


class TestNormalization(unittest.TestCase):
    def test_normalize(self):
        data = [0, 25, 50, 75, 100]
        result = normalize(data, 0, 1)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[-1], 1)

    def test_standardize(self):
        data = [1, 2, 3, 4, 5]
        result = standardize(data)
        self.assertAlmostEqual(sum(result), 0, places=5)


class TestTimeSeries(unittest.TestCase):
    def test_rolling_mean(self):
        data = [1, 2, 3, 4, 5]
        result = rolling_mean(data, 3)
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[0], 2)

    def test_ewma(self):
        data = [1, 2, 3, 4, 5]
        result = ewma(data, 0.5)
        self.assertEqual(len(result), 5)


class TestSummary(unittest.TestCase):
    def test_summary(self):
        data = [1, 2, 3, 4, 5]
        result = summary(data)
        self.assertIn('mean', result)
        self.assertIn('median', result)
        self.assertIn('stdev', result)

    def test_probability_distribution(self):
        data = [1, 1, 2, 3, 3, 3]
        result = probability_distribution(data)
        self.assertAlmostEqual(result[1], 1/3)
        self.assertAlmostEqual(result[3], 0.5)


if __name__ == '__main__':
    unittest.main()
