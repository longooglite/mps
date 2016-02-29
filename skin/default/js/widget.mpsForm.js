// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

//
// Ubiquitous MPS Form Widgets with:
//      Error Validation (from Array; and/or Top Text)
//      Email Validation (on email address inputs)
//      Date Pickers (with several date-format features)
//      Repeating Text & Select Controls
//      Repeating Forms
//      Table'd Repeating Forms (Repeating Forms with a summary table above them)
//

isUxDebugMode = false;

$(function() {
    //
    // Many Admin & some other pages do not load through Workflow or other meta pages, so look for a special className to
    //      load those forms without the triggered ajax .done() type event.
    //      Note: the newer versions of the Form & individual widgets are multi-init safe ;!).

    $('body').find('form.mps-form-widgets').mpsForm();

    //
    // Global Scope Trigger handler for AJAX'd form code paths to init all the neat new widgets:
    //
    $('body').on('safeInitFormWidgets', 'form', function(e, opts){
        var $form = $(e.target),
            zEmails = $form.find('.mps-validate-email'),
            zRepeatingTexts = $form.find('.mps-repeating-text'),
            zRepeatingForms = $form.find('.mps-repeating-form'),
            zDatePickerz = $form.find('.mps-date-picker');

        if(!$form.is( ":data('mpsWidgets-mpsForm')" )){
            $form.mpsForm(opts);
        }

        $.each(zEmails, function(i,o){
            var $obj = $(o);
            if(!$obj.is( ":data('mpsWidgets-mpsClientSideEmailAddy')" )){
                $obj.mpsClientSideEmailAddy(opts);
            }
        });

        $.each(zRepeatingTexts, function(i,o){
            var $obj = $(o);
            if(!$obj.is( ":data('mpsWidgets-mpsRepeatingText')" )){
                $obj.mpsRepeatingText(opts);
            }
        });

        $.each(zRepeatingForms, function(i,o){
            var $obj = $(o);
            if(!$obj.is( ":data('mpsWidgets-mpsRepeatingForm')" )){
                $obj.mpsRepeatingForm(opts);
            }
        });

        $.each(zDatePickerz, function(i,o){
            var $obj = $(o);
            if(!$obj.is( ":data('mpsWidgets-mpsDatePicker')" )){
                $obj.mpsDatePicker(opts);
            }
        });
    });

});

$.widget( "mpsWidgets.mpsForm", {
    options: {
        datePickers: true,
        repeatingText: true,
        repeatingSelects: true,
        repeatingForms: true,
        tabledRepeatingForms: true,
        emailValidation: true,
        classNames: {
            mpsDatePickerClass: 'mps-date-picker',
            emailValidationClass: 'mps-validate-email',
            repeatingTextClass:'Repeating_Text',
            repeatingSelectClass: 'Repeating_Select',
            repeatingFormClass: 'Repeating-Form-Wrapper',
            tabledRepeatingFormClass: 'Tabled-Form-Wrapper'
        },
        beforeSubmit: false
    },
    _create: function(){
        var $this = this,
            $form = $this.element;

        // Init all the widgets in this form:
        $form.trigger('safeInitFormWidgets', [$this.options]);

        // DatePicker sometimes requires init separate from trigger set (BUGBUG: not sure why, but try pcn.html without this...)
        $this.element.find('.mps-date-picker').mpsDatePicker();

        cvApp._handleRepeatingFields({
            iCols: 'none',
            iOffset: 'none',
            sClass: 'wf-form-right'
        }, $form);

        $this._bindings();

    },

    processReturnedErrorArray: function(zErrors){},
    processReturnedErrorText: function(sError){},

    _bindings: function(){
        var $this = this,
            $form = $this.element;

        // beforeSubmit handler
        $form.on('submit', function(e){
            if(typeof $this.options.beforeSubmit == 'function'){
                return $this.options.beforeSubmit();
            }
            else{
                return true;
            }
        });

        // BUGBUG: Older rare radio-button UX swapping.  Used only in ????
        $this.element.on('change', 'input[type=radio]', function(e){
            var $el = $(e.target);

            $el.closest('.quest_wrap').find('.opt_target').hide();
            if(typeof $el.data('expando') != 'undefined' && $el.data('expando').length > 0){
                $this.element.find('[data-target='+$el.data('expando')+']').show();
            }
        });

        // Uber Form bindings.
        $this.element.on('change', '.UberRadio', function(e) {
            var $el = $(e.target);
            mpsApp._uberFlipFlop($el);
            e.stopPropagation();
        });

        $this.element.on('change', '.UberDropdown', function(e) {
            var $el = $(e.target);
            var $opt = $el.find(":selected")
            mpsApp._uberFlipFlop($opt);
            e.stopPropagation();
        });

        $this.element.on('change', '.UberCheckbox', function(e) {
            var $el = $(e.target);
            if($el.is(':checked')) {
                mpsApp._uberShow($el);
            } else {
                mpsApp._uberHide($el);
            };
            e.stopPropagation();
        });

        $this.element.on('change', '.UberCheckboxHideWhenChecked', function(e) {
            var $el = $(e.target);
            if($el.is(':checked')) {
                mpsApp._uberHide($el);
            } else {
                mpsApp._uberShow($el);
            };
            e.stopPropagation();
        });

        $this.element.on('change, datePick', '.UberText', function(e) {
            var $el = $(e.target);
            if($.trim($el.val()).length > 0) {
                mpsApp._uberShow($el);
            } else {
                mpsApp._uberHide($el);
            };
            e.stopPropagation();
        });

        $this.element.on('keypress', '#saved_set_name', function(e){
            // Save Template btn should hit it's own button on Keyboard Enter, not the Form Submit currently hidden
            if(e.which == 13) {
                e.preventDefault();
                e.stopPropagation();
                $(this).next('button').click();
            }
        });
    }
});

$.widget( "mpsWidgets.mpsRepeatingText", {
    options: {
        form: false
    },
    _create: function(){},
    _bindings: function(){

    }
});

$.widget( "mpsWidgets.mpsRepeatingSelect", {
    options: {
        form: false
    },
    _create: function(){},
    _bindings: function(){

    }
});

