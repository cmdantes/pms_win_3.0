// $(document).ready(function(){

//     $('#total').change(function(e) {
//         let total = $('#total').val();
//         let nv = total / 1.12;
//         let nvt = nv.toFixed(2);

//         //$('#nonvat').val(nvt);
//         $('#cash').val(total);


//         let vt = total / 1.12 * 0.12;
//         let vat = vt.toFixed(2);
//         $('#vat').val(vat);
//         $('#nonvat').val(nvt);
       
//     //    $('#vatexempt').val(0);
//     //    $('#damount').val(0);
    
//         e.preventDefault();
    
    
// })

// // $(".go").click(function(){
  
// //     if ($('#ticket').val() !== "" && $('#total').val() !== ""  && $('#bdate').val() !== "" && $('#operator').val() !== "" && $('#timein').val() !== "" && $('#timeout').val() !== "" && $('#plate').val() !== "" ){
// //         return true;
       
// //     } else {
        
// //         $('#field').modal("show");
// //     }
    
// // }); 

// });

// function calc(divID, element)
//             {
           
//             document.getElementById('senior').style.visibility = element.value == 'REGULAR' ? 'hidden' : 'visible';
            //document.getElementById('senior').style.visibility = element.value == 'PWD_DISC' ? 'visible' : 'hidden';

           // }
        
 
    
//     function calc()
//             {
//                 var total = parseFloat(document.getElementById('total').value);
//                 var vatexempt =   document.getElementById('vatexempt').value;
//                 var discount =   document.getElementById('damount').value;
//                 var vat = document.getElementById('vat').value;
                
//                 var oper = document.getElementById('discount').value;
                
//                 if(oper === 'REGULAR DISCOUNT')
//                 {
//                     document.getElementById('vat').value = (total / 1.12 * .12).toFixed(2);
//                     document.getElementById('nonvat').value =  (total / 1.12).toFixed(2);
//                     document.getElementById('damount').value =  (total * .2).toFixed(2);
//                     document.getElementById('cash').value =  (total * .8).toFixed(2);
//                     document.getElementById('vatexempt').value =  0.00;
//                     document.getElementById('total').readOnly = true;
//                     var element = document.getElementById('total');
//                     element.classList.add("bg-dark", "text-white")
//                 }
                
//                 else if(oper === 'SENIOR')
//                 {
                    
//                     stotal = total;
//                     document.getElementById('total').value = (stotal).toFixed(2);
//                     document.getElementById('vat').value = (stotal / 1.12 * .12).toFixed(2);
//                     document.getElementById('nonvat').value =  0.00;
//                     document.getElementById('vatexempt').value = (stotal / 1.12 ).toFixed(2);
//                     document.getElementById('damount').value =  (stotal / 1.12 * .2).toFixed(2);
//                     document.getElementById('cash').value = (stotal - vat - ((stotal - vat) * 0.2 )).toFixed(2);
//                     document.getElementById('total').readOnly = true;
//                     var element = document.getElementById('total');
//                     element.classList.add("bg-dark", "text-white")
//                 }
                
//                 else if(oper === 'PWD')
//                 {
                    
//                     stotal = total;
//                     document.getElementById('total').value = (stotal).toFixed(2);
//                     document.getElementById('vat').value = (stotal / 1.12 * .12).toFixed(2);
//                     document.getElementById('nonvat').value =  0.00;
//                     document.getElementById('vatexempt').value = (stotal / 1.12 ).toFixed(2);
//                     document.getElementById('damount').value =  (stotal / 1.12 * .2).toFixed(2);
//                     document.getElementById('cash').value = (stotal - vat - ((stotal - vat) * 0.2 )).toFixed(2);
//                     document.getElementById('total').readOnly = true;
//                     var element = document.getElementById('total');
//                     element.classList.add("bg-dark", "text-white") 
//                 }
//                 else if(oper === '-'){
//                     document.getElementById('vat').value = (total  / 1.12 * .12).toFixed(2);
//                     document.getElementById('nonvat').value =  (total / 1.12).toFixed(2);
//                     document.getElementById('damount').value =  0;
//                     document.getElementById('cash').value =  total;
//                     document.getElementById('vatexempt').value =  0;
//                     document.getElementById('total').readOnly = false;
//                     var element = document.getElementById('total');
//                     element.classList.remove("bg-dark", "text-white")
//                 }
//             }
            

//     document.getElementById('vatex').onclick = function() {
//         document.getElementById('vatexempt').removeAttribute('readonly');
//         document.getElementById('vatexempt').classList.remove("bg-dark");
//         document.getElementById('nonvat').readOnly = true;
//         document.getElementById('nonvat').classList.add("bg-dark");
//         document.getElementById('nonvat').value = 0;
//         document.getElementById('vatex').style.visibility = "hidden";
//         document.getElementById('vatable').style.visibility = "visible";
//         //alert('tae');
//     };

//     document.getElementById('vatable').onclick = function() {
//         document.getElementById('nonvat').removeAttribute('readonly');
//         document.getElementById('nonvat').classList.remove("bg-dark");
//         document.getElementById('vatexempt').readOnly = true;
//         document.getElementById('vatexempt').classList.add("bg-dark");
//         document.getElementById('vatexempt').value = 0;
//         document.getElementById('vatable').style.visibility = "hidden";
//         document.getElementById('vatex').style.visibility = "visible";
//         //alert('tae');
//     };


   