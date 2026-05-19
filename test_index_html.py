import unittest
from html.parser import HTMLParser

class IndexHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.attrs = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.append(dict(attrs))

class TestIndexHTML(unittest.TestCase):
    def setUp(self):
        with open('index.html', 'r', encoding='utf-8') as f:
            self.html_content = f.read()
        self.parser = IndexHTMLParser()
        self.parser.feed(self.html_content)

    def test_doctype_and_html_lang(self):
        self.assertTrue(self.html_content.lstrip().startswith('<!DOCTYPE html>'))
        self.assertIn('<html lang="en">', self.html_content)

    def test_meta_and_title_tags(self):
        self.assertIn('<meta charset="UTF-8" />', self.html_content)
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0" />', self.html_content)
        self.assertIn('<title>', self.html_content)

    def test_brand_tokens_in_style(self):
        style_start = self.html_content.find('<style>')
        style_end = self.html_content.find('</style>')
        self.assertNotEqual(style_start, -1)
        self.assertNotEqual(style_end, -1)
        style_content = self.html_content[style_start:style_end]
        allowed_tokens = ['--brand-primary', '--brand-accent', '--text-primary', '--surface-background']
        for token in allowed_tokens:
            self.assertIn(token, style_content)

    def test_hero_section_and_primary_button(self):
        self.assertIn('<HeroSection', self.html_content)
        self.assertIn('<PrimaryButton>', self.html_content)

    def test_telemetry_hero_section(self):
        self.assertIn('Telemetry Initialization', self.html_content)
        self.assertIn('Configure telemetry baselines and observability', self.html_content)
        self.assertIn('Initialize Telemetry', self.html_content)

    def test_script_tag(self):
        self.assertIn('<script type="module" src="/src/main.ts"></script>', self.html_content)

if __name__ == '__main__':
    unittest.main()
