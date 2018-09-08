'use strict';

import gulp from 'gulp';
import sourcemaps from 'gulp-sourcemaps';
import clean from 'gulp-clean';
import flatten from 'gulp-flatten';
import ext_replace from 'gulp-ext-replace';

import postcss from 'gulp-postcss';
import sass from 'gulp-sass';
import autoprefixer from 'autoprefixer';
import cssnano from 'cssnano';

import browserify from 'browserify';
import babelify from 'babelify';
import source from 'vinyl-source-stream';
import buffer from 'vinyl-buffer';
import uglify from 'gulp-uglify';
import eslint from 'gulp-eslint';

import image_resize from 'gulp-image-resize';

let browsersync = require('browser-sync').create();

const dirs = {
	src: 'src/',
	dest: 'static/dist/',
	images: 'static/images/',
	fonts: 'static/fonts/',
	fontawesome: 'node_modules/@fortawesome/fontawesome-pro/'
};

gulp.task('css', () => {

	let processors = [
		autoprefixer(),
		cssnano({"preset": ["default", {"discardComments": {"removeAll": true}}]})
	];

	return gulp.src(dirs.src + 'scss/style.scss')
		.pipe(ext_replace('.css'))
		.pipe(sourcemaps.init())
		.pipe(sass())
		.pipe(postcss(processors))
		.pipe(sourcemaps.write('.'))
		.pipe(gulp.dest(dirs.dest))
		.pipe(browsersync.stream({match: '*.css'}))
});

gulp.task('test-js', () => {

	const options = {
		parserOptions: {
			ecmaVersion: 6,
			sourceType: 'module'
		},
		extends: 'eslint:recommended',
		rules: {
			'quotes': ['error', 'single'],
			'linebreak-style': ['error', 'unix'],
			'eqeqeq': ['warn', 'always'],
			'indent': ['error', 'tab']
		}
	};

	return gulp.src(dirs.src + 'js/**/*.js')
		.pipe(eslint(options))
		.pipe(eslint.format())
		.pipe(eslint.failAfterError())
});

gulp.task('js', gulp.series('test-js', () => {

	const b = browserify({
		debug: true,
		entries: dirs.src + 'js/app.js'
	});

	b.transform('babelify', {
		presets: ['@babel/preset-env'], sourceMaps: true
	});

	return b.bundle()
		.pipe(source(dirs.src + 'js/app.js'))
		.pipe(buffer())
		.pipe(sourcemaps.init())
		.pipe(uglify())
		.pipe(sourcemaps.write('.'))
		.pipe(flatten())
		.pipe(gulp.dest(dirs.dest))
		.pipe(browsersync.stream({match: '*.js'}))
}));

gulp.task('vendor', () => {
	return gulp.src('node_modules/bootstrap/dist/css/bootstrap.min.css*')
		.pipe(gulp.dest(dirs.dest))
});

gulp.task('fonts', () => {
	return gulp.src(dirs.fontawesome + 'webfonts/fa-regular-*')
		.pipe(gulp.dest(dirs.fonts))
});

gulp.task('clean', () => {
	return gulp.src(dirs.dest, {read: false, allowEmpty: true})
		.pipe(clean());
});

gulp.task('images', () => {
	return gulp.src(dirs.images + 'full/*')
		.pipe(image_resize({
			width : 250,
			height : 250,
			crop : false,
			upscale : false
		}))
		.pipe(gulp.dest(dirs.images + 'med'));

});

gulp.task('default', gulp.series('clean', gulp.parallel('vendor', 'css', 'js')));

gulp.task('watch', gulp.series('default', (done) => {
	gulp.watch(dirs.src + 'scss/**/*.scss', gulp.series('css'));
	gulp.watch(dirs.src + 'js/**/*.js', gulp.series('js'));
	done();
}));

gulp.task('browsersync', gulp.parallel('watch', (done) => {

	browsersync.init({
		proxy: 'http://127.0.0.1:5000/',
	});

	gulp.watch('templates/**/*.html').on('change', browsersync.reload);
	done();
}));