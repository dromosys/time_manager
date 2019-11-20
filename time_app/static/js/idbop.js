var dbPromise = idb.open('time-db', 5, function(upgradeDb) {
	upgradeDb.createObjectStore('time',{keyPath:'pk'});
});


	//collect latest post from server and store in idb localhost:8000
	fetch('https://www.dromosys.com/time/getdata/').then(function(response){
		return response.json();
	}).then(function(jsondata){
		dbPromise.then(function(db){
			var tx = db.transaction('time', 'readwrite');
	  		var timeStore = tx.objectStore('time');
	  		
	  		for(var key in jsondata){
	  			if (jsondata.hasOwnProperty(key)) {
			    	timeStore.put(jsondata[key]);	
			  	}
	  		}
		});
	});

	//retrive data from idb and display on page
	var post="";
	dbPromise.then(function(db){
		var tx = db.transaction('time', 'readonly');
  		var timeStore = tx.objectStore('time');
  		return timeStore.openCursor();
	}).then(function logItems(cursor) {
		  if (!cursor) {
		  	document.getElementById('offlinedata').innerHTML=post;
		    return;
		  }
		  for (var field in cursor.value) {
		    	if(field=='fields'){
		    		timeData=cursor.value[field];
		    		for(var key in timeData){
		    			if(key =='name'){
		    				var title = ''+timeData[key]+'';
		    			}
		    			if(key =='date'){
		    				var author = timeData[key];
		    			}
		    			if(key == 'start_time'){
		    				var body = ''+timeData[key]+'';
		    			}	
		    		}
		    		post=post+'<br>'+title+' '+author+' '+body;
		    	}
		    }
		  return cursor.continue().then(logItems);
		});
