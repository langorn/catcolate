/////////////////
// Created by Mark 2015-11-24
// AngularJS
/////////////////

PER_HOURS = 6
var member = {
	'price':5,
	'promotion':2
}

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

// $scope.foods = [
// 	{id:'1', name:'greentea' , unit_price:3.0 },
// 	{id:'2', name:'black tea' , unit_price:3.0 },
// 	{id:'3', name:'waffer' , unit_price:6.0 }
// ]
Payment.foods()
.success(function(data){
	$scope.foods = [data][0].records;
	// $scope.myfood = $scope.foods[1];
})


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



// chosenBill state
/*
chosenBill = {
	'id': -,
	'spent':-,
	'total_amount':'',
	'foodAmount':'',
	'foodAndTime':'',
	'total_amount':'',
	'orders':[],
	'orderName':[],
	'pay_status':'',
	'end_time':'',
	'start_from':'',
	'is_hold':false,
}
*/

$scope.pay_state = 
[
	{'0':'unpay'},
	{'1':'time hold'},
	{'2':'pay success'},
	{'3':'bill cancel'}
]

$scope.tableNow = 0 ;

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

	$scope.tableNow = tableNo;
	Payment.getTable(tableNo)
	.success(function(data){
		// $scope.records = [data][0].records;
		$scope.records = convertArray([data][0].records);
		console.log($scope.records);
	})

}

function convertArray(records){

	//var result = [];
	// records[record].orders = [records[record].orders]

	for(var record in records){

		if(records[record].orders!=""){
			var orders = records[record].orders.split(',')

			for(var order in orders){
				order.order = order.toString()
			}
			records[record].orders = orders;
		}


		// else{
		// 	records[record].orders = []
		// }
	}
	return records
}

$scope.findCard = function(card_no){
	Payment.findCard(card_no)
	.success(function(data){
		// $scope.records = [data][0].records;
		$scope.records = convertArray([data][0].records);
	})
}


$scope.selectTableUsers = function(){
	$scope.payTogetherState = true;
	Payment.getTable($scope.tableNow)
	.success(function(data){

		$scope.payTogether = [];
		// $scope.records = [data][0].records;
		$scope.records = convertArray([data][0].records);
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

	console.log($scope.payTogether);
	Payment.hold($scope.payTogether)
	// Payment.hold($scope.usersBill)
	.success(function(){
		// $scope.showdetail($scope.chosenBill);
		$scope.payTogether = [];

		$scope.selectTable($scope.tableNow);
	})
}

$scope.hold_bills = function(){
	Payment.hold_table($scope.tableNow)
	.success(function(){
		// $scope.showdetail($scope.chosenBill);
		$scope.payTogether = [];
		$scope.selectTable($scope.tableNow);
	})
}

$scope.clear_all = function(){
	$scope.usersBill = [];
	$scope.payTogether = []; // pay with table
	$scope.totalAmount = 0;
	$('input[type=checkbox]').attr('checked',false);
}

//this is for after click the option 
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
		$scope.foodTotal = 0;
		console.log($scope.together_bills);
		for(var record in $scope.together_bills){
			var foodPrice = 0; //each player's food total;
			var subTotal = 0; // subtotal of food & time;
			var timestamp = $scope.time_convert( $scope.together_bills[record].end_time,  $scope.together_bills[record].start_from);
			
			// if member , then pay member price
			var time_spent = $scope.time_cost(timestamp, record.member_price);
			var foodName = findFoodName($scope.together_bills[record], $scope.foods);
			console.log(foodName);

			for(var f in foodName.orderName){
				if(foodName.orderName[f].unit_price!="undefined"){
					$scope.foodTotal += parseFloat(foodName.orderName[f].unit_price);
					foodPrice += parseFloat(foodName.orderName[f].unit_price);
				}
			}

			var bill = {
				'id': $scope.together_bills[record].id,
				'time':timestamp.hrs.toFixed(2), //+':'+timestamp.min,
				'time_spent':time_spent.toFixed(2),
				'orderName':foodName.orderName,
				'foodTotal':foodPrice,
				'subTotal':(parseFloat(time_spent) + parseFloat(foodPrice)).toFixed(2)
			}

			$scope.totalAmount += time_spent;
			$scope.usersBill.push(bill);
			console.log($scope.usersBill);
		}
	})
	// alert($scope.payTogether);
}

$scope.bill_by_table = function(){
	$scope.payTogetherFlag = true;
	console.log($scope.records);
	$scope.selectTableUsers();
	$scope.totalAmount = 0;
	$scope.foodTotal = 0;
	$scope.foodAndTime = 0;

	$scope.usersBill = [];
	for(var record in $scope.records){

		var isMember = $scope.records[record].member_price;
		var foodPrice = 0; //each player's food total;
		var subTotal = 0; // subtotal of food & time;
		var timestamp = $scope.time_convert( $scope.records[record].end_time,  $scope.records[record].start_from);
		// if member , then pay member price
		var time_spent = $scope.time_cost(timestamp, isMember);
		var foodName = findFoodName($scope.records[record], $scope.foods);

		// console.log(foodName);


		for(var f in foodName.orderName){
			console.log(foodName.orderName[f])

			$scope.foodTotal += parseFloat(foodName.orderName[f].unit_price);
			foodPrice += parseFloat(foodName.orderName[f].unit_price);
		
		}

		var bill = {
			'id': $scope.records[record].id,
			'time':timestamp.hrs.toFixed(2), //+':'+timestamp.min,
			'time_spent':time_spent.toFixed(2),
			'orderName':foodName.orderName,
			'foodTotal':foodPrice, //+ time_spent
			'subTotal':(parseFloat(time_spent) + parseFloat(foodPrice)).toFixed(2)
		}

		$scope.totalAmount += time_spent;
		$scope.usersBill.push(bill);

	}
	$scope.foodAndTime = $scope.totalAmount + $scope.foodTotal;
	var content = $('.showReceipt').html();
	console.log(content);
	$('.receipt').html(content);

}

