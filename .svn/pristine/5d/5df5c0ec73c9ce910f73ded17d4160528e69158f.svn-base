// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$.widget( "mpsWidgets.mpsDatePicker", {
    options: {
        form: false
    },
    _create: function(){
        var $this = this,
            $el = $this.element,
            $wrap = $('<div class="input-group date mps-date-picker-wrapper"></div>'),
            $btn = $('<span class="input-group-addon btn btn-primary"><span class="glyphicon glyphicon-calendar"></span></span>'),
            $parent = $el.parent();

        // Just in case we get a request to datePickerize a cloned DOM, let's check to see if the wrapper & icon already exist
        if($parent.is('.mps-date-picker-wrapper') && $parent.find('.input-group-addon').length > 0){
            mpsApp.mpsDatePickerizeDom($parent);
        }
        else{  // No wrapper & icon - add them
            $wrap.append($btn);
            $wrap.insertAfter($el);
            $wrap.append($el);
            mpsApp.mpsDatePickerizeDom($wrap);
        }
    },
    _bindings: function(){

    }
});

var mpsApp = mpsApp || {};
mpsApp.mpsDatePickerizeDom = function(dom){
    // Accepts a DOM & smart-date-picker-izes based on new Date Picker app classNames

    // We want to make sure that all single-input date-pickers are wrapped with the correct button & wrapper, so:
    dom.find('.mps-date-picker').filter(function(i,el){
        var $dp = $(el);
        return !$dp.is( ":data('mpsWidgets-mpsDatePicker')" );
    }).mpsDatePicker();

    // Date-Pickers:
    var zDPs = (dom.is('.mps-date-picker-wrapper')) ? dom : dom.find('.mps-date-picker-wrapper');
    zDPs.each(function(iDP, picker){
        var $picker = $(picker),
            $input = $picker.find('input'),
            sFormat = typeof $input.attr('placeholder') != 'undefined' && $input.attr('placeholder') != 'now' ? $input.attr('placeholder') : (typeof $input.attr('placeholder') != 'undefined' && $input.attr('placeholder') == 'now' && typeof $input.data('nowDateFormat') != 'undefined') ? $input.data('nowDateFormat') : 'MM/DD/YYYY';

        // Console Out for bad date formats...
        if(sFormat.indexOf('now') < 0 && sFormat.toLowerCase().indexOf('yy') < 0){
            console.log('Datepicker might have a bad format:', sFormat, $picker);
        }

        if($input.prop('disabled') === false){
            $picker.datetimepicker({
                format: sFormat,
                doNotPreventDefaultOn: ['37', '39', '84'],
                keepInvalid: true,
                useStrict: true,
                keyBinds: {
                    t: function () {
                        return;
                    }
                }
            });
        }
        else{
            $picker.find('.input-group-addon').removeClass('btn btn-primary');
        }

        // Funny one-off for inline date strings that should change with the form's picker/input changes
        var changeDynaTxt = function(){
            var $wrap = $input.closest('form'),
                $dyna = $wrap.find('.wf-dyna-date:first');
            $dyna.text($input.val());
        };

        $input.on('change blur', function(e){changeDynaTxt();});
        $input.on('change', function(e){ $input.trigger('datePick'); }); // Trigger custom uberEvent in case a DP field has uber-kinders
        $picker.on('dp.change', function(e){
            changeDynaTxt();
            $input.trigger('datePick'); // Trigger custom uberFlipFlop event in case this field has uber-kinders
        });
    });
}