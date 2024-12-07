import unittest
from agents.link_genuinity_classifier import LinkGenuinityClassifier

class TestLinkGenuinityClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = LinkGenuinityClassifier()

    def test_ssl_certificate_check(self):
        result = self.classifier.check_ssl_certificate("https://www.google.com")
        self.assertTrue(
            result['valid'], 
            f"Expected valid SSL certificate but got: {result}"
        )
        self.assertIn("issuer", result, "Issuer information missing")
        self.assertIn("subject", result, "Subject information missing")
        self.assertIn("expiration", result, "Expiration date missing")

    def test_domain_age_check(self):
        # Test domain age check
        result = self.classifier.check_domain_age("https://www.google.com")
        self.assertTrue(result['valid'])
        self.assertTrue(result.get('age_days', 0) > 0)

    def test_analyze_link(self):
        # Test link analysis
        result = self.classifier.analyze_link("https://www.example.com")
        self.assertIsNotNone(result)
        self.assertIn('is_safe', result.model_dump())

    def test_health_check(self):
        # Test health check method
        health_status = self.classifier.health_check()
        self.assertEqual(health_status['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()