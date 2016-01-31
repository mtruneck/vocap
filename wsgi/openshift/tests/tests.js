define([
	'jquery',
	'searchForm',
	'searchResults',
	'sinon',
	'test_data',
], function($, SearchForm, SearchResults){

	module('searchForm', {
		setup: function(){
			formElement = $('<form><input name="search_query" id="search_query"><span id="submit_search">Search</span></form>');
			//formElement = $('<form><input name="q"><input type="submit"></form>');
		},
		teardown: function(){}
	});

	test('constructor', function(){
		var sf = new SearchForm( formElement );
		ok(sf instanceof SearchForm);
	});

    test( 'search event is triggered with query', function() {
      var sf = new SearchForm( formElement );
      var spy = sinon.spy();

      sf.el.on( 'search', spy );

      formElement.find( 'input[name="search_query"]' ).val( 'squeamish' );
      formElement.trigger( 'submit' );

      stop();
      setTimeout(function(){
	    start();
        ok( spy.called, "The submit event was triggered." );
        QUnit.equal( spy.args[0][1], 'squeamish', "And the correct value was sent with the event." );
	  }, 1000);
    });


    test( 'search form is submitted using the span button', function() {
      var sf = new SearchForm( formElement );
      var spy = sinon.spy();

      sf.el.on( 'search', spy );

      formElement.find( 'input[name="search_query"]' ).val( 'squeamish' );
      formElement.find('#submit_search').click();

      stop();
      setTimeout(function(){
	    start();
        ok( spy.called, "The submit event was triggered." );
        QUnit.equal( spy.args[0][1], 'squeamish', "And the correct value was sent with the event." );
	  }, 1000);
    });

    test( 'no search event with empty query', function() {
      var sf = new SearchForm( formElement );
      var spy = sinon.spy();

      $(sf).on( 'search', spy );

      formElement.find( 'input[name="search_query"]' ).val( '   ' );
      formElement.trigger( 'submit' );

      stop();
      setTimeout(function(){
	    start();
        ok( !spy.called );
	  }, 1000);
    });

    module('searchResults', {
		setup: function(){
			resultElement = $('<div id="result">');
		},
		teardown: function(){}
	});

	test('constructor', function() {
		var sr = new SearchResults( resultElement );
		ok(sr instanceof SearchResults);
	});

	test('Filling Results with data', function() {
		var data = searchResults_test_data;
		var sr = new SearchResults( resultElement );
		sr.setResults(data);
		QUnit.equal( sr.el.find('.no-results-found').length, 0, 'There should no message about empty results' );
		QUnit.equal( sr.el.find('.play').length, 50, 'There are exactly 50 play buttons' );
		QUnit.equal( sr.el.find('h3').length, 6, 'There are exactly 6 titles' );
	});

	test('Filling Results with empty data', function() {
		var data = { results: [] };
		var sr = new SearchResults( resultElement );
		sr.setResults(data);
		QUnit.equal( sr.el.find('.no-results-found').length, 1, 'There should a message about empty results' );
		QUnit.equal( sr.el.find('.play').length, 0, 'There should be no play buttons' );
		QUnit.equal( sr.el.find('h3').length, 0, 'There should be no titles' );
	});


	test('Clicking on Play button triggers a "play" event', function() {
		var data = {results: [ { matches: [{
							time: '345',
							human_time: '0:04:44',
							text: 'Testing text',
							}],
						title: "test",
						vid: "testtesttest",
					}]};
		var sr = new SearchResults( resultElement );
		sr.setResults(data);

		QUnit.equal( sr.el.find('.no-results-found').length, 0, 'There should no message about empty results' );
		QUnit.equal( sr.el.find('.play').length, 1, 'There is exactly 1 play button' );
		QUnit.equal( sr.el.find('h3').length, 1, 'There is exactly 1 title' );

		spy = sinon.spy();
		sr.el.on('play', spy);

		sr.el.find('.play').click();
		ok(spy.called);
		QUnit.equal(spy.args[0][1].time, '345');
		QUnit.equal(spy.args[0][1].vid, 'testtesttest');

	});

	test('Loading... state', function() {
		var sr = new SearchResults( resultElement );
		sr.pending();
		QUnit.equal( sr.el.find('.loading').length, 1, 'There is exactly 1 message about loading....' );
	});

}) ;

