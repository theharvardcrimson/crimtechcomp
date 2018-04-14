// Namespace
var Crimson = Crimson || {};
Crimson.Table = {};

// Updates the head of the table
Crimson.Table.update_head = function(table, table_data) {
	var head = table_data.head;
	var head_html = "";

	// Build header row once cell at a time
	for (c in head) {
		var cell = head[c];
		head_html += "<th>" + cell + "</th>";
	}

	// Add markup for row and insert into the head
	head_html = "<tr>" + head_html + "</tr>";
	$('thead', table).html(head_html);
};

// Return new table object with rows containing "query" in the specified column
Crimson.Table.filter_rows = function(table_data, query, column) {

	// Make sure comparison is case-insensitive
	query = query.toLowerCase();

	// To be returned. Should not modify "table_data" since it's passed by
	//   reference
	var filtered_data = {"head": table_data.head, "body": []};
	var body = table_data.body;

	// Build up result one row at a time
	for (row in body) {
		var to_search = body[row][column].toLowerCase();

		// If query found, add to the result
		if (to_search.search(query) != -1) {
			filtered_data.body.push(body[row]);
		}
	}

	return filtered_data
};

// Updates the body of the table
Crimson.Table.update_body = function(table, table_data, query) {
	// HTML to replace the current table. Start with title row.
	var table_html = "";

	var num_cols = table_data.head.length;
	var body = table_data.body;

	// Message if no match. Use 'colspan' to span entire width of the table.
	if (body.length == 0){
		table_html = "\
			<tr>\
				<td colspan='" + num_cols + "'>\
					<i>No results for &ldquo;" + query + "&rdquo;</i>\
				</td>\
			</tr>";
	}

	// Build up the table
	for (r in body) {

		var row = body[r];
		var row_html = "";

		// Build HTML for the row one cell at a time
		for (var cell = 0; cell < num_cols; cell++){
			row_html += "<td>" + row[cell] + "</td>";
		}

		// Build and add row
		table_html += "<tr>" + row_html + "</tr>";
	}

	// Replace current table
	$('tbody', table).html(table_html);
};
