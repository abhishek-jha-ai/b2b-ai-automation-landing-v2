import unittest

class TestIndexHtml(unittest.TestCase):
    def setUp(self):
        with open('index.html', 'r', encoding='utf-8') as f:
            self.html_content = f.read()

    def test_title_contains_initialize_monorepo(self):
        # Accepts either the fallback or the ContentSlot tag
        self.assertTrue(
            'Initialize Monorepo' in self.html_content or
            '<ContentSlot content-key="index_html.initialize_monorepo"' in self.html_content
        )

    def test_hero_section_present(self):
        self.assertIn('class="hero-section"', self.html_content)

    def test_hero_title_present(self):
        # Accepts either the fallback or the ContentSlot tag
        self.assertTrue(
            'Welcome to the Monorepo' in self.html_content or
            '<ContentSlot content-key="index_html.welcome_to_the_monorepo"' in self.html_content
        )

    def test_get_started_button_present(self):
        # Accepts either the fallback or the ContentSlot tag
        self.assertTrue(
            'Get Started' in self.html_content or
            '<ContentSlot content-key="index_html.get_started"' in self.html_content
        )

if __name__ == '__main__':
    unittest.main()
