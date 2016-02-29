// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

//
// Widget takes a select and some JSON, then fills in the identified values within a form when the value in the select changes
// SOURCE: select class="mps-multifill-master" data-master-key="code"
// TARGET: all data-child-key="[key/code from result data]" inputs & selects supported

$(function() {
    $.widget( "wfWidgets.mpsFormFillingSelect", {
        options: {
            data: false,
            masterKey: false
        },
        _create: function(){
            var $this = this,
                $el = $this.element,
                $form = $el.closest('form');

            if($this.options.masterKey === false){$this.options.masterKey = $el.data('masterKey')}

            $el.on('change', function(e){
                $this.selectVal($el.val());
            });
        },
        selectVal: function(sVal){
            var $this = this,
                $form = $this.element.closest('form'),
                sVal = $this.element.val(),
                jDetails = $this._findItemJSON(sVal);

            if(jDetails !== false){
                // Found some details to fill
                $.each(jDetails, function(i,v){
                    // Each key in the result MIGHT have a named input for it...
                    var zInputs = $form.find('[data-child-key="'+i+'"]');
                    if(zInputs.length > 0){
                        // Values should either be STRING or ARRAY (for eg multiple address lines)
                        if(typeof v == 'string'){
                            //Just set the value
                            $(zInputs[0]).val(v);
                        }
                        else if($.isArray(v)){
                            // Might need to expand or remove address lines...
                            $.each(v, function(j, val){
                                if(zInputs.length-1 < j){
                                    // There is not yet an input for the value, so add a line
                                    var $par = $(zInputs[zInputs.length-1]).parent();
                                    $par.find('.cv-add-field').click();
                                }
                            });
                            // Now just fill them in N -> N
                            $.each(v, function(j, val){
                                $form.find('[data-child-key="'+i+'"]').eq(j).val(val);
                            });
                            // Also be friendly and remove any extras:
                            while($form.find('[data-child-key="'+i+'"]').length > v.length){
                                $form.find('[data-child-key="'+i+'"]:last').parent().find('.cv-remove-field').click();
                            }
                        }
                        else{
                            // BUGBUG: error or more to do?  Should we handle Checkboxes?  Radios?  Selects?
                        }
                    }
                });
            }
            else{
                // BUGBUG: No matching results found
            }
        },
        _findItemJSON: function(sItemCode){
            var $this = this,
                jDetails = false;
            $.each($this.options.data, function(i,j){
                if($this.options.data[i][$this.options.masterKey] == sItemCode){
                    jDetails = $this.options.data[i];
                }
            });
            return jDetails;
        }
    });
});
