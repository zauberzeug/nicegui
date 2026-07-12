from pathlib import Path
from unittest.mock import ANY, MagicMock, patch

from nicegui.dependencies import register_esm_glob, register_library_glob, register_vue_component_glob, resolve_glob

# ---------------------------------------------------------------------------
# resolve_glob
# ---------------------------------------------------------------------------


def test_resolve_glob_absolute_path(tmp_path):
    f = tmp_path / 'a.js'
    f.touch()
    assert resolve_glob(f, base=Path('/irrelevant')) == [f]


def test_resolve_glob_relative_to_base(tmp_path):
    f = tmp_path / 'a.js'
    f.touch()
    assert resolve_glob('a.js', base=tmp_path) == [f]


def test_resolve_glob_pattern_sorted_by_stem(tmp_path):
    (tmp_path / 'b.js').touch()
    (tmp_path / 'a.js').touch()
    assert resolve_glob('*.js', base=tmp_path) == [tmp_path / 'a.js', tmp_path / 'b.js']


def test_resolve_glob_no_match_returns_empty(tmp_path):
    assert resolve_glob('missing.js', base=tmp_path) == []


# ---------------------------------------------------------------------------
# register_library_glob
# ---------------------------------------------------------------------------

def test_register_library_glob_single_file(tmp_path):
    f = tmp_path / 'lib.js'
    f.touch()
    with patch('nicegui.dependencies.register_library', return_value=MagicMock()) as mock:
        results = register_library_glob('lib.js', base=tmp_path)
    mock.assert_called_once_with(f, import_name=None, max_time=ANY)
    assert len(results) == 1


def test_register_library_glob_passes_import_name(tmp_path):
    f = tmp_path / 'lib.js'
    f.touch()
    with patch('nicegui.dependencies.register_library', return_value=MagicMock()) as mock:
        register_library_glob('lib.js', base=tmp_path, import_name='my_mod')
    mock.assert_called_once_with(f, import_name='my_mod', max_time=ANY)


def test_register_library_glob_multi_file_shares_max_time(tmp_path):
    (tmp_path / 'a.js').touch()
    (tmp_path / 'b.js').touch()
    with patch('nicegui.dependencies.register_library', return_value=MagicMock()) as mock:
        results = register_library_glob('*.js', base=tmp_path)
    assert mock.call_count == 2
    assert len(results) == 2
    max_times = {call.kwargs['max_time'] for call in mock.call_args_list}
    assert len(max_times) == 1, 'all matched files must share the same max_time'


def test_register_library_glob_no_match_returns_empty(tmp_path):
    with patch('nicegui.dependencies.register_library') as mock:
        results = register_library_glob('missing.js', base=tmp_path)
    mock.assert_not_called()
    assert results == []


# ---------------------------------------------------------------------------
# register_esm_glob
# ---------------------------------------------------------------------------

def test_register_esm_glob_single_file(tmp_path):
    f = tmp_path / 'mod.js'
    f.touch()
    with patch('nicegui.dependencies.register_esm') as mock:
        register_esm_glob('mykey', 'mod.js', base=tmp_path)
    mock.assert_called_once_with('mykey', f, max_time=ANY)


def test_register_esm_glob_multi_file_shares_max_time(tmp_path):
    (tmp_path / 'a.js').touch()
    (tmp_path / 'b.js').touch()
    with patch('nicegui.dependencies.register_esm') as mock:
        register_esm_glob('mykey', '*.js', base=tmp_path)
    assert mock.call_count == 2
    max_times = {call.kwargs['max_time'] for call in mock.call_args_list}
    assert len(max_times) == 1, 'all matched files must share the same max_time'


# ---------------------------------------------------------------------------
# register_vue_component_glob
# ---------------------------------------------------------------------------

def test_register_vue_component_glob_single_file(tmp_path):
    f = tmp_path / 'widget.js'
    f.touch()
    sentinel = MagicMock()
    with patch('nicegui.dependencies.register_vue_component', return_value=sentinel) as mock:
        result = register_vue_component_glob('widget.js', base=tmp_path)
    mock.assert_called_once_with(f, max_time=ANY)
    assert result is sentinel


def test_register_vue_component_glob_multi_file_returns_last_and_shares_max_time(tmp_path):
    (tmp_path / 'a.js').touch()
    (tmp_path / 'b.js').touch()
    last = MagicMock()
    side_effects = [MagicMock(), last]
    with patch('nicegui.dependencies.register_vue_component', side_effect=side_effects) as mock:
        result = register_vue_component_glob('*.js', base=tmp_path)
    assert mock.call_count == 2
    assert result is last
    max_times = {call.kwargs['max_time'] for call in mock.call_args_list}
    assert len(max_times) == 1, 'all matched files must share the same max_time'


def test_register_vue_component_glob_no_match_returns_none(tmp_path):
    with patch('nicegui.dependencies.register_vue_component') as mock:
        result = register_vue_component_glob('missing.js', base=tmp_path)
    mock.assert_not_called()
    assert result is None


def test_register_esm_glob_no_match_calls_nothing(tmp_path):
    with patch('nicegui.dependencies.register_esm') as mock:
        register_esm_glob('mykey', 'missing.js', base=tmp_path)
    mock.assert_not_called()
