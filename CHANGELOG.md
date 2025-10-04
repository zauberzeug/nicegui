## [Unreleased]

### Bugfixes

- Fix docker builds by not excluding dist/ directories from the build context (#5200, #5202 by @Yuerchu, @rodja, @falkoschindler)

### Testing

- Check disabled state before clicking or clearing via user simulated interaction (#5191, #5209 by @igro-marczak, @rodja)

### Documentation

- Fix menu by disabling the deselection of tree elements (#5207, #5208 by @python-and-novella, @rodja)
- Fix custom toggle button demo (#5203 by @rodja)

### Infrastructure

- Re-run poetry lock to fix nicegui-highcharts incompatibility (#5204 by @evnchn)
- Use poetry 2.1.2 in the devcontainer (#5205 by @evnchn)
- Fix fly docker build (#5210 by @rodja)
