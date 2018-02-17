

catcolateApp.directive('payment', function($http){
	return {
		restrict: "EA",
		replace: true,
		transclude : true,
		templateUrl: 'http://localhost:8000/static/js/angularjs/angular_templates/payment.html',
		scope: {
			payalone:"=",
			paytogether:"=",
			billtogether:"=",
			foods:'=',
			record:"=",
			pricetype:"=",
			addproduct:"&",
			paynow:"&",
			showdetail:"&",
			changetable:"&"
		},
		link:function(scope,element,attr,Payment){

			scope.upte = function(no,index){
				scope.record.orders[index] = no;

				console.log(scope.record.orders);
				console.log(scope.record.orders[index])

				console.log(no +'/'+index);
				// console.log(scope.record.orders[index]);
				var csrfmiddlewaretoken = '{{csrf_token}}';
					$http({method: "POST", url: "/counter/bill/update/"+scope.record.id+'/', 
					data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
						   'member':scope.record.member,
						   'end_time':scope.record.end_time,
						   'remark': scope.record.remark,
						   'orders':scope.record.orders,
						   'pay_status':scope.record.pay_status,
				}})
				scope.showdetail(scope.record);	
			}

			scope.confirm_del = function(index){
				var ans = confirm('Are you really want to delete this item ?');
				if(ans){
					// console.log(scope.record.orders);
					scope.record.orders.splice(index,1);
					var csrfmiddlewaretoken = '{{csrf_token}}';
						$http({method: "POST", url: "/counter/bill/update/"+scope.record.id+'/', 
						data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
							   'member':scope.record.member,
							   'end_time':scope.record.end_time,
							   'remark': scope.record.remark,
							   'orders':scope.record.orders,
							   'pay_status':scope.record.pay_status,
					}})
					scope.showdetail(scope.record);	
				}
			}

			scope.update_card_no = function(){
				var csrfmiddlewaretoken = '{{csrf_token}}';
					$http({method: "POST", url: "/counter/bill/card/update/"+scope.record.id+'/', 
					data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
						   'card_no':scope.record.card_no
				}})
			}


			scope.update_remark = function(){
				var csrfmiddlewaretoken = '{{csrf_token}}';
					$http({method: "POST", url: "/counter/bill/remark/update/"+scope.record.id+'/', 
					data: {'csrfmiddlewaretoken':csrfmiddlewaretoken,
						   'remark':scope.record.remark
				}})
			}



			element.on('click',function(){

				// scope.record.member = "Musashi";
				// if(typeof scope.record.orders === 'undefined'){
				// 	scope.record.orders = [];
				// 	scope.record.orders.push('x');
				// }else{
				// 	scope.record.orders.push('x');
				// }
				
				// scope.addPayment();
				// console.log(scope);
				// console.log(attr);
				// // this.addPayment();
				// console.log(element);
				// ('<select><option> -- Please Select -- </option><option> Orange Juice  </option><option> Apple Pie </option></select>'
			})


		}
	}
})

