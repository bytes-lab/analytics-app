const ModuleScopePlugin = require("react-dev-utils/ModuleScopePlugin");
// module.exports = (config, env) => {
//   config.resolve.plugins = config.resolve.plugins.filter(
//     (plugin) => !(plugin instanceof ModuleScopePlugin)
//   );

//   return config;
// };

// In version 1 of react-scripts it was possible to have multiple applications
// coexist on a single page without conflicts, but version 2 uses some webpack
// features that cause errors when two or more apps try to render themselves on
// the one page. For this reason we use react-app-rewired to override some of
// the internal webpack config of react-scripts. This fixes those errors, and
// lets us keep relying on react-scripts to manage our build tooling for us.

module.exports = (configuration, env) => {
  const config = configuration;
  config.resolve.plugins = config.resolve.plugins.filter(
    (plugin) => !(plugin instanceof ModuleScopePlugin)
  );
  config.optimization.runtimeChunk = false;
  config.optimization.splitChunks = {
    cacheGroups: {
      default: false,
    },
  };
  return config;
};
