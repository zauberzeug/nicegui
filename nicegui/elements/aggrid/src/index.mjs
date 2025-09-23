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

export default {
  createGrid,
  themes: {
    alpine: themeAlpine,
    balham: themeBalham,
    material: themeMaterial,
    quartz: themeQuartz,
  },
  colorSchemeDark,
  colorSchemeLight,
};
