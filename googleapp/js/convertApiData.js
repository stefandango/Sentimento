function getRows(data, dateFormat){
var i = 0;
var res = [];
var fillIn = null;
var xAxisName = "Tid";

// Match values and make rows
$.each(data, function(k,obj){
	if(_.isEmpty(res)){
		res = _.pairs(obj);
	}else{
		$.each(obj, function(j, val){
			var matchingRow = _.find(res, function(row){
				return row[0] == j // first in row is the date string
			});
			if(_.isUndefined(matchingRow)){
				var newRow = [j];
				for(var l = 0; l < i; l++){
					newRow.push(fillIn);
				}
				newRow.push(val);
				res.push(newRow);	
			}else{
				matchingRow.push(val);	
			}
		})
	}
	i++;
});

// Make sure all rows are of the same length
var lengthOfRows = i + 1;
$.each(res, function(i, v){
	var numOfFillInsToAdd = lengthOfRows - v.length;
	for(var j = 0; j < numOfFillInsToAdd; j++){
		v.push(fillIn);
	}
})

if(dateFormat){
	// Convert date string to date object to get a continues axis on Google Chart Tool
	$.each(res, function(i, v){
		var dateObj = moment(v[0], dateFormat).toDate();
		v[0] = dateObj;
		});

		// Sort by date
		res = _.sortBy(res, function(v){ return v[0] })
	}

	// Add colum names
var columnNames = _.keys(data);
columnNames.unshift(xAxisName);
res.unshift(columnNames);

console.log(res);

return res;
}