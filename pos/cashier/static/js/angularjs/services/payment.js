catcolateApp
.factory("Payment", function PaymentFactory($http){
	return {
		all: function(){
			return $http({method: "GET", url: "/counter/payments/"});
		},
		foods: function(){
			return $http({method: "GET", url: "/counter/foods/"});
		},
		add: function(id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/add/", 
				data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
					   'table_no':id
			}})

			// .then(function successCallback(response){
			// 	console.log('add payment success')
			// 	return $http({method: "GET", url: "/counter/table/"+String(id)+"/"});
			// }, function errorCallback(response) {
			// 	console.log('add pay failed');
			// 	return $http({method: "GET", url: "/counter/table/"+String(id)+"/"});
   //  // called asynchronously if an error occurs
   //  // or server returns response with an error status.
 		// 	 });
			
		},
		view: function(id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "GET", url: "/counter/bill/view/"+id+"/"});
		},
		hold_it:function(id){
			var csrfmiddlewaretoken = '{{csrf_token}}';

			console.log(id);
			return $http({method: "POST", url: "/counter/bill/hold_it/", 
				data: {
					'csrfmiddlewaretoken':csrfmiddlewaretoken,
					'id':id
				}})

		},
		hold: function(bills){

			//hold a serious of bill
			var csrfmiddlewaretoken = '{{csrf_token}}';

			console.log(bills);
			return $http({method: "POST", url: "/counter/bill/hold/", 
				data: {
					'csrfmiddlewaretoken':csrfmiddlewaretoken,
					'bills':bills
				}})
		},
		hold_table:function(table_id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/hold_table/"+table_id+"/", 
				data: {
					'csrfmiddlewaretoken':csrfmiddlewaretoken,
				}})
		},
		single_pay:function(bill_id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/single_pay/"+bill_id+"/", 
				data: {
					'csrfmiddlewaretoken':csrfmiddlewaretoken,
					'bill_id':bill_id
				}})
		},
		pay: function(bills){
			// pay couple of bills
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/pay/", 
				data: {
					'csrfmiddlewaretoken':csrfmiddlewaretoken,
					'bills':bills
				}})
		},
		pay_table: function(id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/pay_table/", 
				data: {
					'csrfmiddlewaretoken':csrfmiddlewaretoken,
					'table_no':id
				}})
		},
		cancel: function(id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/cancel/"+id+"/", data: {'csrfmiddlewaretoken':csrfmiddlewaretoken}})

		},
		findCard: function(card_no){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "GET", url: "/counter/bill/card_no/"+card_no+"/"});
		},
		getTable: function(id){
			console.log(typeof id);
			return $http({method: "GET", url: "/counter/table/"+String(id)+"/"});
		},
		together: function(user_lists){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/together/", 
				data: {
					'csrfmiddlewaretoken':csrfmiddlewaretoken,
					'user_lists':user_lists
			}})
		},
		move: function(payment_id, id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/move/"+payment_id+"/", 
				data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
					   'table_no':id
			}})
		},
		membership_price:function(payment_id, table_id){
			var csrfmiddlewaretoken = '{{csrf_token}}';
			return $http({method: "POST", url: "/counter/bill/membership_price/", 
				data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
					   'payment_id':payment_id,
					   'table_id':table_id
			}})

		}
	}
});

