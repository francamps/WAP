
d3.json('formatted_familia.json', function (data) {

	var w = 900,
		h = 1200,
		hFactor = 1,
		maxChar = 2400,
		rW = 4;

	var svg = d3.select('#graph').append('svg')
		.attr('width', w)
		.attr('height', h);

	var blanca = [],
		franc = [],
		ma = [],
		pa = [];

	// Separate data objects for sonia and Franc
	data.forEach(function (d) {
		var day = Object.keys(d)[0]
			dayObj = d[day];

		francDay = {};
		francDay[day] = [];
		blancaDay = {};
		blancaDay[day] = [];
		maDay = {};
		maDay[day] = [];
		paDay = {};
		paDay[day] = [];


		for (var msg in dayObj) {
			var author = dayObj[msg].author; 
			if (author === "Franc Camps") {
				francDay[day].push(dayObj[msg]);
			} else if (author === "Blanca" ) {
				blancaDay[day].push(dayObj[msg]);
			} else if (author === "Anna Febrer Rotger" ) {
				maDay[day].push(dayObj[msg]);
			} else if (author === "Pau" ) {
				paDay[day].push(dayObj[msg]);
			}
		}
		blanca.push(blancaDay);
		franc.push(francDay);
		ma.push(maDay);
		pa.push(paDay)
	});

	var pink = 'rgb(243, 38, 114)';
		purple = 'rgb(71, 3, 166)';

	var format = d3.time.format("%Y-%m-%d");

	var timeScale = d3.time.scale()
						.domain([format.parse('2014-10-01'), format.parse('2015-10-18')])
					  	.range([0, h]);

	var charScale = d3.scale.linear()
						.domain([0, maxChar])
						.range([0, 600]);

	function getCharacters(d) {
		var numChar = 0,
			msgs = d[Object.keys(d)[0]];
		for (msg in msgs) {
			numChar += msgs[msg].text.length;
		}
		return numChar;
	}

	var lineFunction = d3.svg.line()
		.y(function(d) { return timeScale(format.parse(Object.keys(d)[0])); })
		.x(function(d) { return charScale(getCharacters(d)); })
		.interpolate("basis");

	var lineFunction2 = d3.svg.line()
		.y(function(d) { return timeScale(format.parse(Object.keys(d)[0])); })
		.x(function(d) { return charScale(getCharacters(d)) + 200; })
		.interpolate("basis");

	var lineFunction3 = d3.svg.line()
		.y(function(d) { return timeScale(format.parse(Object.keys(d)[0])); })
		.x(function(d) { return charScale(getCharacters(d)) + 400; })
		.interpolate("basis");

	var lineFunction4 = d3.svg.line()
		.y(function(d) { return timeScale(format.parse(Object.keys(d)[0])); })
		.x(function(d) { return charScale(getCharacters(d)) + 600; })
		.interpolate("basis");

	var francLine = svg.append("path")
		.attr("d", lineFunction(franc))
		.attr("stroke", pink)
		.attr("stroke-width", 0)
		.style('opacity', 1)
		.attr("fill", pink);

	var blancaLine = svg.append("path")
		.attr("d", lineFunction2(blanca))
		.attr("stroke", pink)
		.attr("stroke-width", 0)
		.style('opacity', 1)
		.attr("fill", pink);

	var maLine = svg.append("path")
		.attr("d", lineFunction3(ma))
		.attr("stroke", pink)
		.attr("stroke-width", 0)
		.style('opacity', 1)
		.attr("fill", pink);

	var paLine = svg.append("path")
		.attr("d", lineFunction4(pa))
		.attr("stroke", pink)
		.attr("stroke-width", 0)
		.style('opacity', 1)
		.attr("fill", pink);

/*var area = d3.svg.area()
	    .x(function(d) { return timeScale(format.parse(Object.keys(d)[0])); })
	    .y0(h/2)
	    .y1(function(d) { return charScale(getCharacters(d)); })
	    .interpolate('basis');

	var areaLow = d3.svg.area()
	    .x(function(d) { return timeScale(format.parse(Object.keys(d)[0])); })
	    .y0(h/2)
	    .y1(function(d) { return charScale(-getCharacters(d)); })
	    .interpolate('basis');

  	svg.append("path")
	    	.datum(data)
      		.attr("class", "area")
      		.attr("d", area)
      		.style('fill', 'rgb(243, 38, 114)');

  	svg.append("path")
	    	.datum(data)
      		.attr("class", "area")
      		.attr("d", areaLow)
      		.style('fill', 'rgb(243, 38, 114)');
    */

	

});