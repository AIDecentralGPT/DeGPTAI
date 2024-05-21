import _classCallCheck from "@babel/runtime/helpers/classCallCheck";import _createClass from "@babel/runtime/helpers/createClass";import _inherits from "@babel/runtime/helpers/inherits";import _possibleConstructorReturn from "@babel/runtime/helpers/possibleConstructorReturn";import _getPrototypeOf from "@babel/runtime/helpers/getPrototypeOf";function _createSuper(Derived) {var hasNativeReflectConstruct = _isNativeReflectConstruct();return function _createSuperInternal() {var Super = _getPrototypeOf(Derived),result;if (hasNativeReflectConstruct) {var NewTarget = _getPrototypeOf(this).constructor;result = Reflect.construct(Super, arguments, NewTarget);} else {result = Super.apply(this, arguments);}return _possibleConstructorReturn(this, result);};}function _isNativeReflectConstruct() {if (typeof Reflect === "undefined" || !Reflect.construct) return false;if (Reflect.construct.sham) return false;if (typeof Proxy === "function") return true;try {Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {}));return true;} catch (e) {return false;}}import colors from 'colors';
import fse from 'fs-extra';
import Plugin from 'broccoli-plugin';
import rsvp from 'rsvp';
import sort from 'gulp-sort';
import vfs from 'vinyl-fs';

import i18nTransform from './transform.js';

var Promise = rsvp.Promise;var

i18nextParser = /*#__PURE__*/function (_Plugin) {_inherits(i18nextParser, _Plugin);var _super = _createSuper(i18nextParser);
  function i18nextParser(inputNodes) {var _this;var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};_classCallCheck(this, i18nextParser);
    _this = _super.apply(this, arguments);
    _this.options = options;return _this;
  }_createClass(i18nextParser, [{ key: "build", value:

    function build() {var _this2 = this;
      var outputPath = this.outputPath;
      return new Promise(function (resolve, reject) {
        var files = [];
        var count = 0;

        vfs.
        src(_this2.inputPaths.map(function (x) {return x + '/**/*.{js,hbs}';})).
        pipe(sort()).
        pipe(
          new i18nTransform(_this2.options).
          on('reading', function (file) {
            if (!this.options.silent) {
              console.log('  [read]  '.green + file.path);
            }
            count++;
          }).
          on('data', function (file) {
            files.push(fse.outputFile(file.path, file.contents));
            if (!this.options.silent) {
              console.log('  [write] '.green + file.path);
            }
          }).
          on('error', function (message, region) {
            if (typeof region === 'string') {
              message += ': ' + region.trim();
            }
            console.log('  [error] '.red + message);
          }).
          on('finish', function () {
            if (!this.options.silent) {
              console.log();
              console.log(
                '  Stats:  '.yellow + String(count) + ' files were parsed'
              );
            }

            Promise.all(files).then(function () {
              resolve(files);
            });
          })
        );
      });
    } }]);return i18nextParser;}(Plugin);export { i18nextParser as default };
//# sourceMappingURL=broccoli.js.map