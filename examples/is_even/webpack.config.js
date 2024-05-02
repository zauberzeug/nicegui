const path = require("path");

module.exports = {
  entry: "is-odd/index.js",
  mode: "development",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "is-odd.js",
    library: "isOdd",
    libraryTarget: "umd",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
    ],
  },
};
