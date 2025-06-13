import re

import pytest

from nicegui.elements.sub_pages import SubPages

# pylint: disable=protected-access


def test_exact_match_simple_path():
    """Test exact matching of simple paths without parameters."""
    assert SubPages._match_path('/', '/') == {}
    assert SubPages._match_path('/home', '/home') == {}
    assert SubPages._match_path('/users', '/users') == {}
    assert SubPages._match_path('/api/v1', '/api/v1') == {}


def test_exact_match_no_match():
    """Test that non-matching paths return None."""
    assert SubPages._match_path('/', '/home') is None
    assert SubPages._match_path('/home', '/') is None
    assert SubPages._match_path('/users', '/user') is None
    assert SubPages._match_path('/api/v1', '/api/v2') is None
    assert SubPages._match_path('/home', '/home/sub') is None
    assert SubPages._match_path('/home/sub', '/home') is None


def test_single_parameter_match():
    """Test matching patterns with a single parameter."""
    assert SubPages._match_path('/user/{id}', '/user/123') == {'id': '123'}
    assert SubPages._match_path('/user/{id}', '/user/abc') == {'id': 'abc'}
    assert SubPages._match_path('/user/{id}', '/user/test-user') == {'id': 'test-user'}
    assert SubPages._match_path('/{category}', '/books') == {'category': 'books'}
    assert SubPages._match_path('/api/{version}', '/api/v1') == {'version': 'v1'}


def test_single_parameter_no_match():
    """Test that single parameter patterns correctly reject non-matches."""
    assert SubPages._match_path('/user/{id}', '/user/') is None  # Empty parameter
    assert SubPages._match_path('/user/{id}', '/user') is None   # Missing parameter
    assert SubPages._match_path('/user/{id}', '/admin/123') is None  # Wrong path
    assert SubPages._match_path('/user/{id}', '/user/123/edit') is None  # Extra segments
    assert SubPages._match_path('/{category}', '/') is None  # Empty parameter


def test_multiple_parameters_match():
    """Test matching patterns with multiple parameters."""
    assert SubPages._match_path('/user/{id}/post/{post_id}', '/user/123/post/456') == {
        'id': '123', 'post_id': '456'
    }
    assert SubPages._match_path('/{category}/{subcategory}', '/books/fiction') == {
        'category': 'books', 'subcategory': 'fiction'
    }
    assert SubPages._match_path('/api/{version}/{endpoint}', '/api/v1/users') == {
        'version': 'v1', 'endpoint': 'users'
    }
    assert SubPages._match_path('/{a}/{b}/{c}', '/x/y/z') == {
        'a': 'x', 'b': 'y', 'c': 'z'
    }


def test_multiple_parameters_no_match():
    """Test that multiple parameter patterns correctly reject non-matches."""
    assert SubPages._match_path('/user/{id}/post/{post_id}', '/user/123/post') is None
    assert SubPages._match_path('/user/{id}/post/{post_id}', '/user/123') is None
    assert SubPages._match_path('/user/{id}/post/{post_id}', '/user/123/comment/456') is None
    assert SubPages._match_path('/{a}/{b}', '/x') is None
    assert SubPages._match_path('/{a}/{b}', '/x/y/z') is None


def test_mixed_static_and_parameter_segments():
    """Test patterns mixing static segments with parameters."""
    assert SubPages._match_path('/api/v1/user/{id}', '/api/v1/user/123') == {'id': '123'}
    assert SubPages._match_path('/static/{dynamic}/more', '/static/test/more') == {'dynamic': 'test'}
    assert SubPages._match_path('/prefix/{middle}/suffix', '/prefix/value/suffix') == {'middle': 'value'}
    assert SubPages._match_path('/user/{id}/settings', '/user/123/settings') == {'id': '123'}


def test_mixed_static_and_parameter_no_match():
    """Test that mixed patterns correctly reject non-matches."""
    assert SubPages._match_path('/api/v1/user/{id}', '/api/v2/user/123') is None
    assert SubPages._match_path('/static/{dynamic}/more', '/static/test/less') is None
    assert SubPages._match_path('/user/{id}/settings', '/user/123/profile') is None
    assert SubPages._match_path('/prefix/{middle}/suffix', '/prefix/value') is None


def test_parameter_names_with_underscores_and_numbers():
    """Test parameter names with valid identifier characters."""
    assert SubPages._match_path('/user/{user_id}', '/user/123') == {'user_id': '123'}
    assert SubPages._match_path('/post/{post_id2}', '/post/abc') == {'post_id2': 'abc'}
    assert SubPages._match_path('/{param1}/{param_2}', '/a/b') == {'param1': 'a', 'param_2': 'b'}
    # Valid parameter names (Python identifiers)
    assert SubPages._match_path('/path/{_}', '/path/value') == {'_': 'value'}
    assert SubPages._match_path('/path/{_param}', '/path/value') == {'_param': 'value'}
    assert SubPages._match_path('/path/{param_}', '/path/value') == {'param_': 'value'}
    assert SubPages._match_path('/path/{a1}', '/path/value') == {'a1': 'value'}
    assert SubPages._match_path('/path/{param123}', '/path/value') == {'param123': 'value'}


