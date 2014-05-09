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

        .constant('sbAccountsUrl', [
            'activate/:key',
            'login',
            'logout',
            'password/change',
            'password/change/done',
            'password/reset',
            'password/reset/confirm/:token/',
            'password/reset/complete',
            'password/reset/done',
            'register',
            'register/complete'
        ])

        .constant('sbTranslate', {
            en: {
                appName: 'songbook',
                signIn: 'sign in',
                signOut: 'sign out',
                loggedAs: 'logged as',
                menuHome: 'home',
                menuSongs: 'songs',
                menuSong: 'song',
                home: 'home',
                song: 'song',
                songList: 'songs',
                performer: 'performer',
                composer: 'composer',
                year: 'year'
            },
            pl: {
                appName: 'śpiewnik',
                signIn: 'zaloguj',
                signOut: 'wyloguj',
                loggedAs: 'zalogowano jako',
                menuHome: 'strona główna',
                menuSongs: 'piosenki',
                menuSong: 'piosenka',
                home: 'strona główna',
                song: 'piosenka',
                songList: 'piosenki',
                performer: 'wykonawca',
                composer: 'kompozytor',
                year: 'rok'
            }
        })

        .filter('sbUpperFirst', function () {
            return function upperFirst(input) {
                return input.charAt(0).toUpperCase() + input.slice(1);
            }
        });

}());
