import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ContactSavePage = publicWidget.Widget.extend({
     selector: "#contactForm",
     events: {
         'click #saveBtn': '_onSaveBtnClick',
         'click #editBtn': '_onEditBtnClick'
     },
     _onSaveBtnClick: function(event){
         event.preventDefault()
         var form_detail = {
             "name": $('#contact_name').val(),
             "vat": $('#input_tax_id').val(),
             "email": $('#contact_email').val(),
             "phone": $('#contact_phone').val(),
             "function": $('#job_position').val(),
             "mobile": $('#contact_mobile').val(),
             "website": $('#website').val(),
         }
         var contact_id = $(event.currentTarget).data('id')
         form_detail['contact_id'] = contact_id

         rpc('/contact/update',form_detail).then(
             function(response){
                 var input_tag = document.getElementById('contactForm').getElementsByTagName('input')
                 for (let i=0; i<input_tag.length; i++){
                     input_tag[i].setAttribute('readonly',true)
                 }
             }
         )},

     _onEditBtnClick: function(event){
         event.preventDefault()
         var input_tag = document.getElementById('contactForm').getElementsByTagName('input')
         for (let i=0; i<input_tag.length; i++){
                input_tag[i].removeAttribute('readonly')
         }
     }
 });