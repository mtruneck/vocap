;(function() {

var isTest = window.location.href.match(/test/);

require.config({
	deps: [ isTest ? 'tests' : 'main' ],

    paths: {
      text: '../lib/text',
      jquery: '../lib/jquery',
      jqueryui: '../lib/jquery-ui',
      underscore: '../lib/underscore',
	  rsvp: '../lib/rsvp',
	  colorbox: '../lib/colorbox',
      templates: '../templates',
      results_template: '../templates/results.html',

      tests: '../../../openshift/tests/tests',
      sinon: '../../../openshift/tests/sinon',
      squire: '../../../openshift/tests/squire',
      test_data: '../../../openshift/tests/data',
    },

    shim: {
      colorbox: {
          deps: [ "jquery" ],
	  },
      jqueryui: {
          deps: [ "jquery" ],
	  },
      underscore: {
        exports: '_'
      },
    },
	//urlArgs: "bust=" +  (new Date()).getTime(),
  });
}());
