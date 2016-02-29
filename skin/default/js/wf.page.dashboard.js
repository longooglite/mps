// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function () {

    $('.wf-gridWidget').gridWidget({
        url:'/appt/page/dashboard',
        page:'dashboard',
        columns:[
            {
                title: 'Type',
                guid: 'events',
                visible: false
            },
            {
                title: 'Last Updated',
                guid: 'lastupdated',
                visible: true
            },
            {
                title: 'Name',
                guid: 'names',
                visible: true
            },
            {
                title: sDeptLabel,
                guid: 'departments',
                visible: true
            },
            {
                title: 'Title / Rank',
                guid: 'titles',
                visible: true
            },
            {
                title: 'PCN',
                guid: 'pcns',
                visible: true
            },
            {
                title: 'Track',
                guid: 'tracks',
                visible: false
            },
            {
                title: 'MetaType',
                guid: 'metatype',
                visible: false
            },
            {
                title: 'Workflow',
                guid: 'workflows',
                visible: false
            },
            {
                title: 'Positions',
                guid: 'positions',
                visible: false
            },
            {
                title: 'ActionType',
                guid: 'actions',
                visible: false
            },
            {
                title: '&nbsp;',
                guid: 'deleteLink',
                visible: true
            }
        ]
    });

});
