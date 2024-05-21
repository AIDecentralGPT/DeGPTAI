(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.i18nextResourcesToBackend = factory());
})(this, (function () { 'use strict';

  var resourcesToBackend = function resourcesToBackend(res) {
    return {
      type: 'backend',
      init: function init(services, backendOptions, i18nextOptions) {},
      read: function read(language, namespace, callback) {
        if (typeof res === 'function') {
          if (res.length < 3) {
            try {
              var r = res(language, namespace);
              if (r && typeof r.then === 'function') {
                r.then(function (data) {
                  return callback(null, data && data.default || data);
                }).catch(callback);
              } else {
                callback(null, r);
              }
            } catch (err) {
              callback(err);
            }
            return;
          }
          res(language, namespace, callback);
          return;
        }
        callback(null, res && res[language] && res[language][namespace]);
      }
    };
  };

  return resourcesToBackend;

}));
