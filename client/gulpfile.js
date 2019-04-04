const autoprefixer = require('autoprefixer')
const sourcemaps = require('gulp-sourcemaps')
const browsersync = require('browser-sync').create()
const cssnano = require('cssnano')
const gulp = require('gulp')
const plumber = require('gulp-plumber')
const postcss = require('gulp-postcss')
const rename = require('gulp-rename')
const sass = require('gulp-sass')
const path = require('path')

// BrowserSync
function browserSync(done) {
  browsersync.init({
    proxy: 'localhost:8080',
    port: 3000
  })
  done()
}

// BrowserSync Reload
function browserSyncReload(done) {
  browsersync.reload()
  done()
}

// Error handling
function onError (err) {
  console.log(err.message)
  this.emit('end')
}

// CSS task
function css() {
  const config = {
    isDev: process.env.NODE_ENV === 'development',
    entry: './scss/**/*.scss',
    dest: gulp.dest(path.resolve(__dirname, '../static/dist/css/'))
  }

  if (config.isDev) {
    return gulp
      .src(config.entry)
      .pipe(plumber({ errorHandler: onError }))
      .pipe(sourcemaps.init())
      .pipe(sass({ outputStyle: 'expanded' }))
      .pipe(postcss([autoprefixer(), cssnano()]))
      .pipe(sourcemaps.write('.'))
      .pipe(config.dest)
      .pipe(browsersync.stream())
  }

  return gulp
    .src(config.entry)
    .pipe(plumber({ errorHandler: onError }))
    .pipe(sass({ outputStyle: 'compressed' }))
    .pipe(postcss([autoprefixer(), cssnano()]))
    .pipe(config.dest)
}

// Watcher
function watchFiles() {
  gulp.watch('./scss/**/*', css)
  gulp.watch(
    ['../templates/**/*'],
    browserSyncReload
  )
}

const build = gulp.series(css)
const watch = gulp.parallel(watchFiles, browserSync)

exports.build = build
exports.watch = watch
exports.default = build
