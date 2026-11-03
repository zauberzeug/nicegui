from nicegui.props import Props


class _DummyElement:
    def update(self) -> None:
        pass


def test_rename_moves_deprecated_prop_to_new_name():
    props = Props(element=_DummyElement())
    props.add_rename('old_name', 'new-name')

    props['old_name'] = 'A'

    assert 'old_name' not in props
    assert props['new-name'] == 'A'


def test_rename_does_not_clobber_new_value_on_later_changes():
    props = Props(element=_DummyElement())
    props.add_rename('old_name', 'new-name')
    props['old_name'] = 'A'

    props['new-name'] = 'B'
    props['unrelated'] = 'x'  # trigger another update pass over the renames

    assert props['new-name'] == 'B'
    assert 'old_name' not in props
