const config = {
  plugins: [
    //require('autoprefixer'),

    //This plugin is required for nested @keyframe rules
    require('postcss-nested'),

    //require('postcss-discard-comments')({
    //  removeAll: true,
    //}),
  ]
}
module.exports = config
