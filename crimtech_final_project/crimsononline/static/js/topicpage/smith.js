$(document).ready(function() {

	$("#pinned").pin({containerSelector: "#title-wrapper", minWidth: "600px"});

	nv.addGraph(function() {
		var chart = nv.models.lineChart().showLegend(false);

		chart.xAxis
		.axisLabel('Fiscal Year')
		.tickFormat(d3.format('r'))
       .tickValues([2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]);

		chart.yAxis
		.axisLabel('Market Value ($B)')
		.tickFormat(d3.format('.02f'));

		chart.tooltipContent(function(key, y, e, graph) {
			return '<h2>' + y + '</h2><p>$' + e + ' billion</p>'
		});

		var values = [{x: 2001, y: 7.8}, {x: 2002, y: 8.1}, {x: 2003, y: 8.9},
		{x: 2004, y: 10.3}, {x: 2005, y: 11.9}, {x: 2006, y: 13.4},
		{x: 2007, y: 16.0}, {x: 2008, y: 16.7}, {x: 2009, y: 11.7}];

		d3.select('#endowment svg')
		.datum([{
			values: values,
			key: '',
			color: '#ba0600'
		}])
		.transition().duration(500)
		.call(chart);

	   // added this janky line
	   d3.select('#endowment .nv-y .nv-axis .nv-axislabel').attr('y', '-50');
	   nv.utils.windowResize(function() {
	       d3.select('#endowment svg').call(chart);
	       // added this janky line
	       d3.select('#endowment .nv-y .nv-axis .nv-axislabel').attr('y', '-50');
	   });

		return chart;
	});


	nv.addGraph(function() {
		var chart = nv.models.lineChart().showLegend(false)

		chart.xAxis
		.axisLabel('Fiscal Year')
		.tickFormat(d3.format('r'));

		chart.yAxis
		.axisLabel('Ladder Faculty Members')
		.tickFormat(d3.format('r'));

		chart.tooltipContent(function(key, y, e, graph) {
			return '<h2>' + y + '</h2><p>' + e + ' faculty members</p>'
		});

		var values = [{x: 1988, y: 599}, {x: 1989, y: 601}, {x: 1990, y: 602},
					  {x: 1991, y: 599}, {x: 1992, y: 613}, {x: 1993, y: 596},
					  {x: 1994, y: 607}, {x: 1995, y: 591}, {x: 1996, y: 597},
					  {x: 1997, y: 597}, {x: 1998, y: 596}, {x: 1999, y: 587},
					  {x: 2000, y: 586}, {x: 2001, y: 598}, {x: 2002, y: 619},
					  {x: 2003, y: 623}, {x: 2004, y: 637}, {x: 2005, y: 653},
					  {x: 2006, y: 675}, {x: 2007, y: 701}, {x: 2008, y: 712},
					  {x: 2009, y: 719}, {x: 2010, y: 720}, {x: 2011, y: 721},
					  {x: 2012, y: 722}, {x: 2013, y: 712}, {x: 2014, y: 710}]

		d3.select('#faculty svg')
		.datum([{
			values: values,
			key: '',
			color: '#ba0600'
		}])
		.transition().duration(500)
		.call(chart);

	   // added this janky line
	   d3.select('#faculty .nv-y .nv-axis .nv-axislabel').attr('y', '-50');
	   nv.utils.windowResize(function() {
	       d3.select('#faculty svg').call(chart);
	       // added this janky line
	       d3.select('#faculty .nv-y .nv-axis .nv-axislabel').attr('y', '-50');
	   });

		return chart;
	});

});