def test_parameter_values_with_special_characters():
    """Test that parameter values can contain various characters (except /)."""
    assert SubPages._match_path('/user/{id}', '/user/123-abc') == {'id': '123-abc'}
    assert SubPages._match_path('/user/{id}', '/user/test_user') == {'id': 'test_user'}
    assert SubPages._match_path('/user/{id}', '/user/user@example.com') == {'id': 'user@example.com'}
    assert SubPages._match_path('/file/{name}', '/file/document.pdf') == {'name': 'document.pdf'}
    assert SubPages._match_path('/search/{query}', '/search/hello%20world') == {'query': 'hello%20world'}

    # Parameter values cannot contain forward slashes
    assert SubPages._match_path('/user/{id}', '/user/123/456') is None
    assert SubPages._match_path('/file/{path}', '/file/folder/file.txt') is None


def test_empty_strings_and_edge_cases():
    """Test edge cases with empty strings and unusual inputs."""
    assert SubPages._match_path('', '') == {}
    assert SubPages._match_path('', '/') is None
    assert SubPages._match_path('/', '') is None
    assert SubPages._match_path('/user/{id}', '/user/') is None  # Empty parameter


def test_case_sensitivity():
    """Test that matching is case-sensitive."""
    assert SubPages._match_path('/User', '/user') is None
    assert SubPages._match_path('/user', '/User') is None
    assert SubPages._match_path('/user/{ID}', '/user/abc') == {'ID': 'abc'}  # Parameter name is case-sensitive


def test_special_characters_in_patterns():
    """Test that special regex characters in static parts are handled correctly."""
    # Should match literally
    assert SubPages._match_path('/api.v1', '/api.v1') == {}
    assert SubPages._match_path('/search?', '/search?') == {}
    assert SubPages._match_path('/path[0]', '/path[0]') == {}
    assert SubPages._match_path('/price$', '/price$') == {}
    assert SubPages._match_path('/regex*', '/regex*') == {}

    # Should not match due to literal interpretation
    assert SubPages._match_path('/api.v1', '/apixv1') is None
    assert SubPages._match_path('/search?', '/search') is None

    # Literal curly braces (not valid parameter syntax)
    assert SubPages._match_path('/path{', '/path{') == {}
    assert SubPages._match_path('/path}', '/path}') == {}
    assert SubPages._match_path('/path{invalid', '/path{invalid') == {}
    assert SubPages._match_path('/path{', '/path}') is None
    assert SubPages._match_path('/path}', '/path{') is None


def test_invalid_parameter_names():
    """Test handling of invalid parameter names in patterns."""
    # Numbers are not valid parameter names - cause regex errors
    with pytest.raises(re.error):
        SubPages._match_path('/path{123}', '/path{123}')

    with pytest.raises(re.error):
        SubPages._match_path('/path{123abc}', '/path{123abc}')

    # Patterns that don't match \w+ are treated as literal text
    assert SubPages._match_path('/path{param-name}', '/path{param-name}') == {}
    assert SubPages._match_path('/path{param.name}', '/path{param.name}') == {}
    assert SubPages._match_path('/path{param space}', '/path{param space}') == {}

    # These should not match if the path is different
    assert SubPages._match_path('/path{param-name}', '/path{different}') is None
    assert SubPages._match_path('/path{param.name}', '/path{other.name}') is None


def test_adjacent_parameters():
    """Test patterns with parameters that are adjacent (no static separators)."""
    # This is an edge case - adjacent parameters without separators
    result = SubPages._match_path('/{a}{b}', '/xy')
    # The first parameter will match as much as possible, leaving minimum for the second
    assert result is not None
    assert 'a' in result and 'b' in result
    assert result['a'] + result['b'] == 'xy'


def test_real_world_patterns():
    """Test patterns similar to those used in real applications."""
    # Blog-style URLs
    assert SubPages._match_path('/blog/{year}/{month}/{slug}', '/blog/2023/12/my-post') == {
        'year': '2023', 'month': '12', 'slug': 'my-post'
    }

    # API endpoints
    assert SubPages._match_path('/api/v1/users/{user_id}/posts/{post_id}',
                                '/api/v1/users/123/posts/456') == {
        'user_id': '123', 'post_id': '456'
    }

    # File paths
    assert SubPages._match_path('/files/{category}/{filename}',
                                '/files/images/photo.jpg') == {
        'category': 'images', 'filename': 'photo.jpg'
    }

    # E-commerce
    assert SubPages._match_path('/shop/{category}/{product_id}',
                                '/shop/electronics/laptop-123') == {
        'category': 'electronics', 'product_id': 'laptop-123'
    }
