// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$.widget( "mpsWidgets.mpsClientSideEmailAddy", {
    //
    // Supports variable delimeter, either in json {allowedDelimiter: 'foo} OR as data-delimeter="foo" on element
    // Supports client side required="required" Attribute on element to prevent empty strings on required fields, client side.
    //
    // Present in Evaluator Add/Edit, resend email from WF

    options: {
        form: false,
        timeout: 250,
        allowedDelimiter: false
    },

    _create: function(){
        var $this = this,
            $email = $this.element;

        $this.$form = ($this.options.form === false) ? $email.closest('form') : $this.options.form;

        if(typeof $email.data('delimeter') === 'string' && typeof $this.options.allowedDelimiter !== 'string'){
            // Friendly set the delimiter from element attribute
            $this.options.allowedDelimiter = $email.data('delimeter');
        }

        $this.isDelimited = (typeof $this.options.allowedDelimiter == 'string') ? true : false;

        $email.on('blur change', function(e){
            $this._fireOnce($this.checkEmailAddy($this));
        });

    },

    checkEmailAddy: function(){
        var $this = this,
            sTxt = $this.element.val();

        var $this = this,
            $mail = $this.element,
            sMail = sTxt || $mail.val();

        // We allow either single email addy OR delimited version...
        if($this.isDelimited){
            var zStrs = sMail.split($this.options.allowedDelimiter);

            if(zStrs.length > 1){
                for(i=0; i < zStrs.length;i++){
                    if($.trim(zStrs[i]).length > 0 && !mpsApp._isValidEmailAddy($.trim(zStrs[i]))){
                        cvApp._showPopoverErrorOnElement({
                            target: $mail,
                            title: '',
                            body: 'Valid email addresses are required',
                            code: $mail.attr('name'),
                            placement: 'right'
                        });

                        //wfApp._renderFormErrors([{message:'', code:$mail.attr('name')}], $('#mainform'));
                        return false;
                    }
                }
                return true;
            }
        }

        if( (sMail.length > 0 && !mpsApp._isValidEmailAddy(sMail.substring(0, sMail.lastIndexOf('.')).toLowerCase()+sMail.substring(sMail.lastIndexOf('.'))) )
            || (sMail.length == 0 && $mail.attr('required') == 'required' )){
            cvApp._showPopoverErrorOnElement({
                target: $mail,
                title: '',
                body: 'A valid email address is required',
                code: $mail.attr('name'),
                placement: 'right',
                focus: false
            });
            return false;
        }
        else{
            return true;
        }

    },

    _fireOnce: function(cb, context){
        var $this = this;
        clearTimeout($this.timeout);
        $this.timeout = setTimeout(cb, $this.options.timeout);
    }
});

var mpsApp = mpsApp || {};
mpsApp._isValidEmailAddy = function(str){
    var re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    return re.test(str);
}