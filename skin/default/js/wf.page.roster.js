// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

var _indentClass = function(meta, type){
    return '';
    if(meta.row == 0){
        return '';
    }
    else{
        console.log(meta, type);
        if(meta.settings.aoData[meta.row]._aData.pcns != meta.settings.aoData[meta.row-1]._aData.pcns){
            return '';
        }
        if(meta.col == 0 && meta.settings.aoData[meta.row]._aData.pcns == meta.settings.aoData[meta.row-1]._aData.pcns){
            return 'wf-roster-row-indent';
        }
        else if(meta.col == 1 && meta.settings.aoData[meta.row]._aData.departments == meta.settings.aoData[meta.row-1]._aData.departments){
            return 'wf-roster-row-indent';
        }
        else if(meta.col == 2 && meta.settings.aoData[meta.row]._aData.names == meta.settings.aoData[meta.row-1]._aData.names){
            return 'wf-roster-row-indent';
        }
        else if(meta.col == 30 && meta.settings.aoData[meta.row]._aData.tracks == meta.settings.aoData[meta.row-1]._aData.tracks){
            return 'wf-roster-row-indent';
        }
        return '';
    }
}

var zWebAppCols = [
    {
        title: 'PCN',
        guid: 'pcns',
        visible: true,
        render: function(data, type, full, meta){
            //if(meta.row == 1 || meta.row == 2)console.log(data, type, full, meta);
            if(full.rawData.pcn_url == ''){
                return '<span class="'+_indentClass(meta, type)+'">'+full.rawData.pcn+'</span>'
            }
            else{
                return '<a href="'+full.rawData.pcn_url+'" class="'+_indentClass(meta, type)+'">'+data+'</a>';
            }
        }
    },
    {
        title: sDeptLabel,
        guid: 'departments',
        visible: true,
        render: function(data, type, full, meta){
            return '<span class="'+_indentClass(meta, type)+'">'+data+'</span>';
        }
    },
    {
        title: 'Name',
        guid: 'names',
        visible: true,
        render: function(data, type, full, meta){
            var sName = (typeof full.z_person_url != 'undefined' && full.z_person_url.length > 0) ? '<a href="'+full.z_person_url+'" class="'+_indentClass(meta, type)+'">'+data+'</a>' : '<span class="'+_indentClass(meta, type)+'">'+data+'</span>',
                sSec = (full.z_row_appt.is_primary === false) ? '<span class="medGray">Secondary: </span>' : '';
            return sSec + sName;
        }
    },
    {
        title: 'Track',
        guid: 'tracks',
        visible: true,
        render: function(data, type, full, meta){
            return '<span class="'+_indentClass(meta, type)+'">'+data+'</span>';
        }
    },
    {
        title: 'Title / Rank',
        guid: 'titles',
        visible: true
    },
    {
        title: 'Position / TIR',
        guid: 'tir',
        visible: true
    },
    {
        title: 'TIR Filter',
        guid: 'tir_filter',
        visible: false
    },
    {
        title: 'Position',
        guid: 'positions',
        visible: false
    },
    {
        title: 'Action',
        guid: 'actions',
        visible: true,
        render: function(data, type, full, meta){
            return (typeof full.z_action_url != 'undefined' && full.z_action_url.length > 0) ? '<a href="'+full.z_action_url+'">'+data+'</a>' : (data.length > 1) ? data : '<span class="liteGray">--</span>';
        }
    },
    {
        title: 'Status',
        guid: 'statuses',
        visible: true,
        render: function(data, type, full, meta){
            return data; //(typeof full.z_action_url != 'undefined' && full.z_action_url.length > 0) ? '<a href="'+full.z_action_url+'">'+data+'</a>' : (data.length > 1) ? data : '<span class="liteGray">--</span>';
        }
    },
    {
        title: 'Last Updated',
        guid: 'proposedstart',
        visible: false,
        render: function(data, type, full, meta){
            return (data.length > 0) ? data : '<span class="liteGray">--</span>';
        }
    },
    {
        title: 'Proposed Start',
        guid: 'proposedstart',
        visible: true,
        render: function(data, type, full, meta){
            var sTxt = (data !== false) ? ( ((data != '') ? data : '') ) : '<span class="liteGray">--</span>';
            return sTxt;
        }
    },
    {
        title: 'rawData',
        guid: 'rawData',
        visible: false
    }
];

var zExportCols = [
    {
        title: 'PCN',
        guid: 'pcns',
        visible: true
    },
    {
        title: sDeptLabel,
        guid: 'departments',
        visible: true
    },
    {
        title: 'Name',
        guid: 'names',
        visible: true
    },
    {
        title: 'Track',
        guid: 'tracks',
        visible: true
    },
    {
        title: 'Title / Rank',
        guid: 'titles',
        visible: true
    },
    {
        title: 'Position / TIR',
        guid: 'tir',
        visible: true
    },
    {
        title: 'Action',
        guid: 'actions',
        visible: true
    },
    {
        title: 'Status',
        guid: 'statuses',
        visible: true
    },
    {
        title: 'Last Updated',
        guid: 'lastupdated',
        visible: true
    }
];

$(function () {
    $('.wf-gridWidget').rosterWidget({
        page:'roster',
        columns:zWebAppCols
    });
});
