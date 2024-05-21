import _classCallCheck from "@babel/runtime/helpers/classCallCheck";import _createClass from "@babel/runtime/helpers/createClass";import _inherits from "@babel/runtime/helpers/inherits";import _possibleConstructorReturn from "@babel/runtime/helpers/possibleConstructorReturn";import _getPrototypeOf from "@babel/runtime/helpers/getPrototypeOf";function _createSuper(Derived) {var hasNativeReflectConstruct = _isNativeReflectConstruct();return function _createSuperInternal() {var Super = _getPrototypeOf(Derived),result;if (hasNativeReflectConstruct) {var NewTarget = _getPrototypeOf(this).constructor;result = Reflect.construct(Super, arguments, NewTarget);} else {result = Super.apply(this, arguments);}return _possibleConstructorReturn(this, result);};}function _isNativeReflectConstruct() {if (typeof Reflect === "undefined" || !Reflect.construct) return false;if (Reflect.construct.sham) return false;if (typeof Proxy === "function") return true;try {Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {}));return true;} catch (e) {return false;}}import EventEmitter from 'events';var

BaseLexer = /*#__PURE__*/function (_EventEmitter) {_inherits(BaseLexer, _EventEmitter);var _super = _createSuper(BaseLexer);
  function BaseLexer() {var _this;var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};_classCallCheck(this, BaseLexer);
    _this = _super.call(this);
    _this.keys = [];
    _this.functions = options.functions || ['t'];return _this;
  }_createClass(BaseLexer, [{ key: "validateString", value:

    function validateString(string) {
      var regex = new RegExp('^' + BaseLexer.stringPattern + '$', 'i');
      return regex.test(string);
    } }, { key: "functionPattern", value:

    function functionPattern() {
      return '(?:' + this.functions.join('|').replace('.', '\\.') + ')';
    } }], [{ key: "singleQuotePattern", get:

    function get() {
      return "'(?:[^'].*?[^\\\\])?'";
    } }, { key: "doubleQuotePattern", get:

    function get() {
      return '"(?:[^"].*?[^\\\\])?"';
    } }, { key: "backQuotePattern", get:

    function get() {
      return '`(?:[^`].*?[^\\\\])?`';
    } }, { key: "variablePattern", get:

    function get() {
      return '(?:[A-Z0-9_.-]+)';
    } }, { key: "stringPattern", get:

    function get() {
      return (
        '(?:' +
        [BaseLexer.singleQuotePattern, BaseLexer.doubleQuotePattern].join('|') +
        ')');

    } }, { key: "stringOrVariablePattern", get:

    function get() {
      return (
        '(?:' +
        [
        BaseLexer.singleQuotePattern,
        BaseLexer.doubleQuotePattern,
        BaseLexer.variablePattern].
        join('|') +
        ')');

    } }]);return BaseLexer;}(EventEmitter);export { BaseLexer as default };
//# sourceMappingURL=base-lexer.js.map