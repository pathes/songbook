(function() {
    'use strict';

    angular.module('sbUtils', [])

        .constant('sbUrl', [
            {
                caption: 'menuHome',
                url: '/',
                templateUrl: '/static/songbook/html/home.html',
                controller: 'sbHomeController',
                inMenu: true
            },
            {
                caption: 'menuSongs',
                url: '/song',
                templateUrl: '/static/songbook/html/songlist.html',
                controller: 'sbSongListController',
                inMenu: true
            },
            {
                caption: 'menuSong',
                url: '/song/:songId',
                templateUrl: '/static/songbook/html/song.html',
                controller: 'sbSongController',
                inMenu: false
            }
        ])

        .filter('sbUpperFirst', function () {
            return function upperFirst(input) {
                return input.charAt(0).toUpperCase() + input.slice(1);
            }
        });

}());
