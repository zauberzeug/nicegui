from website.seo import breadcrumb_jsonld, extract_description, page_seo_html


def test_extract_description_plain_text():
    text = 'This is a simple description that is long enough to pass the minimum length threshold for extraction.'
    result = extract_description(text)
    assert result == text


def test_extract_description_returns_none_for_short_text():
    assert extract_description('Too short') is None
    assert extract_description('') is None


def test_extract_description_strips_markdown_bold():
    text = 'This is **bold text** that should be cleaned up properly by the extraction function.'
    result = extract_description(text)
    assert '**' not in result
    assert 'bold text' in result


def test_extract_description_strips_markdown_italic():
    text = 'This is _italic text_ that should be cleaned up properly by the extraction function.'
    result = extract_description(text)
    assert result is not None
    assert '_italic' not in result
    assert 'italic text' in result


def test_extract_description_strips_markdown_links():
    text = 'Click [this link](https://example.com) to visit the site and learn about the features.'
    result = extract_description(text)
    assert result is not None
    assert 'this link' in result
    assert 'https://example.com' not in result
    assert '[' not in result
    assert '](' not in result


def test_extract_description_strips_rst_links():
    text = 'See `NiceGUI documentation <https://nicegui.io>`_ for more information about all features.'
    result = extract_description(text)
    assert result is not None
    assert 'NiceGUI documentation' in result
    assert 'https://nicegui.io' not in result
    assert '`' not in result


def test_extract_description_strips_backtick_code():
    text = 'Use the `ui.button` element to create interactive buttons in your Python application.'
    result = extract_description(text)
    assert result is not None
    assert 'ui.button' in result
    assert '`' not in result


def test_extract_description_strips_html_tags():
    text = 'This has <b>bold HTML</b> and <a href="url">a link</a> that need to be properly cleaned.'
    result = extract_description(text)
    assert result is not None
    assert '<b>' not in result
    assert '<a ' not in result
    assert 'bold HTML' in result


def test_extract_description_truncates_long_text():
    text = 'A ' * 200  # very long text
    result = extract_description(text)
    assert result is not None
    assert len(result) <= 160
    assert result.endswith('...')


def test_extract_description_truncates_at_word_boundary():
    text = 'word ' * 50  # 250 chars
    result = extract_description(text)
    assert result is not None
    assert len(result) <= 160
    assert result.endswith('...')
    assert not result.endswith(' ...')  # should not have trailing space before ellipsis


def test_extract_description_strips_param_directives():
    text = ('This function does something useful and important for the application.\n'
            ':param name: the name of the element\n'
            ':type name: str')
    result = extract_description(text)
    assert result is not None
    assert ':param' not in result
    assert 'something useful' in result


def test_extract_description_strips_return_directives():
    text = ('This function returns a value that is useful for the calling application.\n'
            ':return the computed value')
    result = extract_description(text)
    assert result is not None
    assert ':return' not in result


def test_extract_description_collapses_whitespace():
    text = 'This   has    lots\n\nof    whitespace   scattered   throughout   the  entire  text  string.'
    result = extract_description(text)
    assert result is not None
    assert '  ' not in result


def test_page_seo_html_contains_meta_description():
    result = page_seo_html(title='Test', description='A test page', path='/test')
    assert '<meta name="description"' in result
    assert 'A test page' in result


def test_page_seo_html_contains_canonical():
    result = page_seo_html(title='Test', description='A test page', path='/test')
    assert '<link rel="canonical"' in result
    assert 'https://nicegui.io/test' in result


def test_page_seo_html_contains_open_graph():
    result = page_seo_html(title='Test', description='A test page', path='/test')
    assert 'og:title' in result
    assert 'og:description' in result
    assert 'og:url' in result
    assert 'og:type' in result
    assert 'og:site_name' in result


def test_page_seo_html_contains_twitter_card():
    result = page_seo_html(title='Test', description='A test page', path='/test')
    assert 'twitter:card' in result
    assert 'twitter:title' in result


def test_page_seo_html_escapes_special_characters():
    result = page_seo_html(title='Test & "Quotes"', description='A <b>bold</b> description', path='/test')
    assert 'Test &amp; &quot;Quotes&quot;' in result
    assert '&lt;b&gt;bold&lt;/b&gt;' in result


def test_page_seo_html_og_type_default():
    result = page_seo_html(title='Test', description='Desc', path='/')
    assert 'content="website"' in result


def test_page_seo_html_og_type_article():
    result = page_seo_html(title='Test', description='Desc', path='/', og_type='article')
    assert 'content="article"' in result


def test_breadcrumb_jsonld_structure():
    result = breadcrumb_jsonld([('Home', '/'), ('Docs', '/docs')])
    assert '<script type="application/ld+json">' in result
    assert '</script>' in result
    assert 'BreadcrumbList' in result
    assert '"position":1' in result
    assert '"position":2' in result
    assert '"name":"Home"' in result
    assert '"name":"Docs"' in result


def test_breadcrumb_jsonld_includes_full_urls():
    result = breadcrumb_jsonld([('Home', '/'), ('Docs', '/docs')])
    assert 'https://nicegui.io/' in result
    assert 'https://nicegui.io/docs' in result


def test_breadcrumb_jsonld_escapes_closing_script():
    result = breadcrumb_jsonld([('Test</script>', '/test')])
    assert '</script><' not in result.replace('</script>', '', 1)  # only the closing tag itself
