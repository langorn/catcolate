/////////////////
// Created by Mark 2015-11-24
// AngularJS
/////////////////

PER_HOURS = 6


var catcolateApp = angular.module('catcolateApp', []);

catcolateApp.config(['$httpProvider',
	function ($httpProvider) {
      //  $httpProvider.interceptors.push(['$q', function ($q) {
      	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
      	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
      // }]);
}]);

catcolateApp.controller('counterController', function($scope, $http, Payment){
  //load the agent's lesson

  $scope.addPayment = function(data){
	  	// Payment.add().success(function(data){
	  	// 	console.log(data);
	  	// })
		console.log('hiha');
		// console.log(data);
		if(typeof data.orders === 'undefined'){
			data.orders = [];
			data.orders.push('0');
		}else if(data.orders ==''){
			data.orders = [];
			data.orders.push('0');
		}else{
			var isString = typeof data.orders
			if(isString=="string"){
				var orderArray = data.orders.split(",")
				data.orders = orderArray;
			}
			data.orders.push('0');
		}

}

$scope.foods = [
	{id:'1', name:'greentea' , unit_price:3.0 },
	{id:'2', name:'black tea' , unit_price:3.0 },
	{id:'3', name:'waffer' , unit_price:6.0 }
]

$scope.tables = [
	{id:'0', name:'Non Specific'}, 
	{id:'99', name:'Event'}, 
	{id:'1', name:'Table 1'},
	{id:'2', name:'Table 2'},
	{id:'3', name:'Table 3'},
	{id:'4', name:'Table 4'},
	{id:'5', name:'Table 5'},
	{id:'6', name:'Table 6'},
	{id:'7', name:'Table 7'},
	{id:'8', name:'Table 8'},
	{id:'9', name:'Table 9'},
	{id:'10', name:'Table 10'},
]



$scope.pay_state = 
[
	{'0':'unpay'},
	{'1':'time hold'},
	{'2':'pay success'},
	{'3':'bill cancel'}
]

$scope.tableNow = 0 ;

$scope.myfood = $scope.foods[1];
$scope.chosenBill = {}; // view the chosen bill 

$scope.payTogether = []; //
$scope.payTogetherState = true;
$scope.payTogetherFlag = false;
$scope.together_bills = [];

$scope.combineBills = {};
$scope.usersBill = [];
$scope.totalAmount = 0;
$scope.card_no = null;
$scope.userPay = 0;
$scope.moneyChanger = 0;

$scope.selectTable = function(tableNo){

	$scope.class = "active";
	// $this.addClass('active');
	$scope.tableNow = tableNo;
	Payment.getTable(tableNo)
	.success(function(data){
		$scope.records = [data][0].records;
	})

}
$scope.findCard = function(card_no){
	Payment.findCard(card_no)
	.success(function(data){
		$scope.records = [data][0].records;
	})

	// var result = null;
	// for(var record in $scope.records){
	// 	if($scope.records[record].card_no){
	// 		if($scope.records[record].card_no==card_no){
	// 			result = $scope.records[record]
	// 		}	
	// 	}
	// }
	// console.log(result);
	// $scope.records[0] = result;
}


$scope.selectTableUsers = function(){
	$scope.payTogetherState = true;
	Payment.getTable($scope.tableNow)
	.success(function(data){

		$scope.payTogether = [];
		$scope.records = [data][0].records;
		for(var record in $scope.records){
			$scope.payTogether.push($scope.records[record].id)

		}
	})
}

$scope.unselectedTableUsers = function(){
	$scope.payTogetherFlag = false;
	$scope.payTogether = [];
}


$scope.addCustomer = function(){
	Payment.add($scope.tableNow)
	.success(function(data){
		getAll($scope.tableNow);
	  		// $scope.records = [data][0].records;
	  	})
}

$scope.calculate = function(totalAmount){
	$scope.moneyChange = $scope.userPay - totalAmount;
}


function getAll(id){
	$scope.selectTable(id);
}

$scope.updateOpt = function(){
	console.log($scope.myfood);
}

$scope.changeTable = function(record){
	var table_id = prompt('Please Enter the table you want to change');
	Payment.move(record.id, table_id)
	.success(function(){
		$scope.selectTable($scope.tableNow);
	})
}

$scope.paynow = function(){
	// alert('aleh');
}

$scope.hold_bill = function(){
	Payment.hold($scope.payTogether)
	.success(function(){
		$scope.showdetail($scope.chosenBill);
	})
}

$scope.clear_all = function(){
	$scope.usersBill = [];
	$scope.payTogether = [];
	$scope.totalAmount = 0;
	$('input[type=checkbox]').attr('checked',false);
}

$scope.billTogether = function(member_id){

	$scope.usersBill = [];

	var isHere = $scope.payTogether.indexOf(member_id);
	if(isHere==-1){
		$scope.payTogether.push(member_id);
	}else{
		$scope.payTogether.splice(isHere,1);
	}
	Payment.together($scope.payTogether)
	.success(function(data){

		
		$scope.payTogetherFlag = true;
		$scope.together_bills = [data][0].records;

		//need to refactor this
		$scope.totalAmount = 0;
		console.log($scope.together_bills);
		for(var record in $scope.together_bills){

			// console.log($scope.together_bills[record].end_time);
			// console.log($scope.together_bills[record].end_time+' - '+$scope.together_bills[record].start_from);
			var timestamp = $scope.time_convert( $scope.together_bills[record].end_time,  $scope.together_bills[record].start_from);
			var time_spent = $scope.time_cost(timestamp);
			var foodName = findFoodName($scope.records[record], $scope.foods);

			console.log(foodName);
			var bill = {
				'id': $scope.together_bills[record].id,
				'time':timestamp.hrs+':'+timestamp.min,
				'time_spent':time_spent.toFixed(2),
				'orderName':foodName
			}
			$scope.totalAmount += time_spent;
			$scope.usersBill.push(bill);
		}
	})
	// alert($scope.payTogether);
}

$scope.bill_by_table = function(){
	$scope.payTogetherFlag = true;
	console.log($scope.records);
	$scope.selectTableUsers();
	$scope.totalAmount = 0;
	$scope.usersBill = [];
	
	for(var record in $scope.records){
		var timestamp = $scope.time_convert( $scope.records[record].end_time,  $scope.records[record].start_from);
		var time_spent = $scope.time_cost(timestamp);
		var foodName = findFoodName($scope.records[record], $scope.foods);


		var bill = {
			'id': $scope.records[record].id,
			'time':timestamp.hrs.toFixed(2), //+':'+timestamp.min,
			'time_spent':time_spent.toFixed(2),
			'orderName':foodName.orderName
		}
		$scope.totalAmount += time_spent;
		$scope.usersBill.push(bill);

	}
}

function findFoodName(record, foods){
  	// find the Order Name
  	var orderList = [];
  	for(var k in record.orders){
  		for(var f in foods){
  			// console.log($scope.chosenBill.orders[k]);
	  		if($scope.foods[f].id == record.orders[k] ){

	  			orderList.push(
	  				{
	  					'id':$scope.foods[f].id,
	  					'name':$scope.foods[f].name,
	  					'unit_price':$scope.foods[f].unit_price
	  				})
	  		}
  		}
  	}
  	record.orderName = orderList;
  	// console.log(record.orderName);
  	return record
}



$scope.pay_bill = function(){
	Payment.pay($scope.payTogether)
	.success(function(){
		// $scope.showdetail($scope.chosenBill);
		$scope.selectTable($scope.tableNow);
	})
}

$scope.pay_table = function(){
	var table_no = $scope.tableNow
	Payment.pay_table(table_no)
	.success(function(){
		// $scope.showdetail($scope.chosenBill);
		$scope.selectTable($scope.tableNow);
	})


}

$scope.cancel_bill = function(){
	Payment.cancel($scope.chosenBill.id)
	.success(function(){
		// $scope.showdetail($scope.chosenBill);
		$scope.selectTable($scope.tableNow);
	})
}

$scope.time_convert = function(end, start){
	if(end == 0){
		end = new Date();
	}
	var total_time_stamp = end-start// new Date ((end - start));
	// console.log(total_time_stamp);
	total_time_stamp = ((total_time_stamp) / 3600)/1000;
	// alert(total_time_stamp)
	// var spentTime = {
	// 	'hrs':total_time_stamp.getUTCHours(),
	// 	'min':total_time_stamp.getUTCMinutes()
	// }
	console.log(total_time_stamp);
	var spentTime = {	
		'hrs':total_time_stamp,
		'min':total_time_stamp

	}

	return spentTime
}

function timeConverter(UNIX_timestamp){
 var a = new Date(UNIX_timestamp*1000);
     var hour = a.getUTCHours();
     var min = a.getUTCMinutes();
     var sec = a.getUTCSeconds();
     var time = hour+':'+min+':'+sec ;
     return time;
 }


$scope.time_cost = function(spentTime){
	var cost = spentTime.hrs * PER_HOURS;
	// cost += ((spentTime.min/60) * PER_HOURS);
	console.log(cost+'='+spentTime.hrs+'*'+PER_HOURS);
	return cost;
}

$scope.reload = function(){

}

$scope.showdetail = function(record){

	$scope.payTogetherFlag = false;

	$scope.chosenBill = record;
	// var total_time = Math.floor(Date.now() / 1000) - record.start_from
	var total_time = (new Date().getTime()) - record.start_from

	// var total_time_stamp = end-start// new Date ((end - start));
	// console.log(total_time_stamp);
	total_time_stamp = ((total_time) / 3600)/1000;
	// alert(total_time_stamp)
	// var spentTime = {
	// 	'hrs':total_time_stamp.getUTCHours(),
	// 	'min':total_time_stamp.getUTCMinutes()
	// }
	// var spentTime = {	
	// 	'hrs':total_time_stamp,
	// 	'min':total_time_stamp

	// }


	// var total_time_stamp = new Date(total_time * 1000);
	var hrs = total_time_stamp;
	var min = total_time_stamp;

	$scope.chosenBill.spent = hrs+':'+min;
	  	// calculate the total amount
	  	var totalFood = 0;
	  	$scope.chosenBill.total_amount = (hrs*PER_HOURS) //+ (min/60*PER_HOURS);
	  	for(var i in $scope.chosenBill.orders){
	  		for(var f in $scope.foods){
	  			// console.log($scope.chosenBill.orders[k]);
		  		if($scope.foods[f].id == $scope.chosenBill.orders[i] ){
		  			totalFood += $scope.foods[f].unit_price;
		  		}
	  		}
	  	}
	  	$scope.chosenBill.foodAmount = totalFood;
	  	$scope.chosenBill.total_amount = $scope.chosenBill.total_amount.toFixed(2);

	  	// find the Order Name
	  	var orderList = [];
	  	for(var k in $scope.chosenBill.orders){
	  		for(var f in $scope.foods){
	  			// console.log($scope.chosenBill.orders[k]);
		  		if($scope.foods[f].id == $scope.chosenBill.orders[k] ){

		  			orderList.push(
		  				{
		  					'id':$scope.foods[f].id,
		  					'name':$scope.foods[f].name,
		  					'unit_price':$scope.foods[f].unit_price
		  				})
		  		}
	  		}
	  	}
	  	$scope.chosenBill.orderName = orderList
	  	$scope.chosenBill.pay_status = record.pay_status;
	  }


	  $scope.records = [];
	  Payment.all()
	  .success(function(data){
	  	$scope.records = [data][0].records;
	  	console.log(typeof [data][0].records.orders);
	  });
		// $scope.records = Payment.all();
		// console.log($scope.records);
	})
// });