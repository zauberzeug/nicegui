import {
  ModuleRegistry,
  AllCommunityModule,
  createGrid,
  themeAlpine,
  themeBalham,
  themeMaterial,
  themeQuartz,
  colorSchemeDark,
  colorSchemeLight,
} from "ag-grid-community";

ModuleRegistry.registerModules([AllCommunityModule]);

export default { createGrid, themeAlpine, themeBalham, themeMaterial, themeQuartz, colorSchemeDark, colorSchemeLight };
