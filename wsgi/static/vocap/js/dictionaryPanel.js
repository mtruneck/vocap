define([
	'jquery',
	'underscore',
	'colorbox',
], function($, _){

	var dictionaryPanel = function( elem ){
		this.el = $( elem );
		return this;
	};

	dictionaryPanel.prototype.setQuery = function( query ) {

		dictionaries = [];
		dictionaries.push({name: "Cambridge dict.",
			template: 'http://dictionary.cambridge.org/search/learner-english/direct/?q=<%- query %>'});
		dictionaries.push({name: "Seznam slovník",
			template: 'http://slovnik.seznam.cz/en-cz/word/?q=<%- query %>'});
		dictionaries.push({name: "Longman dict.",
			template: 'http://www.ldoceonline.com/search/?q=<%- query %>'});

		var elem = this.el;
		elem.html("");
		elem.append(_.template('Search <b>"<%- query %>"</b> in dictionaries:', {query: query}));
		_.each(dictionaries, function( dict ){
			url = _.template(dict.template, {query: query});
			console.log();
			elem.append(' &nbsp; ');
			link = $('<a href="'+url+'" class="iframe">'+dict.name+'</a>');
			elem.append(link);
		});

        // Enable showing the links in the floating iframe
        this.el.find(".iframe").colorbox({iframe:true, width:"900px", height:"80%"});

	};

	return dictionaryPanel;

});
