# CSP Test Coverage

This document tracks which test files have CSP (Content Security Policy) enabled.

## Summary

- **Total test files**: 117
- **CSP-enabled test files**: 64 (55%)
- **Tests using dynamic CSS**: 2 tests (test_dialog_scroll_behavior, test_popup_scroll_behavior)

## Strategy

1. **Module-level CSP**: Most test files have a module-level `enable_csp_for_module` fixture that enables CSP for all tests in that module.

2. **Selective disable**: For test files that contain both CSP-compatible and incompatible tests (test_dialog.py, test_select.py), we:
   - Enable CSP at module level
   - Add a `disable_csp` fixture for specific tests that use `ui.add_css()` or dynamic style injection

3. **Excluded files**: Some test files are excluded because they:
   - Test features that inherently require dynamic CSS/JavaScript
   - Test specific functionality that bypasses CSP
   - Don't exist (were listed but not found)

## CSP-Enabled Test Files

The following test files have CSP enabled:

1. test_aggrid.py
2. test_audio.py
3. test_binding.py
4. test_button.py
5. test_button_dropdown.py
6. test_button_group.py
7. test_card.py
8. test_carousel.py
9. test_chat_message.py
10. test_chip.py
11. test_code.py
12. test_color_input.py
13. test_colors.py
14. test_context_menu.py
15. test_csp.py
16. test_dark_mode.py
17. test_date.py
18. test_date_input.py
19. test_defaults.py
20. test_dialog.py ⚠️ (one test disables CSP)
21. test_echart.py
22. test_element.py
23. test_events.py
24. test_expansion.py
25. test_fab.py
26. test_header.py
27. test_highchart.py
28. test_image.py
29. test_input.py
30. test_input_chips.py
31. test_interactive_image.py
32. test_json.py
33. test_knob.py
34. test_label.py
35. test_link.py
36. test_list.py
37. test_log.py
38. test_markdown.py
39. test_menu.py
40. test_notification.py
41. test_number.py
42. test_page.py
43. test_page_title.py
44. test_pagination.py
45. test_plotly.py
46. test_radio.py
47. test_range.py
48. test_rating.py
49. test_refreshable.py
50. test_select.py ⚠️ (one test disables CSP)
51. test_slide_item.py
52. test_spinner.py
53. test_splitter.py
54. test_stepper.py
55. test_table.py
56. test_tabs.py
57. test_teleport.py
58. test_time.py
59. test_timeline.py
60. test_toggle.py
61. test_tooltip.py
62. test_tree.py
63. test_upload.py
64. test_video.py

## Files Without CSP

These files don't have CSP enabled yet:

- test_add_html.py (explicitly tests dynamic HTML injection)
- test_alternate_ui_frameworks.py
- test_anywidget.py
- test_api_router.py
- test_auto_context.py
- test_awaitable_response.py
- test_background_tasks.py
- test_clipboard.py
- test_codemirror.py
- test_download.py
- test_editor.py
- test_element_delete.py
- test_element_filter.py
- test_endpoint_docs.py
- test_event.py
- test_favicon.py
- test_fullscreen.py
- test_helpers.py
- test_html.py
- test_javascript.py
- test_joystick.py
- test_json_editor.py
- test_keyboard.py
- test_leaflet.py
- test_lifecycle.py
- test_main_file_marker.py
- test_mermaid.py
- test_navigate.py
- test_observables.py
- test_outbox.py
- test_prod_js.py
- test_quasar_tailwind_interplay.py
- test_query.py
- test_restructured_text.py
- test_root_page.py
- test_run.py
- test_scene.py
- test_scene_view.py
- test_serving_files.py
- test_socketio_too_long.py
- test_speculative_loading.py
- test_storage.py
- test_sub_pages.py
- test_sub_pages_match_path.py
- test_textarea.py
- test_tree_view.py
- test_ui.py
- test_upload_file.py
- test_value_error.py
- And others...

## Known Limitations

### Features Incompatible with CSP

1. **ui.add_css()** - Dynamic CSS injection via JavaScript
2. **ui.add_scss()** - Dynamic SCSS compilation and injection
3. **ui.add_sass()** - Dynamic SASS compilation and injection
4. **Dynamic HTML with inline styles/scripts** - When added after page load via JavaScript

### Workarounds

For tests that need these features:
- Add `disable_csp` fixture parameter to the test function
- Document why CSP needs to be disabled with a comment

Example:
```python
def test_dynamic_css(screen: Screen, disable_csp):
    """This test uses ui.add_css() which is incompatible with CSP."""
    @ui.page('/')
    def page():
        ui.add_css('.my-class { color: red; }')
```

## Testing CSP Coverage

To test CSP-enabled files:
```bash
# Test all CSP-enabled files
pytest tests/test_label.py tests/test_button.py tests/test_input.py ...

# Test a specific CSP-enabled file
pytest tests/test_label.py -v

# Run all tests (CSP-enabled and disabled)
pytest tests/
```

## Future Work

Potential improvements:
1. Enable CSP for more test files
2. Investigate if some excluded tests can be made CSP-compatible
3. Add CSP testing to CI/CD pipeline
4. Document CSP compatibility in main documentation