//search the food return a object with price.
function findFoodName(record, foods){
  	// find the Order Name
  	var orderList = [];
  	for(var k in record.orders){

  		for(var f in foods){
	  		if($scope.foods[f].id == record.orders[k] ){

	  			if(record.member_price){
	  				var price = $scope.foods[f].promotion_price
	  			}else{
	  				var price = $scope.foods[f].unit_price
	  			}
	  			orderList.push(
	  				{
	  					'id':$scope.foods[f].id,
	  					'name':$scope.foods[f].name,
	  					'unit_price':price,

	  				})
	  		}
  		}
  	}
  	record.orderName = orderList;
  	return record
}



$scope.pay_bill = function(){
	Payment.pay($scope.payTogether)
	.success(function(){
		$scope.payTogether = [];
		$scope.selectTable($scope.tableNow);
	})
}

$scope.user_pay = function($index){
	var payment_id = $scope.usersBill[$index].id;
	var ans = confirm("Are you sure you want to pay Bill:" + payment_id);
	if(ans){
		Payment.single_pay(payment_id)
		.success(function(p_id){
			$scope.usersBill.splice($index,1); 
			$scope.payTogether = [];
			$scope.selectTable($scope.tableNow);
		})
	}
}

$scope.pay_table = function(){
	var table_no = $scope.tableNow
	Payment.pay_table(table_no)
	.success(function(){
		$scope.payTogether = [];
		$scope.selectTable($scope.tableNow);
	})


}

$scope.cancel_bill = function(){
	Payment.cancel($scope.chosenBill.id)
	.success(function(){
		$scope.selectTable($scope.tableNow);
	})
}

$scope.time_convert = function(end, start){
	if(end == 0){
		end = new Date();
	}
	var total_time_stamp = end-start// new Date ((end - start));
	total_time_stamp = ((total_time_stamp) / 3600)/1000;

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


$scope.time_cost = function(spentTime, isMember){
	console.log(isMember)
	if(isMember){
		var cost = spentTime.hrs * member.price
	}else{
		var cost = spentTime.hrs * PER_HOURS;
	}
	// cost += ((spentTime.min/60) * PER_HOURS);
	// console.log(cost+'='+spentTime.hrs+'*'+PER_HOURS);
	return cost;
}

$scope.reload = function(){

}

$scope.checkmembership = function(record){
	Payment.membership_price(record.id)
	.success(function(result){
		console.log(result);
		$scope.selectTable($scope.tableNow);
	});
}
			// scope.membership_price = function(){
			// 	var csrfmiddlewaretoken = '{{csrf_token}}';
			// 		$http({method: "POST", url: "/counter/bill/remark/update/"+scope.record.id+'/', 
			// 		data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
			// 			   'remark':scope.record.remark
			// 	}})
			// }


$scope.showdetail = function(record){

	$scope.payTogetherFlag = false;

	$scope.chosenBill = record;
	console.log(record);

	if(record.end_time){
		var total_time = record.end_time - record.start_from
	}else{
		var total_time = (new Date().getTime()) - record.start_from
	}


	total_time_stamp = ((total_time) / 3600)/1000;
	var hrs = total_time_stamp;
	var min = total_time_stamp;

	$scope.chosenBill.spent = hrs.toFixed(2); //+':'+min;
	  	// calculate the total amount
	  	var totalFood = 0;
	  	$scope.chosenBill.total_amount = (hrs*PER_HOURS) //+ (min/60*PER_HOURS);
	  	for(var i in $scope.chosenBill.orders){
	  		for(var f in $scope.foods){
		  		if($scope.foods[f].id == $scope.chosenBill.orders[i] ){
		  			totalFood += parseFloat($scope.foods[f].unit_price);
		  			$scope.foodTotal = totalFood;
		  		}
	  		}
	  	}
	  	$scope.chosenBill.foodAmount = totalFood;
	  	$scope.chosenBill.total_amount = $scope.chosenBill.total_amount.toFixed(2);
	  	$scope.chosenBill.foodAndTime = parseFloat($scope.chosenBill.foodAmount) + parseFloat($scope.chosenBill.total_amount);
	  	console.log($scope.chosenBill);
	  	// find the Order Name
	  	var orderList = [];
	  	for(var k in $scope.chosenBill.orders){
	  		for(var f in $scope.foods){
		  		if($scope.foods[f].id == $scope.chosenBill.orders[k] ){
		  			orderList.push(
		  				{
		  					'id':$scope.foods[f].id,
		  					'name':$scope.foods[f].name,
		  					'unit_price':$scope.foods[f].unit_price,
		  					'promotion_price':$scope.foods[f].promotion_price
		  				})
		  		}
	  		}
	  	}
	  	$scope.chosenBill.orderName = orderList
	  	$scope.chosenBill.pay_status = record.pay_status;

	  	if(!$scope.chosenBill.end_time){
	  		$scope.chosenBill.end_time = '';
	  	}


	  	if($scope.chosenBill.pay_status=='1'){
	  		$scope.chosenBill.is_hold = "HOLD";
	  	}else{
	  		$scope.chosenBill.is_hold = "";
	  	}
	  }


	  $scope.records = [];
	  $scope.selectTable($scope.tableNow);
	})


// });